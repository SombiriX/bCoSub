from rest_framework import serializers
from .models import Risk, RiskField, Choice

# Useful defines for riskField object's field type
TXT = 'T'
NUM = 'N'
DAT = 'D'
ENM = 'E'


class RiskSerializer(serializers.ModelSerializer):
    """
    Read \ Writes a serialized Risk object
    """
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
        kwargs['required'] = False
        super(riskFieldFieldSerializer, self).__init__(**kwargs)

    def to_representation(self, obj):
        if obj.field_type == TXT:
            return obj.field_text
        if obj.field_type == NUM:
            return obj.field_num
        if obj.field_type == DAT:
            return obj.field_date
        if obj.field_type == ENM:
            return obj.field_enum
        raise AssertionError("Field type is not defined")

    def to_internal_value(self, data):
        return {
            'field': data
            }


class RiskFieldSerializer(serializers.ModelSerializer):
    """
    Read \ Writes a serialized RiskField object
    """
    risk_id = serializers.PrimaryKeyRelatedField(queryset=Risk.objects.all())
    field = riskFieldFieldSerializer()

    class Meta:
        model = RiskField
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        # Create a new riskField with required fields
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
        rField.risk = validated_data.get('risk_id', rField.risk)

        # Clear all fields if the field type is changing
        in_field_type = validated_data.get('field_type', rField.field_type)
        if rField.field_type != in_field_type:
            rField.field_text = None
            rField.field_num = None
            rField.field_date = None
            rField.field_enum = None
            rField.field_type = in_field_type

            rField.save()
            return rField

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
            rField.field_enum = field_input
        else:
            raise AssertionError("Invalid Field type", rField.field_type)
        rField.save()

        return rField

    def validate(self, data):
        field_input = data.get('field', None)
        if data['field_type'] == TXT:
            data.field_text = field_input
        elif data['field_type'] == NUM:
            data.field_num = field_input
        elif data['field_type'] == DAT:
            data.field_date = field_input
        elif data['field_type'] == ENM:
            data.field_enum = field_input
        else:
            raise AssertionError("Invalid Field type", data.field_type)
        return data


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Read \ Writes a serialized Choice object
    """
    risk_field = serializers.PrimaryKeyRelatedField(queryset=RiskField.objects.all())

    class Meta:
        model = Choice
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        # Create a new choice with required fields
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
