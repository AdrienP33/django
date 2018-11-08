from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView

from imports.models import ImportOptimum, Import, Pa, Pmz, Imb


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    template_name = 'suivi/index.html'


class PmView(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = Pmz
    template_name = 'suivi/suiviPm.html'
    context_object_name = 'pm_detail'
    queryset = Pmz.objects.all()


class PaView(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = Pa
    template_name = 'suivi/suiviPa.html'
    context_object_name = 'pa_detail'
    queryset = Pa.objects.all()


class ImbView(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = Imb
    template_name = 'suivi/suiviImb.html'
    context_object_name = 'imb_detail'
    queryset = Imb.objects.all()
