import codecs
import re

from classes.text import Text
import nltk

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from HanTa import HanoverTagger as ht
from nltk.corpus import stopwords

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer

from sklearn.metrics.pairwise import cosine_similarity

class MySemanticSpaceVU:
    # Klasse zur Konstruktion eines semantischen Raums auf Basis
    # des Korpus von Valentin Unger (2021).

    # „Desired dimensionality of output data. Must be strictly less than the number of features. 
    # The default value is useful for visualisation. For LSA, a value of 100 is recommended.“
    _conf = {
        "n_components": 4
    }

    def __init__(self, conf = {}):
        # Config
        if conf:
            for key in conf.keys():
                self._conf[key] = conf[key]

        # LSA Datenstrukturen
        self.dtm, self.vocabulary, self.vectorizer = self.build_dtm()
        self.tfidf_dtm = self.build_tfidf()
        self.lsa = self.build_tfidf_lsa()
        self.svd = self.build_tfidf_svd()

    # Methoden für weitere Texte

    def vectorize_on_vocabulary(self, text):
        # Build a list with one entry containing text as string.
        lemmatized_text = [" ".join(text.lemmatized_words)]
        # Build vector via word counting.
        vectorizer = CountVectorizer(min_df=1, vocabulary = self.vocabulary)
        return vectorizer.transform(lemmatized_text)

    def tfidf_on_vocabulary(self, text):
        return Normalizer(copy=False).fit_transform(self.vectorize_on_vocabulary(text))

    def project_on_semantic_space(self, text):
        vector = self.tfidf_on_vocabulary(text)
        return self.svd.transform(vector)

    def cosine(self, text_x, text_y):
        x = self.project_on_semantic_space(text_x)
        y = self.project_on_semantic_space(text_y)
        return cosine_similarity(x, y)
    
    # LSA Methoden

    def build_tfidf_svd(self):
        svd_tfidf = TruncatedSVD(self._conf["n_components"], algorithm='randomized')
        svd_tfidf.fit(self.tfidf_dtm)
        return svd_tfidf

    def build_tfidf_lsa(self):
        # Führe LSA mit TFIDF-gewichteter DTM aus.
        svd = TruncatedSVD(self._conf["n_components"], algorithm='randomized')
        lsa_tfidf = svd.fit_transform(self.tfidf_dtm)
        lsa_tfidf = Normalizer(copy=False).fit_transform(lsa_tfidf)
        return lsa_tfidf

    def build_tfidf(self):
        tfidf_transformer = TfidfTransformer()
        tfidf_dtm = tfidf_transformer.fit_transform(self.dtm)
        return tfidf_dtm
    
    def build_dtm(self):
        lemmatized_corpus = self.get_lemmatized_plaintext_corpus()
        # Generiere Document-Term-Matrix und vocabulary
        vectorizer = CountVectorizer(min_df=1)
        dtm = vectorizer.fit_transform(lemmatized_corpus)
        lex = vectorizer.get_feature_names_out()
        return dtm, lex, vectorizer

    def plot_components(self):
        # Sammlung von DataFrame pro Dimension
        result = list()

        for i in range(0, self._conf["n_components"]):
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

        # Erstelle Plot mit 2 Spalten.
        fig = plt.figure()
        fig.subplots_adjust(hspace=.5, wspace=.5)
        for i in range(0, self._conf["n_components"]):
            n_rows = int(self._conf["n_components"] / 2) + (self._conf["n_components"] % 2)
            n_columns = 2
            ax = fig.add_subplot(n_rows, n_columns, i+1)
            ax.barh(result[i]['terms'],result[i]['weights'], align="center")
            ax.set_title('Dimension %d' % (i))
        plt.show()

    # Korpus Methoden

    def read_corpus_file(self):
        if not hasattr(self, '_corpus'):
            # Texte einlesen
            textfile = codecs.open("./texteVU.txt", "r", "utf-8")
            texts = textfile.read()
            textfile.close()
            # Fix errors in file
            texts = texts.replace("§4", "4")
            texts = texts.replace("§A", "§\r\nA")
            texts = texts.replace("B_IG_LB1_MZPI_BR07GEF_Haupterhebungich", "B_IG_LB1_MZPI_BR07GEF_Haupterhebung\r\n§\r\nich")
            texts = texts.replace("-999", "")
            texts = texts.replace("Text fehlt noch", "")
            # Trenne Texte anhand von Trennzeichen 
            # Trenner: Zeilenumbruch Paragraph-Zeichen Zeilenumbruch
            texts = re.split("\r\n\§\r\n", texts)
            # Erstelle Datenstruktur für die Texte
            self._corpus = list()
            for i in range(len(texts)):
                if (i%2 == 0):
                    # Ungerader Index: ID
                    # Gerader Index:   Text
                    # Check if text is empty.
                    if texts[i+1].strip():
                        t = Text(
                            plaintext = texts[i+1].strip(),
                            author = texts[i].strip()
                            )
                        self._corpus.append(t)
        return self._corpus

    def get_lemmatized_plaintext_corpus(self):
        corpus = self.build_bag_of_lemmalists()
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
        return [t.sentences for t in self.read_corpus_file()]

    def build_bag_of_tokenlists(self):
        return [t.words for t in self.read_corpus_file()]

    def build_bag_of_tagglists(self):
        return [t.tagged_sentences for t in self.read_corpus_file()]        

    def build_bag_of_lemmalists(self):
        return [t.lemmatized_sentences for t in self.read_corpus_file()]        