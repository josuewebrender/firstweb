from django.urls import path

from . import views

urlpatterns = [
    path('', views.autenticacion, name="autenticacion"),
    path('historial', views.historial, name="historial"),
    path('signout', views.signout, name="signout"),
]