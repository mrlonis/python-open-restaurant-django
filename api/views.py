from datetime import datetime
from typing import cast

from django.db.models import Q
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request

from api.models import Restaurant
from api.serializers import RestaurantSerializer


class SharedRestaurantQueryset(GenericAPIView):
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Restaurant.objects.all()
        request = cast(Request, self.request)
        date_param = request.query_params.get("date")
        if date_param is not None:
            date = datetime.fromisoformat(date_param)
            query_time = date.time()
            weekday = date.weekday()
            queryset = queryset.filter(
                Q(Q(Q(open_weekday=weekday) & Q(open_time__lte=query_time)) | Q(open_weekday__lt=weekday))
                & Q(Q(Q(close_weekday=weekday) & Q(close_time__gte=query_time)) | Q(close_weekday__gt=weekday))
            )
        return queryset


class RestaurantListCreateAPI(SharedRestaurantQueryset, ListCreateAPIView):
    serializer_class = RestaurantSerializer


class RestaurantAPIView(SharedRestaurantQueryset, RetrieveUpdateDestroyAPIView):
    # pylint: disable=too-many-ancestors
    serializer_class = RestaurantSerializer
