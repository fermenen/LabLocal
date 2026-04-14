"""Proxy de las llamadas al servicio LabLocalAI."""
import http.client
import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, StreamingHttpResponse
from django.views import View

from ..models import AILicense

logger = logging.getLogger(__name__)


def _ai_headers(request):
    """Cabeceras comunes para llamar a LabLocalAI."""
    license = AILicense.get_active()
    if not license:
        logger.warning('ai_proxy: no hay licencia activa')
        return None, None
    try:
        user_uuid = str(request.user.userprofile.user_uuid)
    except Exception as e:
        logger.warning('ai_proxy: no se pudo obtener user_uuid: %s', e)
        return None, None
    return {
        'Content-Type': 'application/json',
        'X-API-Key': license.api_key,
        'X-User-UUID': user_uuid,
    }, os.environ.get('LAB_LOCAL_AI_URL', '').rstrip('/')


class AIProxyMixin(LoginRequiredMixin):

    def _check(self, request):
        headers, ai_url = _ai_headers(request)
        if not headers or not ai_url:
            return None, None, JsonResponse({'error': 'IA no disponible'}, status=503)
        return headers, ai_url, None

    def _fetch(self, url, headers, method='GET', body=None):
        req = urllib.request.Request(url, data=body, headers=headers, method=method)
        try:
            resp = urllib.request.urlopen(req, timeout=30)
            return resp, None
        except urllib.error.HTTPError as e:
            body_text = e.read().decode('utf-8', errors='replace')
            logger.error('ai_proxy upstream %s %s → %s: %s', method, url, e.code, body_text)
            return None, (e.code, body_text)
        except Exception as e:
            logger.error('ai_proxy upstream %s %s → error: %s', method, url, e)
            return None, (503, str(e))


class ConversationsView(AIProxyMixin, View):

    def get(self, request):
        headers, ai_url, err = self._check(request)
        if err:
            return err
        limit = request.GET.get('limit', '50')
        resp, error = self._fetch(f'{ai_url}/api/conversations/?limit={limit}', headers)
        if error:
            return JsonResponse({'error': error[1]}, status=error[0])
        return JsonResponse(json.loads(resp.read()))

    def post(self, request):
        headers, ai_url, err = self._check(request)
        if err:
            return err
        resp, error = self._fetch(
            f'{ai_url}/api/conversations/', headers, method='POST', body=request.body
        )
        if error:
            return JsonResponse({'error': error[1]}, status=error[0])
        return JsonResponse(json.loads(resp.read()), status=201)


class MessagesView(AIProxyMixin, View):

    def get(self, request, conversation_id):
        headers, ai_url, err = self._check(request)
        if err:
            return err
        limit = request.GET.get('limit', '100')
        resp, error = self._fetch(
            f'{ai_url}/api/conversations/{conversation_id}/messages?limit={limit}', headers
        )
        if error:
            return JsonResponse({'error': error[1]}, status=error[0])
        return JsonResponse(json.loads(resp.read()))

    def post(self, request, conversation_id):
        headers, ai_url, err = self._check(request)
        if err:
            return err

        # Usamos http.client directamente para poder usar read1(),
        # que devuelve lo disponible sin bloquear hasta llenar el buffer.
        parsed = urllib.parse.urlparse(ai_url)
        host = parsed.hostname
        port = parsed.port or (443 if parsed.scheme == 'https' else 80)

        if parsed.scheme == 'https':
            conn = http.client.HTTPSConnection(host, port, timeout=120)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=120)

        path = f'/api/conversations/{conversation_id}/messages'
        body_bytes = request.body

        try:
            conn.request('POST', path, body=body_bytes, headers=headers)
            upstream = conn.getresponse()
        except Exception as e:
            logger.error('ai_proxy SSE connect error: %s', e)
            return JsonResponse({'error': str(e)}, status=503)

        if upstream.status != 200:
            error_body = upstream.read().decode('utf-8', errors='replace')
            logger.error('ai_proxy SSE upstream → %s: %s', upstream.status, error_body)
            conn.close()
            return JsonResponse({'error': error_body}, status=upstream.status)

        logger.info('ai_proxy SSE stream started for conversation %s', conversation_id)

        def stream():
            try:
                while True:
                    # read1() devuelve lo que haya disponible ahora mismo,
                    # sin esperar a llenar el buffer — clave para SSE.
                    chunk = upstream.read1(4096)
                    if not chunk:
                        break
                    yield chunk
            except Exception as e:
                logger.error('ai_proxy SSE stream error: %s', e)
            finally:
                conn.close()

        response = StreamingHttpResponse(stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response
