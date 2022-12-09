# latent_semantic_analysis.py - Provides a collection of metrics based on Latent Semantic Analysis.
#
# Implements LSASS, LSAPP, LSAGN.
#

from ..awe_text_representation.text import Text

from itertools import combinations
import statistics


def local_lsa_overlap_sentences(text, space):
    """Returns mean and standard derivation of cosine similarities between
    adjacent sentences as measure of text cohesion.
    """
    cosines = []
    # Use one whitespace to generate empty Text object
    # Text uses strip() on initialization.
    last_sentence = Text(plaintext = " ")
    for sent in text.sentences:
        sentence = Text(plaintext = sent)
        if last_sentence.plaintext != "":
            cosines.append( space.cosine(sentence, last_sentence) )
        last_sentence = sentence
    if len(cosines) > 1:
        return statistics.mean(cosines), statistics.stdev(cosines), len(cosines)
    else:
        return cosines[0], 0, len(cosines)

def global_lsa_overlap_sentences(text, space):
    """Returns mean and standard derivation of cosine similarities between
     sentences as measure of text cohesion.
    """
    # Iterate over sentences and compute cosines
    # counter each time if an overlap is found. Divide by total
    # number of comparisons.
    cosines = []
    for pair in combinations(text.sentences, 2):
        sentence = Text(plaintext = pair[0])
        other_sentence = Text(plaintext = pair[1])
        cosines.append( space.cosine(sentence, other_sentence) )
    if len(cosines) > 1:
        return statistics.mean(cosines), statistics.stdev(cosines), len(cosines)
    else:
        return cosines[0], 0, len(cosines)

def local_lsa_overlap_paragraphs(text, space):
    """Returns mean and standard derivation of cosine similarities between
    adjacent sentences as measure of text cohesion.
    """
    cosines = []
    last_paragraph = ""
    for para in text.paragraphs:
        paragraph = Text(plaintext = para)
        if last_paragraph != "":
            cosines.append( space.cosine(paragraph, last_paragraph) )
        last_paragraph = paragraph
    if len(cosines) > 1:
        return statistics.mean(cosines), statistics.stdev(cosines), len(cosines)
    else:
        return cosines[0], 0, len(cosines)

def global_lsa_overlap_paragraphs(text, space):
    """Returns mean and standard derivation of cosine similarities between
     paragraphs as measure of text cohesion.
    """
    # Iterate over paragraphs and compute cosines.
    cosines = []
    for pair in combinations(text.paragraphs, 2):
        paragraph = Text(plaintext = pair[0])
        other_paragraph = Text(plaintext = pair[1])
        cosines.append( space.cosine(paragraph, other_paragraph) )
    if len(cosines) > 1:
        return statistics.mean(cosines), statistics.stdev(cosines), len(cosines)
    else:
        return cosines[0], 0, len(cosines)

def lsa_overlap_given_new_sentences(text, space):
    """Returns [TODO]
    """
    raise NotImplementedError
