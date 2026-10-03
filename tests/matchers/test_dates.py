from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest

from matchers.dates import Dates


@pytest.fixture
def sut() -> Dates:
    return Dates()


@pytest.fixture
def birthday(sut) -> date:
    return sut.get_birthday()


@pytest.fixture
def meeting_time(sut) -> datetime:
    return sut.get_meeting_time()


@pytest.fixture
def conference_start(sut) -> datetime:
    return sut.get_conference_start()


@pytest.fixture
def event_timestamp(sut) -> datetime:
    return sut.get_event_timestamp()


@pytest.fixture
def work_start(sut) -> time:
    return sut.get_work_start()


@pytest.fixture
def project_deadline(sut) -> date:
    return sut.get_project_deadline()


# date assertions
def test_should_be_1990_05_15(birthday):
    assert birthday == date(1990, 5, 15)


def test_should_be_before_today(birthday):
    assert birthday < date.today()


def test_should_be_after_1980_01_01(birthday):
    assert birthday > date(1980, 1, 1)


def test_should_be_in_may(birthday):
    assert birthday.month == 5


def test_should_be_in_year_1990(birthday):
    assert birthday.year == 1990


def test_should_be_on_day_15(birthday):
    assert birthday.day == 15


def test_project_deadline_should_be_in_future(project_deadline):
    assert project_deadline > date(2024, 1, 1)


def test_project_deadline_should_be_between_dates(project_deadline):
    assert date(2024, 1, 1) <= project_deadline <= date(2025, 12, 31)


# datetime assertions (naive, i.e. without time zone)
def test_meeting_time_should_be_2024_03_20_at_14_30(meeting_time):
    assert meeting_time == datetime(2024, 3, 20, 14, 30, 0)


def test_meeting_time_should_be_before_now(meeting_time):
    assert meeting_time < datetime.now()


def test_meeting_time_should_have_hour_14(meeting_time):
    assert meeting_time.hour == 14


def test_meeting_time_should_have_minute_30(meeting_time):
    assert meeting_time.minute == 30


def test_meeting_time_should_be_in_march_2024(meeting_time):
    assert (meeting_time.year, meeting_time.month) == (2024, 3)


# time assertions
def test_work_start_should_be_09_00(work_start):
    assert work_start == time(9, 0)


def test_work_start_should_be_before_noon(work_start):
    assert work_start < time(12, 0)


def test_work_start_should_have_hour_9(work_start):
    assert work_start.hour == 9


def test_work_start_should_be_between_08_and_10(work_start):
    assert time(8, 0) <= work_start <= time(10, 0)


# datetime assertions (aware, i.e. with time zone)
def test_conference_start_should_be_in_berlin_timezone(conference_start):
    assert conference_start.tzinfo == ZoneInfo("Europe/Berlin")


def test_conference_start_should_be_correct_date_time(conference_start):
    assert conference_start == datetime(2024, 6, 1, 9, 0, 0, tzinfo=ZoneInfo("Europe/Berlin"))
    # aware datetimes are compared as points in time: 09:00 in Berlin is 07:00 UTC in summer
    assert conference_start == datetime(2024, 6, 1, 7, 0, 0, tzinfo=timezone.utc)


def test_conference_start_should_have_european_offset(conference_start):
    assert conference_start.utcoffset() in (timedelta(hours=1), timedelta(hours=2))


# timestamp assertions (UTC)
def test_event_timestamp_should_be_correct(event_timestamp):
    assert event_timestamp == datetime.fromisoformat("2024-01-15T10:30:00+00:00")


def test_event_timestamp_should_be_in_past(event_timestamp):
    assert event_timestamp < datetime.now(timezone.utc)


def test_event_timestamp_should_be_close_to_expected(event_timestamp):
    expected = datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)
    assert abs(event_timestamp - expected) <= timedelta(seconds=1)
    # alternative: `pytest.approx` supports numbers (not datetimes) => compare the timestamps
    assert event_timestamp.timestamp() == pytest.approx(expected.timestamp(), abs=1)


# Advanced: timedelta
def test_birthday_should_be_more_than_30_years_ago(birthday):
    today = date.today()
    assert birthday < today.replace(year=today.year - 30)


def test_meeting_should_be_at_least_2_hours_after_noon(meeting_time):
    noon = meeting_time.replace(hour=12, minute=0, second=0)
    duration = meeting_time - noon
    assert duration >= timedelta(hours=2)


# Combined assertions
def test_should_combine_multiple_date_assertions(birthday):
    assert date(1980, 1, 1) < birthday < date.today()
    assert birthday == date(1990, 5, 15)
    assert (birthday.year, birthday.month, birthday.day) == (1990, 5, 15)
