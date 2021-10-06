from django.db import models
from django.core.exceptions import ValidationError
from constants import *


# Create your models here.
class BoardingVisit(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ('first_name', 'last_name')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(START_DATE_INVALID)
