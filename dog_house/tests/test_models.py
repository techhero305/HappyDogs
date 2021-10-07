import datetime

from constants import *
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from dog_house.models import BoardingVisit


class BoardingVisitSuccessTestCase(TestCase):
    def setUp(self):
        BoardingVisit.objects.create(first_name="test", last_name="dog", start_date="2021-10-06", end_date="2021-10-07")

    def test_dogs_first_name(self):
        dog_visit = BoardingVisit.objects.get(id=1)
        self.assertEqual(dog_visit.first_name, "test")

    def test_dogs_last_name(self):
        dog_visit = BoardingVisit.objects.get(id=1)
        self.assertEqual(dog_visit.last_name, "dog")


class BoardingVisitFailureTestCase(TestCase):
    def test_dogs_date_validation(self):
        dog_visit = BoardingVisit(first_name="test", last_name="dog",
                                  start_date=datetime.datetime.strptime("2021-10-06", "%Y-%m-%d").date(),
                                  end_date=datetime.datetime.strptime("2021-10-05", "%Y-%m-%d").date())
        with self.assertRaises(ValidationError, msg=START_DATE_GREATER_END_DATE):
            dog_visit.clean()

    def test_dogs_start_date_validation(self):
        dog_visit = BoardingVisit(first_name="test", last_name="dog",
                                  start_date=datetime.datetime.strptime("2021-10-05", "%Y-%m-%d").date(),
                                  end_date=datetime.datetime.strptime("2021-10-06", "%Y-%m-%d").date())
        with self.assertRaises(ValidationError, msg=START_DATE_INVALID):
            dog_visit.clean()

    def test_dogs_unique_field_start_date_validation(self):
        BoardingVisit.objects.create(first_name="test", last_name="dog",
                                     start_date=datetime.datetime.strptime("2021-10-06", "%Y-%m-%d").date(),
                                     end_date=datetime.datetime.strptime("2021-10-08", "%Y-%m-%d").date())
        with self.assertRaises(IntegrityError):
            BoardingVisit.objects.create(first_name="test", last_name="dog",
                                         start_date=datetime.datetime.strptime("2021-10-06", "%Y-%m-%d").date(),
                                         end_date=datetime.datetime.strptime("2021-10-09", "%Y-%m-%d").date())

    def test_dogs_unique_field_end_date_validation(self):
        BoardingVisit.objects.create(first_name="test", last_name="dog",
                                     start_date=datetime.datetime.strptime("2021-10-06", "%Y-%m-%d").date(),
                                     end_date=datetime.datetime.strptime("2021-10-08", "%Y-%m-%d").date())
        with self.assertRaises(IntegrityError):
            BoardingVisit.objects.create(first_name="test", last_name="dog",
                                         start_date=datetime.datetime.strptime("2021-10-07", "%Y-%m-%d").date(),
                                         end_date=datetime.datetime.strptime("2021-10-08", "%Y-%m-%d").date())
