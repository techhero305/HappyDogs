from django.urls import path
from dog_house.views import DogBoardingVisit

urlpatterns = [
    path('', DogBoardingVisit.as_view(), name='boarding-visit'),
]
