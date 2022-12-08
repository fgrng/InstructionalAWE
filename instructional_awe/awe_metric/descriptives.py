# descriptives.py - Provides descriptive indices.
#
# Implements DESPC, DESSC, DESWC, DESPL, DESSL, DESWL.
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

# Development notes:
# ==================
# Implementation derived from:
#   McNamara, Danielle S., Arthur C. Graesser, Philip M. McCarthy, und Zhiqiang Cai. (2014)
#   Automated evaluation of text and discourse with Coh-Metrix.
#   New York, NY: Cambridge University Press.
#
# See P. 61ff
#   „Coh-Metrix provides descriptive indices to help the user check the Coh-Metrix output
#   (e.g., to make sure that the numbers make senes) and interpret patterns of data.“

from .metric import Metric
import pyphen
import statistics
import nltk


def number_of_paragraphs(text):
    """Returns the total number of paragraphs in the text.
    Paragraphs are usually defined by hard returns within the text.
    """
    return len(text.paragraphs)

def number_of_sentences(text):
    """Returns the total number of sentences in the text.
    Sentences are identified by the nltk Punkt sentence tokenizer.
    """
    return len(text.sentences)

def number_of_words(text):
    """Returns the total number of words in the text.
    Words are identified by the nltk tokenizer. 
    """
    return len(_pos_list_words(text))


def paragraph_length_in_sentences(text):
    """Returns the mean length (and standard deviation) of paragraphs.
    This is the average number of sentences in each paragraph within the text.
    """
    language, _ = text.language()
    sentence_counts = [len(
        nltk.sent_tokenize(paragraph, language = language)
    ) for paragraph in text.paragraphs]
    return statistics.mean(sentence_counts), statistics.stdev(sentence_counts), number_of_sentences(text)

def sentence_length_in_words(text):
    """Returns the mean number of words (and standard deviation) of sentences.
    This is the average number of words in each sentence within the text,
    where a word is anything that is tagged as a part-of-speech by the
    HanTa PoS-Tagger (HanoverTagger).
    """
    # PoS-Tags for punctuation or unknown parts of speech.
    not_words = ["XY", "$.", "$,", "$("]
    word_counts = [len(
        [word for word in sentence if word[1] not in not_words]
    ) for sentence in text.tagged_sentences()]
    return statistics.mean(word_counts), statistics.stdev(word_counts), number_of_words(text)

def word_length_in_syllables(text):
    """Returns the mean number of syllables (and standard deviation) in words.
    Syllables are identified by hyphenation rules using the pyphens included dictionary.
    """
    # Get dictiornary for hyphenation.
    _, lang = text.language()
    dictionary = pyphen.Pyphen(lang = lang)
    # number of positions for hyphenization plus 1 for each word
    syllable_counts = [(len(dictionary.positions(word)) + 1) for word in _list_words(text)]
    number_of_syllables = sum(syllable_counts)
    return statistics.mean(syllable_counts), statistics.stdev(syllable_counts), number_of_syllables

def word_length_in_characters(text):
    """Returns the mean number of letters ()and standard deviation) in words.
    This is the average number of letters for all of the words in the text.
    """
    # number of characters for hyphenization plus 1 for each word
    character_counts = [len(word) for word in _list_words(text)]
    number_of_characters = sum(character_counts)
    return statistics.mean(character_counts), statistics.stdev(character_counts), number_of_characters


## Helper methods

def _pos_list_all(text):
    return [tag[2] for tag in text.tagged_words()]

def _pos_list_words(text):
    not_words = ["XY", "$.", "$,", "$("]
    return [tag for tag in _pos_list_all(text) if tag not in not_words]

def _list_words(text):
    not_words = ["XY", "$.", "$,", "$("]
    return [tag[0] for tag in text.tagged_words() if tag[2] not in not_words]
