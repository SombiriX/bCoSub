from rest_framework import serializers
from .models import Risk, RiskField, Choice


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = '__all__'
        depth = 1


class RiskFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskField
        fields = '__all__'
        depth = 1


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'
        depth = 1
