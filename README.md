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
============================================================1

# Orðtökutól/Lexicon Acquisition Tool

2

​

3

Orðtökutólið er ætlað til þess að safna saman orðum úr [Risamálheildinni](https://malheildir.arnastofnun.is/) sem vantar í önnur textasöfn, fyrst og fremst [Beygingarlýsingu íslensks nútímamáls (BÍN)](bin.arnastofnun.is/) og hins vegar [Íslenska nútímamálsorðabók (ISLEX)](https://islenskordabok.arnastofnun.is/).

4

​

5

Það má þó einnig nota til þess að setja inn eigin textaskjöl og bera innihald þeirra saman við BÍN og ISLEX, sem ætti t.a.m. að geta nýst við samansöfnun íðorða og annarra orða sem einkenna textann.

6

​

7

Tólið er notað á skipanalínu og uppsetning þess fer fram með því að keyra þessa skipun:

8

​

9

```

10

python setup.py

11

```

12

​

13

Við uppsetningu er notandi beðinn um inntak, sem segir til um hvaða staðværu (e. local) gagnagrunnar skuli settir upp.

14

​

15

```

16

============================================================

17

Hvaða gagnasöfn viltu setja upp?

18

============================================================1

# Orðtökutól/Lexicon Acquisition Tool

2

​

3

Orðtökutólið er ætlað til þess að safna saman orðum úr [Risamálheildinni](https://malheildir.arnastofnun.is/) sem vantar í önnur textasöfn, fyrst og fremst [Beygingarlýsingu íslensks nútímamáls (BÍN)](bin.arnastofnun.is/) og hins vegar [Íslenska nútímamálsorðabók (ISLEX)](https://islenskordabok.arnastofnun.is/).

4

​

5

Það má þó einnig nota til þess að setja inn eigin textaskjöl og bera innihald þeirra saman við BÍN og ISLEX, sem ætti t.a.m. að geta nýst við samansöfnun íðorða og annarra orða sem einkenna textann.

6

​

7

Tólið er notað á skipanalínu og uppsetning þess fer fram með því að keyra þessa skipun:

8

​

9

```

10

python setup.py

11

```

12

​

13

Við uppsetningu er notandi beðinn um inntak, sem segir til um hvaða staðværu (e. local) gagnagrunnar skuli settir upp.

14

​

15

```

16

============================================================

17

Hvaða gagnasöfn viltu setja upp?

18

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

Notandi er beðinn um inntak, sem ræður því hvers eðlis úttakið verður. Eftirfarandi úttök eru möguleg: 

FYRIR BÍN:
- Tíðnilistar á CSV formi þar sem allar lemmur sem ekki er að finna í Beygingarlýsingunni eru taldar upp ásamt tíðni þeirra í inntaksmálheildinni. 
- Tíðnilistar á FREQ formi þar sem allar lemmur sem ekki er að finna í Beygingarlýsingunni eru taldar upp ásamt tíðni þeirra, en jafnframt eru allar orðmyndir viðkomandi lemmu sem koma fyrir í inntaksmálheildinni taldar upp.  
- Tíðnilistar á CSV formi þar sem allar lemmur sem er ekki að finna í Beygingarlýsingunni eru taldar upp ásamt heildartíðni þeirra, en auk þess tíðni hverrar lemmu innan ákveðinnar gerðar texta (t.d. fréttir, stærðfræði eða fótbolti).
- Tíðnilistar á CSV formi þar sem allar orðmyndir sem ekki er að finna í Beygingarlýsingunni eru taldar upp ásamt tíðni þeirra í inntaksmálheildinni.
- Tíðnilistar á FREQ formi þar sem allar orðmyndir sem ekki er að finna í Beygingarlýsingunni eru taldar upp ásamt tíðni þeirra, en jafnframt eru allar lemmur viðkomandi lemmu sem koma fyrir í inntaksmálheildinni taldar upp. 

FYRIR ISLEX:
- Tíðnilistar á FREQ formi þar sem allar lemmur sem ekki er að finna í Nútímamálsorðabókinni eru taldar upp ásamt tíðni þeirra í inntaksmálheildinni. 
- Tíðnilistar á CSV formi þar sem allar lemmur sem er ekki að finna í Nútímamálsorðabókinni eru taldar upp ásamt heildartíðni þeirra, en auk þess tíðni hverrar lemmu innan ákveðinnar gerðar texta (t.d. fréttir, stærðfræði eða fótbolti). 

Ef um ómarkaða og ólemmaða inntaksmálheild á txt-formi er að ræða er aðeins í boði úttak þar sem allar orðmyndir sem ekki koma fyrir í viðeigandi gagnasami eru taldar upp ásamt tíðni þeirra. 

__Athugið að allt sem er inni í all_filters.txt er hunsað. Þar inni eru innsláttar- og stafsetningarvillur, erlend heiti, skammstafanir o.fl. Eðli málsins samkvæmt er sumt af því huglægu mati háð.__
