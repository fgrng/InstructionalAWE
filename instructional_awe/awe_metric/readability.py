# readability.py - Provides readability metrics.
#

from . import descriptives
import pyphen

def lesbarkeitsindex_LIX(text):
    """Calculate the value of the metric in the text.

    Eine sehr populäre Formel wurde von Björnsson 1968 vorgeschlagen:
    der Lesbarkeitsindex LIX (im Originaltext 'Läsbarhetsindex').
    Dieser ergibt sich aus der Summe der durschnittlichen Satzlänge eines Textes
    und des prozentualen Anteils langer Wörter (mehr als sechs Buchstaben).
    Auf diese Weise erhält man eine ungefähre Einschätzung der Schwierigkeit
    von Texten. [https://www.psychometrica.de/lix.html]

    Returns: an appropriate data structure for the corresponding to the metric.
    """
    # Get dictiornary for hyphenation.
    language, lang = text.language()
    dictionary = pyphen.Pyphen(lang = lang)

    # Durchschnittliche Satzlänge (in Wörtern)
    average_sentence_length = descriptives.number_of_words(text) / len(text.sentences)
    # Prozentanteil der langen Wörter mit mehr als sechs Buchstaben
    percentage_of_long_words = len([word for word in [w for w in descriptives._list_words(text)] if len(word) > 6]) / descriptives.number_of_words(text)

    match language:
        case "german":
            return average_sentence_length + (100 * percentage_of_long_words)
        case "englisch":
            raise ValueError("No valid language given for Wiener Sachtextformel index.")
        case _:
            raise ValueError("No valid language given for Wiener Sachtextformel index.")


def wiener_sachtextformel(text):
    """Calculate the value of the metric in the text.

    Die Wiener Sachtextformel dient zur Berechnung
    der Lesbarkeit deutschsprachiger Texte.
    Sie gibt an, für welche Schulstufe ein Sachtext geeignet ist.
    Die Skala beginnt bei Schulstufe 4 und endet bei 15,
    wobei ab der Stufe 12 eher von Schwierigkeitsstufen
    als von Schulstufen gesprochen werden sollte.
    Ein Wert von 4 steht demnach für sehr leichten Text,
    dagegen bezeichnet 15 einen sehr schwierigen Text. [Wikipedia]

    Returns: an appropriate data structure for the corresponding to the metric.
    """
    # Get dictiornary for hyphenation.
    language, lang = text.language()
    dictionary = pyphen.Pyphen(lang = lang)

    # MS ist der Prozentanteil der Wörter mit drei oder mehr Silben, [Wikipedia]
    #   (number of syllables = number of positions for hyphenization plus 1)
    ms = len([word for word in [w for w in descriptives._list_words(text)] if len(dictionary.positions(word)) + 1 >= 3]) / descriptives.number_of_words(text)
    ms = 100 * ms
    # SL ist die mittlere Satzlänge (Anzahl Wörter), [Wikipedia]
    sl = descriptives.number_of_words(text) / len(text.sentences)
    # IW ist der Prozentanteil der Wörter mit mehr als sechs Buchstaben, [Wikipedia]
    iw = len([word for word in [w for w in descriptives._list_words(text)] if len(word) > 6]) / descriptives.number_of_words(text)
    iw = 100 * iw
    # ES ist der Prozentanteil der einsilbigen Wörter. [Wikipedia]
    #   (number of syllables = number of positions for hyphenization plus 1)
    es = len([word for word in [w for w in descriptives._list_words(text)] if len(dictionary.positions(word)) + 1 == 1]) / descriptives.number_of_words(text)
    es = 100 * es

    match language:
        case "german":
            return (0.1935 * ms) + (0.1672 * sl) + (0.1297 * iw) - (0.0327 * es) - 0.875
        case "englisch":
            raise ValueError("No valid language given for Wiener Sachtextformel index.")
        case _:
            raise ValueError("No valid language given for Wiener Sachtextformel index.")

def flesch_reading_ease(text):
    """Calculate the value of the metric in the text.

    Der Lesbarkeitsindex Flesch-Reading-Ease, auch Flesch-Grad genannt,
    ist ein numerischer Wert für die Lesbarkeit,
    der aus einem Text berechnet werden kann.
    Je höher der Wert ist, desto leichter verständlich ist der Text.
    Gut verständliche Texte weisen einen Wert von etwa 60 bis 70 auf. [Wikipedia]

    Returns: an appropriate data structure for the corresponding to the metric.
    """

    # Get dictiornary for hyphenation.
    language, lang = text.language()
    dictionary = pyphen.Pyphen(lang = lang)

    # Average Sentence Length (ASL)
    average_sentence_length = descriptives.number_of_words(text) / len(text.sentences)
    # Average Number of Syllables per Word (ASW)
    #   (number of syllables = number of positions for hyphenization plus 1)
    average_syllables_per_word = sum([len(dictionary.positions(word)) + 1 for word in [word for word in descriptives._list_words(text)]]) / descriptives.number_of_words(text)

    match language:
        case "german":
            return 206.835 - (1.015 * average_sentence_length) - (84.6 * average_syllables_per_word)
        case "englisch":
            return 164.835 - (1.000 * average_sentence_length) - (58.5 * average_syllables_per_word)
        case _:
            raise ValueError("No valid language given for flesch index.")
