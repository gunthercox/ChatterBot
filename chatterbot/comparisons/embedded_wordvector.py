from .comparator import Comparator
from collections import OrderedDict
from chatterbot import languages
from nltk.corpus import stopwords
import numpy as np
from sklearn.decomposition import PCA
import spacy
import math
import string
import hashlib
import logging

# FIXME: spurious runtime divide errors from numpy.
np.seterr(divide='ignore', invalid='ignore')

nlp = spacy.load('en_core_web_lg')

logger = logging.getLogger(__name__)


class CacheDict(OrderedDict):
    def __init__(self, *args, max=0, **kwargs):
        self._max = max
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        if self._max > 0:
            if len(self) > self._max:
                self.popitem(False)

class EmbeddedWordVector(Comparator):
    """
    Calculate the similarity of two statements based on the research
    https://openreview.net/pdf?id=SyK00v5xx
    """

    def __init__(self):
        super().__init__()

        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        self.language = languages.ENG

        self.stopwords = stopwords.words(self.language.ENGLISH_NAME.lower())

        self.short_term_cache = CacheDict(max=1000)
        self.long_term_cache = CacheDict(max=10000)

    def get_word_frequency(self, word_text):
        return 0.0001 # TODO user Counter on chatbot statements for better match

    def word_to_vec(self, sentence, embedding_size, sif: float=1e-3):
        sentence_set = []
        vs = np.zeros(embedding_size)  # add all word2vec values into one vector for the sentence
        sentence_length = len(sentence)
        for word, vector in sentence.items():
            a_value = sif / (sif + self.get_word_frequency(word))  # smooth inverse frequency, SIF
            vs = np.add(vs, np.multiply(a_value, vector))  # vs += sif * word_vector
        vs = np.divide(vs, sentence_length)  # weighted average
        sentence_set.append(vs)  # add to our existing re-calculated set of sentences

        # calculate PCA of this sentence set
        pca = PCA()
        pca.fit(np.array(sentence_set))
        u = pca.components_[0]  # the PCA vector
        u = np.multiply(u, np.transpose(u))  # u x uT

        # pad the vector?  (occurs if we have less sentences than embeddings_size)
        if len(u) < embedding_size:
            for i in range(embedding_size - len(u)):
                u = np.append(u, 0)  # add needed extension for multiplication below

        # resulting sentence vectors, vs = vs -u x uT x vs
        sentence_vecs = []
        for vs in sentence_set:
            sub = np.multiply(u,vs)
            sentence_vecs.append(np.subtract(vs, sub))

        return sentence_vecs



    def sentences_to_vectors(self, sentence):
        embedding_size = 300   # dimension of spacy word embeddings https://spacy.io/usage/vectors-similarity
        # convert the above sentences to vectors using spacy's large model vectors
        word_list = {}
        for word in sentence.strip().split(' '):
            if word not in self.stopwords:
                token = nlp.vocab[word]
                if token.has_vector:  # ignore OOVs
                    word_list[word] = token.vector
                else:
                    logger.debug(f'Ignoring {word} coz no vector found.')

        sentence_vector_lookup = {}
        if len(word_list) > 0:  # did we find any words (not an empty set)
            sentence_vectors = self.word_to_vec(word_list, embedding_size)  # all vectors converted together
            for i in range(len(sentence_vectors)):
                sentence_vector_lookup[sentence] = sentence_vectors[i]

        return sentence_vector_lookup


    # euclidean distance between two vectors
    def l2_dist(self, v1, v2):
        sum = 0.0
        if len(v1) == len(v2):
            for i in range(len(v1)):
                delta = v1[i] - v2[i]
                sum += delta * delta
        diff = math.sqrt(sum)
        if diff < 3.0:
            diff = diff/3.0
        else:
            diff = 1.0
        return diff



    def compare(self, statement, other_statement):
        """
        Return the similarity of two statements based on
        their calculated sentiment values.

        :return: The percent of similarity between the sentiment value.
        :rtype: float
        """
        # Make both strings lowercase
        a = statement.text.lower()
        b = other_statement.text.lower()

        # Remove punctuation from each string
        a = a.translate(self.punctuation_table)
        b = b.translate(self.punctuation_table)

        if not a or not b:
            return 0.0

        st_hash = hashlib.md5(a.encode('utf-8')).hexdigest()
        v1 = self.short_term_cache.get(st_hash, self.sentences_to_vectors(a))
        self.short_term_cache[st_hash] = v1

        lt_hash = hashlib.md5(b.encode('utf-8')).hexdigest()
        v2 = self.long_term_cache.get(lt_hash, self.sentences_to_vectors(b))
        self.long_term_cache[lt_hash] = v2

        difference = self.l2_dist(v1[a], v2[b])

        return 1.0 - difference
