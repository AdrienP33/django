from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'suivi'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('suiviPm', views.PmView.as_view(), name='suiviPm'),
    path('suiviPa', views.PaView.as_view(), name='suiviPa'),
    path('suiviImb', views.ImbView.as_view(), name='suiviImb'),
]
