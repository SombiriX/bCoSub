from rest_framework import viewsets
from .models import Risk, RiskField, Choice
from .serializers import RiskSerializer, RiskFieldSerializer, ChoiceSerializer


class RiskSerializerViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer


class RiskFieldSerializerViewSet(viewsets.ModelViewSet):
    queryset = RiskField.objects.all()
    serializer_class = RiskFieldSerializer


class ChoiceSerializerViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
