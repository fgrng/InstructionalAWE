from metrics.metric import Metric
import pyphen
import statistics
import nltk

class Descriptives(Metric):
    """Parent class for metrics based on descriptives and word countings.
    """
    def __init__(self, name='Descriptive text metrics', column_name='descriptives'):
        super(Descriptives, self).__init__(name, column_name)

    def number_of_paragraphs(self):
        raise len(self.text.paragraphs)

    def number_of_sentences(self):
        raise len(self.text.sentences)

    def number_of_words(self):
        return len(self._pos_list_words())

    def paragraph_length_in_sentences(self):
        """Returns mean and standard deviation.
        """
        sentence_counts = [len(
            nltk.sent_tokenize(paragraph, language = self.text._conf['language'])
        ) for paragraph in self.text.paragraphs]
        return statistics.mean(sentence_counts), statistics.stdev(sentence_counts), self.number_of_sentences()

    def sentence_length_in_words(self):
        """Returns mean and standard deviation.
        """
        not_words = ["XY", "$.", "$,", "$("]
        word_counts = [len(
            [word for word in sentence if word[1] not in not_words]
        ) for sentence in self.text.tagged_sentences]
        return statistics.mean(word_counts), statistics.stdev(word_counts), self.number_of_words()

    def word_length_in_syllables(self):
        """Returns mean and standard deviation.
        """
        # Get dictiornary for hyphenation.
        dictionary = pyphen.Pyphen(lang = self.text._conf['language_short'])
        # number of positions for hyphenization plus 1 for each word
        syllable_counts = [(len(dictionary.positions(word)) + 1) for word in self._list_words()]
        number_of_syllables = sum(syllable_counts)
        return statistics.mean(syllable_counts), statistics.stdev(syllable_counts), number_of_syllables
    
    def word_length_in_characters(self):
        """Returns mean and standard deviation.
        """
        # number of characters for hyphenization plus 1 for each word
        character_counts = [len(word) for word in self._list_words()]
        number_of_characters = sum(character_counts)
        return statistics.mean(character_counts), statistics.stdev(character_counts), number_of_characters
    
    # Helper methods

    def _pos_list_all(self):
        return [tag[2] for tag in self.text.tagged_words]

    def _pos_list_words(self):
        not_words = ["XY", "$.", "$,", "$("]
        return [tag for tag in self._pos_list_all() if tag not in not_words]

    def _list_words(self):
        not_words = ["XY", "$.", "$,", "$("]
        return [tag[0] for tag in self.text.tagged_words if tag[2] not in not_words]


class Words(Metric):
    """
    """
    def __init__(self, name='Number of Words', column_name='words'):
        super(Words, self).__init__(name, column_name)

    def value(self):
        return self.number_of_words()