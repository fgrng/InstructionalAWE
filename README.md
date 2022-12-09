# InstructionalAWE
Project for Automated Writing Evaluation in educational or instructional settings (primary for german languages). 

## Quellen und Referenzen

Dieses Projekt re-implementiert unter Anderem einige der Berechnungsfunktionen für die „Coh-Metrix“ Indikatoren von McNamara et al. (2014). Coh-Metrix berechnet Indikatoren für Kohäsion und Kohärenz von englischsprachigen Texten und wird via http://cohmetrix.com/ als Webtool angeboten.

Die hier implementierten Berechnungsfunktionen wurden auf Basis der Beschreibungen in McNamara et al. (2014) entworfen. Teilweise wurde auf andere Quellen zurückgegriffen. Bei der Projektstruktur habe ich mich an [„Coh-Metrix-Port“](https://github.com/nilc-nlp/coh-metrix-port) von Andre Luiz Verucci da Cunha (Copyright (C) 2014, published under GNU General Public License as published by the Free Software Foundation) orientiert.

### Quellen

McNamara, D. S., Graesser, A. C., McCarthy, P. M., & Cai, Z. (2014). Automated evaluation of text and discourse with Coh-Metrix. Cambridge University Press.

Graesser, A. C., & McNamara, D. S. (2011). Computational Analyses of Multilevel Discourse Comprehension. Topics in Cognitive Science, 3(2), 371–398. 

McCarthy, P.M., Jarvis, S. MTLD, vocd-D, and HD-D. (2010). A validation study of sophisticated approaches to lexical diversity assessment. Behavior Research Methods 42, 381–392. Verfügbar unter: https://doi.org/10.3758/BRM.42.2.381

McCarthy, P. M., & Jarvis, S. (2007). vocd: A theoretical and empirical evaluation. Language Testing, 24(4), 459–488. Verfügbar unter: https://doi.org/10.1177/0265532207080767

Charbonnier, J., & Wartena, C. (2020). Predicting the concreteness of German Words. In SWISSTEXT & KONVENS 2020: Swiss Text Analytics Conference & Conference on Natural Language Processing 2020; Proceedings of the 5th Swiss Text Analytics Conference (SwissText) & 16th Conference on Natural Language Processing (KONVENS), CEUR Workshop Proceedings Vol. 2624. Verfügbar unter: https://doi.org/10.25968/opus-2075 

### Ressourcen

- [Coh-Metrx Webtool](http://cohmetrix.com/)
- [Coh-Metrix-Port 2.0](https://github.com/nilc-nlp/coh-metrix-port)
- Artikel [Vorverarbeitung von Texten mit Python und NLTK](https://textmining.wp.hs-hannover.de/Preprocessing.html) von Christian Wartena(?)
- [Deutsches Wortart-Tagset STTS](https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/STTS-Tagset.pdf)
- [Hanover-Tagger „HanTa“](https://github.com/wartaal/HanTa)
- [German dictionaries for Hunspell](https://www.j3e.de/ispell/igerman98/index_en.html)

### Weitere Ressourcen

Unter [German-NLP](https://github.com/adbar/German-NLP) findet man eine sehr hilfreiche „[c]urated list of open-access/open-source/off-the-shelf resources and tools developed with a particular focus on German“.

Morphologie und Wortartenerkennung
- [clevertagger](https://github.com/rsennrich/clevertagger). Mögliche Alternative für den Hanover-Tagger.
- [The Zurich Morphological Analyzer for German](https://pub.cl.uzh.ch/users/sennrich/zmorge/)
- [DEMorphy](https://github.com/DuyguA/DEMorphy).

Ein paar Sammlungen für Textcorpora und Wortdatenbanken, die ich teilweise zum Testen bei der Implementierung verwendet habe.
- [Textsammlungen und Datenbanken zur Verwendung des Deutschen – Materialien für Korpuslinguistik, Sprachwissenschaft und Sprachunterricht (DaF & DaZ)](https://www.sprache-spiel-natur.de/2020/06/14/textsammlungen-und-datenbanken-zur-verwendung-des-deutschen/) aus „Sprache, Spiel Natur“
- [TIGER Korpus](https://www.ims.uni-stuttgart.de/forschung/ressourcen/korpora/tiger/)
- [dlexDB](http://alpha.dlexdb.de/pages/api/)
- [COSMAN II](https://cosmas2.ids-mannheim.de/cosmas2-web/) vom Leibniz-Institut für deutsche Sprache und Zugang zu den Korpora geschriebener Gegenwartssprache des IDS (DeReKo)
- [GermaNet](https://uni-tuebingen.de/en/faculties/faculty-of-humanities/departments/modern-languages/department-of-linguistics/chairs/general-and-computational-linguistics/ressources/lexica/germanet/). Lexikalisch-semantisches Wortnetz der Universität Tübingen.

Die Implementierung von Analyseverfahren von Grammatik und Syntax steht noch aus. Mögliche Bibliotheken für die Umsetzung:
- [The Zurich Dependency Parser for German](https://github.com/rsennrich/parzu) für die Analyse von Satzstrukturen
- [BitPar](https://www.cis.lmu.de/~schmid/tools/BitPar/). Ein Grammatik-Parser (auch) für die deutsche Sprache.
- [jwcdg](https://gitlab.com/nats/jwcdg) „is a constraint-based dependency parser for natural language sentences“.

## Installation und Bedienung 

**TODO*

## Bestandteile des Projekts

Hier werden die einzelnen Komponenten des Projekts und die implementierten Berechnungsfunktionen beschrieben.

### Textrepräsentation

Die `Text`-Klasse ermöglicht die Repräsentation von Texten. Metainformationen eines Texts können in den Attributen `title`, `author` und `source` gespeichert werden. Bei Initialisierung kann der Text als String via `plaintext` oder per Dateipfad in `filepath` bereitgestellt werden.

In der Klasse wird der Eingabetext in der Form erwartet, dass jede Zeile einen Absatz des Texts enthält. 

Die Klasse ist in der Lage den Text in unterschiedlichen Datenstrukturen aufzubereiten:

- Das Attribut `plaintext` liefert den Text als String zurück. Absätze sind per `\n` getrennt.
- Das Attribut `paragraphs` liefert den Text als Liste von Strings zurück, wobei jeder String ein Absatz des Textes ist.
- Das Attribut `sentences` liefert den Text als Liste von Strings zurück, wobei jeder String ein Absatz des Textes ist. Die Sätze werden mit Hilfe des *Sentence Tokenizer* von `NLTK` für die deutsche Sprache extrahiert.
- Das Attribut `words` liefert den Text als geschachtelte Liste zurück, um Zugriff auf die einzelnen Wörter zu ermöglichen. Ruckgabewert ist eine Liste von Listen, wobei jede innere Liste die einzelnen Wörter (und Satzzeichen) eines Satzes als Strings beinhaltet. Die Wörter werden mit Hilfe des *Word Tokenizers* von `NLTK` für die deutsche Sprache extrahiert. Das Attribut `all_words` liefert eine Liste sämtlicher Wörter (und Satzzeichen) des Textes.

Die Klasse ermöglicht Wortartenerkennung, Stemming und Lemmatisierung und verwendet dafür den [Hanover-Tagger „HanTa“](https://github.com/wartaal/HanTa). Für den Hanover-Tagger scheint es keine Tag-Dokumentation zu geben; er scheint sich aber größtenteils [an dieses STTS-Tag](https://www.cis.lmu.de/~schmid/tools/TreeTagger/data/STTS-Tagset.pdf) zu halten. Ich bin auf den Hanover-Tagger über [einen Textmining-Artikel](https://textmining.wp.hs-hannover.de/Preprocessing.html) aufmerksam geworden und habe mir die Funktionsweise [über diese Demo-Implementation](https://github.com/wartaal/HanTa/blob/master/Demo.ipynb) erarbeitet.

Über die Methoden `tagged_sentences()` und `tagged_words()` erhält man (je nach gesetztem `taglevel`) entsprechende Listen von Tupeln, die die einzelnen Wörter, Wortarten, etc. enthalten. Die Methoden `lemmatized_sentences()` und `lemmatized_words()` liefert die lemmatisierte Form der Wörter zurück; `stemmed_sentences()` und `stemmed_words()` liefert die Wortstämme zurück.

### Deskriptive Oberflächenmerkmale

> „Coh-Metrix provides descriptive indices to help the user check the Coh-Metrix output (e.g., to make sure that the numbers make senes) and interpret patterns of data.
> (McNamara et al., 2014, S. 61ff)

Das Modul `descriptives` implementiert die Indikatoren DESPC, DESSC, DESWC, DESPL, DESSL, DESWL von Coh-Metrix.

- Die Funktionen `number_of_*(text)` gibt die Anzahl an Absätzen, Sätzen oder Wörtern in dem gegebenen Textobjekt zurück.
- Modul liefert verschieden Längenmaße für Textobjekte. Die Funktion `paragraph_length_in_sentences(text)` gibt die mittlere Länge der Absätze, gemessen in der Anzahl an Sätzen, dessen Standardabweichung und die Anzahl an Absätzen als Tripel zurück. Analog kann die mittlere Satzlänge in Wörten, die mittlere Wortlänge in Silben und die mittlere Wortlänge in Buchstaben bestimmt werden.

Das Modul greift auch auf Funktionalitäten aus `NLTK` zurück. Für die Silbenerkennung wird das Paket `pyphen` verwendet. Mittelwert und Standardabweichung wird mit `statistics` berechnet.

### Indizes für verschiedene Wortarten 

Das Modul `word_information` implementiert WRDNOUN, WRDVORB, WRDARJ, WRDADV, WRDPRO, WRDPRP[1-3], WRDFRQ, WRDAOA, WRDFAM, WRDCNC, FRDIMG, WRDMEA, WRDPOL, WRDHYP.

- Das Modul erlaubt die Berechnung der Inzidenz von Verben, Nomen, Adjektiven, Adverben und Pronomen.
- Zusätzlich kann die Inzidenz von *Content Words* und *Function Words* bestimmt werden. *Content Words* habe ich für die deutsche Sprache grob als Autosemantika verstanden; *Function Words* entsprechend als Synsemantika, und wie folgt implementiert: 
    ```python
    content_word_tags = noun_tags + lexical_verb_tags + adjective_tags + adverb_tags + foreign_tags
    ```
    bzw. 
    ```python
    function_word_tags = article_tags + conjunction_tags + particle_tags + pronoun_tags + adposition_tags + modal_verb_tags + auxiliary_verb_tags
    ```
- Für die Berechnungen von Promonen-Inzidenzen habe ich adhoc von Hand Matching-Lister erstellt, etwa `matching_list = ["du", "dich", "dir", "deiner", "Du", "Dich", "Dir", "Deiner"]` für die Inzidenz von Pronomen der zweiten Person in `second_person_pronoun_incidence(text)`.
    ```python
    def first_person_singular_pronoun_incidence(text):
        # …
        matching_list = ["ich", "mich", "mir", "meiner"]
        # …

    def first_person_plural_pronoun_incidence(text):
        # …
        matching_list = ["wir", "uns", "unser"]
        # …

    def second_person_pronoun_incidence(text):
        # …
        matching_list = ["du", "dich", "dir", "deiner", "Du", "Dich", "Dir", "Deiner"]
        # matching_list += ["ihr", "euch", "euer", "eu", "Ihr", "Euch", "Euer", "Eu"]
        # …

    def third_person_singular_pronoun_incidence(text):
        # …
        matching_list = ["er", "sie", "es", "ihn", "ihm", "seiner", "ihrer"]
        # …

    def third_person_plural_pronoun_incidence(text):
        # …
        matching_list = ["sie","Sie", "ihnen", "Ihnen", "ihrer", "Ihrer"]
        # …
    ```

### Häufigkeiten von Wörtern in globalen Lexika

Die originalen Coh-Metrix verwenden das CELEX-Wörterbuch, um die Häufigkeit der im Textobjekt verwendeten Wörter in globalen Lexika nachzuschlagen. Für das Modul `word_information` habe ich diese Funktionlitäten für das DWDS-Lexikon implementiert.

Die API von https://www.dwds.de/d/api ist in `awe_foreign/dwds.py` implementiert.

Auf Basis der Daten von DWDS wird die mittlere Häufigkeit der *Content Words* / Autosemantika berechnet. Analog kann die mittlere log-Häufigkeit und der Mittelwert der jeweiligen minimalen log-Häufigkeit der Wörter in den einzelnen Sätzen eines Textes bestimmt werden. 

### Psychologische Ratings von Wörtern

Die originalen Coh-Metrix bieten die Berechnung von Textmerkmalen auf Basis von psychologischen Ratings einzelnen Wörter an (etwa durchschnittliches Alter, in dem man das Wort lernt; wahrgenommene Konkretheit des Worts, …). Für die deutsche Sprache habe ich kein freies Wörterbuch für solche Informationen gefunden.

```python
def age_acquisition_content_words(text):
    raise NotImplementedError

def familiarity_content_words(text):
    raise NotImplementedError

def concreteness_content_words(text):
    raise NotImplementedError

def imagability_content_words(text):
    raise NotImplementedError

def meaningfulness_colorodo_content_words(text):
    raise NotImplementedError
```

### Polysemie und Hypernomie

Die originalen Coh-Metrix bieten Berechnungsfunktionen auf Basis der Polysemie und Hypernomie von *Content Words**, Nomen und Verben im Textobjekt an. Da ich hierfür kein frei verfügbares Wörterbuch gefunden habe, versuche ich die Funktionalität über einen Wiktionary-Parser nachzuahmen.

**TODO**

### Lesbarkeitsindizes

Das Modul `readability` implementiert Lesbarkeitsindizes für die deutsche Sprache und weicht hier von den in den originalen Coh-Metrix vorgesehenen Indizes ab (da diese für die englische Sprache ausgewählt wurden).

Für die Silbenanzahlen, die für die Berechnung der Lesbarkeitsindizes benötigt werden, wird das Paket `pyphen` verwendet.

#### Lesbarkeitsindex LIX

> Eine sehr populäre Formel wurde von Björnsson 1968 vorgeschlagen: der Lesbarkeitsindex LIX (im Originaltext 'Läsbarhetsindex'). Dieser ergibt sich aus der Summe der durschnittlichen Satzlänge eines Textes und des prozentualen Anteils langer Wörter (mehr als sechs Buchstaben). Auf diese Weise erhält man eine ungefähre Einschätzung der Schwierigkeit von Texten.
> (Quelle: https://www.psychometrica.de/lix.html)

```python
    # …
    # Durchschnittliche Satzlänge (in Wörtern)
    average_sentence_length = descriptives.number_of_words(text) / len(text.sentences)
    # Prozentanteil der langen Wörter mit mehr als sechs Buchstaben
    percentage_of_long_words = len([word for word in [w for w in descriptives._list_words(text)] if len(word) > 6]) / descriptives.number_of_words(text)
    # …
    return average_sentence_length + (100 * percentage_of_long_words)
```

#### Wiener Sachtextformel

> Die Wiener Sachtextformel dient zur Berechnung der Lesbarkeit deutschsprachiger Texte. Sie gibt an, für welche Schulstufe ein Sachtext geeignet ist. Die Skala beginnt bei Schulstufe 4 und endet bei 15, wobei ab der Stufe 12 eher von Schwierigkeitsstufen als von Schulstufen gesprochen werden sollte. Ein Wert von 4 steht demnach für sehr leichten Text, dagegen bezeichnet 15 einen sehr schwierigen Text. 
> (Quelle: Wikipedia, Wiener Sachtextformel)

```python
    # …
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
    # …
    return (0.1935 * ms) + (0.1672 * sl) + (0.1297 * iw) - (0.0327 * es) - 0.875
    
```

#### Flesch-Reading-Ease

> Der Lesbarkeitsindex Flesch-Reading-Ease, auch Flesch-Grad genannt, ist ein numerischer Wert für die Lesbarkeit, der aus einem Text berechnet werden kann. Je höher der Wert ist, desto leichter verständlich ist der Text. Gut verständliche Texte weisen einen Wert von etwa 60 bis 70 auf. 
> (Quelle: Wikipedia, Flesch-Reading-Ease)

```python
    # …
    # Average Sentence Length (ASL)
    average_sentence_length = descriptives.number_of_words(text) / len(text.sentences)
    # Average Number of Syllables per Word (ASW)
    #   (number of syllables = number of positions for hyphenization plus 1)
    average_syllables_per_word = sum([len(dictionary.positions(word)) + 1 for word in [word for word in descriptives._list_words(text)]]) / descriptives.number_of_words(text)
    # …
    return 206.835 - (1.015 * average_sentence_length) - (84.6 * average_syllables_per_word)

```

### Referenzielle Kohäsion (Rekurrenz)

Referenzielle Kohäsion oder Rekurrenz ist eine Möglichkeit um auf Textoberflächenebene den syntaktisch-semantischen Zusammenhang zu erhöhen und so die Textkohäsion zu verbessern. Im Sinner der Coh-Metrix werden referenzielle Kohäsionswerte auf Basis von wiederkehrenden Worten oder Wortbestandteilen berechnet.

> Referential cohesion refers to overlap in content words between local sentences, or coreference. […] coreference is a linguaistic cue that can aid readers in making connections […] in their textbase understanding. 
> (McNamara et al., 2014, S. 63ff)

Das Modul `coreference` implementiert CRFNO, CRFAO, CRFSO, CRFCWO, CRFANP. 

- Die Rekurrenz von Nomen wird mit `global_noun_overlap(text)` und `local_nout_overlap` berechnet. 
- Die Rekurrenz von Argumenten (Nomen und Pronomen) wird mit `global_argument_overlap(text)` und `local_argument_overlap(text)` berechnet.
- Die Rekurrenz von von Nomen, Pronomen und *Content Words* wird mit `global_stem_overlap(text)` und `local_stem_overlap(text)` berechnet.

Die nötigen Wortartenerkennungen werden mit Hilfe des HanoverTagger durchgeführt. Die „lokalen“ Varianten vergleichen jeweils aufeinanderfolgende Sätze. Die „globalen“ Varianten vergleichen jede mögliche Paarkombination an Sätzen aus dem Text. Zurückgegeben wird jeweils die durchschnittliche Anzahl an Textvergleichen, in denen eine Rekurrenz vorgekommen ist.

Die Rekurrenz von *Content Words* wird gemäß der Coh-Metrix Webtool Dokumentation anders berechnet.

> This measure considers the proportion of explicit content words that overlap between pairs of sentences. For example, if a sentence pair has fewer words and two words overlap, the proportion is greater than if a pair has many words and two words overlap.
> (Quelle: http://cohmetrix.com/, Documentation)

Das wird vermutlich nicht 100% der Originalimplementierung entsprechen; ich habe mich jedoch für folgende Umsetzung entschieden. Den Anteil an überlappenden *Content Words* bestimme ich im Vergleich zu der Anzahl an insgesamt vorliegenden *Content Words* in beiden Vergleichssätzen zusammen.

```python
        content_words = {tag[0] for tag in pair[0] if tag[2] in content_word_tags}
        other_content_words = {tag[0] for tag in pair[1] if tag[2] in content_word_tags}
        count_inter = len(content_words.intersection(other_content_words))
        count_union = len(content_words.union(other_content_words))
        content_word_proportion =  count_inter / count_union
```

#### Anaphor overlap (fehlende Implementierung)

> This measure considers the anphor overlap between pairs of sentences. A pair of sentences has an anphor overlap if the later sentence contains a pronoun that refers to a pronoun or noun in the earlier sentence. 
> (Quelle: http://cohmetrix.com/, Documentation)

Ich habe zu aktuellem Zeitpunkt keine Ahnung, wie ich das implementieren könnte. Diese Funktion ist nicht implementiert.

#### Weitere TODOs

In den Funktionen `global_argument_overlap(text)` und `local_argument_overlap(text)` soll laut Dokumentation von Coh-Metrix auch dann eine Rekurrenz gezählt werden, wenn das Nomen in einem Satz in Singularform und im anderen Satz in Pluralform vorliegt. Das ist in der aktuellen Version nicht berücksichtigt. 

Analog kann auch in `global_stem_overlap(text)` und `local_stem_overlap(text)` in diesem Sinne falsch gezählt werden, wenn sich Wortstamm von Singular- und Pluralform unterscheiden.

> There are different variants of the five measures coreference. Some indices consider only pairs of adjacent sentences, whereas others consider all possible pairs of sentences in a paragraph. When all possible pairs of sentences are considered, there is the distinction between weighted and unweighted metrics that are sensitive to the distance between sentences.
> (Graesser & McNamara, 2011, 382**

Anders als in der Dokumentation des Coh-Metrix Webtools wird hier darauf hingewiesen, dass bei den „globalen“ Kenngrößen jeweils der Abstand der verglichenen Sätze im Text berücksichtigt werden sollte.

Das ist so noch nicht implementiert. In der jetzigen Version wird jeder Satzvergleich gleich gewichtet.

### Kohäsion auf Basis von Latent Semantic Analyses

**TODO**

### Lexikalische Diversität

Die lexikalische Diversität bezieht sich auf die Anzahl an eindeutigen Wörtern (**types*) im Vergleich zu der Gesamtanzahl an Wörtern in einem Text (*tokens*). Das Modul `lexical_diversity` implementiert LDTTR, LDMTLD, LDVOCD.

- Die Funktion `type_token_ratio(text, …)` bestimmt die Type-Token-Relation (TTR). Dabei wird die Anzahl an eindeutigen Wörten gezählt und durch die Anzahl aller Wörter geteilt.
    ```python
        n_tokens = len(list_of_words)
        n_types = len(set(list_of_words))
        return n_types / n_tokens
    ```
    Mit Blick auf die Dokumentation von Coh-Metrix ist mir nicht klar, ob es hier Sinn ergibt, wirklich alle Vorkommen einzelner Wörter einzeln zu zählen. Mit dem Parameter `use_lemmatized_words = True` kann die Wortzählung daher auf Basis der Wordstämme durchgeführt werden. Die Type-Token-Relation kann für alle Wörter oder nur für *Content Words* berechnet werden. Mit dem Parameter `use_content_words = True` erfolgt hierfür die Auswahl. Die TTR ist mit der Textlänge korreliert / konfundiert.
- Die Funktion `mtld(text, …)` berechnet das *MTLD* (measure of textual lexical diversity). Die Implementierung habe ich [von *kristopherkyle* übernommen](https://github.com/kristopherkyle/lexical_diversity). Das MLTD geht auf McCarthy and Jarvis (2007, 2010) zurück. Die Schätzung der lexikalischen Diversität mit dem *MTLD* ist weniger bis kaum von der Textlänge beeinflusst.
    > MTLD is calculated as the mean length of sequential word strings in a text that maintain a given TTR value. 
    > (McNamara et al., 2014, S. 67)
- Die Funktion `vocd(text, …)` schätzt lexikalische Diversität auf Basis von zufälligen Wörter-Samples. Die Implementierung habe ich [von *kristopherkyle* übernommen](https://github.com/kristopherkyle/lexical_diversity). Das *vocd* geht auf McCarthy and Jarvis (2007, 2010** zurück.Die Schätzung der lexikalischen Diversität mit dem *vocd* ist zum Teil weniger von der Textlänge beeinflusst.
    > The index produced by vocd is calculated through a computational procedure that fits TTR random samples with ideal TTR curves.
    > (McNamara et al., 2014, S. 67)

### Konjunktionen / Connectves

**TODO**

### Situationsmodell

**TODO**

### Syntaktische Komplexität

**TODO**

### Dichte von syntaktischen Mustern

**TODO**
