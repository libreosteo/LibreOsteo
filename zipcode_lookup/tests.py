from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import ZipcodeMapping

UserModel = get_user_model()

class TestViews(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_superuser(
            "test", "test@test.com", "testpw")
        self.client.login(username='test', password='testpw')

        ZipcodeMapping.objects.bulk_create([
            # One zipcode, two cities
            ZipcodeMapping(city='A', zipcode='12345'),
            ZipcodeMapping(city='Abis', zipcode='12345'),
            # one zipcode one city
            ZipcodeMapping(city='B', zipcode='00000'),
            # one city two zipcodes
            ZipcodeMapping(city='C', zipcode='11111'),
            ZipcodeMapping(city='C', zipcode='11112'),
        ])
    
    def test_zipcode_lookup(self):
        self.assertEqual(
            self.client.get('/zipcode_lookup/zipcode_lookup/54321').json(),
            []
        )
        self.assertEqual(
            self.client.get('/zipcode_lookup/zipcode_lookup/12345').json(),
            [{'city': 'A', 'zipcode': '12345'}, {'city': 'Abis', 'zipcode': '12345'}]
        )
        self.assertEqual(
            self.client.get('/zipcode_lookup/zipcode_lookup/00000').json(),
            [{'city': 'B', 'zipcode': '00000'}]
        )
        self.assertEqual(
            self.client.get('/zipcode_lookup/zipcode_lookup/11111').json(),
            [{'city': 'C', 'zipcode': '11111'}]
        )
