# word_information.py - Provides metrics based on word information.
#
# Implements WRDNOUN, WRDVORB, WRDARJ, WRDADV, WRDPRO, WRDPRP[1-3], WRDFRQ, WRDAOA, WRDFAM, WRDCNC, FRDIMG, WRDMEA, WRDPOL, WRDHYP


# from metrics.descriptives import Words
import statistics
import time

from ..awe_foreign.dwds import DWDS
from ..awe_foreign.babelnet import BabelNet

# Configure Logging
import logging, sys, os
logging.basicConfig(stream=sys.stderr)
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)

# Basice Word Count Indices

# Using HanoverTagger for POS-Tagging.
# No Tag-Documantation specific for HanTa given. We are using the
# Stuttgart-Tübingen Tagset (STTS) here and hope the best:
#   https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/STTS-Tagset.pdf
# See also:
#   https://textmining.wp.hs-hannover.de/Preprocessing.html
#   https://github.com/wartaal/HanTa
#   https://github.com/wartaal/HanTa/blob/master/Demo.ipynb

# Matching Tags for standard PoS.
# ===============================
# Matching tags for adjectives (also: starts with "ADJ")
adjective_tags = ["ADJA", "ADJD"]
# Matching tags for adverbs
adverb_tags = ["ADV"]
# Matching tags for adposations (also: starts with "AP")
adposition_tags = ["APPR", "APPRART", "APPO", "APZR"]
# Matching tags for artiles
article_tags = ["ART"]
# Matching tags for cardinal numbers
cardinal_tags = ["CARD"]
# Matching tags for foreign material
foreign_tags = ["FM"]
# Matching tags for interjections
interjection_tags = ["ITJ"]
# Matching tag for conjunctions (also: starts with KO)
conjunction_tags = ["KOUI", "KOUS", "KON", "KOKOM"]
# Matching tags for nouns (also: starts with N).
noun_tags = ["NN", "NE"]
# Matching tags for pronouns
# (also: starts with "P", but second char is not "T"
# or: starts with ["PD", "PI", "PP", "PW"]).
pronoun_tags = ["PDS", "PDAT", "PIS", "PIAT", "PIDAT", "PPER", "PPOSS", "PPOSAT", "PRELS", "PRELAT", "PRF", "PWS", "PWAT", "PWAV", "PAV"]
# Matching tags for particles (also: starts with "PT")
particle_tags = ["PTKZU", "PTKNEG", "PTKVZ", "PTKANT", "PTKA"]
# Matching tags for "Kompositions-Erstglied"
trunc_tags = ["TRUNC"]
# Matching tags for verbs (also starts with "V")
verb_tags = ["VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP", "VAFIN", "VAIMP", "VAINF", "VAPP", "VMFIN", "VMINF", "VMPP"]
# Matching tags for lexical verbs (also starts with "VV")
lexical_verb_tags = ["VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP"]
# Matching tags for auxiliary verb (also start with "VA")
auxiliary_verb_tags = ["VAFIN", "VAIMP", "VAINF", "VAPP"] 
# Matching tag for modal verbs (also starts with "VM")
modal_verb_tags = ["VMFIN", "VMINF", "VMPP"]
# Matching tags for non-words
nonword_tags = ["XY"]
# Matching tags for punctuation (also starts with "$")
punctuation_tags = ["$.", "$,", "$("]

# Matching Tags  for specific PoS-metrics
# =======================================
# Matching pronoun tags for argument overlap.
argument_pronoun_tags = ["PDS", "PIS", "PWS", "PPER" ]
# Matching tags for content words.
#   Via Wikipedia (Autosemantikum): „Wortarten, die Autosemantika enthalten können,
#   sind Substantive, [Voll-]Verben, Adjektive, Adverbien. Es gibt in diesen aber
#   verschiedentlich auch Elemente, die Synsemantika sind, z. B. Hilfsverben.
#   Dagegen sind Artikel, Konjunktionen, Subjunktionen und Präpositionen
#   in der Regel synsemantisch.“
content_word_tags = noun_tags + lexical_verb_tags + adjective_tags + adverb_tags + foreign_tags
non_noun_content_word_tags = lexical_verb_tags + adjective_tags + adverb_tags + foreign_tags
# Matching words for function words.
#   Via Wikipedia (Synsemantikum): „Zu ihnen zählen Artikel, Konjunktionen, Partikel,
#   Pronomen, Präpositionen, Modalverben und Hilfsverben“
function_word_tags = article_tags + conjunction_tags + particle_tags + pronoun_tags + adposition_tags + modal_verb_tags + auxiliary_verb_tags

# Helper functions for word counting.
# ===================================

def pos_list_for_tags(text, taglist = [], taglevel = 0):
    """Returns list of tags
    """
    if taglevel == 0:
        return [tag for tag in text.tagged_words(taglevel) if tag in taglist]
    if taglevel == 1 or taglevel == 2:
        return [tag for tag in text.tagged_words(taglevel) if tag[2] in taglist]
    if taglevel >= 3:
        return [tag for tag in text.tagged_words(taglevel) if tag[3] in taglist]

def wordcount_for_tags(text, taglist = []):
    return len(pos_list_for_tags(text, taglist))

def wordcount_total(text):
    pos_list_all_words = [tag for tag in text.tagged_words(taglevel = 0) if tag not in nonword_tags]
    return len(pos_list_all_words)

def incidence_for_tags(text, taglist = [], per = 1000):
    """Returns incidence value for words in taglist for given population size.
    """
    count = wordcount_for_tags(text, taglist)
    population = wordcount_total(text)
    return incidence(count, population, per)

def incidence(count, population, per):
    return (count / population) * per

# Incidence Values for words / parts of speech.
# =============================================

def verb_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = verb_tags
    return incidence_for_tags(text, taglist, per = 1000)

def noun_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    """
    """
    taglist = noun_tags
    return incidence_for_tags(text, taglist, per = 1000)

def adjective_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = adjective_tags
    return incidence_for_tags(text, taglist, per = 1000)

def adverb_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = adverb_tags
    return incidence_for_tags(text, taglist, per = 1000)

def pronoun_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = pronoun_tags
    return incidence_for_tags(text, taglist, per = 1000)

def content_word_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = content_word_tags
    return incidence_for_tags(text, taglist, per = 1000)

def function_word_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = function_word_tags
    return incidence_for_tags(text, taglist, per = 1000)

# Incidence Values for words / parts of speech (graduated).
# =========================================================

def first_person_singular_pronoun_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = pronoun_tags
    pos_list = pos_list_for_tags(text, taglist, taglevel = 1)
    matching_list = ["ich", "mich", "mir", "meiner"]
    count = len([tag for tag in pos_list if tag[0] in matching_list])
    population = wordcount_total(text)
    return incidence(count, population, per = 1000)

def first_person_plural_pronoun_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = pronoun_tags
    pos_list = pos_list_for_tags(text, taglist, taglevel = 1)
    matching_list = ["wir", "uns", "unser"]
    count = len([tag for tag in pos_list if tag[1] in matching_list])
    population = wordcount_total(text)
    return incidence(count, population, per = 1000)

def second_person_pronoun_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = pronoun_tags
    pos_list = pos_list_for_tags(text, taglist, taglevel = 1)
    # Use explicit word (not stem or lemma).
    matching_list = ["du", "dich", "dir", "deiner", "Du", "Dich", "Dir", "Deiner"]
    # matching_list += ["ihr", "euch", "euer", "eu", "Ihr", "Euch", "Euer", "Eu"]
    count = len([tag for tag in pos_list if tag[0] in matching_list])
    population = wordcount_total(text)
    return incidence(count, population, per = 1000)

def third_person_singular_pronoun_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = pronoun_tags
    pos_list = pos_list_for_tags(text, taglist, taglevel = 1)
    # Use explicit word (not stem or lemma).
    matching_list = ["er", "sie", "es", "ihn", "ihm", "seiner", "ihrer"]
    count = len([tag for tag in pos_list if tag[0] in matching_list])
    population = wordcount_total(text)
    return incidence(count, population, per = 1000)

def third_person_plural_pronoun_incidence(text):
    """Returns the relative frequency of the given word category by
    counting the number of instances of the category per 1000 words
    of text.
    """
    taglist = pronoun_tags
    pos_list = pos_list_for_tags(text, taglist, taglevel = 1)
    # Use explicit word (not stem or lemma).
    matching_list = ["sie","Sie", "ihnen", "Ihnen", "ihrer", "Ihrer"]
    count = len([tag for tag in pos_list if tag[0] in matching_list])
    population = wordcount_total(text)
    return incidence(count, population, per = 1000)

# Word Frequency
# ==============

def celex_word_frequency_content_words(text):
    """Returns the mean word frequency for content words.

    Coc-Metrix uses CELEX. We are using DWDS.
    """
    content_words = pos_list_for_tags(text, taglist = content_word_tags, taglevel = 1)
    content_words = [tag[0] for tag in content_words]
    dw = DWDS()
    freqs = list()
    logger.debug("Starting requests for DWDS")
    for word in content_words:
        logger.debug("Get frequency from DWDS for '%s'" % word)
        r = dw.get_frequency(word)
        freq = (int(r['hits']) / int(r['total'])) * 1000000
        freqs.append(freq)
        time.sleep(0.2)
    return statistics.mean(freqs)

def celex_log_frequency_all_words(text):
    """Returns the mean of the logarithms of word frequency for all words.

    Coc-Metrix uses CELEX. We are using DWDS.
    """
    all_words = [tag for tag in text.tagged_words(taglevel = 1) if tag not in nonword_tags]
    all_words = [tag[0] for tag in all_words]
    dw = DWDS()
    logs = list()
    logger.debug("Starting requests for DWDS")
    for word in all_words:
        logger.debug("Get frequency from DWDS for '%s'" % word)
        r = dw.get_frequency(word)
        log = float(r['frequency'])
        logs.append(log)
        time.sleep(0.2)
    return statistics.mean(logs)

def celex_min_frequency_content_words(text):
    """Returns the average minimum logarithmic
    frequency for content words across sentences.

    Coh-Metrixs uses CELEX. We are usung DWDS.
    """
    dw = DWDS()
    mins = list()
    for sentence in text.tagged_sentences():
        content_words = [tag[0] for tag in sentence if tag in content_word_tags]
        freqs = list()
        for word in content_words:
            logger.debug("Get frequency from DWDS for '%s'" % word)
            r = dw.get_frequency(word)
            log = float(r['frequency'])
            freqs.append(log)
            time.sleep(0.2)
        # Collect smallest frequency of function word in sentence, if list is not empty.
        if freqs:
            mins.append(min(freqs))

    return statistics.mean(mins)

# Psychological Ratings
# =====================

def age_acquisition_content_words(text):
    """
    """
    # TODO
    raise NotImplementedError

def familiarity_content_words(text):
    """
    """
    # TODO
    raise NotImplementedError

def concreteness_content_words(text):
    """
    """
    # TODO
    raise NotImplementedError

def imagability_content_words(text):
    """
    """
    # TODO
    raise NotImplementedError

def meaningfulness_colorodo_content_words(text):
    """
    """
    # TODO
    raise NotImplementedError


# Psychological Ratings
# =====================

def polysemy_content_words(text):
    """
    """
    # TODO
    raise NotImplementedError

def hypernymy_nouns(text):
    """Provides estimates of hypernymy for nouns in the text.

    A hypernym is denotes a supertype in semantic relationships.
    """
    nouns = pos_list_for_tags(text, taglist = noun_tags, taglevel = 1)
    nouns = [tag[1] for tag in nouns]

    from wiktionaryparser import WiktionaryParser
    parser = WiktionaryParser()
    parser.url = "https://de.wiktionary.org/wiki/{}?printable=yes"
    parser.set_default_language("german")
    parser.include_part_of_speech("noun")
    parser.include_relation("hypernyms")

    #for noun in nouns:
    noun = nouns[0]
    results = parser.fetch(noun)
    for result in results:
        #     for definition in result["definitions"]:
        #         hypernyms = [ hy["words"] for hy in definition["relatedWords"] if hy["relationshipType"] == "hypernyms" ]
        print(noun, ":", result)


def hypernymy_verbs(text):
    """Provides estimates of hypernymy for verbs in the text.
    A hypernym is denotes a supertype in semantic relationships.
    """
    # TODO
    raise NotImplementedError

def hypernymy_nouns_and_verbs(text):
    """Provides estimates of hypernymy for nouns and verbs in the text.
    A hypernym is denotes a supertype in semantic relationships.
    """
    # TODO
    raise NotImplementedError

