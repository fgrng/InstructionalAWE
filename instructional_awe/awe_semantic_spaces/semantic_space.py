# semanti_space.py - Provides base class for the construction of semantic spaces.
#

# Utility Libraries
# import codecs
import os
import inspect
import re

# Math Libraries
import pandas as pd
import numpy as np

# Libraries for Natural Language Processing
# and Latent Semantic Analysis
import nltk
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.metrics.pairwise import cosine_similarity

# Text Class from this Project
from ..awe_text_representation.text import Text

# Libraries to handle Stopwords
#   from HanTa import HanoverTagger as ht
#   from nltk.corpus import stopwords

# Configure Logging
import logging, sys
logging.basicConfig(stream=sys.stderr)
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)

class SemanticSpace:
    """Abstract class for construction of semantic spaces.

    Contains methods to compute matrix representations of text corpus,
    project new text onto the semantic space. Method to read in text files
    has to be implemented by specific corpus class.
    """

    # „Desired dimensionality of output data.
    # Must be strictly less than the number of features.
    # The default value is useful for visualisation.
    # For LSA, a value of 100 is recommended.“
    _config = {
        "n_components": 4
    }

    # Handle path for corpora files.
    @staticmethod
    def get_corpora_path():
        """Get base path of corpora files."""
        # navigate the folder structure:
        #   module folder
        #     assets
        #       corpora            <- here are the corpora files.
        #       …
        #     awe_semantic_spaces  <- here is this file.
        #     …
        corpora_path = os.path.dirname(inspect.getfile(SemanticSpace))
        corpora_path += "/../assets/corpora"
        return corpora_path


    # Initialization Methods

    def __init__(self, conf = {}):
        """Creates an new semantic space instance by reading in
        the text files and computing matrix representations of
        given text corpus.
        """
        logger.debug("Initializing new corpus object.")

        # Override standard configuration.
        if conf:
            for key in conf.keys():
                self._config[key] = conf[key]

        # LSA Datenstrukturen
        logger.debug("Compute document-term-matrix (DTM).")
        self.dtm, self.vocabulary, self.vectorizer = self.build_dtm()
        logger.debug("Compute term-frequency-inverse-document-frequency-matrix (tf-idf).")
        self.tfidf_dtm = self.build_tfidf()
        logger.debug("Building semantic spaces with %s components." % self._config["n_components"])
        self.lsa = self.build_tfidf_lsa()
        self.svd = self.build_tfidf_svd()
        logger.debug("Initialization complete.")


    # Methods for working with additional texts

    def vectorize_on_vocabulary(self, text):
        """Computes vector representation of given Text object."""
        # Build a list with one entry containing text as string.
        lemmatized_text = [" ".join(text.lemmatized_words())]
        # Build vector via word counting.
        vectorizer = CountVectorizer(min_df=1, vocabulary = self.vocabulary)
        return vectorizer.transform(lemmatized_text)

    def tfidf_on_vocabulary(self, text):
        """Computes tfidf-weighted vector representation of given Text object."""
        return Normalizer(copy=False).fit_transform(self.vectorize_on_vocabulary(text))

    def project_on_semantic_space(self, text):
        """Projects vector of given Text Object on semantic space."""
        vector = self.tfidf_on_vocabulary(text)
        return self.svd.transform(vector)

    def cosine(self, text_x, text_y):
        """Computes cosine-similarity of two given Text objects in the semantic space."""
        x = self.project_on_semantic_space(text_x)
        y = self.project_on_semantic_space(text_y)
        cosine = cosine_similarity(x, y)[0][0]
        return cosine


    # LSA Methods

    def build_tfidf_svd(self):
        """Method computes SVD with TFIDF-weighted DTM. Returns fitted SVD object."""
        svd_tfidf = TruncatedSVD(self._config["n_components"], algorithm='randomized')
        svd_tfidf.fit(self.tfidf_dtm)
        return svd_tfidf

    def build_tfidf_lsa(self):
        """Method computes LSA with TFIDF-weighted DTM.
        Returns normalized fitted semantic space.
        """
        svd = TruncatedSVD(self._config["n_components"], algorithm='randomized')
        lsa_tfidf = svd.fit_transform(self.tfidf_dtm)
        lsa_tfidf = Normalizer(copy=False).fit_transform(lsa_tfidf)
        return lsa_tfidf

    def build_tfidf(self):
        """Method to build term-frequency inverse-document-frequency matrix.
        Returns transformed DTM matrix.
        """

        tfidf_transformer = TfidfTransformer()
        tfidf_dtm = tfidf_transformer.fit_transform(self.dtm)
        return tfidf_dtm

    def build_dtm(self):
        """Method to build the document term matrix
        Returns matrix, lexicon of terms and vectorizer object.
        """
        lemmatized_corpus = self.get_lemmatized_plaintext_corpus()
        # Generiere Document-Term-Matrix und vocabulary
        vectorizer = CountVectorizer(min_df=1)
        dtm = vectorizer.fit_transform(lemmatized_corpus)
        lex = vectorizer.get_feature_names_out()
        return dtm, lex, vectorizer

    def get_components(self):
        # Sammlung von DataFrame pro Dimension
        result = list()

        for i in range(0, self._config["n_components"]):
            # Sammle Wörter und Gewichte aus Dimension
            sing_vecs = self.svd.components_[i]
            index = np.argsort(sing_vecs).tolist()
            index.reverse()
            terms = [self.vocabulary[weightIndex] for weightIndex in index[0:10]]
            weights = [sing_vecs[weightIndex] for weightIndex in index[0:10]]
            terms.reverse()
            weights.reverse()
            # Strukturiere Wörter/Gewichte in DataFrame
            temp = pd.DataFrame(columns=('terms','weights'))
            temp['terms'] = terms
            temp['weights'] = weights
            # Füge Dimension der Sammlung zu
            result.append(temp)
        return result

    def print_components(self):
        components = self.get_components()
        for i in range(0, self._config["n_components"]):
            print(components[i])
            print("\n")

    def plot_components(self):
        # Load library for plotting.
        import matplotlib.pyplot as plt

        components = self.get_components()
        # Erstelle Plot mit 2 Spalten.
        fig = plt.figure()
        fig.subplots_adjust(hspace=.5, wspace=.5)
        for i in range(0, self._config["n_components"]):
            n_rows = int(self._config["n_components"] / 2) + (self._config["n_components"] % 2)
            n_columns = 2
            ax = fig.add_subplot(n_rows, n_columns, i+1)
            ax.barh(components[i]['terms'],components[i]['weights'], align="center")
            ax.set_title('Dimension %d' % (i))
        plt.show()


    # Corpus Methods

    def read_corpus_file(self):
        """
        Read in the corpus texts from file. Stores the processed
        texts in self._corpus, if not already read. (Has to be implemented
        by specific corpus class.)

        Returns corpus as list of Text objects.
        """
        raise NotImplementedError()

    def get_lemmatized_plaintext_corpus(self):
        """[TODO]
        """
        # corpus = self.build_bag_of_lemmalists()
        corpus = []
        for t in self.read_corpus_file():
            corpus = corpus + [Text(plaintext=p).lemmatized_sentences() for p in t.paragraphs]
        lemma_corpus = list()
        # Iteriere über Sätze.
        for text in corpus:
            lemma_text = list()
            for sentence in text:
                # Iteriere über Tags.
                for lemma in sentence:
                    # Keine Satzzeichen.
                    if lemma != "--":
                        # Nur Kleinschreibung
                        lemma_text.append(lemma)
            # Füge Satz zusammen.
            lemma_corpus.append(" ".join(lemma_text))
        return lemma_corpus

    def build_bag_of_sentences(self):
        return [t.sentences() for t in self.read_corpus_file()]

    def build_bag_of_tokenlists(self):
        return [t.words() for t in self.read_corpus_file()]

    def build_bag_of_tagglists(self):
        return [t.tagged_sentences() for t in self.read_corpus_file()]

    def build_bag_of_lemmalists(self):
        return [t.lemmatized_sentences() for t in self.read_corpus_file()]
