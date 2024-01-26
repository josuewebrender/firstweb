from rest_framework.serializers import ModelSerializer
from vistaTablas.models import dataSalud

class scoopsaludSerializer(ModelSerializer):
    class Meta:
        model = dataSalud
        fields = ['id','id_empresa', 'Cargadora','id_dispositivo', 'id_parametro', 'valor_parametro', 'fh_lecturamaquina', 'fh_escrituranube']
        