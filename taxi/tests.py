from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from taxi.models import Driver, Car, Manufacturer


class SearchTests(TestCase):

    def setUp(self):
        self.user = Driver.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Создаем уникальные license_number для каждого водителя
        self.driver1 = Driver.objects.create(username="driver1", license_number="ABC123")
        self.driver2 = Driver.objects.create(username="driver2", license_number="DEF456")

        # Создаем уникальные модели автомобилей и присваиваем производителю
        self.manufacturer1 = Manufacturer.objects.create(name="Manufacturer1", country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Manufacturer2", country="Germany")

        self.car1 = Car.objects.create(model="CarModel1", manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="CarModel2", manufacturer=self.manufacturer2)

    def test_search_driver_by_username(self):
        # Тест на поиск водителя по username
        response = self.client.get(reverse("taxi:driver-list"), {"q": "driver1"})
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_search_car_by_model(self):
        # Тест на поиск автомобиля по модели
        response = self.client.get(reverse("taxi:car-list"), {"q": "CarModel1"})
        self.assertContains(response, "CarModel1")
        self.assertNotContains(response, "CarModel2")

    def test_search_manufacturer_by_name(self):
        # Тест на поиск производителя по имени
        response = self.client.get(reverse("taxi:manufacturer-list"), {"q": "Manufacturer1"})
        self.assertContains(response, "Manufacturer1")
        self.assertNotContains(response, "Manufacturer2")
