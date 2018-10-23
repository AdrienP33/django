from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.utils import timezone
from django.views import generic


import csv

from django.views.generic import TemplateView

from adaptor.model import CsvDbModel
from .models import ImportOptimum
from .forms import ImportFileForm


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    template_name = 'imports/index.html'
    context_object_name = 'latest_importOptimum_list'

    def get_queryset(self):
        """Return the last five published import."""
        return ImportOptimum.objects.order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = ImportOptimum
    template_name = 'imports/detail.html'


class ImporterView(LoginRequiredMixin, generic.FormView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = ImportOptimum
    template_name = 'imports/importer.html'
    form_class = ImportFileForm
    success_url = 'success.html'


def upload_csv(request):
    if request.method == 'POST':
        form = ImportFileForm(request.POST, request.FILES)
        csv_file = request.FILES['csv_file'].name
        if form.is_valid():
            with open(csv_file, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")
                for row in reader:
                    p = ImportOptimum(charges_etude=row['Chargé d\'étude'], pez=row['PEZ'],  pub_date=timezone.now())
                    p.save()
            # form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ImportFileForm()
    return render_to_response('importer.html', {'form': form})


class LoginView(TemplateView):

    def post(self, request, **kwargs):

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL )

        return render(request, self.template_name)


class LogoutView(TemplateView):

    def get(self, request, **kwargs):

        logout(request)

        return render(request, self.template_name)


class MyCsvModel(CsvDbModel):

    class Meta:
        dbModel = ImportOptimum
        delimiter = ";"



