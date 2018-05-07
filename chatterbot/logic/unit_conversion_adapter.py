from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
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
        from mathparse import mathparse

        response = Statement(text='')
        response.confidence = 1
        p = re.match(self.pattern, statment.text)
        if p is None:
            response.confidence = 0
            return response
        unit_from = p.group("from")
        unit_target = p.group("target")
        number = mathparse.parse(p.group("number"), "ENG")

        return response

