from chatterbot.logic import LogicAdapter
import re


class UnitConversion(LogicAdapter):
    def __init__(self, **kwargs):
        super(UnitConversion, self).__init__(**kwargs)
        self.number = (
            '(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten|'
            'eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|'
            'eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|'
            'eighty|ninety|hundred|thousand)'
        )
        self.pattern = r'''([Hh]ow many)(\s+)(?P<from>\S+)(\s+)((are)*\s+in)(\s+)(?P<number>\d+|(%s[-\s]?)+)(\s+)(?P<target>\S+)\?''' % self.number

    def can_process(self, statment):
        return re.match(self.pattern, statment.text)

    def process(self, statment):
        pass
