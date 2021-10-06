import json

from constants import *
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from dog_house.forms import DogHouseVisitForm
from dog_house.models import BoardingVisit


# Create your views here.
class DogBoardingVisit(TemplateView):
    form_class = DogHouseVisitForm
    template_name = 'dog_house/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class DogBoardingCalenderVisit(View):
    def post(self, request, *args, **kwargs):
        data = BoardingVisit.objects.filter(
            start_date__range=[request.POST.get('start_date'), request.POST.get('end_date')],
            end_date__range=[request.POST.get('start_date'), request.POST.get('end_date')]).values('first_name',
                                                                                                   'last_name',
                                                                                                   'start_date',
                                                                                                   'end_date')
        for d in data:
            d['start_date'] = str(d['start_date'])
            d['end_date'] = str(d['end_date'])
        return JsonResponse({'data': json.dumps(list(data))})
