from .logic_adapter import LogicAdapter
from .best_match import BestMatch
from .closest_match import ClosestMatchAdapter
from .closest_meaning import ClosestMeaningAdapter
from .low_confidence import LowConfidenceAdapter
from .mathematical_evaluation import MathematicalEvaluation
from .multi_adapter import MultiLogicAdapter
from .no_knowledge_adapter import NoKnowledgeAdapter
from .specific_response import SpecificResponseAdapter
from .time_adapter import TimeLogicAdapter

BaseMatchAdapter = BestMatch
