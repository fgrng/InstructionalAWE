from metrics.descriptives import Words
import pyphen

# Basice Word Count Indices

class VerbIncidence(Words):
    """
    """
    def __init__(self, name='Verb incidence',
                 column_name='verbs'):
        super(VerbIncidence, self).__init__(name, column_name)

    def value(self):
        return self.n_verbs() / self.n_words()

    def n_verbs(self):
        return len(self._pos_verbs())

    def _pos_verbs(self):
        # For explicit comparison:
        #   verbs = ["VVFIN", "VVIMP", "VVINF", "VVIZU", "VVPP", "VAFIN", "VAIMP", "VAINF", "VAPP", "VMFIN", "VMINF", "VMPP"]
        #   return [tag for tag in self._pos_all if tag in verbs]
        return [tag for tag in self._pos_all() if tag[0] == "V"]

class NounIncidence(Words):
    """
    """
    def __init__(self, name='Noun incidence',
                 column_name='nouns'):
        super(NounIncidence, self).__init__(name, column_name)

    def value(self):
        return self.n_nouns() / self.n_words()

    def n_nouns(self):
        return len(self._pos_nouns())

    def _pos_nouns(self):
        return [tag for tag in self._pos_all() if tag[0] == "N"]

class AdjectiveIncidence(Words):
    """
    """
    def __init__(self, name='Adjective incidence',
                 column_name='adjectives'):
        super(AdjectiveIncidence, self).__init__(name, column_name)

    def value(self):
        return self.n_adjectives() / self.n_words()

    def n_adjectives(self):
        return len(self._pos_adjectives())

    def _pos_adjectives(self):
        return [tag for tag in self._pos_all() if tag[0:2] == "ADJ"]

class AdverbIncidence(Words):
    """
    """
    def __init__(self, name='Adjective incidence',
                 column_name='adverbs'):
        super(AdverbIncidence, self).__init__(name, column_name)

    def value(self):
        return self.n_adverbs() / self.n_words()

    def n_adverbs(self):
        return len(self._pos_adverbs())

    def _pos_adverbs(self):
        return [tag for tag in self._pos_all() if tag[0:2] == "ADV"]

class PronounIncidence(Words):
    """
    """
    def __init__(self, name='Pronoun incidence',
                 column_name='pronouns'):
        super(PronounIncidence, self).__init__(name, column_name)

    def value(self):
        return self.n_pronouns() / self.n_words()

    def n_pronouns(self):
        return len(self._pos_pronouns())

    def _pos_pronouns(self):
        # Pronomen aber keine Partikel.
        return [tag for tag in self._pos_all() if (tag[0] == "P" and tag[0:1] != "PT")]

class FirstPersonSingularPronounIncidence(Words):
    """
    """
    def __init__(self, name='First person singular pronoun incidence',
                 column_name='1st_sing_incidence'):
        super(FirstPersonSingularPronounIncidence, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class FirstPersonPluralPronounIncidence(Words):
    """
    """
    def __init__(self, name='First person plural pronoun incidence',
                 column_name='1st_plural_incidence'):
        super(FirstPersonPluralPronounIncidence, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class SecondPersonPronounIncidence(Words):
    """
    """
    def __init__(self, name='Second person pronoun incidence',
                 column_name='2nd_person_incidence'):
        super(SecondPersonPronounIncidence, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class ThirdPersonSingularPronounIncidence(Words):
    """
    """
    def __init__(self, name='First person singular pronoun incidence',
                 column_name='1st_sing_incidence'):
        super(FirstPersonSingularPronounIncidence, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class ThirdPersonPluralPronounIncidence(Words):
    """
    """
    def __init__(self, name='Third person plural pronoun incidence',
                 column_name='3rd_plural_incidence'):
        super(FirstPersonPluralPronounIncidence, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class CelexWordFrequencyContentWords(Words):
    """
    """
    def __init__(self, name='CELEX word frequency for content words, mean',
                 column_name='CELEX freq content words'):
        super(CelexWordFrequencyContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class CelexLogFrequencyContentWords(Words):
    """
    """
    def __init__(self, name='CELEX log frequency for all words, mean',
                 column_name='CELEX log all words'):
        super(CelexLogFrequencyContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class CelexMinFrequencyContentWords(Words):
    """
    """
    def __init__(self, name='CELEX Log minimum frequency for content words, mean',
                 column_name='CELEX min content words'):
        super(CelexMinFrequencyContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class AgeAcquisitionContentWords(Words):
    """
    """
    def __init__(self, name='Age of acquisition for content words, mean',
                 column_name='Acquisition age content words'):
        super(AgeAcquisitionContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class FamiliarityContentWords(Words):
    """
    """
    def __init__(self, name='Familiarity for content words, mean',
                 column_name='Familiarity content words'):
        super(FamiliarityContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError
        
class ConcretenessContentWords(Words):
    """
    """
    def __init__(self, name='Concreteness for content words, mean',
                 column_name='Concreteness content words'):
        super(ConcretenessContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class ImagabilityContentWords(Words):
    """
    """
    def __init__(self, name='Imagability for content words, mean',
                 column_name='Imagability content words'):
        super(ImagabilityContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError
    
class MeaningfulnessColorodoContentWords(Words):
    """
    """
    def __init__(self, name='Meaningfulness Colorodo norms for content words, mean',
                 column_name='Meaningfulness content words'):
        super(MeaningfulnessColorodoContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class PolysemyContentWords(Words):
    """
    """
    def __init__(self, name='Polysemy for content words, mean',
                 column_name='Polysemy content words'):
        super(PolysemyContentWords, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class HypernymyNouns(Words):
    """
    """
    def __init__(self, name='Hypernymy for nouns',
                 column_name='Hypernymy nouns'):
        super(HypernymyNouns, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class HypernymyVerbs(Words):
    """
    """
    def __init__(self, name='Hypernymy for verbs',
                 column_name='Hypernymy verbs'):
        super(HypernymyVerbs, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class HypernymyNounsAndVerbs(Words):
    """
    """
    def __init__(self, name='Hypernymy for nouns and verbs',
                 column_name='Hypernymy n+v'):
        super(HypernymyNounsAndVerbs, self).__init__(name, column_name)

    def value(self):
        # TODO
        raise NotImplementedError

class ContentWordIncidence(Words):
    """
    """
    def __init__(self, name='Content word incidence',
                 column_name='content_words'):
        super(ContentWordIncidence, self).__init__(name, column_name)

    def value(self):
        raise NotImplementedError
        # content_words = filter(pos_tagger.poset.is_content_word,
        #                        t.tagged_words)
        # return ilen(content_words) / ilen(t.all_words)

class FunctionWordIncidence(Words):
    """
    """
    def __init__(self, name='Function word incidence',
                 column_name='function_words'):
        super(FunctionWordIncidence, self).__init__(name, column_name)

    def value(self):
        raise NotImplementedError
        # function_words = filter(pos_tagger.poset.is_function_word,
        #                         t.tagged_words)
        # return ilen(function_words) / ilen(t.all_words)