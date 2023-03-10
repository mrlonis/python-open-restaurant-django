from rest_framework import serializers

from api import models


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        # pylint: disable=too-few-public-methods
        model = models.Restaurant
        fields = "__all__"
