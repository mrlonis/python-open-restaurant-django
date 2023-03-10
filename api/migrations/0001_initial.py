# pylint: disable=invalid-name
# Generated by Django 4.1.7 on 2023-03-10 04:48
import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("open_weekday", models.IntegerField()),
                ("open_time", models.TimeField()),
                ("close_weekday", models.IntegerField()),
                ("close_time", models.TimeField()),
            ],
        ),
    ]
