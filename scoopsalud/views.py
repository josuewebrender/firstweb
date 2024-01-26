from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from scoopsalud.serializers import scoopsaludSerializer

from vistaTablas.models import dataSalud
from django.http import JsonResponse
from vistaTablas import models
from datetime import datetime
import pytz

DEBUG = False

class scoopsaludViewSet(ModelViewSet):
    serializer_class = scoopsaludSerializer
    queryset = dataSalud.objects.all()
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        print(request)
        print(request.data)
        print(request.headers)
        cabecera = request.headers
        try:
            if(cabecera["ApiKey"]!="41FFC272-4960-484F-998F-CB981EE3E01B"):
                return JsonResponse({'envio': 'Error en header ApiKey'}, status=500)
        except:
            return JsonResponse({'envio': 'Error en header ApiKey'}, status=500)
        datos = request.data
        
        try:
            if(not(datos["registro"])):
                return JsonResponse({'envio': 'Error'}, status=500)
        except:
            return JsonResponse({'envio': 'Error'}, status=500)

        try:
            if(not(datos["id_empresa"])):
                return JsonResponse({'envio': 'Error'}, status=500)
        except:
            return JsonResponse({'envio': 'Error'}, status=500)

        try:
            if(not(datos["Cargadora"])):
                return JsonResponse({'envio': 'Error'}, status=500)
        except:
            return JsonResponse({'envio': 'Error'}, status=500)

        try:
            if(not(datos["id_dispositivo"])):
                return JsonResponse({'envio': 'Error'}, status=500)
        except:
            return JsonResponse({'envio': 'Error'}, status=500)

        
        data = datos["registro"]
        idEmpresa = datos["id_empresa"]
        cargadora = datos["Cargadora"]
        idDispositivo = datos["id_dispositivo"]
        for i in data:
            #print(i)
            nuevoRegistro = models.dataSalud()
            nuevoRegistro.id_empresa      = idEmpresa
            nuevoRegistro.Cargadora       = cargadora
            nuevoRegistro.id_dispositivo  = idDispositivo
            nuevoRegistro.id_parametro    = i["I"]
            nuevoRegistro.valor_parametro = i["P"]
            fecha = datetime.fromtimestamp(int(i["F"])).strftime('%Y-%m-%d %H:%M:%S')
            fecha_datetime = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
            zona_horaria = pytz.timezone('America/Lima')
            fecha_y_hora_con_zona_horaria = zona_horaria.localize(fecha_datetime)
            nuevoRegistro.fh_lecturamaquina = fecha_y_hora_con_zona_horaria
            nuevoRegistro.save()
        
        return JsonResponse({'envio': 'OK'}, status=200)