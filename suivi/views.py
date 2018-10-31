from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.views.generic import TemplateView
from dal import autocomplete

from imports.models import ImportOptimum, Import, Pa


class IndexView(LoginRequiredMixin, TemplateView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    template_name = 'suivi/index.html'


class PaAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView, generic.FormView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = Pa
    template_name = 'suivi/suivi.html'
    form_class = Pa
    success_url = 'success.html'

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return Pa.objects.none()

        qs = Pa.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
