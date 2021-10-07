import datetime

from constants import *
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class BoardingVisit(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = [['first_name', 'last_name', 'start_date'], ['first_name', 'last_name', 'end_date']]

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError({'start_date': START_DATE_GREATER_END_DATE})
        if self.start_date < datetime.date.today():
            raise ValidationError({'start_date': START_DATE_INVALID})
        if BoardingVisit.objects.filter(start_date__range=[self.start_date, self.end_date],
                                        end_date__range=[self.start_date, self.end_date]).exists():
            raise ValidationError(INVALID_RECORD_CREATION)
