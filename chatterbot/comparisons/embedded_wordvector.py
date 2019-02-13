import logging
import math
import os
import pickle
import string
from collections import defaultdict
from random import randint

import numpy as np
import spacy
from nltk.corpus import stopwords
from sklearn import cluster, metrics
from sklearn.decomposition import PCA
from spacy.strings import hash_string
from spacy.vectors import Vectors

from chatterbot import languages
from chatterbot.conversation import Statement

from .comparator import Comparator

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
        self.vocab = Vectors(shape=(20000, 300)) # 20000 sentences with 300 as dimension


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
                token = nlp.vocab[word.lower()]
                if token.has_vector:  # ignore OOVs
                    word_list[word] = token.vector
                else:
                    logger.debug(f'Ignoring {word} coz no vector found.')

        # if a sentence contains all stop words, we tag it a filler
        if len(word_list) == 0:
            word_list['filler'] = nlp('filler').vector

        sentence_vector_lookup = None
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


    def model_create_or_load(self, bot_statements_list):
        if not os.path.exists('models'):
            os.makedirs('./models')

        if not os.path.exists("models/cluster.pickle"):
            vectors = []
            self.lines = list(bot_statements_list)
            logger.debug("loaded lines")

            for l in self.lines:
                l = l.text.translate(self.punctuation_table).lower()
                v = self.sentences_to_vectors(l)
                if v is not None and v is not [None]:
                    vectors.append(v)
                    self.vocab.add(l, vector=v)
                else:
                    logger.warning('FATAL: Ignoring sentence will cause kmeans skewed index ' + l)

            self.vocab.to_disk('models/sentences.vocab')

            vectors = np.asarray(vectors)
            self.model = cluster.KMeans(n_clusters=NUM_CLUSTERS)
            self.model.fit(vectors)
            with open("models/cluster.pickle","wb") as rb:
                pickle.dump(self.model, rb)
            with open('models/sentences.txt', 'w') as rb:
                rb.writelines(map(lambda s: s.text + '\n', self.lines))

        elif os.path.exists('models/cluster.pickle'):
            with open('models/cluster.pickle', 'rb') as rb:
                self.model = pickle.load(rb)
            self.vocab.from_disk('models/sentences.vocab')
            with open('models/sentences.txt', 'r') as rb:
                self.lines = [ Statement(l.strip()) for l in rb.readlines()]

        return True


    def clusters_create_or_load(self):
        self.clusters = defaultdict(set)
        for i in range(1, NUM_CLUSTERS + 1):
            for c in self.cluster_indices_group(i, self.model.labels_):
                self.clusters[i].add(self.lines[c])
            sz = len(self.clusters[i])
            logger.debug(f"bucket {i} has {sz} elements")
        return True


    def compare(self, statement, bot_statements_list):
        """
        Return the similarity of two statements embedded vector distance.

        :return: vector distance
        :rtype: float
        """
        logger.debug("Word2vec entering")
        if not self.model:
            self.model_create_or_load(bot_statements_list)
            logger.debug("created model")

        if not self.clusters:
            self.clusters_create_or_load()
            logger.debug("created clusters")

        text = statement.text.translate(self.punctuation_table)
        logger.debug(f"word2vec looking up {text}")
        v1 = self.sentences_to_vectors(text)
        v = v1.reshape(1, -1)
        index = self.model.predict(v)[0]
        if index == 0: #prediction failed
            index = randint(1, NUM_CLUSTERS)
        logger.debug(f"predicted {index} for input")

        min_match = 0.0
        m_confidence = 100.0
        m_statement = Statement('')
        ii = 0
        for vals in self.clusters[index]:
            ii += 1
            plain_text = vals.text.translate(self.punctuation_table).lower()
            num_id = hash_string(plain_text)
            v2 = self.vocab[num_id]
            dist = self.l2_dist(v1, v2)
            min_match = max(min_match, dist)
            if dist < m_confidence:
                m_confidence = dist
                m_statement = vals
        logger.debug(f"compared {ii} values")
        m_statement.confidence = 0.0
        if min_match != 0.0:
            m_statement.confidence = 1.0 - m_confidence / min_match

        logger.debug(f"Closest match found {m_statement.text}")
        return m_statement
