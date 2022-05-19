"""A set of predefined observable events"""

import time
from datetime import date

from . import Observer
from . import Observable


class Timer(Observable):
    """A Timer object notifies all interested clients periodically, in the specified intervals."""

    def __init__(self, interval):
        """Args:
            - interval: int :: Defines the period of busy-waiting in seconds. After `interval` seconds
                               the observers get notified.
        """
        super().__init__()
        self.interval = interval

    def run(self):
        """Repeatedly, busy-waits for the desired amount of time and then notifies the observers"""

        while True:
            time.sleep(self.interval)
            self.notify(time=time.time())


class DateChange(Observable, Observer):
    """A DateChange object notifies all interested clients periodically when the date has changed. In order to achieve
    this, DateChange observes a Timer that defines when the checks will take place."""

    def __init__(self, check_interval: int = 60, initial_date: date = None):
        self.timer = Timer(check_interval)
        self.current_date = initial_date
        Observable.__init__(self)
        Observer.__init__(self, self.timer)

    def on_notify(self, *args, **kwargs):
        today = date.today()
        if today != self.current_date:
            yesterday = self.current_date
            self.current_date = today
            self.notify(date=yesterday)

    def run(self):
        self.timer.run()
