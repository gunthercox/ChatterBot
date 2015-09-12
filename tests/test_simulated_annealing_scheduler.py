from chatterbot.adapters.io.twitter_io import SimulatedAnnealingScheduler
from unittest import TestCase


class DummyEndpoint(object):
    def __init__(self):
        self.index = 0
        self.data = [
            True,
            False,
            False,
            True,
        ]

    def get(self):
        result = self.data[self.index]
        index += 1

        if self.index == len(self.data):
            self.index = 0

        return result


class SimulatedAnnealingSchedulerTests(TestCase):

    def setUp(self):
        self.endpoint = DummyEndpoint()

        self.scheduler = SimulatedAnnealingScheduler(
            self.function,
            self.check
        )

    def function(self):
        return self.endpoint.get()

    def check(self, data):
        return data

    def test_decrease_interval(self):
        interval_before = self.scheduler.interval
        self.scheduler.decrease_interval()
        interval_after = self.scheduler.interval

        self.assertTrue(interval_before > interval_after)

    def test_increase_interval(self):
        interval_before = self.scheduler.interval
        self.scheduler.increase_interval()
        interval_after = self.scheduler.interval

        self.assertTrue(interval_before < interval_after)

