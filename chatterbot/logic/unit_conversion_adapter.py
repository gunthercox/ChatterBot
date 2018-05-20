from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot import parsing
from pint import UnitRegistry
from mathparse import mathparse
import re


class UnitConversion(LogicAdapter):
    def __init__(self, **kwargs):
        super(UnitConversion, self).__init__(**kwargs)
        self.patterns = [
            (
                re.compile(r'''
                   (([Hh]ow\s+many)\s+
                   (?P<target>\S+)\s+ # meter, celsius, hours
                   ((are)*\s*in)\s+
                   (?P<number>([+-]?\d+(?:\.\d+)?)|(a|an)|(%s[-\s]?)+)\s+
                   (?P<from>\S+)\s*) # meter, celsius, hours
                   ''' % (parsing.numbers),
                    (re.VERBOSE | re.IGNORECASE)
                ),
                lambda m, s: self.handle_matches(m, s)
            ),
            (
                re.compile(r'''
                   ((?P<number>([+-]?\d+(?:\.\d+)?)|(%s[-\s]?)+)\s+
                   (?P<from>\S+)\s+ # meter, celsius, hours
                   (to)\s+
                   (?P<target>\S+)\s*) # meter, celsius, hours
                   ''' % (parsing.numbers),
                    (re.VERBOSE | re.IGNORECASE)
                ),
                lambda m, s: self.handle_matches(m, s)
            ),
            (
                re.compile(r'''
                   ((?P<number>([+-]?\d+(?:\.\d+)?)|(a|an)|(%s[-\s]?)+)\s+
                   (?P<from>\S+)\s+ # meter, celsius, hours
                   (is|are)\s+
                   (how\s+many)*\s+
                   (?P<target>\S+)\s*) # meter, celsius, hours
                   ''' % (parsing.numbers),
                    (re.VERBOSE | re.IGNORECASE)
                ),
                lambda m, s: self.handle_matches(m, s)
            )
        ]

    def get_unit(self, ureg, unit_variations):
        for unit in unit_variations:
            try:
                return getattr(ureg, unit)
            except Exception:
                continue
        return None

    def get_valid_units(self, ureg, from_unit, target_unit):
        from_unit_variations = [from_unit.lower(), from_unit.upper()]
        target_unit_variations = [target_unit.lower(), target_unit.upper()]
        from_unit = self.get_unit(ureg, from_unit_variations)
        target_unit = self.get_unit(ureg, target_unit_variations)
        return from_unit, target_unit

    def handle_matches(self, match, statment):
        response = Statement(text='')
        try:
            from_parsed = match.group("from")
            target_parsed = match.group("target")
            n_statement = match.group("number")

            if n_statement == 'a' or n_statement == 'an':
                n_statement = '1.0'

            n = mathparse.parse(n_statement, "ENG")

            ureg = UnitRegistry()
            from_parsed, target_parsed = self.get_valid_units(ureg, from_parsed, target_parsed)

            if from_parsed is None or target_parsed is None:
                raise

            from_value = ureg.Quantity(float(n), from_parsed)
            target_value = from_value.to(target_parsed)
            response.confidence = 1
            response.text = str(target_value.magnitude)
        except Exception:
            response.confidence = 0
        finally:
            return response

    def can_process(self, statment):
        for expression, func in self.patterns:
            if expression.match(statment.text) is not None:
                return True
        return False

    def process(self, statement):
        try:
            response = Statement(text='')
            for pattern, func in self.patterns:
                p = pattern.match(statement.text)
                if p is not None:
                    response = func(p, statement)
                    if response.confidence == 1:
                        break
        except Exception:
            response.confidence = 0
        finally:
            return response
