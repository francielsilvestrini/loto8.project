from django.urls import path
from . import views


app_name = 'resultados'

urlpatterns = [
    path('importar/', views.importar_resultados, name='importar'),
    path('listar/', views.listar_resultados, name='listar'),
    path('', views.dashboard, name='dashboard'),
]
