# referential_cohesion.py - Provides a collection of metrics based on coreference measures.
#
# Implements CRFNO, CRFAO, CRFSO, CRFCWO.
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
#   [1] McNamara, Danielle S., Arthur C. Graesser, Philip M. McCarthy, und Zhiqiang Cai. (2014)
#   Automated evaluation of text and discourse with Coh-Metrix.
#   New York, NY: Cambridge University Press.
#   [2] Graesser, A. C., & McNamara, D. S. (2011). Computational Analyses of Multilevel Discourse
#   Comprehension. Topics in Cognitive Science, 3(2), 371–398. 
#
# See [1], P. 63ff
#   „Referential cohesion refers to overlap in content words between local sentences,
#   or coreference. […] coreference is a linguaistic cue that can aid readers in making
#   connections […] in their textbase understanding.“
#
# See [2] P. 382
#   „There are different variants of the five measures coreference. Some indices consider only
#   pairs of adjacent sentences, whereas others consider all possible pairs of sentences
#   in a paragraph. When all possible pairs of sentences are considered, there is the distinction
#   between weighted and unweighted metrics that are sensitive to the distance between sentences.“

import pyphen
import statistics
import nltk

from itertools import combinations

# Matching tags for pronouns.
pronoun_tags = ['PDS', 'PIS', 'PWS', 'PPER' ]
# Matching tags for nouns.
noun_tags = ['NN', 'NE']
# Matching tags for content words.
# Via Wikipedia: „Wortarten, die Autosemantika enthalten können, sind Substantive, [Voll-]Verben,
# Adjektive, Adverbien. Es gibt in diesen aber verschiedentlich auch Elemente,
# die Synsemantika sind, z. B. Hilfsverben. Dagegen sind Artikel, Konjunktionen,
# Subjunktionen und Präpositionen in der Regel synsemantisch.“
content_word_tags = ['ADJA', 'ADJD', 'ADV', 'FM', 'NN', 'NE', 'VVFIN', 'VVIMP', 'VVINF', 'VVIZU', 'VVPP']
# Matching words for function words.
function_word_tags = ['APPR', 'APPRART', 'APPO', 'APZR', 'ART', 'KOUI', 'KOUS', 'KON', 'KOKOM', 'PDS', 'PDAT', 'PIS', 'PIAT', 'PIDAT', 'PPER', 'PPOSS', 'PPOSAT', 'PRELS', 'PRELAT', 'PRF', 'PWS', 'PWAT', 'PWAV', 'PAV', 'PTKZU', 'PTKNEG', 'PTKVZ', 'PTKANT', 'PTKA', 'VAFIN', 'VAIMP', 'VAINF', 'VAPP', 'VMFIN', 'VMINF', 'VMPP']

def local_noun_overlap(text):
    """Returns the adjacent noun overlap.
    This is a measures of local overlap between sentences
    in terms of nouns. Adjacent noun overlap represents the average number
    of sentences in the text that have noun overlap from one sentence
    back to the previous sentence. Nouns must match exactly, in form an plurality.

    Nouns are identified by part-of-speech tagging using the
    HanTa PoS-Tagger (HanoverTagger).
    """
    # Iterate over sentences and compare sets of nouns. Increment
    # counter each time if an overlap is found.
    count_noun_overlap = 0
    # set of nouns from last sentence
    prev_nouns = set()
    # Use tagged sentences (a sentence is a list of triples)
    for sentence in text.tagged_sentences():
        nouns = {tag[0] for tag in sentence if tag[2] in noun_tags}
        if nouns.intersection(prev_nouns):
            count_noun_overlap += 1
        prev_nouns = nouns
    return count_noun_overlap / len(text.sentences)

def global_noun_overlap(text):
    """Returns the global noun overlap.
    This is a measures of global overlap between sentences
    in terms of nouns. Global noun overlap represents the average number
    of sentences in the text that have noun overlap from one sentence
    to other sentences. Nouns must match exactly, in form an plurality.

    Nouns are identified by part-of-speech tagging using the
    HanTa PoS-Tagger (HanoverTagger).
    """
    # Iterate over sentences and compare sets of nouns. Increment
    # counter each time if an overlap is found. Divide by total
    # number of comparisons.
    count_noun_overlap = 0
    count_comparisons = ((len(text.sentences) - 1) * len(text.sentences)) / 2
    # Use tagged sentences (a sentence is a list of triples)
    for pair in combinations(text.tagged_sentences(), 2):
        nouns = {tag[0] for tag in pair[0] if tag[2] in noun_tags}
        other_nouns = {tag[0] for tag in pair[1] if tag[2] in noun_tags}
        if nouns.intersection(other_nouns):
            count_noun_overlap += 1
    # Return average occurance relative to number of sentences.
    # First sentence does not have a previous sentence.
    return count_noun_overlap / count_comparisons

def local_argument_overlap(text):
    """Returns the adjacent argument overlap.
    This is a measures of local overlap between sentences
    in terms of nouns and pronouns. Adjacent argument overlap occurs,
    when there is overlap between a noun in one sentence and the same noun
    (in singular or plural form) in the previous sentence; it also occurs when
    there are matching personal pronouns. It represents the average number
    of sentences in the text that have argument overlap from one sentence
    back to the previous sentence.

    Nouns and pronouns are identified by part-of-speech tagging using the
    HanTa PoS-Tagger (HanoverTagger).
    """
    # Iterate over sentences and compare sets of nouns. Increment
    # counter each time if an overlap is found.
    count_argument_overlap = 0
    # set of nouns from last sentence
    prev_arguments = set()
    # Use tagged sentences (a sentence is a list of triples)
    for sentence in text.tagged_sentences():
        # Use lemma comparison for nouns to ignore plural/singular differences.
        arguments = {tag[0] for tag in sentence if tag[2] in pronoun_tags}
        arguments.union({tag[1] for tag in sentence if tag[2] in noun_tags})
        if arguments.intersection(prev_arguments):
            count_argument_overlap += 1
        prev_arguments = arguments
    return count_argument_overlap / (len(text.sentences) - 1)

def global_argument_overlap(text):
    """Returns the global argument overlap.
    This is a measures of global overlap between sentences
    in terms of nouns and pronouns. Global argument overlap occurs,
    when there is overlap between a noun in one sentence and the same noun
    (in singular or plural form) in another sentences in the text;
    it also occurs when there are matching personal pronouns.
    It represents the average number sentence pairs in the text
    that have argument overlap.

    Nouns and pronouns are identified by part-of-speech tagging
    using the HanTa PoS-Tagger (HanoverTagger).
    """
    # Iterate over sentences and compare sets of nouns. Increment
    # counter each time if an overlap is found. Divide by total
    # number of comparisons.
    count_noun_overlap = 0
    count_comparisons = ((len(text.sentences) - 1) * len(text.sentences)) / 2
    # Use tagged sentences (a sentence is a list of triples)
    for pair in combinations(text.tagged_sentences(), 2):
        nouns = {tag[0] for tag in pair[0] if tag[2] in pronoun_tags}
        nouns.union({tag[1] for tag in pair[0] if tag[2] in noun_tags})
        other_nouns = {tag[0] for tag in pair[1] if tag[2] in pronoun_tags}
        other_nouns.union({tag[1] for tag in pair[1] if tag[2] in noun_tags})
        if nouns.intersection(other_nouns):
            count_noun_overlap += 1
    # Return average occurance relative to number of sentences.
    # First sentence does not have a previous sentence.
    return count_noun_overlap / count_comparisons

def local_stem_overlap(text):
    """Returns the adjacent stem overlap.
    This is a measures of local overlap between sentences
    in terms of nouns, content words and pronouns. A matching in stems
    is sufficient.

    Nouns, content words and pronouns are identified
    by part-of-speech tagging using the HanTa PoS-Tagger (HanoverTagger).
    """
    # Iterate over sentences and compare sets of nouns. Increment
    # counter each time if an overlap is found.
    count_stem_overlap = 0
    # set of nouns from last sentence
    prev_stemms = set()
    # Use tagged sentences (a sentence is a list of triples)
    for sentence in text.tagged_sentences(taglevel = 2):
        pronouns = {tag[0] for tag in sentence if tag[2] in pronoun_tags}
        # Use stem comparison for nouns and content words.
        nouns = {tag[1] for tag in sentence if tag[2] in noun_tags}
        content_words = {tag[1] for tag in sentence if tag[2] in content_word_tags}
        stemms = pronouns.union(nouns)
        if stemms.intersection(prev_stemms):
            count_stem_overlap += 1
        prev_stemms = pronouns.union(content_words)
    return count_stem_overlap / (len(text.sentences) - 1)

def global_stem_overlap(text):
    """Returns the global stem overlap.
    This is a measure of global overlap between sentences
    in terms of nouns, content words and pronouns. There
    is no exact match required. A matching in stems is sufficient.

    Nouns, content words and pronouns  are identified by
    part-of-speech tagging using the HanTa PoS-Tagger (HanoverTagger).
    """
    # Iterate over sentences and compare sets of nouns. Increment
    # counter each time if an overlap is found. Divide by total
    # number of comparisons.
    count_stem_overlap = 0
    count_comparisons = ((len(text.sentences) - 1) * len(text.sentences)) / 2
    # Use tagged sentences (a sentence is a list of triples)
    for pair in combinations(text.tagged_sentences(taglevel = 2), 2):
        stemms = {tag[0] for tag in pair[0] if tag[2] in pronoun_tags}
        stemms.union({tag[1] for tag in pair[0] if tag[2] in noun_tags})
        other_stemms = {tag[0] for tag in pair[1] if tag[2] in pronoun_tags}
        other_stemms.union({tag[1] for tag in pair[1] if tag[2] in content_word_tags})
        if stemms.intersection(other_stemms):
            count_stem_overlap += 1
    # Return average occurance relative to number of sentences.
    # First sentence does not have a previous sentence.
    return count_stem_overlap / count_comparisons

def local_content_words_overlap(text):
    """Returns the mean local content word overlap.
    This measure considers the proportion of explicit
    content words that overlap between pairs of sentences.

    Content words are identified by part-of-speech tagging
     using the HanTa PoS-Tagger (HanoverTagger).
    """
    # Iterate over sentences and compare sets of nouns.
    # Append overlap proportion to list and report statistics.
    content_word_overlap = []
    # set of nouns from last sentence
    prev_content_words = set()
    # Use tagged sentences (a sentence is a list of triples)
    for sentence in text.tagged_sentences():
        content_words = {tag[0] for tag in sentence if tag[2] in content_word_tags}
        count_inter = len(content_words.intersection(prev_content_words))
        count_union = len(content_words.union(prev_content_words))
        content_word_proportion =  count_inter / count_union
        content_word_overlap.append(content_word_proportion)
        prev_content_words = content_words

    # The first comparison in the loop above performs
    # an empty comparison. Here we remove the first value.
    content_word_overlap.popleft()

    return statistics.mean(content_word_overlap), statistics.stdev(content_word_overlap), len(content_word_overlap)


def global_content_words_overlap(text):
    """Returns mean the global content word overlap.
    This measure considers the proportion of explicit
    content words that overlap between pairs of sentences.

    Content words are identified by part-of-speech tagging
     using the HanTa PoS-Tagger (HanoverTagger).
    """
    # Iterate over sentences and compare sets of content words.
    # Append overlap proportion to list and report statistics.
    content_word_overlap = []
    count_comparisons = ((len(text.sentences) - 1) * len(text.sentences)) / 2
    # Use tagged sentences (a sentence is a list of triples)
    for pair in combinations(text.tagged_sentences(), 2):
        content_words = {tag[0] for tag in pair[0] if tag[2] in content_word_tags}
        other_content_words = {tag[0] for tag in pair[1] if tag[2] in content_word_tags}
        count_inter = len(content_words.intersection(other_content_words))
        count_union = len(content_words.union(other_content_words))
        content_word_proportion =  count_inter / count_union
        content_word_overlap.append(content_word_proportion)
    # Return average occurance relative to number of sentences.
    # First sentence does not have a previous sentence.
    return statistics.mean(content_word_overlap), statistics.stdev(content_word_overlap), count_comparisons





# Helper methods

def _pos_list_all(text):
    return [tag[2] for tag in text.tagged_words()]

def _pos_list_words(text):
    not_words = ["XY", "$.", "$,", "$("]
    return [tag for tag in _pos_list_all() if tag not in not_words]

def _list_words(text):
    not_words = ["XY", "$.", "$,", "$("]
    return [tag[0] for tag in text.tagged_words() if tag[2] not in not_words]
