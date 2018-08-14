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
    field_text = models.TextField(null=True, blank=True)
    field_num = models.FloatField(null=True, blank=True)
    field_date = models.DateTimeField(null=True, blank=True)
    field_enum_text = models.CharField(max_length=200, null=True, blank=True)
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

    @property
    def field(self):
        if self.field_type == self.TXT:
            return self.field_text
        if self.field_type == self.NUM:
            return self.field_num,
        if self.field_type == self.DAT:
            return self.field_date,
        if self.field_type == self.ENM:
            return self.field_enum_text
        raise AssertionError("Field type is not defined")


class Choice(models.Model):
    choice_text = models.CharField(max_length=200, null=True)
    risk_field = models.ForeignKey(
        RiskField,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
