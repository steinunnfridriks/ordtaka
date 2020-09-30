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

Notandi er beðinn um inntak, sem ræður því hvers eðlis úttakið verður. Athugið að til þess að forritið nefni úttaksskrárnar rétt er mikilvægt að inntaksmálheildir séu vistaðar á sama hátt og er gert í sýnismöppunum hér. Með öðrum orðum þarf að vista Risamálheildina innan aðalmöppunnar corpora og undirmöppunnar RMH, undir tveimur aðskildum möppum sem heita [CC_BY](https://repository.clarin.is/repository/xmlui/handle/20.500.12537/33) og [MIM](https://repository.clarin.is/repository/xmlui/handle/20.500.12537/41). Ef um aðrar málheildir er að ræða þarf að vista þær undir aðalmöppunni corpora. Eftirfarandi úttök eru möguleg: 

FYRIR BÍN:
- Tíðnilistar á CSV formi þar sem allar lemmur sem ekki er að finna í Beygingarlýsingunni eru taldar upp ásamt tíðni þeirra í inntaksmálheildinni. Þetta má nýta til þess að ákveða hvaða orð koma til greina að bæta við í orðabækur og -söfn.
- Tíðnilistar á CSV formi þar sem allar orðmyndir sem ekki er að finna í Beygingarlýsingunni eru taldar upp ásamt tíðni þeirra í inntaksmálheildinni. Þetta má nýta til þess að ákveða hvaða orð koma til greina að bæta við í orðabækur og -söfn.
- Tíðnilista á FREQ formi þar sem allar lemmur sem ekki er að finna í Beygingarlýsingunni eru taldar upp ásamt tíðni þeirra, en jafnframt eru allar orðmyndir viðkomandi lemmu sem koma fyrir taldar upp. Nýtist til að kanna hvort tiltekin orðmynd er mun algengari en aðrar og þar með hvort orðið tilheyri einkum ákveðnu orðtaki.
- Tíðnilistar á FREQ formi þar sem allar orðmyndir sem ekki er að finna í Beygingarlýsingunni eru taldar upp ásamt tíðni þeirra, en jafnframt eru allar lemmur viðkomandi orðmyndar sem koma fyrir taldar upp. Veitir upplýsingar um hvort tiltekin orðmynd getur tilheyrt fleiri en einum orðflokki og hvort sjálfvirk lemmun skili réttum niðurstöðum.
- Tíðnilistar á CSV formi þar sem allar lemmur sem er ekki að finna í Beygingarlýsingunni eru taldar upp ásamt heildartíðni þeirra, en auk þess tíðni hverrar lemmu innan ákveðinnar gerðar texta (t.d. fréttir, stærðfræði eða fótbolti). Má nýta við smíði íðorðasafna. 

FYRIR ISLEX:
- Tíðnilistar á FREQ formi þar sem allar lemmur sem ekki er að finna í Nútímamálsorðabókinni eru taldar upp ásamt tíðni þeirra í inntaksmálheildinni. 
- Tíðnilistar á CSV formi þar sem allar lemmur sem er ekki að finna í Nútímamálsorðabókinni eru taldar upp ásamt heildartíðni þeirra, en auk þess tíðni hverrar lemmu innan ákveðinnar gerðar texta (t.d. fréttir, stærðfræði eða fótbolti). 

Ef um ómarkaða og ólemmaða inntaksmálheild á txt-formi er að ræða er aðeins í boði úttak þar sem allar orðmyndir sem ekki koma fyrir í viðeigandi gagnasafni eru taldar upp ásamt tíðni þeirra. 

__Athugið að allt sem er inni í all_filters.txt er hunsað. Þar inni eru innsláttar- og stafsetningarvillur, erlend heiti, skammstafanir o.fl. Eðli málsins samkvæmt er sumt af því huglægu mati háð.__

__Ef upp koma villur eða vandamál við notkun Orðtökutólsins má hafa samband við Steinunni Rut Friðriksdóttur (srf2@hi.is) eða Atla Jasonarson (atlijas@simnet.is)__ 
