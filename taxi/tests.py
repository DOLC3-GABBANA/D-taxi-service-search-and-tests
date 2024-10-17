from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from taxi.models import Driver, Car, Manufacturer


class UserTestCase(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.login(username="testuser", password="testpass")


class ManufacturerViewTests(UserTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer1", country="Japan"
        )
        self.manufacturer2 = Manufacturer.objects.create(
            name="Manufacturer2", country="Germany"
        )

    def test_search_manufacturer_by_name(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"manufacturer_search_query": "Manufacturer1"})
        self.assertContains(response, "Manufacturer1")
        self.assertNotContains(response, "Manufacturer2")

    def test_manufacturer_list_without_search(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertContains(response, "Manufacturer1")
        self.assertContains(response, "Manufacturer2")


class CarViewTests(UserTestCase):
    def setUp(self):
        super().setUp()
        self.manufacturer1 = Manufacturer.objects.create(
            name="Manufacturer1", country="Japan"
        )
        self.car1 = Car.objects.create(model="CarModel1", manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="CarModel2", manufacturer=self.manufacturer1)

    def test_search_car_by_model(self):
        response = self.client.get(reverse("taxi:car-list"), {"car_search_query": "CarModel1"})
        self.assertContains(response, "CarModel1")
        self.assertNotContains(response, "CarModel2")

    def test_car_list_without_search(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertContains(response, "CarModel1")
        self.assertContains(response, "CarModel2")


class DriverViewTests(UserTestCase):
    def setUp(self):
        super().setUp()
        self.driver1 = Driver.objects.create(username="driver1", license_number="ABC123")
        self.driver2 = Driver.objects.create(username="driver2", license_number="DEF456")

    def test_search_driver_by_username(self):
        response = self.client.get(reverse("taxi:driver-list"), {"driver_search_query": "driver1"})
        self.assertContains(response, "driver1")
        self.assertNotContains(response, "driver2")

    def test_driver_list_without_search(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertContains(response, "driver1")
        self.assertContains(response, "driver2")


class ManufacturerModelTests(TestCase):
    def test_manufacturer_creation(self):
        manufacturer = Manufacturer.objects.create(name="TestManufacturer", country="TestCountry")
        self.assertEqual(manufacturer.name, "TestManufacturer")
        self.assertEqual(manufacturer.country, "TestCountry")


class CarModelTests(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(name="TestManufacturer", country="TestCountry")

    def test_car_creation(self):
        car = Car.objects.create(model="TestCarModel", manufacturer=self.manufacturer)
        self.assertEqual(car.model, "TestCarModel")
        self.assertEqual(car.manufacturer.name, "TestManufacturer")


class DriverModelTests(TestCase):
    def test_driver_creation(self):
        driver = Driver.objects.create(username="TestDriver", license_number="XYZ123")
        self.assertEqual(driver.username, "TestDriver")
        self.assertEqual(driver.license_number, "XYZ123")
