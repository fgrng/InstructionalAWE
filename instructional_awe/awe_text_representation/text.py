# text.py - Basic classes for Text representations.
#
# Based on Coh-Metrix-Port's functionalities from
# Andre Luiz Verucci da Cunha [Copyright (C) 2014] published
# under GNU General Public License as published by the Free
# Software Foundation.
#
# Copyright (C) 2021 Fabian Grünig <gruenig@posteo.de>
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

# Utility Packages
import codecs
from itertools import chain
from functools import partial

# Use Natural Language Toolki (nltk) for Sentence Tokenization.
# See: https://www.nltk.org/api/nltk.tokenize.html
import nltk

# Use HanoverTagger for POS-Tagging.
# No Tag-Documantation given. Maybe related: https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/STTS-Tagset.pdf
# See also:
# https://textmining.wp.hs-hannover.de/Preprocessing.html
# https://github.com/wartaal/HanTa
# https://github.com/wartaal/HanTa/blob/master/Demo.ipynb
from HanTa import HanoverTagger as ht


class Text(object):
    """Represents a text: its content and metadata.
    A text has several (optional) attributes: title, author,
    and source.
    """

    _config = {
        "language": "german",
        "language_short": "de_DE"
    }

    def __init__(self, filepath="", plaintext="", encoding='utf-8', title='', author='',
                 source=''):
        """Form basic class of Text representation from plaintext argument or file.
        One of the following two arguments is required:
        filepath -- a path to the file containing the text. The text is
            supposed to be formatted as one paragraph per line, with
            multiple sentences per paragraph. Blank lines are ignored.
        plaintext -- a string containing the text. The text is
            supposed to be formatted as one paragraph per line, with
            multiple sentences per paragraph. Blank lines are ignored.

        Keyword arguments:
        encoding -- The encoding of the input file (default "utf-8")
        title -- The title of the text (default "").
        author -- The author of the text (default "").
        source -- Where the text came from, usually a URL (default "").
        """
        self.title = title
        self.author = author
        self.source = source

        # Should text represantations be cached?
        # Set to True, if self.paragraphs will be static.
        # Set to False, if self.paragraphs might change.
        self.cache_representations = True
        self.cache_taglevel = 1

        if plaintext:
            # plaintext argument was given.
            # ignore whitespace lines
            plaintext = plaintext.splitlines()

        if filepath:
            # filepath argument is given as argument.
            # Override plaintext argument.
            with codecs.open(filepath, mode='r', encoding=encoding) as input_file:
                plaintext = input_file.readlines()

        if plaintext:
            self._paragraphs = [line.strip() for line in plaintext if not line.isspace()]
        else:
            # No text (filpath nor plaintext) argument given.
            raise ValueError("No valid filepath or plaintext given.")

    def __str__(self):
        # Print object information including first 70 characters.
        return '<Text: "%s...">' % (self.plaintext[:70])

    # ===
    # Properties for basic text representation.

    @property
    def paragraphs(self):
        return self._paragraphs

    @property
    def plaintext(self):
        return "\n".join(self.paragraphs)

    @property
    def sentences(self):
        """Return a list of strings, each one being a sentence of the text.
        """
        if (not hasattr(self, '_sentences')) or (not self.cache_representations):
            self._sentences = list()
            for paragraph in self.paragraphs:
                self._sentences += nltk.sent_tokenize(paragraph, language = Text._config['language'])

        return self._sentences

    @property
    def words(self):
        """Return a list of lists of strings, where each list of strings
        corresponds to a sentence, and each string in the list is a word.
        """
        if (not hasattr(self, '_words')) or (not self.cache_representations):
            # apply word_tokenize() to sentences list.
            # (language parameter has to be 'constant' list of same length. we use partial for that.)
            tokenice_partial = partial(nltk.tokenize.word_tokenize, language = Text._config['language'])
            self._words = list(map(tokenice_partial, self.sentences))
        return self._words

    @property
    def all_words(self):
        """Return all words of the text in a single list.
        """
        if (not hasattr(self, '_all_words')) or (not self.cache_representations):
            self._all_words = list(chain.from_iterable(self.words))

        return self._all_words

    # ===
    # Properties for advanced text representation using Part of Speech (POS) Tagging
    # and Lemmatization.

    def sentences_in_paragraphs(self):
        """Return a list of list of strings, each one being a paragraph
        containing a list of sentences (as strings) of the text.
        """
        if (not hasattr(self, '_sentences_in_paragraphs')) or (not self.cache_representations):
            self._sentences_in_paragraphs = list()
            for paragraph in self.paragraphs:
                self._sentences_in_paragraphs.append(
                    nltk.sent_tokenize(paragraph, language = Text._config['language'])
                    )

        return self._sentences_in_paragraphs

    def tagged_sentences(self, taglevel = 1):
        """Return a list of lists of triples (string, string, string), 
        representing the sentences with lemmaticed and tagged words.
        """
        if (not hasattr(self, '_tagged_sentences')) or (not self.cache_representations) or (taglevel != self.cache_taglevel):
            # Create list of sentences.
            self._tagged_sentences = list()
            for sentence in self.words:
                # Create lists of triples (word, lemma, tag) from sentence.
                self._tagged_sentences.append(self.tagger().tag_sent(sentence, taglevel))
        self.cache_taglevel = taglevel
        return self._tagged_sentences

    def tagged_words(self, taglevel = 1):
        """Return a list of triples (string, string, sting), representing the tokens
        not separated in sentences.
        """
        return list(chain.from_iterable(self.tagged_sentences(taglevel)))

    def lemmatized_sentences(self):
        """Return a list of strings, each one being a sentence of the text
        containing only lemmatized words.
        """
        if (not hasattr(self, '_lemmatized_sentences')) or (not self.cache_representations):
            self._lemmatized_sentences = list()
            for sentence in self.tagged_sentences(taglevel = 1):
                l_sentence = [t[1] for t in sentence]
                self._lemmatized_sentences.append(l_sentence)

        return self._lemmatized_sentences

    def lemmatized_words(self):
        """Return a list of strings, representing the lemmatized words
        not separated in sentences.
        """
        if (not hasattr(self, '_lemmatized_words')) or (not self.cache_representations):
            self._lemmatized_words = list(
                chain.from_iterable(self.lemmatized_sentences()))

        return self._lemmatized_words

    def stemmed_sentences(self):
        """Return a list of strings, each one being a sentence of the text
        containing only stemmed words.
        """
        if (not hasattr(self, '_lemmatized_sentences')) or (not self.cache_representations):
            self._stemmed_sentences = list()
            for sentence in self.tagged_sentences(taglevel = 2):
                s_sentence = [t[1] for t in sentence]
                self._stemmed_sentences.append(s_sentence)

        return self._stemmed_sentences

    def stemmed_words(self):
        """Return a list of strings, representing the stemmed words
        not separated in sentences.
        """
        if (not hasattr(self, '_lemmatized_words')) or (not self.cache_representations):
            self._stemmed_words = list(
                chain.from_iterable(self.stemmed_sentences))

        return self._stemmed_words

    def tagger(self):
        # Lade Tagger für Lemmatisierung und Worterkennung.
        # Liefert methoden:
        #   analyze(word, taglevel),
        #   tag_word(word, casesensitive, cutoff),
        #   tag_sent(tokenized_sent, casesensitive, taglevel)
        # If the taglevel is set to 1 the Hanover Tagger tries to generate the correct lemma.
        # For the levels 2 and 3 the stem of te word is given.
        if (not hasattr(self, '_tagger')):
            if self._config['language'] == 'german':
                self._tagger = ht.HanoverTagger('morphmodel_ger.pgz')
        return self._tagger

    def language(self):
        return self._config['language'], self._config['language_short']
