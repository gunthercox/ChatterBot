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
        self.pattern = r'''([Hh]ow many)(\s+)(?P<target>\S+)(\s+)((are)*\s+in)(\s+)(?P<number>\d+|(%s[-\s]?)+)(\s+)(?P<from>\S+)\?''' % self.number

    def get_unit(self, text):
        pass

    def can_process(self, statment):
        return re.match(self.pattern, statment.text)

    def process(self, statment):
        from pint import UnitRegistry
        from mathparse import mathparse

        response = Statement(text='')
        p = re.match(self.pattern, statment.text)
        if p is None:
            response.confidence = 0
            return response

        n = mathparse.parse(p.group("number"), "ENG")

        ureg = UnitRegistry()
        from_unit_pint = float(n) * ureg.kilometer
        target_unit_pint = from_unit_pint.to(ureg.inch)
        response.text = target_unit_pint.magnitude
        return response
