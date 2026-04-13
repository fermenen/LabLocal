"""Vistas de composición corporal."""
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView

from ..forms import BodyCompositionForm
from ..models import BodyCompositionReport


class BodyCompositionListView(LoginRequiredMixin, ListView):
    """Lista de registros de composición corporal con gráfica de evolución de IMC."""

    model = BodyCompositionReport
    template_name = 'labs/body/list.html'
    context_object_name = 'records'

    def get_queryset(self):
        return BodyCompositionReport.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        all_ordered = sorted(ctx['records'], key=lambda r: r.date)

        records_with_bmi = [r for r in all_ordered if r.bmi is not None]
        if records_with_bmi:
            ctx['chart_data'] = json.dumps({
                'labels': [r.date.strftime('%d/%m/%Y') for r in records_with_bmi],
                'values': [r.bmi for r in records_with_bmi],
            })

        aging_records = [r for r in all_ordered if r.body_fat_pct is not None or r.muscle_mass is not None]
        if aging_records:
            labels = [r.date.strftime('%d/%m/%Y') for r in aging_records]
            ctx['aging_chart_data'] = json.dumps({
                'labels': labels,
                'fat': [float(r.body_fat_pct) if r.body_fat_pct is not None else None for r in aging_records],
                'muscle': [float(r.muscle_mass) if r.muscle_mass is not None else None for r in aging_records],
                'has_fat': any(r.body_fat_pct is not None for r in aging_records),
                'has_muscle': any(r.muscle_mass is not None for r in aging_records),
            })
        return ctx


class BodyCompositionCreateView(LoginRequiredMixin, View):
    """Crea un nuevo registro de composición corporal."""

    template_name = 'labs/body/form.html'

    def get(self, request):
        return render(request, self.template_name, {'form': BodyCompositionForm(), 'editing': False})

    def post(self, request):
        form = BodyCompositionForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Registro guardado correctamente.')
            return redirect('body_detail', pk=record.pk)
        return render(request, self.template_name, {'form': form, 'editing': False})


class BodyCompositionDetailView(LoginRequiredMixin, DetailView):
    """Detalle de un registro de composición corporal."""

    model = BodyCompositionReport
    template_name = 'labs/body/detail.html'
    context_object_name = 'record'

    def get_queryset(self):
        return BodyCompositionReport.objects.filter(user=self.request.user)


class BodyCompositionUpdateView(LoginRequiredMixin, View):
    """Edita un registro de composición corporal."""

    template_name = 'labs/body/form.html'

    def _get_record(self, request, pk):
        return get_object_or_404(BodyCompositionReport, pk=pk, user=request.user)

    def get(self, request, pk):
        record = self._get_record(request, pk)
        return render(request, self.template_name, {'form': BodyCompositionForm(instance=record), 'record': record, 'editing': True})

    def post(self, request, pk):
        record = self._get_record(request, pk)
        form = BodyCompositionForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro actualizado correctamente.')
            return redirect('body_detail', pk=record.pk)
        return render(request, self.template_name, {'form': form, 'record': record, 'editing': True})


class BodyCompositionDeleteView(LoginRequiredMixin, DeleteView):
    """Elimina un registro de composición corporal."""

    model = BodyCompositionReport
    success_url = reverse_lazy('body_list')
    context_object_name = 'record'

    def get_queryset(self):
        return BodyCompositionReport.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return redirect('body_detail', pk=self.get_object().pk)
