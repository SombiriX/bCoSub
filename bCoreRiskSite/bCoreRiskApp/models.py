from django.db import models


class Risk(models.Model):
    risk_class = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class RiskField(models.Model):
    TXT = 'T'
    NUM = 'N'
    DAT = 'D'
    ENM = 'E'
    FIELD_TYPE_CHOICES = (
        (TXT, 'Text'),
        (NUM, 'Number'),
        (DAT, 'Date'),
        (ENM, 'Enum'),
    )
    field_name = models.CharField(max_length=200)
    field_text = models.TextField(null=True, blank=True, max_length=1000)
    field_num = models.FloatField(null=True, blank=True)
    field_date = models.DateField(null=True, blank=True)
    field_enum = models.IntegerField(null=True, blank=True)
    field_type = models.CharField(
        max_length=1,
        choices=FIELD_TYPE_CHOICES,
    )
    risk = models.ForeignKey(
        Risk,
        related_name='risk_fields',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    risk_field = models.ForeignKey(
        RiskField,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
