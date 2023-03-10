import uuid
from datetime import time
from typing import cast

from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase


def build_test_data():
    return {
        "name": "test restaurant",
        "open_weekday": 0,
        "open_time": time(0, 0, 0),
        "close_weekday": 0,
        "close_time": time(12, 0, 0),
    }


class RestaurantAPITest(APITestCase):
    client: APIClient

    def setUp(self):
        self.url = "/api/restaurant/"

    def test_create_restaurant(self):
        response = cast(Response, self.client.post(self.url, data=build_test_data(), format="json"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_restaurant(self):
        # Create restaurant
        response = cast(Response, self.client.post(self.url, data=build_test_data(), format="json"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_response_json = response.json()

        # Get restaurant
        url = f"{self.url}{post_response_json['id']}/"
        response = cast(Response, self.client.get(url, format="json"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_response_json = response.json()
        self.assertEqual(post_response_json, get_response_json)

    def test_get_restaurant_that_does_n0t_exist(self) -> None:
        # Get restaurant
        url = f"{self.url}{str(uuid.uuid4())}/"
        response = cast(Response, self.client.get(url, format="json"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_restaurant(self):
        # Create restaurant
        response = cast(Response, self.client.post(self.url, data=build_test_data(), format="json"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_response_json = response.json()

        # Update restaurant
        update_data = {
            "name": "updated restaurant name",
            "open_weekday": 1,
            "open_time": time(1, 0, 0),
            "close_weekday": 1,
            "close_time": time(1, 0, 0),
        }
        url = f"{self.url}{post_response_json['id']}/"
        response = cast(Response, self.client.put(url, data=update_data, format="json"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        put_response_json = response.json()

        self.assertEqual(put_response_json["name"], "updated restaurant name")
        self.assertEqual(put_response_json["open_weekday"], 1)
        self.assertEqual(put_response_json["open_time"], "01:00:00")
        self.assertEqual(put_response_json["close_weekday"], 1)
        self.assertEqual(put_response_json["close_time"], "01:00:00")

    def test_delete_restaurant(self):
        # Create restaurant
        response = cast(Response, self.client.post(self.url, data=build_test_data(), format="json"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_response_json = response.json()

        # Get restaurant
        url = f"{self.url}{post_response_json['id']}/"
        response = cast(Response, self.client.get(url, format="json"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete restaurant
        url = f"{self.url}{post_response_json['id']}/"
        response = cast(Response, self.client.delete(url, format="json"))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
