import json
from collections import Counter

from constants import *
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from dog_house.forms import DogHouseVisitForm
from dog_house.generate_fake_data import generate_fake_data
from dog_house.models import BoardingVisit


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class DogBoardingVisit(TemplateView):
    form_class = DogHouseVisitForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'dog_house/index.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = BoardingVisit.objects.filter(
                start_date__range=[request.POST.get('start_date'), request.POST.get('end_date')],
                end_date__range=[request.POST.get('start_date'), request.POST.get('end_date')]).values('first_name',
                                                                                                       'last_name',
                                                                                                       'start_date',
                                                                                                       'end_date').order_by(
                'start_date', 'end_date', 'first_name')
            for d in data:
                d['start_date'] = str(d['start_date'])
                d['end_date'] = str(d['end_date'])
            signs = Counter(k['start_date'] for k in data if k.get('start_date'))
            calendar_data = [{'title': f'{count} dogs' if count > 1 else f'{count} dog', 'start': str(sign)} for
                             sign, count in signs.most_common()]

            return render(request, 'dog_house/details.html',
                          {'data': json.dumps(calendar_data), 'calender_data': json.dumps(list(data)),
                           'start_date': request.POST.get('start_date'),
                           'end_date': request.POST.get('end_date')})
        messages.warning(request, FORM_FIELD_ERRORS)
        return render(request, 'dog_house/index.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class GenerateFakeRandomData(View):
    def post(self, request, *args, **kwargs):
        fake_data = generate_fake_data()
        delete_data = BoardingVisit.objects.all()
        delete_data.delete()
        for data in fake_data:
            board_visit = BoardingVisit(first_name=data['first_name'], last_name=data['last_name'],
                                        start_date=data['start_date'],
                                        end_date=data['end_date'])
            board_visit.save()

        return JsonResponse(data={'message': "Fake data created successfully"})
