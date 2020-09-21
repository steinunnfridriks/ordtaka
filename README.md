# Orðtökutól/Lexicon Acquisition Tool

Orðtökutólið er ætlað til þess að safna saman orðum úr [Risamálheildinni](https://malheildir.arnastofnun.is/) sem vantar í önnur textasöfn, fyrst og fremst [Beygingarlýsingu íslensks nútímamáls (BÍN)](bin.arnastofnun.is/) og hins vegar [Íslenska nútímamálsorðabók (ISLEX)](https://islenskordabok.arnastofnun.is/).

Það má þó einnig nota til þess að setja inn eigin textaskjöl og bera innihald þeirra saman við BÍN og ISLEX, sem ætti t.a.m. að geta nýst við samansöfnun íðorða og annarra orða sem einkenna textann.

Tólið er notað á skipanalínu og uppsetning þess fer fram með því að keyra þessa skipun:

```
python setup.py
```

Við uppsetningu er notandi beðinn um inntak, sem segir til um hvaða staðværu (e. local) gagnagrunnar skuli settir upp.

```
============================================================
Hvaða gagnasöfn viltu setja upp?
============================================================

Stimplaðu tölurnar inn með bili á milli og ýttu á ENTER.

Til að setja upp SHsnid.csv og ordmyndir.txt stimplarðu inn:
1 2
============================================================


(1) SHsnid.csv
(2) ordmyndir.txt
(3) islex_fletta_ofl.csv
```

Að uppsetningu gagnagrunna lokinni er hægt að nota orðtökutólið sjálft með þessari skipun:

```
python run.py
```

Notandi er beðinn um inntak, sem ræður því hvers eðlis úttakið verður, t.d. hvort óskað sé eftir orðmyndum sem finnast ekki í BÍN eða lemmum sem finnast hvorki í BÍN né ISLEX.
