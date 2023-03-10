from typing import cast

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase


class RestaurantAPITest(APITestCase):
    client: APIClient

    def setUp(self):
        self.url = "/api/restaurant/"

    def test_restaurants_route_no_params(self):
        response = cast(Response, self.client.get(self.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 276)
