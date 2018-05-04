from chatterbot.logic import LogicAdapter


class UnitConversion(LogicAdapter):
    def __init__(self, **kwargs):
        super(UnitConversion, self).__init__(**kwargs)

    def can_process(self, statment):
        return True

    def process(self, statment):
        return statment
