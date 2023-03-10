import csv
from datetime import time
from pathlib import Path
from typing import Literal, cast

from django.db.models.base import ModelBase

T = Literal["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]  # pylint: disable=invalid-name

ACRONYM_MAP = {
    "Mon": 0,
    "Tues": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
}


def map_weekday_acronym_to_int(acronym: T):
    result = ACRONYM_MAP.get(acronym)
    assert result is not None
    return result


def csv_import(file_path: str, model: ModelBase) -> list[ModelBase]:
    restaurants: list[ModelBase] = []

    with open(Path(file_path).resolve(), newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = cast(str, row["Restaurant Name"])
            hours = cast(str, row["Hours"])

            split_hours = hours.split("  / ")
            for split_hour in split_hours:
                # Weekday range
                weekday_range = _process_weekday_range(split_hour)

                # Time Processing
                open_time, open_time_am_pm, close_time, close_time_am_pm = _process_time(split_hour)

                # Build Weekdays
                restaurants.extend(
                    _build_restaurants(
                        name, weekday_range, open_time, open_time_am_pm, close_time, close_time_am_pm, model=model
                    )
                )

    return restaurants


def _process_weekday_range(weekday_range: str):
    weekdays: list[int] = []

    comma_split = weekday_range.split(", ")
    for split in comma_split:
        space_split = split.split(" ")
        split = space_split[0]

        if "-" in split:
            weekday_range_split = split.split("-")
            if len(weekday_range_split) < 2:
                raise ValueError("weekday_range_split was less than 2 despite having a -")

            start_weekday = cast(T, weekday_range_split[0])
            end_weekday = cast(T, weekday_range_split[1])
            weekdays.extend(
                list(range(map_weekday_acronym_to_int(start_weekday), map_weekday_acronym_to_int(end_weekday) + 1))
            )
        else:
            weekdays.append(map_weekday_acronym_to_int(cast(T, split)))

    return weekdays


def _parse_time(time_str: str, am_pm: str):
    # Check for Colon
    colon_split = time_str.split(":")
    if len(colon_split) == 2:
        return_time = time(int(colon_split[0]), int(colon_split[1]))
    elif len(colon_split) == 1:
        return_time = time(int(colon_split[0]))
    else:
        raise ValueError("Invalid Time")

    # If AM we need to set to 0 if 12
    if am_pm == "am" and return_time.hour == 12:
        return_time = time(0, return_time.minute)

    # If PM we need to add 12 hours
    if am_pm == "pm" and return_time.hour < 12:
        return_time = time(return_time.hour + 12, return_time.minute)

    return return_time


def _process_time(time_str: str) -> tuple[time, str, time, str]:
    # Time Processing
    space_split = time_str.split(" ")
    if len(space_split) < 6:
        raise ValueError("Length of time split was not 6 or more")

    # Open Time
    open_time_am_pm = space_split[-4]
    open_time = _parse_time(space_split[-5], open_time_am_pm)

    # Close Time
    close_time_am_pm = space_split[-1]
    close_time = _parse_time(space_split[-2], close_time_am_pm)

    return open_time, open_time_am_pm, close_time, close_time_am_pm


def _build_restaurants(
    name: str,
    weekday_range: list[int],
    open_time: time,
    open_time_am_pm: str,
    close_time: time,
    close_time_am_pm: str,
    model: ModelBase,
):
    restaurants: list[ModelBase] = []

    for weekday in weekday_range:
        close_weekday = weekday
        # If open time is PM and close time is AM
        # or if open time is AM and close time is AM and open time is greater than close time
        # we need to add 1 day to the close time
        if (close_time_am_pm == "am" and open_time_am_pm == "pm") or (
            open_time_am_pm == "am" and close_time_am_pm == "am" and open_time.hour > close_time.hour
        ):
            close_weekday += 1

            # If close weekday is 7, set to 0
            if close_weekday == 7:
                close_weekday = 0

        temp_restaurant = model(
            name=name,
            open_weekday=weekday,
            open_time=open_time,
            close_weekday=close_weekday,
            close_time=close_time,
        )
        restaurants.append(temp_restaurant)

    return restaurants
