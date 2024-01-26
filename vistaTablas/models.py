from django.db import models
from django.contrib.auth.models import User

# Create your models here.
import pytz
from django.utils import timezone

lima_timezone = pytz.timezone('America/Lima')
lima_time = timezone.now().astimezone(
     pytz.timezone('America/Lima'))

class dataSalud(models.Model):
    id               = models.BigAutoField(primary_key=True)
    id_empresa       = models.CharField(max_length=50, null=False)
    Cargadora        = models.CharField(max_length=50, null=False)
    id_dispositivo   = models.CharField(max_length=50, null=False)
    
    id_parametro     = models.CharField(max_length=50, null=False)
    valor_parametro  = models.CharField(max_length=50, null=False)
    fh_lecturamaquina = models.DateTimeField(auto_now_add=False,  null=True)
    
    fh_escrituranube = models.DateTimeField(auto_now_add=True,  null=True)

    def __str__(self):
        return str(self.id)+" "+str(self.id_maquina)+str(self.id_empresa)

    class Meta:
        db_table = 'Historial'