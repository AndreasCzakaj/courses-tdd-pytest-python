from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo


class Dates:
    def get_birthday(self) -> date:
        return date(1990, 5, 15)

    def get_meeting_time(self) -> datetime:
        return datetime(2024, 3, 20, 14, 30, 0)

    def get_conference_start(self) -> datetime:
        return datetime(2024, 6, 1, 9, 0, 0, tzinfo=ZoneInfo("Europe/Berlin"))

    def get_event_timestamp(self) -> datetime:
        return datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc)

    def get_work_start(self) -> time:
        return time(9, 0)

    def get_project_deadline(self) -> date:
        return date(2024, 12, 31)
