from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from . import models
from django.db.models import Q
import pytz
from django.utils import timezone

# Create your views here.
TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")'
)

def autenticacion(request):
    if request.method == "POST":

        user = authenticate(
        request, username = request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'login.html')
        else:
            login(request, user)
            return redirect('historial') 
    
    if request.method == 'GET':
        print("Ingreso a GET de autenticacion")
        return render(request, "login.html")
    
    return render(request, "login.html")

@login_required(login_url='autenticacion')
def historial(request):
    data = models.dataSalud.objects.all()
    datos = { 'dataSalud' : data}
    
    return render(request, "historial/historial.html", datos)

@login_required(login_url='autenticacion')
def signout(request):
    logout(request)
    return redirect("autenticacion")