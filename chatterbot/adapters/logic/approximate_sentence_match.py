# -*- coding: utf-8 -*-
# Imports
from .base_match import BaseMatchAdapter
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
from nltk.corpus import wordnet
import string
from chatterbot.adapters import Adapter

class ApproximateSentenceMatchAdapter(BaseMatchAdapter):
    """
    The Jaccard index is composed of a numerator and denominator.
    In the numerator, we count the number of items that are shared between the sets.
    In the denominator, we count the total number of items across both sets.
    Let’s say we define sentences to be equivalent if 50% or more of their tokens are equivalent.  Here are two sample sentences:
        The young cat is hungry.
        The cat is very hungry.
    When we parse these sentences to remove stopwords, we end up with the following two sets:
        {young, cat, hungry}
        {cat, very, hungry}
    In our example above, our intersection is {cat, hungry}, which has count of two.
    The union of the sets is {young, cat, very, hungry}, which has a count of four.
    Therefore, our Jaccard similarity index is two divided by four, or 50%.
    Given our threshold above, we would consider this to be  a match
    """

    def __init__(self, **kwargs):
        super(ClosestMatchAdapter, self).__init__(**kwargs)
        # Get default English stopwords and extend with punctuation
        self.stopwords = nltk.corpus.stopwords.words('english')
        self.stopwords.extend(string.punctuation)
        self.stopwords.append('')
        self.lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()

    def get_wordnet_pos(self, pos_tag):
        if pos_tag[1].startswith('J'):
            return (pos_tag[0], wordnet.ADJ)
        elif pos_tag[1].startswith('V'):
            return (pos_tag[0], wordnet.VERB)
        elif pos_tag[1].startswith('N'):
            return (pos_tag[0], wordnet.NOUN)
        elif pos_tag[1].startswith('R'):
            return (pos_tag[0], wordnet.ADV)
        else:
            return (pos_tag[0], wordnet.NOUN)


    def is_ci_lemma_stopword_set_match(self,a, b, threshold=0.5):
        """Check if a and b are matches."""
        print("ask",a)
        ratio = 0
        pos_a = map(self.get_wordnet_pos, nltk.pos_tag(nltk.tokenize.word_tokenize(a)))
        pos_b = map(self.get_wordnet_pos, nltk.pos_tag(nltk.tokenize.word_tokenize(b)))
        lemmae_a = [self.lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_a \
                        if pos == wordnet.NOUN and token.lower().strip(string.punctuation) not in self.stopwords]
        lemmae_b = [self.lemmatizer.lemmatize(token.lower().strip(string.punctuation), pos) for token, pos in pos_b \
                        if pos == wordnet.NOUN and token.lower().strip(string.punctuation) not in self.stopwords]

        # Calculate Jaccard similarity
        try:
            ratio = len(set(lemmae_a).intersection(lemmae_b)) / float(len(set(lemmae_a).union(lemmae_b)))
        except Exception as e:
            print("Error", e)
        return (ratio >= threshold)

    def get(self, input_statement):
        """
        Takes a statement string and a list of statement strings.
        Returns the closest matching statement from the list.
        """
        statement_list = self.context.storage.get_response_statements()

        if not statement_list:
            if self.has_storage_context:
                # Use a randomly picked statement
                return 0, self.context.storage.get_random()
            else:
                raise self.EmptyDatasetException()

        confidence = -1
        sentence_match = input_statement
        # Find the  matching known statement
        for statement in statement_list:
            ratio = self.is_ci_lemma_stopword_set_match(input_statement.text, statement.text)
            if ratio:
                closest_match = statement
            else:
                closest_match = statement
        return 50, closest_match
