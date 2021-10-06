from django.urls import path
from dog_house.views import DogBoardingVisit, DogBoardingCalenderVisit

urlpatterns = [
    path('', DogBoardingVisit.as_view(), name='boarding-visit'),
    path('calender/', DogBoardingCalenderVisit.as_view(), name='boarding-calender')
]
