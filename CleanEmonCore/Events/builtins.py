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

        last_call = time.time()
        while True:

            # busy_time denotes the amount of time spent on the last notify()
            # If that time is greater than the defined interval, there is no need to wait any longer: notify immediately
            # Otherwise, wait for as long as needed until the defined interval has actually passed
            busy_time = time.time() - last_call
            if busy_time < self.interval:
                time.sleep(self.interval - busy_time)
            last_call = time.time()
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
