from .import views #haciendolo asi no hae falta especificar nombres de funciones
from django.urls import path

urlpatterns = [
    path('',views.index, name="index"),
    path('signup/',views.signup, name="signup"),
    path('signin/',views.signin, name="signin"),
    path('logout/',views.logout, name="logout"),
]