import uuid

from django.db import models


# Create your models here.
class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    open_weekday = models.IntegerField(null=False, blank=False)
    open_time = models.TimeField(null=False, blank=False)
    close_weekday = models.IntegerField(null=False, blank=False)
    close_time = models.TimeField(null=False, blank=False)
