from datetime import datetime
from typing import Dict, List, cast

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from api.models import Restaurant


class RestaurantAPITest(APITestCase):
    client: APIClient

    def setUp(self):
        self.url = "/api/restaurants"

    def test_restaurants_route_no_params(self):
        response = cast(Response, self.client.get(self.url))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(len(response_json), 276)

    def test_restaurants_route_with_datetime_param(self):
        # datetime.now() check for 200 response
        param = datetime.now()
        response = cast(Response, self.client.get(f"{self.url}?date={param.isoformat()}"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Thursday December 8th, 11:11 AM
        param = datetime(2022, 12, 8, 11, 11)
        response = cast(Response, self.client.get(f"{self.url}?date={param.isoformat()}"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        restaurants: List[Dict] = response.json()
        assert len(restaurants) == 25
        restaurant = Restaurant(**restaurants[0])
        assert restaurant.name == "The Cowfish Sushi Burger Bar"

        # Thursday December 8th - No Time
        response = cast(Response, self.client.get(f"{self.url}?date=2022-12-08"))
        assert response.status_code == 200
        restaurants: list[dict] = response.json()
        assert len(restaurants) == 5

        # Thursday December 8th, 12:00 AM
        param = datetime(2022, 12, 8, 0, 0)
        response = cast(Response, self.client.get(f"{self.url}?date={param.isoformat()}"))
        assert response.status_code == 200
        restaurants: list[dict] = response.json()
        assert len(restaurants) == 5
