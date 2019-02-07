from .comparator import Comparator
import hashlib
import logging
import math
import os
import pickle
import string
from collections import defaultdict

import numpy as np
import spacy
from nltk.corpus import stopwords
from sklearn import cluster, metrics
from sklearn.decomposition import PCA

from chatterbot import languages
from chatterbot.conversation import Statement

# FIXME: spurious runtime divide errors from numpy.
np.seterr(divide='ignore', invalid='ignore')

nlp = spacy.load('en_core_web_lg')

logger = logging.getLogger(__name__)

NUM_CLUSTERS=10


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

        self.punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))

        self.model = None
        self.clusters = None
        self.lines = []

        if os.path.exists('cluster.pickle'):
            with open('cluster.pickle', 'rb') as rb:
                self.model = pickle.load(rb)

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
            # if word not in self.stopwords:
            token = nlp.vocab[word]
            if token.has_vector:  # ignore OOVs
                word_list[word] = token.vector
            else:
                logger.debug(f'Ignoring {word} coz no vector found.')

        sentence_vector_lookup = None
        if len(word_list) > 0:  # did we find any words (not an empty set)
            sentence_vectors = self.word_to_vec(word_list, embedding_size)  # all vectors converted together
            for i in range(len(sentence_vectors)):
                sentence_vector_lookup = sentence_vectors[i]

        return sentence_vector_lookup


    # euclidean distance between two vectors
    def l2_dist(self, v1, v2):
        sum = 0.0
        if len(v1) == len(v2):
            for i in range(len(v1)):
                delta = v1[i] - v2[i]
                sum += delta * delta
        diff = math.sqrt(sum)
        return diff


    def cluster_indices_group(self, clustNum, labels_array):
        return np.where(labels_array == clustNum)[0]


    def model_create_or_load(self):
        if not os.path.exists("cluster.pickle"):
            vectors = []
            for l in self.lines:
                l = l.text.translate(self.punctuation_table)
                v = self.sentences_to_vectors(l)
                if v is not None and v is not [None]:
                    vectors.append(v)
                else:
                    print('FATAL: Ignoring sentence will cause kmeans skewed index', l)

            vectors = np.asarray(vectors)
            self.model = cluster.KMeans(n_clusters=NUM_CLUSTERS)
            self.model.fit(vectors)
            with open("cluster.pickle","wb") as rb:
                pickle.dump(self.model, rb)

        return True


    def clusters_create_or_load(self):
        self.clusters = defaultdict(set)
        for i in range(1, NUM_CLUSTERS + 1):
            for c in self.cluster_indices_group(i, self.model.labels_):
                self.clusters[i].add(self.lines[c])
        return True


    def compare(self, statement, bot_statements_list):
        """
        Return the similarity of two statements embedded vector distance.

        :return: vector distance
        :rtype: float
        """
        self.lines = list(bot_statements_list)

        if not self.model:
            self.model_create_or_load()

        if not self.clusters:
            self.clusters_create_or_load()

        text = statement.text
        v1 = self.sentences_to_vectors(text.translate(self.punctuation_table))
        v = v1.reshape(1, -1)
        index = self.model.predict(v)[0]

        min_match = 0.0
        m_confidence = 100.0
        m_statement = Statement('')

        for vals in self.clusters[index]:
            v2 = self.sentences_to_vectors(vals.text.translate(self.punctuation_table))
            dist = self.l2_dist(v1, v2)
            min_match = max(min_match, dist)
            if dist < m_confidence:
                m_confidence = dist
                m_statement = vals

        if min_match != 0.0:
            m_statement.confidence = 1.0 - m_confidence / min_match
        else:
            m_statement.confidence = 1.0
        return m_statement

