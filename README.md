# InstructionalAWE
Project for Automated Writing Evaluation in educational or instructional settings (primary for german languages). 

## Quellen und Referenzen

Dieses Projekt re-implementiert unter Anderem einige der Berechnungsfunktionen für die „Coh-Metrix“ Indikatoren von McNamara et al. (2014). Coh-Metrix berechnet Indikatoren für Kohäsion und Kohärenz von englischsprachigen Texten und wird via http://cohmetrix.com/ als Webtool angeboten.

Die hier implementierten Berechnungsfunktionen wurden auf Basis der Beschreibungen in McNamara et al. (2014) entworfen. Teilweise wurde auf andere Quellen zurückgegriffen. Bei der Projektstruktur habe ich mich an [„Coh-Metrix-Port“](https://github.com/nilc-nlp/coh-metrix-port) von Andre Luiz Verucci da Cunha (Copyright (C) 2014, published under GNU General Public License as published by the Free Software Foundation) orientiert.

## Installation und Bedienung 

TODO

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
> McNamara et al. (2014, S. 61ff)

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
.
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

Die API von https://www.dwds.de/d/api ist in `awe_foreign.dwds.py` implementiert.

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

Die originalen Coh-Metrix bieten Berechnungsfunktionen auf Basis der Polysemie und Hypernomie von *Content Words*, Nomen und Verben im Textobjekt an. Da ich hierfür kein frei verfügbares Wörterbuch gefunden habe, versuche ich die Funktionalität über einen Wiktionary-Parser nachzuahmen.

TODO

### Lesbarkeitsindizes

Das Modul `readability` implementiert Lesbarkeitsindizes für die deutsche Sprache und weicht hier von den in den originalen Coh-Metrix vorgesehenen Indizes ab (da diese für die englische Sprache ausgewählt wurden).

Für die Silbenanzahlen, die für die Berechnung der Lesbarkeitsindizes benötigt werden, wird das Paket `pyphen` verwendet.

#### Lesbarkeitsindex LIX

> Eine sehr populäre Formel wurde von Björnsson 1968 vorgeschlagen: der Lesbarkeitsindex LIX (im Originaltext 'Läsbarhetsindex'). Dieser ergibt sich aus der Summe der durschnittlichen Satzlänge eines Textes und des prozentualen Anteils langer Wörter (mehr als sechs Buchstaben). Auf diese Weise erhält man eine ungefähre Einschätzung der Schwierigkeit von Texten.
> Quelle: https://www.psychometrica.de/lix.html

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
> Quelle: Wikipedia, Wiener Sachtextformel

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
> Quelle: Wikipedia, Flesch-Reading-Ease

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

### TODO 
