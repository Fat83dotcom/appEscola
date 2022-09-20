from django.urls import path
from . import views

urlpatterns = [
    path('consulta-avancada/', views.consultas, name='consultas-avacadas'),
]
