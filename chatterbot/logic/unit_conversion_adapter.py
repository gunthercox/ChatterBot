from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
import re


supported_units = ['meter', 'kilometer', 'hectometer', 'decameter', 'decimeter',
                   'centimeter', 'millimeter', 'micrometer', 'nanometer',
                   'picometer', 'femtometer', 'attometer', 'inches']


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

    def can_process(self, statment):
        return re.match(self.pattern, statment.text)

    def process(self, statment):
        from pint import UnitRegistry
        from mathparse import mathparse
        # Use python-Levenshtein if available
        try:
            from Levenshtein.StringMatcher import StringMatcher as SequenceMatcher
        except ImportError:
            from difflib import SequenceMatcher

        response = Statement(text='')
        response.confidence = 1

        p = re.match(self.pattern, statment.text)
        if p is None:
            response.confidence = 0
            return response

        try:
            n = mathparse.parse(p.group("number"), "ENG")
            target_parsed = p.group("target")
            from_parsed = p.group("from")

            target_unit = [None, 0.0]
            from_unit = [None, 0.0]
            for unit in supported_units:
                target_ratio = SequenceMatcher(None, unit, target_parsed).ratio()
                from_ratio = SequenceMatcher(None, unit, from_parsed).ratio()
                if target_ratio >= target_unit[1]:
                    target_unit[0] = unit
                    target_unit[1] = target_ratio
                if SequenceMatcher(None, unit, from_parsed).ratio() >= from_unit[1]:
                    from_unit[0] = unit
                    from_unit[1] = from_ratio

            response.confidence = (target_unit[1] + target_unit[1]) / 2.0

            ureg = UnitRegistry()
            from_value = float(n) * getattr(ureg, from_unit[0])
            target_value = from_value.to(getattr(ureg, target_unit[0]))
            response.text = target_value.magnitude

        except Exception, e:
            response.confidence = 0

        finally:
            return response
