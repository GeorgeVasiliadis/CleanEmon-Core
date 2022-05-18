"""A set of predefined observable events"""

import time

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


# from datetime import datetime
# from . import Observer
# class DateChange(Observable, Observer):
#     """A DateChange object notifies all interested clients periodically when the date has changed. In order to achieve
#     this, DateChange observes a Timer that defines when the checks will take place."""
#
#     def __init__(self, timer, initial_date=None):
#         self.timer = timer
#         self.current_date = initial_date
#         Observable.__init__(self)
#         Observer.__init__(self, timer)
#
#     def on_notify(self):
#         now = datetime.now()
#         if now != self.current_date:
#             self.current_date = now
#             self.notify(date=now)
