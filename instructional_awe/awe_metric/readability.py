from metrics.descriptives import Descriptives
import pyphen

class LesbarkeitsindexLIX(Descriptives):
    """Eine sehr populäre Formel wurde von Björnsson 1968 vorgeschlagen:
        der Lesbarkeitsindex LIX (im Originaltext 'Läsbarhetsindex'). 
        Dieser ergibt sich aus der Summe der durschnittlichen Satzlänge eines Textes 
        und des prozentualen Anteils langer Wörter (mehr als sechs Buchstaben). 
        Auf diese Weise erhält man eine ungefähre Einschätzung der Schwierigkeit von Texten.
        [https://www.psychometrica.de/lix.html]
    """

    def value(self):
        """Calculate the value of the metric in the text.

        Returns: an appropriate data structure for the corresponding to the metric.
        """
        # Get dictiornary for hyphenation.
        dictionary = pyphen.Pyphen(lang = self.text._conf['language_short'])

        # Durchschnittliche Satzlänge (in Wörtern)
        average_sentence_length = self.number_of_words() / len(self.text.sentences)
        # Prozentanteil der langen Wörter mit mehr als sechs Buchstaben
        percentage_of_long_words = len([word for word in [w for w in self._list_words()] if len(word) > 6]) / self.number_of_words()

        match self.text._conf["language"]:
            case "german":
                return average_sentence_length + (100 * percentage_of_long_words)
            case "englisch":
                raise ValueError("No valid language given for Wiener Sachtextformel index.")
            case _:
                raise ValueError("No valid language given for Wiener Sachtextformel index.")

class WienerSachtextformel(Descriptives):
    """Die Wiener Sachtextformel dient zur Berechnung der Lesbarkeit deutschsprachiger Texte. 
        Sie gibt an, für welche Schulstufe ein Sachtext geeignet ist. 
        Die Skala beginnt bei Schulstufe 4 und endet bei 15, 
        wobei ab der Stufe 12 eher von Schwierigkeitsstufen 
        als von Schulstufen gesprochen werden sollte. 
        Ein Wert von 4 steht demnach für sehr leichten Text, 
        dagegen bezeichnet 15 einen sehr schwierigen Text. [Wikipedia]
    """
    
    def value(self):
        """Calculate the value of the metric in the text.

        Returns: an appropriate data structure for the corresponding to the metric.
        """
        # Get dictiornary for hyphenation.
        dictionary = pyphen.Pyphen(lang = self.text._conf['language_short'])

        # MS ist der Prozentanteil der Wörter mit drei oder mehr Silben, [Wikipedia]
        #   (number of syllables = number of positions for hyphenization plus 1)
        ms = len([word for word in [w for w in self._list_words()] if len(dictionary.positions(word)) + 1 >= 3]) / self.number_of_words()
        ms = 100 * ms
        # SL ist die mittlere Satzlänge (Anzahl Wörter), [Wikipedia]
        sl = self.number_of_words() / len(self.text.sentences)
        # IW ist der Prozentanteil der Wörter mit mehr als sechs Buchstaben, [Wikipedia]
        iw = len([word for word in [w for w in self._list_words()] if len(word) > 6]) / self.number_of_words()
        iw = 100 * iw
        # ES ist der Prozentanteil der einsilbigen Wörter. [Wikipedia]
        #   (number of syllables = number of positions for hyphenization plus 1)
        es = len([word for word in [w for w in self._list_words()] if len(dictionary.positions(word)) + 1 == 1]) / self.number_of_words()
        es = 100 * es

        match self.text._conf["language"]:
            case "german":
                return (0.1935 * ms) + (0.1672 * sl) + (0.1297 * iw) - (0.0327 * es) - 0.875
            case "englisch":
                raise ValueError("No valid language given for Wiener Sachtextformel index.")
            case _:
                raise ValueError("No valid language given for Wiener Sachtextformel index.")

class FleschReadingEase(Descriptives):
    """Der Lesbarkeitsindex Flesch-Reading-Ease, auch Flesch-Grad genannt, 
    ist ein numerischer Wert für die Lesbarkeit, der aus einem Text berechnet werden kann. 
    Je höher der Wert ist, desto leichter verständlich ist der Text. 
    Gut verständliche Texte weisen einen Wert von etwa 60 bis 70 auf. [Wikipedia]
    """
    
    def value(self):
        """Calculate the value of the metric in the text.

        Returns: an appropriate data structure for the corresponding to the metric.
        """
        # Get dictiornary for hyphenation.
        dictionary = pyphen.Pyphen(lang = self.text._conf['language_short'])

        # Average Sentence Length (ASL)
        average_sentence_length = self.number_of_words() / len(self.text.sentences)
        # Average Number of Syllables per Word (ASW)
        #   (number of syllables = number of positions for hyphenization plus 1)
        average_syllables_per_word = sum([len(dictionary.positions(word)) + 1 for word in [word for word in self._list_words()]]) / self.number_of_words()

        match self.text._conf["language"]:
            case "german":
                return 206.835 - (1.015 * average_sentence_length) - (84.6 * average_syllables_per_word)
            case "englisch":
                return 164.835 - (1.000 * average_sentence_length) - (58.5 * average_syllables_per_word)
            case _:
                raise ValueError("No valid language given for flesch index.")
