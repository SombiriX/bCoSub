from rest_framework import serializers
from .models import Risk, RiskField, Choice


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = '__all__'
        depth = 1


class RiskFieldSerializer(serializers.ModelSerializer):
    risk_id = serializers.PrimaryKeyRelatedField(queryset=Risk.objects.all())

    class Meta:
        model = RiskField
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        rField = RiskField.objects.create(
            field_name=validated_data['field_name'],
            field_type=validated_data['field_type'],
            risk=validated_data['risk_id'],
        )

        return rField


class ChoiceSerializer(serializers.ModelSerializer):
    rField_id = serializers.PrimaryKeyRelatedField(queryset=RiskField.objects.all())

    class Meta:
        model = Choice
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        choice = Choice.objects.create(
            choice_text=validated_data['choice_text'],
            risk_field=validated_data['risk_field'],
        )

        return choice
