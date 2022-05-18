from datetime import datetime
from datetime import timedelta
from datetime import date

import pytest

from CleanEmonCore.Events import Observer
from CleanEmonCore.Events.builtins import Timer
from CleanEmonCore.Events.builtins import DateChange


def test_timer():
    assert Timer(2)


def test_date_change():
    assert DateChange()


@pytest.mark.skip
def test_stress_timer():
    class TimerObserver(Observer):
        def on_notify(self, *args, **kwargs):
            raise RuntimeError("Everything works as expected")

    event = Timer(2)
    TimerObserver(event)

    with pytest.raises(RuntimeError, match="Everything works as expected"):
        event.run()


@pytest.mark.skip(reason="This can only be checked when date changes")
def test_stress_date_change():
    """This test is intentionally skipped. It will run patiently waiting for the date to change. In order to utilize it
    please comment out the "skip" mark decorator, run this test and change manually the system date."""

    event = DateChange(5, date.today())

    class DateChangeObserver(Observer):
        def on_notify(self, *args, **kwargs):
            raise RuntimeError("Everything works as expected")

    DateChangeObserver(event)

    with pytest.raises(RuntimeError, match="Everything works as expected"):
        event.run()
