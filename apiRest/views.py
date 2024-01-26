from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from apiRest.serializers import apiRestSerializer

from vistaTablas.models import dataSalud

DEBUG = False

class apiRestViewSet(ModelViewSet):
    serializer_class = apiRestSerializer
    queryset = dataSalud.objects.all()
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

