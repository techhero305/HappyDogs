import datetime

from constants import *
from django.test import RequestFactory, TestCase, Client
from django.urls import reverse
from dog_house.models import BoardingVisit


class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.boarding_visit_1 = BoardingVisit.objects.create(first_name="test", last_name="dog",
                                                             start_date="2021-10-06", end_date="2021-10-07")
        self.boarding_visit_2 = BoardingVisit.objects.create(first_name="test", last_name="dog2",
                                                             start_date="2021-10-06", end_date="2021-10-07")

    def test_can_access_boarding_visit(self):
        response = self.client.get(reverse('boarding-visit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dog_house/index.html')

    def test_boarding_visit(self):
        response = self.client.get(reverse('boarding-visit'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dog_house/index.html')

        response = self.client.post(reverse('boarding-visit'),
                                    {'start_date': datetime.datetime.strptime("2021-10-06", "%Y-%m-%d").date(),
                                     'end_date': datetime.datetime.strptime("2021-10-20", "%Y-%m-%d").date()})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dog_house/details.html')

    def test_validation_error_empty_input_boarding_visit(self):
        response = self.client.post(reverse('boarding-visit'), {})
        self.assertFormError(response, 'form', 'start_date', 'This field is required.')
        self.assertTemplateUsed(response, 'dog_house/index.html')

    def test_validation_error_empty_start_date_boarding_visit(self):
        response = self.client.post(reverse('boarding-visit'),
                                    {'end_date': datetime.datetime.strptime("2021-10-20", "%Y-%m-%d").date()})
        self.assertFormError(response, 'form', 'start_date', 'This field is required.')
        self.assertTemplateUsed(response, 'dog_house/index.html')

    def test_validation_error_empty_end_date_boarding_visit(self):
        response = self.client.post(reverse('boarding-visit'),
                                    {'start_date': datetime.datetime.strptime("2021-10-20", "%Y-%m-%d").date()})
        self.assertFormError(response, 'form', 'end_date', 'This field is required.')
        self.assertTemplateUsed(response, 'dog_house/index.html')

    def test_validation_error_invalid_date_boarding_visit(self):
        response = self.client.post(reverse('boarding-visit'),
                                    {'start_date': datetime.datetime.strptime("2021-10-20", "%Y-%m-%d").date(),
                                     'end_date': datetime.datetime.strptime("2021-10-10", "%Y-%m-%d").date()})
        self.assertFormError(response, 'form', 'start_date', START_DATE_GREATER_END_DATE)
        self.assertTemplateUsed(response, 'dog_house/index.html')
