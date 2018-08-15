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

    def update(self, rField, validated_data):
        # Update the existing field
        # continue with existing data if inputs are None
        rField.field_name = validated_data.get('field_name', rField.field_name)
        rField.field_type = validated_data.get('field_type', rField.field_type)
        rField.risk = validated_data.get('risk_id', rField.risk)
        rField.save()
        return rField


class ChoiceSerializer(serializers.ModelSerializer):
    risk_field = serializers.PrimaryKeyRelatedField(queryset=RiskField.objects.all())

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

    def update(self, choice, validated_data):
        # Update the existing field
        # continue with existing data if inputs are None
        choice.choice_text = validated_data.get('choice_text', choice.choice_text)
        choice.risk_field = validated_data.get('risk_field', choice.risk_field)
        choice.save()
        return choice
