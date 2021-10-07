from django.urls import path
from dog_house.views import DogBoardingVisit, GenerateFakeRandomData

urlpatterns = [
    path('home/', DogBoardingVisit.as_view(), name='boarding-visit'),
    path('fake_data_ajax/', GenerateFakeRandomData.as_view(), name='fake_data_ajax')
]
