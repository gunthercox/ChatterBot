class Comparator:

    def __call__(self, statement_a, statements):
        return self.compare(statement_a, statements)

    def compare(self, statement_a, statements):
        return 0
