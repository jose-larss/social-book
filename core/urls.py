from .import views #haciendolo asi no hae falta especificar nombres de funciones
from django.urls import path

urlpatterns = [
    path('',views.index, name="index")
]