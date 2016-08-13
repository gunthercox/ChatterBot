from chatterbot.trainers import ListTrainer as NewListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer as NewChatterBotCorpusTrainer
from warnings import warn


class DeprecationHelper(object):
    def __init__(self, new_target):
        self.new_target = new_target

    def __call__(self, *args, **kwargs):
        self._warn()
        return self.new_target(*args, **kwargs)

    def __getattr__(self, attr):
        self._warn()
        return getattr(self.new_target, attr)


class ListDeprecationHelper(DeprecationHelper):

    def _warn(self):
        warn('Deprecation Warning: Using `from chatterbot.training.trainers import ListTrainer` is deprecated. Use `from chatterbot.trainers import ListTrainer` instead.')


class CorpusDeprecationHelper(DeprecationHelper):

    def _warn(self):
        warn('Deprecation Warning: Using `from chatterbot.training.trainers import ChatterBotCorpusTrainer` is deprecated. Use `from chatterbot.trainers import ChatterBotCorpusTrainer` instead.')


ListTrainer = ListDeprecationHelper(NewListTrainer)
ChatterBotCorpusTrainer = CorpusDeprecationHelper(NewChatterBotCorpusTrainer)
