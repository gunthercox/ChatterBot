from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot import parsing
import re


class UnitConversion(LogicAdapter):
    def __init__(self, **kwargs):
        super(UnitConversion, self).__init__(**kwargs)
        self.pattern = r'''
                       (([Hh]ow\s+many)\s+
                       (?P<target>\S+)\s+ # meter, kilometer, hectometer
                       ((are)*\s*in)\s+
                       (?P<number>\d+|(a|an)|(%s[-\s]?)+)\s+
                       (?P<from>\S+)\s*\?) # meter, kilometer, hectometer
                       ''' % (parsing.numbers)

    def can_process(self, statment):
        pattern = re.compile(self.pattern, re.VERBOSE)
        return not pattern.match(statment.text) is None

    def process(self, statment):
        from pint import UnitRegistry
        from mathparse import mathparse

        response = Statement(text='')
        response.confidence = 1

        try:
            pattern = re.compile(self.pattern, re.VERBOSE)
            p = pattern.match(statment.text)
            if p is None:
                response.confidence = 0
                return response

            try:
                target_parsed = p.group("target")
                from_parsed = p.group("from")
                n_statement = p.group("number")
                n = mathparse.parse(n_statement, "ENG")
            except Exception:
                if n_statement == 'a' or n_statement == 'an':
                    n = 1.0
                else:
                    raise

            ureg = UnitRegistry()
            from_value = ureg.Quantity(float(n), getattr(ureg, from_parsed))
            target_value = from_value.to(getattr(ureg, target_parsed))
            response.text = target_value.magnitude

        except Exception:
            response.confidence = 0

        finally:
            return response
