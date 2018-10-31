import os

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from django.urls import reverse
from django.utils import timezone
from django.views import generic


import csv

from django.views.generic import TemplateView

from adaptor.model import CsvDbModel
from .models import ImportOptimum, Import, RefImport, Imb
from .forms import ImportFileForm


class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    template_name = 'imports/index.html'
    context_object_name = 'latest_import_list'

    def get_queryset(self):
        """Return the last five published import."""
        return Import.objects.order_by('-pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.ListView):
    login_url = '/login'
    redirect_field_name = 'redirect_to'
    model = ImportOptimum, Import
    template_name = 'imports/detail.html'
    context_object_name = 'import_detail'

    def get_queryset(self):
        return ImportOptimum.objects.filter(import_info=self.kwargs['import_id'])


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
        user = request.user
        csv_file = request.FILES['csv_file'].name
        path = "C:/SI/jeu de données/"
        if form.is_valid():
            r = RefImport.objects.get(pk=1)
            i = Import(pub_date=timezone.now(), author=user, ref=r)
            i.save()
            with open(path + csv_file, 'r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=";")
                for row in reader:
                    p = ImportOptimum(dossier=row['Dossier'], code_regroupement_syndic=row['Code Regroupement Syndic'], import_fk=i)
                    print(row['Dossier'])
                    p.save()
                    for row1 in reader:
                        if row1['Dossier'] != row['Dossier']:
                            imb = Imb(refImb=row1['Dossier'], import_fk=i)
                            imb.save()
            # form.save()
            return HttpResponseRedirect(reverse('imports:index'))
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
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

        return render(request, self.template_name)


class LogoutView(TemplateView):

    def get(self, request, **kwargs):

        logout(request)

        return render(request, self.template_name)


class MyCsvModel(CsvDbModel):

    class Meta:
        dbModel = ImportOptimum
        delimiter = ";"



