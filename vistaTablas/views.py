from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

from django.http.response import HttpResponse
from . import models
from django.db.models import Q
import pytz
from django.utils import timezone
import openpyxl

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
    print("Ingreso historial")
    if request.method == "POST" and request.POST.get("Comando") == "TablaHistorial":
        print("Ingreso TablaHistorial")
        min = request.POST.get("min")
        max = request.POST.get("max")
        draw = int(request.POST.get('draw', 0))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 0))
        search_value = request.POST.get('search[value]', '')
        queryset = models.dataSalud.objects.order_by(
            '-fh_lecturamaquina', '-id')
        if min != "" and max != "":
            queryset = queryset.filter(
                fh_lecturamaquina__range=(min, max)).order_by('-fh_lecturamaquina', '-id')
        if search_value != '':
            queryset = queryset.filter(
                Q(id__icontains=search_value) |
                Q(id_empresa__icontains=search_value) |
                Q(Cargadora__icontains=search_value) |
                Q(id_dispositivo__icontains=search_value) |
                Q(id_parametro__icontains=search_value) |
                Q(valor_parametro__icontains=search_value) |
                Q(fh_lecturamaquina__icontains=search_value) |
                Q(fh_escrituranube__icontains=search_value) 
            ).order_by('-fh_lecturamaquina', '-id')
        total_records = queryset.count()
        queryset = queryset[start:start+length]
        data = []
        id = total_records - start + 1
        for obj in queryset:
            id -= 1
            item = {
                'primarykey': obj.id,
                'id': obj.id,
                'id_empresa': obj.id_empresa,
                'Cargadora': obj.Cargadora,
                'id_dispositivo': obj.id_dispositivo,
                'id_parametro': obj.id_parametro,
                'valor_parametro': obj.valor_parametro,
                'fh_lecturamaquina': obj.fh_lecturamaquina,
                'fh_escrituranube': obj.fh_escrituranube,
            }
            data.append(item)
        response = {
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data
        }
        print(response)
        return JsonResponse(response)
    elif request.method == "GET" and request.GET.get("Comando") == "DescargarExcel":
        print("Descargar Excel")
        min = request.GET.get('FechaInicial')
        max = request.GET.get('FechaFinal')
        search_value = request.GET.get('Search', '')
        queryset = models.dataSalud.objects.order_by('-id')
        print('0')
        print("1")
        if min != "" and max != "":
            queryset = queryset.filter(
                fh_lecturamaquina__range=(min, max)).order_by('-id')
            print("2")
        print(search_value)
        if search_value != '':
           queryset = queryset.filter(
                Q(id__icontains=search_value) |
                Q(id_empresa__icontains=search_value) |
                Q(Cargadora__icontains=search_value) |
                Q(id_dispositivo__icontains=search_value) |
                Q(id_parametro__icontains=search_value) |
                Q(valor_parametro__icontains=search_value) |
                Q(fh_lecturamaquina__icontains=search_value) |
                Q(fh_escrituranube__icontains=search_value) 
            ).order_by('-fh_lecturamaquina', '-id')
        print("3")
        total_records = queryset.count() + 1
        wb = openpyxl.Workbook()
        ws = wb.active
        print("4")
        print(total_records)
        #print(queryset)
        print("4r")
        ws.append(['#', 'id_empresa', 'Cargadora', 'id_dispositivo', 'id_parametro','valor_parametro', 'fh_lecturamaquina', 'fh_escrituranube'])
        #ws.append([str(total_records), str(queryset[0].id_empresa), str(queryset[0].Cargadora), str(queryset[0].id_dispositivo), str(queryset[0].id_parametro), str(queryset[0].valor_parametro), str(queryset[0].fh_lecturamaquina),str(queryset[0].fh_escrituranube)]) 
        #wb.save("test.xlsx")
        #wb.close()
        for item in queryset:
            print(item.id_empresa)
            total_records -= 1
            ws.append([str(total_records), str(item.id_empresa), str(item.Cargadora), str(item.id_dispositivo), str(item.id_parametro), str(item.valor_parametro), str(item.fh_lecturamaquina),str(item.fh_escrituranube)]) 
            #ws.append([str(total_records), item.id_empresa, item.Cargadora, item.id_dispositivo, item.id_parametro, item.valor_parametro, item.fh_lecturamaquina,item.fh_escrituranube])
        #print(ws)
        response = HttpResponse(content_type='application/ms-excel')
        print("5")
        response['Content-Disposition'] = 'attachment; filename="Historial_data.xlsx"'
        print("6")
        #print(response['content-Disposition'])
        #print(response)
        wb.save(response)
        #wb.close()
        print("7")
        return response
        
    data = models.dataSalud.objects.all()
    datos = { 'dataSalud' : data}
    
    return render(request, "historial/historial.html", datos)

@login_required(login_url='autenticacion')
def signout(request):
    logout(request)
    return redirect("autenticacion")
