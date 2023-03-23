from .import views #haciendolo asi no hae falta especificar nombres de funciones
from django.urls import path

urlpatterns = [
    path('',views.index, name="index"),
    path('like-post/',views.like_post, name="like-post"),
    path('upload/',views.upload, name="upload"),
    path('follow/',views.follow, name="follow"),
    path('search/',views.search, name="search"),
    path('profile/<str:username>/',views.profile, name="profile"),
    path('settings/',views.settings, name="settings"),
    path('signup/',views.signup, name="signup"),
    path('signin/',views.signin, name="signin"),
    path('logout/',views.logout, name="logout"),
]