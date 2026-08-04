from datetime import datetime, timedelta, timezone

from gradient_labs._http_client import HttpClient

INSTANT = "2026-08-04T15:00:00.000000Z"


class TestLocalize:
    def test_naive_is_treated_as_utc(self):
        assert HttpClient.localize(datetime(2026, 8, 4, 15, 0, 0)) == INSTANT

    def test_aware_utc(self):
        timestamp = datetime(2026, 8, 4, 15, 0, 0, tzinfo=timezone.utc)
        assert HttpClient.localize(timestamp) == INSTANT

    def test_aware_offsets_are_converted_to_utc(self):
        ahead = datetime(2026, 8, 4, 16, 0, 0, tzinfo=timezone(timedelta(hours=1)))
        behind = datetime(2026, 8, 4, 10, 0, 0, tzinfo=timezone(timedelta(hours=-5)))
        assert HttpClient.localize(ahead) == INSTANT
        assert HttpClient.localize(behind) == INSTANT
