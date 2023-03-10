from django.urls import path

from api.views import RestaurantAPIView, RestaurantListCreateAPI

urlpatterns = [
    path("restaurant/", RestaurantListCreateAPI.as_view(), name="restaurant"),
    path("restaurant/<uuid:pk>/", RestaurantAPIView.as_view(), name="restaurant"),
]
