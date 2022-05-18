"""A simplistic implementation of the Observer Design Pattern."""

from abc import ABC
from abc import abstractmethod


class Observable:
    """Base class for any event generator that would like to massively notify interested observers"""

    def __init__(self):
        self.observers = []

    def register(self, observer):
        """Register an observer to the current observable object

        If the same observer is registered more than once, registration will fail silently.
        """

        if observer not in self.observers:
            self.observers.append(observer)

    def notify(self, *args, **kwargs):
        """Notify all interested (registered) observers"""

        for observer in self.observers:
            observer.on_notify(*args, **kwargs)


class Observer(ABC):
    """Abstract Base Class for any client who should "do something" when an event occurs"""

    def __init__(self, observable):
        observable.register(self)

    @abstractmethod
    def on_notify(self, *args, **kwargs):
        """Default actions that should take place if the desired event occurs"""

        pass
