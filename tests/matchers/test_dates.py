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
@pytest.mark.skip(reason="birthday should be 1990-05-15")
def test_should_be_1990_05_15(birthday):
    pass


@pytest.mark.skip(reason="birthday should be before today")
def test_should_be_before_today(birthday):
    pass


@pytest.mark.skip(reason="birthday should be after 1980-01-01")
def test_should_be_after_1980_01_01(birthday):
    pass


@pytest.mark.skip(reason="birthday should be in May")
def test_should_be_in_may(birthday):
    pass


@pytest.mark.skip(reason="birthday should be in year 1990")
def test_should_be_in_year_1990(birthday):
    pass


@pytest.mark.skip(reason="birthday should be on day 15")
def test_should_be_on_day_15(birthday):
    pass


@pytest.mark.skip(reason="project deadline should be in the future compared to 2024-01-01")
def test_project_deadline_should_be_in_future(project_deadline):
    pass


@pytest.mark.skip(reason="project deadline should be between 2024-01-01 and 2025-12-31")
def test_project_deadline_should_be_between_dates(project_deadline):
    pass


# datetime assertions (naive, i.e. without time zone)
@pytest.mark.skip(reason="meeting time should be 2024-03-20T14:30:00")
def test_meeting_time_should_be_2024_03_20_at_14_30(meeting_time):
    pass


@pytest.mark.skip(reason="meeting time should be before now")
def test_meeting_time_should_be_before_now(meeting_time):
    pass


@pytest.mark.skip(reason="meeting time should have hour 14")
def test_meeting_time_should_have_hour_14(meeting_time):
    pass


@pytest.mark.skip(reason="meeting time should have minute 30")
def test_meeting_time_should_have_minute_30(meeting_time):
    pass


@pytest.mark.skip(reason="meeting time should be in March 2024")
def test_meeting_time_should_be_in_march_2024(meeting_time):
    pass


# time assertions
@pytest.mark.skip(reason="work start should be 09:00")
def test_work_start_should_be_09_00(work_start):
    pass


@pytest.mark.skip(reason="work start should be before noon (12:00)")
def test_work_start_should_be_before_noon(work_start):
    pass


@pytest.mark.skip(reason="work start should have hour 9")
def test_work_start_should_have_hour_9(work_start):
    pass


@pytest.mark.skip(reason="work start should be between 08:00 and 10:00")
def test_work_start_should_be_between_08_and_10(work_start):
    pass


# datetime assertions (aware, i.e. with time zone)
@pytest.mark.skip(reason="conference start should be in Europe/Berlin timezone")
def test_conference_start_should_be_in_berlin_timezone(conference_start):
    pass


@pytest.mark.skip(reason="conference start should be 2024-06-01T09:00 in Berlin")
def test_conference_start_should_be_correct_date_time(conference_start):
    pass


@pytest.mark.skip(reason="conference start should have UTC offset +01:00 or +02:00")
def test_conference_start_should_have_european_offset(conference_start):
    pass


# timestamp assertions (UTC)
@pytest.mark.skip(reason="event timestamp should be 2024-01-15T10:30:00Z")
def test_event_timestamp_should_be_correct(event_timestamp):
    pass


@pytest.mark.skip(reason="event timestamp should be before now")
def test_event_timestamp_should_be_in_past(event_timestamp):
    pass


@pytest.mark.skip(reason="event timestamp should be close to 2024-01-15T10:30:00Z within 1 second")
def test_event_timestamp_should_be_close_to_expected(event_timestamp):
    pass


# Advanced: timedelta
@pytest.mark.skip(reason="birthday should be more than 30 years before today")
def test_birthday_should_be_more_than_30_years_ago(birthday):
    pass


@pytest.mark.skip(reason="meeting time should be at least 2 hours after 12:00 same day")
def test_meeting_should_be_at_least_2_hours_after_noon(meeting_time):
    pass


# Combined assertions
@pytest.mark.skip(reason="TODO: combine multiple date assertions in one test")
def test_should_combine_multiple_date_assertions(birthday):
    pass
