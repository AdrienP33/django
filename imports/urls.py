from django.urls import path

from . import views

app_name = 'imports'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('importer/upload_csv/', views.upload_csv, name='upload_csv'),
    path('importer/', views.ImporterView.as_view(), name='importer'),
    path('importer/success.html', views.ImporterView.as_view(), name='success'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]


