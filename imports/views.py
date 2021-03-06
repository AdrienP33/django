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
import pandas as pd
from datetime import datetime, date

from django.views.generic import TemplateView

from adaptor.model import CsvDbModel
from .models import ImportOptimum, Import, RefImport, Imb, Pmz, Pa
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
        return ImportOptimum.objects.filter(import_fk=self.kwargs['import_id'])


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

                    for row1 in reader:
                        p = ImportOptimum(dossier=row1['Dossier'], code_regroupement_syndic=row1['Code Regroupement Syndic'], import_fk=i)
                        print(row['Dossier'])
                        p.save()
                        if row1['Dossier'] != row['Dossier']:

                            if row1['Id PM'] == '':
                                if row1['Id PA'] == '':
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i)
                                        imb.save()
                                    else:
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i)
                                        imb.save()
                                elif not Pa.objects.get(refPa=row1['Id PA']):
                                    pa = Pa(refPa=row1['Id PA'], import_fk=i)
                                    pa.save()
                                    # pa = Pa(refPa=row1['id PA'], import_fk=i, pmz_fk=pmz)
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i, pa_fk=pa)
                                        imb.save()
                                    elif row1['Dossier'] != '':
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i, pa_fk=pa)
                                        imb.save()
                                else:
                                    pa = Pa.objects.get(refPa=row1['Id PA'])
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i, pa_fk=pa)
                                        imb.save()
                                    else:
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i, pa_fk=pa)
                                        imb.save()

                            elif not Pmz.objects.filter(refPmz=row1['Id PM']):
                                pmz = Pmz(refPmz=row1['Id PM'], import_fk=i)
                                pmz.save()
                                if row1['Id PA'] == '':
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i)
                                        imb.save()
                                    else:
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i)
                                        imb.save()
                                elif not Pa.objects.filter(refPa=row1['Id PA']):
                                    pa = Pa(refPa=row1['Id PA'], import_fk=i, pmz_fk=pmz)
                                    pa.save()
                                    # pa = Pa(refPa=row1['id PA'], import_fk=i, pmz_fk=pmz)
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i, pa_fk=pa)
                                        imb.save()
                                    elif row1['Dossier'] != '':
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i, pa_fk=pa)
                                        imb.save()
                                else:
                                    pa = Pa.objects.get(refPa=row1['Id PA'])
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i, pa_fk=pa)
                                        imb.save()
                                    else:
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i, pa_fk=pa)
                                        imb.save()
                            else:
                                pmz = Pmz.objects.get(refPmz=row1['Id PM'])
                                if row1['Id PA'] == '':
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i)
                                        imb.save()
                                    else:
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i)
                                        imb.save()
                                elif not Pa.objects.filter(refPa=row1['Id PA']):
                                    pa = Pa(refPa=row1['Id PA'], import_fk=i, pmz_fk=pmz)
                                    pa.save()
                                    # pa = Pa(refPa=row1['id PA'], import_fk=i, pmz_fk=pmz)
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i, pa_fk=pa)
                                        imb.save()
                                    elif row1['Dossier'] != '':
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i, pa_fk=pa)
                                        imb.save()
                                else:
                                    pa = Pa.objects.get(refPa=row1['Id PA'])
                                    if row1['Date effective raccordement'] == '' or not Imb.objects.filter(refImb=row1['Dossier']):
                                        imb = Imb(refImb=row1['Dossier'], import_fk=i, pa_fk=pa)
                                        imb.save()
                                    else:
                                        ligne_date = row1['Date effective raccordement']
                                        dates = datetime.strptime(ligne_date, '%d/%m/%Y')
                                        imb = Imb(refImb=row1['Dossier'], date_effective_de_raccordement=dates.date(), import_fk=i, pa_fk=pa)
                                        imb.save()





# try:
                            #      l = row1['id PM']
                            #      pm = Pmz.objects.get(refPmz=l)
                            #      print(pm)
                            # except NameError:
                            #      print("Pm n'existe pas")


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



