from django.conf.urls import url
from django.urls import path

from suivi.views import PaAutocomplete
from . import views

app_name = 'suivi'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('pa-autocomplete/', PaAutocomplete.as_view(), name='pa-autocomplete'),
]
