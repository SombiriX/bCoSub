from rest_framework import serializers
from .models import Risk, RiskField, Choice

TXT = 'T'
NUM = 'N'
DAT = 'D'
ENM = 'E'


class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = '__all__'
        depth = 1


class riskFieldFieldSerializer(serializers.Field):
    """
    Custom field to make a dyanmic read / write field for the
    riskField Model
    """

    def __init__(self, **kwargs):
        kwargs['source'] = '*'
        kwargs['read_only'] = False
        super(riskFieldFieldSerializer, self).__init__(**kwargs)

    def to_representation(self, obj):
        if obj.field_type == TXT:
            return obj.field_text
        if obj.field_type == NUM:
            return obj.field_num,
        if obj.field_type == DAT:
            return obj.field_date,
        if obj.field_type == ENM:
            return obj.field_enum_text
        raise AssertionError("Field type is not defined")

    def to_internal_value(self, data):
        return {
            'field': data
            }


class RiskFieldSerializer(serializers.ModelSerializer):
    risk_id = serializers.PrimaryKeyRelatedField(queryset=Risk.objects.all())
    field = riskFieldFieldSerializer()

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

        # Use the dynamic field "field" to update this risksField's
        # underlying data
        field_input = validated_data.get('field', None)
        if rField.field_type == TXT:
            rField.field_text = field_input
        elif rField.field_type == NUM:
            rField.field_num = field_input
        elif rField.field_type == DAT:
            rField.field_date = field_input
        elif rField.field_type == ENM:
            rField.field_enum_text = field_input
        else:
            raise AssertionError("Invalid Field type", rField.field_type)
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
