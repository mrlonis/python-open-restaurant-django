from django.urls import path

from api.views import RestaurantAPIView, RestaurantListCreateAPI

urlpatterns = [
    path("restaurants", RestaurantListCreateAPI.as_view(), name="restaurant"),
    path("restaurants/<uuid:pk>", RestaurantAPIView.as_view(), name="restaurant"),
]
