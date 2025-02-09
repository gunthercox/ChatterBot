"""
ChatterBot constants
"""
from chatterbot import languages

'''
The maximum length of characters that the text of a statement can contain.
The number 255 is used because that is the maximum length of a char field
in most databases. This value should be enforced on a per-model basis by
the data model for each storage adapter.
'''
STATEMENT_TEXT_MAX_LENGTH = 255

'''
The maximum length of characters that the text label of a conversation can contain.
The number 32 was chosen because that is the length of the string representation
of a UUID4 with no hyphens.
'''
CONVERSATION_LABEL_MAX_LENGTH = 32

'''
The maximum length of text that can be stored in the persona field of the statement model.
'''
PERSONA_MAX_LENGTH = 50

# The maximum length of characters that the name of a tag can contain
TAG_NAME_MAX_LENGTH = 50

# See other model options: https://spacy.io/models/
DEFAULT_LANGUAGE_TO_SPACY_MODEL_MAP = {
    languages.CAT: 'ca_core_news_sm',
    languages.CHI: 'zh_core_web_sm',
    languages.HRV: 'hr_core_news_sm',
    languages.DAN: 'da_core_news_sm',
    languages.DUT: 'nl_core_news_sm',
    languages.ENG: 'en_core_web_sm',
    languages.FIN: 'fi_core_news_sm',
    languages.FRE: 'fr_core_news_sm',
    languages.GER: 'de_core_news_sm',
    languages.GRE: 'el_core_news_sm',
    languages.ITA: 'it_core_news_sm',
    languages.JPN: 'ja_core_news_sm',
    languages.KOR: 'ko_core_news_sm',
    languages.LIT: 'lt_core_news_sm',
    languages.MAC: 'mk_core_news_sm',
    languages.NOR: 'nb_core_news_sm',
    languages.POL: 'pl_core_news_sm',
    languages.POR: 'pt_core_news_sm',
    languages.RUM: 'ro_core_news_sm',
    languages.RUS: 'ru_core_news_sm',
    languages.SLO: 'sl_core_news_sm',
    languages.SPA: 'es_core_news_sm',
    languages.SWE: 'sv_core_news_sm',
    languages.UKR: 'uk_core_news_sm',
}

DEFAULT_DJANGO_APP_NAME = 'django_chatterbot'
