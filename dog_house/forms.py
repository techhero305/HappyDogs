from django import forms
from constants import *


class DogHouseVisitForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        print(start_date, end_date)
        if start_date and end_date:
            if end_date < start_date:
                raise forms.ValidationError("End date should be greater than start date.")
