"""Vistas de electrocardiogramas."""
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView

from django.utils.translation import gettext as _

from ..forms import ECGReportForm
from ..heart_rate import heart_rate_trend
from ..models import ECGReport


class ECGListView(LoginRequiredMixin, ListView):
    """Lista de electrocardiogramas con gráfica de evolución de FC."""

    model = ECGReport
    template_name = 'labs/ecg/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return ECGReport.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        records_with_hr = [r for r in ctx['records'] if r.heart_rate]
        if records_with_hr:
            ordered = sorted(records_with_hr, key=lambda r: r.date)
            ctx['chart_data'] = json.dumps({
                'labels': [r.date.strftime('%d/%m/%Y') for r in ordered],
                'values': [r.heart_rate for r in ordered],
            })
            ctx['ecg_hr_trend'] = heart_rate_trend(ordered[::-1])
        return ctx


class ECGCreateView(LoginRequiredMixin, View):
    """Crea un nuevo electrocardiograma."""

    template_name = 'labs/ecg/form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ECGReportForm(), 'editing': False})

    def post(self, request):
        form = ECGReportForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, _('ECG saved successfully.'))
            return redirect('ecg_detail', pk=record.pk)
        return render(request, self.template_name, {'form': form, 'editing': False})


class ECGDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un electrocardiograma."""

    model = ECGReport
    template_name = 'labs/ecg/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        return ECGReport.objects.filter(user=self.request.user)


class ECGUpdateView(LoginRequiredMixin, View):
    """Edita un electrocardiograma."""

    template_name = 'labs/ecg/form.html'

    def _get_record(self, request, pk):
        return get_object_or_404(ECGReport, pk=pk, user=request.user)

    def get(self, request, pk):
        record = self._get_record(request, pk)
        return render(request, self.template_name, {'form': ECGReportForm(instance=record), 'record': record, 'editing': True})

    def post(self, request, pk):
        record = self._get_record(request, pk)
        form = ECGReportForm(request.POST, request.FILES, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, _('ECG updated successfully.'))
            return redirect('ecg_detail', pk=record.pk)
        return render(request, self.template_name, {'form': form, 'record': record, 'editing': True})


class ECGDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un electrocardiograma."""

    model = ECGReport
    success_url = reverse_lazy('ecg_list')
    context_object_name = 'record'

    def get_queryset(self):
        return ECGReport.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return redirect('ecg_detail', pk=self.get_object().pk)
