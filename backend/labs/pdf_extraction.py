"""Servicio de extracción de biomarcadores desde PDF via LabLocalAI."""
import base64
import json
import logging
import os
import threading
import urllib.error
import urllib.request
from decimal import Decimal, InvalidOperation

from .models import Biomarker, BiomarkerResult

logger = logging.getLogger(__name__)


def extract_biomarkers_from_pdf(report):
    """
    Llama al endpoint de LabLocalAI con el PDF del report y la lista de LOINC codes.

    Payload enviado:
        {
            "pdf": "<base64-utf8>",
            "biomarkers": ["26515-7", "718-7", ...]
        }

    Respuesta esperada:
        {
            "biomarkers": [
                {"loinc_code": "26515-7", "value": 8.1},
                ...
            ]
        }

    Devuelve dict {loinc_code: Decimal} con los valores extraídos, o None si hay error.
    """
    logger.info('extract_biomarkers_from_pdf: inicio para report pk=%s, pdf=%s', report.pk, report.pdf)
    if not report.pdf:
        logger.warning('extract_biomarkers_from_pdf: report pk=%s no tiene PDF adjunto', report.pk)
        return None

    ai_url = os.environ.get('LAB_LOCAL_AI_URL', 'https://lablocalai-production.up.railway.app').rstrip('/')
    if not ai_url:
        logger.warning('extract_biomarkers_from_pdf: LAB_LOCAL_AI_URL no configurado')
        return None
    logger.info('extract_biomarkers_from_pdf: usando ai_url=%s', ai_url)

    # Leer PDF y codificar en base64
    try:
        report.pdf.open('rb')
        pdf_bytes = report.pdf.read()
        report.pdf.close()
    except Exception as e:
        logger.error('pdf_extraction: error leyendo PDF: %s', e)
        return None

    pdf_b64 = base64.b64encode(pdf_bytes).decode('utf-8')

    loinc_codes = list(Biomarker.objects.values_list('loinc_code', flat=True))

    payload = json.dumps({
        'pdf': pdf_b64,
        'biomarkers': loinc_codes,
    }).encode('utf-8')

    headers = {
        'Content-Type': 'application/json',
    }

    logger.info('extract_biomarkers_from_pdf: enviando PDF (%d bytes, %d loinc_codes) a %s', len(pdf_bytes), len(loinc_codes), f'{ai_url}/v1/utils/extract-biomarkers')
    try:
        req = urllib.request.Request(
            f'{ai_url}/v1/utils/extract-biomarkers',
            data=payload,
            headers=headers,
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw_response = resp.read()
            logger.info('extract_biomarkers_from_pdf: respuesta recibida (%d bytes)', len(raw_response))
            data = json.loads(raw_response)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        logger.error('extract_biomarkers_from_pdf: HTTP %s al llamar API: %s', e.code, body)
        return None
    except Exception as e:
        logger.error('extract_biomarkers_from_pdf: error llamando API: %s', e)
        return None

    extracted = {}
    for item in data.get('biomarkers', []):
        loinc = item.get('loinc_code')
        raw_value = item.get('value')
        if loinc and raw_value is not None:
            try:
                extracted[loinc] = Decimal(str(raw_value))
            except InvalidOperation:
                logger.warning('pdf_extraction: valor no numérico para %s: %r', loinc, raw_value)

    logger.info('pdf_extraction: %d valores extraídos del PDF', len(extracted))
    return extracted


def apply_pdf_extraction(report):
    """
    Ejecuta la extracción y crea BiomarkerResult para los valores devueltos.

    Solo crea registros que no existan ya (los valores manuales del formulario tienen prioridad).
    Devuelve el número de resultados creados.
    """
    logger.info('apply_pdf_extraction: inicio para report pk=%s', report.pk)
    extracted = extract_biomarkers_from_pdf(report)
    if not extracted:
        logger.warning('apply_pdf_extraction: extract_biomarkers_from_pdf devolvió vacío/None para report pk=%s', report.pk)
        return 0

    biomarkers_by_loinc = {
        bm.loinc_code: bm
        for bm in Biomarker.objects.filter(loinc_code__in=extracted.keys())
    }

    created = 0
    for loinc_code, value in extracted.items():
        bm = biomarkers_by_loinc.get(loinc_code)
        if bm is None:
            continue
        _, was_created = BiomarkerResult.objects.get_or_create(
            report=report,
            biomarker=bm,
            defaults={'value': value},
        )
        if was_created:
            created += 1

    logger.info('pdf_extraction: %d BiomarkerResult creados para report %s', created, report.pk)
    return created


def _apply_in_thread(report):
    """Extrae biomarcadores del PDF y recalcula PhenoAge. Cierra la conexión de DB al terminar."""
    from django.db import close_old_connections
    from .phenoage import update_report_phenoage
    logger.info('_apply_in_thread: inicio para report pk=%s', report.pk)
    try:
        created = apply_pdf_extraction(report)
        logger.info('_apply_in_thread: extracción completada, %d resultados creados', created)
        update_report_phenoage(report)
        logger.info('_apply_in_thread: PhenoAge actualizado para report pk=%s', report.pk)
    except Exception as e:
        logger.exception('_apply_in_thread: excepción no capturada para report pk=%s: %s', report.pk, e)
    finally:
        close_old_connections()
        logger.info('_apply_in_thread: fin para report pk=%s', report.pk)


def apply_pdf_extraction_async(report):
    """Lanza apply_pdf_extraction en un hilo secundario (fire-and-forget)."""
    logger.info('pdf_extraction_async: lanzando hilo para report pk=%s pdf=%s', report.pk, report.pdf)
    t = threading.Thread(target=_apply_in_thread, args=(report,), daemon=True)
    t.start()
    logger.info('pdf_extraction_async: hilo iniciado (id=%s)', t.ident)
