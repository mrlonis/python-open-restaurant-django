from rest_framework import generics

from api.models import Restaurant
from api.serializers import RestaurantSerializer


class RestaurantListCreateAPI(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RestaurantAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
