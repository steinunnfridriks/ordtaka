"""
This script provides the main functionality of the Lexicon Acquisition
Tool. Using a command line interface, simply run this script and follow
the instructions. An output example is presented with every option in
the run-time instructions.
"""


from ordtaka.find_texttype_freqs import texttype_freqs
from ordtaka.compare_rmh_islex import CompareRmhIslex
from ordtaka.compare_rmh_bin import CompareRmhBIN
from ordtaka.txt_to_data import txt_corpus_freq
from ordtaka.base_output import lemma_output, wordform_output
from ordtaka.lemmabase_wordforms import lemmabase_wordforms
import os.path
from os import path
import glob

def choose_corpus():
    print("""
        ============================================================
        Veldu þá málheild sem þú vilt nota sem inntak.
        ============================================================
        Stimplaðu inn þá tölu sem vísar til málheildarinnar og ýttu
        á ENTER.
        ============================================================
        """)

    corpus = input("""
        (1) Risamálheild
        (2) Önnur málheild á tei-sniði
        (3) Önnur málheild á txt-sniði
        """)

    if corpus == "1":
        print("Risamálheild valin")
    elif corpus == "2":
        print("Málheild á tei-sniði valin")
    elif corpus == "3":
        print("Málheild á txt-sniði valin")
    else:
        print("Þetta er ekki gildur valmöguleiki, vinsamlegast reyndu aftur")
        corpus = choose_corpus()
        if corpus == "3":
            txt_corpus()
        elif corpus == "2":
            tei_corpus()
        elif corpus == "1":
            RMH_corpus()
    return corpus

def choose_data():
    print("""
        ============================================================
        Veldu þann gagnagrunn sem bera á saman við málheildina.
        ============================================================
        Stimplaðu inn þá tölu sem vísar til gagnagrunnsins og ýttu
        á ENTER.
        ============================================================
        """)

    data = input("""
        (1) Beygingarlýsing íslensks nútímamáls (BÍN)
        (2) Nútímamálsorðabókin (ISLEX)
        """)

    if data == "1":
        print("Beygingarlýsing íslensks nútímamáls valin.")
    elif data == "2":
        print("Nútímamálsorðabók valin.")
    else:
        print("Þetta er ekki gildur valmöguleiki, vinsamlegast reyndu aftur")
        data = choose_data()
    return data

def choose_propnames():
    print("""
        ============================================================
        Viltu hunsa sérnöfn í niðurstöðunum?
        ============================================================
        Stimplaðu inn þá tölu sem vísar til valmöguleikans og ýttu
        á ENTER.
        Þetta getur verið gagnlegt vegna þess magns af sérnöfnum sem
        annars kemur fram í niðurstöðunum.
        Athugið að þessi valmöguleiki gildir aðeins fyrir Risa-
        málheildina eða aðrar málheildir sem eru markaðar á sama hátt.
        ============================================================
        """)

    prop_names = input("""
        (1) Já ég vil hunsa sérnöfn
        (2) Nei ég vil ekki hunsa sérnöfn
        """)

    if prop_names == "1":
        print("Sérnöfn hunsuð.")
    elif prop_names == "2":
        print("Sérnöfnum haldið.")
    else:
        print("Þetta er ekki gildur valmöguleiki, vinsamlegast reyndu aftur")
        prop_names = choose_propnames()
    return prop_names

def choose_form():
    print("""
        ============================================================
        Veldu það grunnform sem nota skal (orðmyndir eða lemmur).
        ============================================================
        Stimplaðu inn þá tölu sem vísar til formsins og ýttu
        á ENTER.
        ============================================================
        """)
    base = input("""
        (1) Lemmur
        (2) Orðmyndir
        """)

    if base == "1":
        print("Lemmur valdar")
    elif base == "2":
        print("Orðmyndir valdar")
    else:
        print("Þetta er ekki gildur valmöguleiki, vinsamlegast reyndu aftur")
        base = choose_form()
    return base

def islex_choices():
    print("""
        ============================================================
        Veldu eitt af eftirfarandi:

        Tíðnilisti (lemmur og tíðni þeirra) á CSV sniði.
        - Dæmi: Vera, 100. Gera, 90. Tala, 40.

        Textagerðir (lemmur með tíðni flokkaðar eftir textagerð).
        - Dæmi: Vera, heildartíðni 100, fréttir 50, stærðfræði 50.

        Athugið að textagerðir nýtast best með stökum möppum úr RMH.
        ============================================================
        Stimplaðu inn þá tölu sem vísar til valmöguleikans og ýttu
        á ENTER.
        ============================================================
        """)
    options = input("""
        (1) Tíðnilisti
        (2) Textagerðir
        """)

    if options == "1":
        print("Tíðnilisti valinn")
    elif options == "2":
        print("Textagerðir valdar")
    else:
        print("Þetta er ekki gildur valmöguleiki, vinsamlegast reyndu aftur")
        options = islex_choices()
    return options

def bin_lemma_choices():
    print("""
        ============================================================
        Veldu eitt af eftirfarandi:

        Tíðnilisti (lemmur og tíðni þeirra)
        - Dæmi: Vera, 100. Gera, 90. Tala, 40.

        Lemmur með öllum mögulegum orðmyndum sínum
        - Dæmi: Vera, 100 [orðmyndir: er, var, ert, eruð]

        Textagerðir (lemmur með tíðni flokkaðar eftir textagerð)
        - Dæmi: Vera, heildartíðni 100, fréttir 50, stærðfræði 50.

        Athugið að textagerðir nýtast best með stökum möppum úr RMH.
        ============================================================
        Stimplaðu inn þá tölu sem vísar til valmöguleikans og ýttu
        á ENTER.
        ============================================================
        """)
    options = input("""
        (1) Tíðnilisti
        (2) Lemmur með orðmyndum
        (3) Textagerðir
        """)

    if options == "1":
        print("Tíðnilisti valinn")
    elif options == "2":
        print("Lemmur með orðmyndum valdar")
    elif options == "3":
        print("Textagerðir valdar")
    else:
        print("Þetta er ekki gildur valmöguleiki, vinsamlegast reyndu aftur")
        options = bin_lemma_choices()
    return options

def bin_wordform_choices():
    print("""
        ============================================================
        Veldu eitt af eftirfarandi:

        Tíðnilisti (orðmyndir og tíðni þeirra)
        - Dæmi: Er, 100. Geri, 60. Talaði, 40.

        Orðmyndir með öllum mögulegum lemmum sínum
        - Dæmi: Banka, 70 [lemmur: banka, banki]

        ============================================================
        Stimplaðu inn þá tölu sem vísar til valmöguleikans og ýttu
        á ENTER.
        ============================================================
        """)
    options = input("""
        (1) Tíðnilisti
        (2) Orðmyndir með lemmum
        """)

    if options == "1":
        print("Tíðnilisti valinn")
    elif options == "2":
        print("Orðmyndir með lemmum valdar")
    else:
        print("Þetta er ekki gildur valmöguleiki, vinsamlegast reyndu aftur")
        options = bin_wordform_choices()
    return options

def choose_rmhpart():
    print("""
        ============================================================
        Veldu hvaða hluta Risamálheildarinnar skuli nota sem inntak.
        Valmöguleikarnir eru: Risamálheildin í heild sinni (mun taka
        langan tíma í keyrslu), opni hluti Risamálheildarinnar (allar
        möppur innan CC_BY hlutans), lokaði hluti Risamálheildarinnar
        (allar möppur innan MÍM) eða stök undirmappa (t.d. Vísir).
        ============================================================
        Stimplaðu inn þá tölu sem vísar til valmöguleikans og ýttu
        á ENTER.
        ============================================================
        """)
    rmhpart = input("""
        (1) Öll RMH
        (2) CC_BY
        (3) MÍM
        (4) Stök mappa
        """)

    if rmhpart == "1":
        print("Öll Risamálheildin valin")
    elif rmhpart == "2":
        print("Opni hluti Risamálheildarinnar valinn (CC_BY)")
    elif rmhpart == "3":
        print("Lokaði hluti Risamálheildarinnar valinn (MÍM)")
    elif rmhpart == "4":
        print("Stök mappa innan Risamálheildarinnar valin")
    else:
        print("Þetta er ekki gildur valmöguleiki, vinsamlegast reyndu aftur")
        rmhpart = choose_rmhpart()
    return rmhpart

def choose_rmhdir():
    rmhmappa = input("""
        ============================================================
        Sláðu inn fulla slóð möppunnar innan Risamálheildarinnar.
        ============================================================
        Athugaðu að það þarf að að slá inn slóðina á eftirfarandi
        sniðmáti: RMH/hluti/undirmappa. Ef velja á Vísi væri slóðin
        RMH/CC_BY/visir.
        ============================================================
    """)

    if path.exists("corpora/"+str(rmhmappa)):
        print(rmhmappa + " valin")
    else:
        print("Þessi slóð er ekki til. Reyndu aftur.")
        rmhmappa = choose_rmhdir()
    return rmhmappa

def txt_corpus():
    txtcorpus = input("""
    ============================================================
    Sláðu inn nafn möppunnar sem inniheldur málheildina.
    ============================================================
    Athugaðu að ef vinna á með undirmöppu innan málheildarinnar
    þarf að slá inn alla slóðina, þ.e. txtmalheild/undirmappa.
    ============================================================
    """)
    if path.exists("corpora/"+str(txtcorpus)):
        f = glob.glob("corpora/"+str(txtcorpus)+'/**', recursive=True)
        files = [file for file in f if file.endswith(".txt")]
        if len(files) >= 1:
            if len(files) == sum(1 for i in f if i.endswith('.txt')):
                print(txtcorpus + " valin")
        else:
            print("Þessi málheild er ekki öll á txt-sniði. Reyndu aftur.")
            txtcorpus = txt_corpus()
    else:
        print("Þessi slóð er ekki til. Reyndu aftur.")
        txtcorpus = txt_corpus()

    data = choose_data()
    txt_corpus_freq(str(txtcorpus), data)

def tei_corpus():

    teicorpus = input("""
    ============================================================
    Sláðu inn nafn möppunnar sem inniheldur málheildina.
    ============================================================
    Athugaðu að ef um undirmöppu er að ræða þarf að slá inn fulla
    slóð hennar, þ.e. teimalheild/undirmappa.
    ============================================================
    """)
    if path.exists("corpora/"+str(teicorpus)):
        f = glob.glob("corpora/"+str(teicorpus)+'/**', recursive=True)
        files = [file for file in f if file.endswith(".xml")]
        if len(files) >= 1:
            if len(files) == sum(1 for i in f if i.endswith('.xml')):
                print(teicorpus + " valin")
        else:
            print("Þessi málheild er ekki öll á tei-sniði. Reyndu aftur.")
            teicorpus = tei_corpus()
    else:
        print("Þessi slóð er ekki til. Reyndu aftur.")
        teicorpus = tei_corpus()

    prop_names = choose_propnames()
    data = choose_data()
    if prop_names == "1":   #ignore prop names
        if data == "1":
            base = choose_form()
            if base == "1":
                options = bin_lemma_choices()
                if options == "1":
                    lemma_output("corpora/"+str(teicorpus)+"/**", prop_names=False)
                elif options == "2":
                    lemmabase_wordforms("corpora/"+str(teicorpus), prop_names=False)
                elif options == "3":
                    texttype_freqs(data, 'corpora/'+str(teicorpus)+"/**", prop_names=False)
            elif base == "2":
                options = bin_wordform_choices()
                if options == "1":
                    wordform_output("corpora/"+str(teicorpus)+"/**", prop_names=False)
                elif options == "2":
                    c = CompareRmhBIN(rmh_folder='corpora/'+str(teicorpus)+'/**', proper_nouns=False)
                    c.write_to_file()
        elif data == "2":
            options = islex_choices()
            if options == "1":
                c = CompareRmhIslex(rmh_folder='corpora/'+str(teicorpus), proper_nouns=False)
                c.write_to_file()
            elif options == "2":
                texttype_freqs(data, 'corpora/'+str(teicorpus)+"/**", prop_names=False)

    elif prop_names == "2":
        if data == "1":
            base = choose_form()
            if base == "1":
                options = bin_lemma_choices()
                if options == "1":
                    lemma_output("corpora/"+str(teicorpus)+"/**", prop_names=True)
                elif options == "2":
                    lemmabase_wordforms("corpora/"+str(teicorpus), prop_names=True)
                elif options == "3":
                    texttype_freqs(data, 'corpora/'+str(teicorpus)+"/**", prop_names=True)
            elif base == "2":
                options = bin_wordform_choices()
                if options == "1":
                    wordform_output("corpora/"+str(teicorpus)+"/**", prop_names=True)
                elif options == "2":
                    c = CompareRmhBIN(rmh_folder='corpora/'+str(teicorpus)+'/**', proper_nouns=True)
                    c.write_to_file()
        elif data == "2":
            options = islex_choices()
            if options == "1":
                c = CompareRmhIslex(rmh_folder='corpora/'+str(teicorpus), proper_nouns=True)
                c.write_to_file()
            elif options == "2":
                texttype_freqs(data, 'corpora/'+str(teicorpus)+"/**", prop_names=True)

def RMH_corpus():
    rmhpart = choose_rmhpart()
    prop_names = choose_propnames()

    if rmhpart == "1":
        if prop_names == "1":
            data = choose_data()
            if data == "1":
                base = choose_form()
                if base == "1":
                    options = bin_lemma_choices()
                    if options == "1":
                        lemma_output("corpora/RMH/**/**/", prop_names=False)
                    elif options == "2":
                        lemmabase_wordforms("corpora/RMH/**/**/", prop_names=False)
                    elif options == "3":
                        texttype_freqs(data, "corpora/RMH/**/**/", prop_names=False)

                elif base == "2":
                    options = bin_wordform_choices()
                    if options == "1":
                        wordform_output("corpora/RMH/**/**/", prop_names=False)
                    elif options == "2":
                        c = CompareRmhBIN(rmh_folder='corpora/RMH/**/**/', proper_nouns=False)
                        c.write_to_file()

            elif data == "2":
                options = islex_choices()
                if options == "1":
                    c = CompareRmhIslex(rmh_folder='corpora/RMH/**/**/', proper_nouns=False)
                    c.write_to_file()
                elif options == "2":
                    texttype_freqs(data, "corpora/RMH/**/**/", prop_names=False)

        elif prop_names== "2":
            data = choose_data()
            if data == "1":
                base = choose_form()
                if base == "1":
                    options = bin_lemma_choices()
                    if options == "1":
                        lemma_output("corpora/RMH/**/**/", prop_names=True)
                    elif options == "2":
                        lemmabase_wordforms("corpora/RMH/**/**/", prop_names=True)
                    elif options == "3":
                        texttype_freqs(data, "corpora/RMH/**/**/", prop_names=True)

                elif base == "2":
                    options = bin_wordform_choices()
                    if options == "1":
                        wordform_output("corpora/RMH/**/**/", prop_names=True)
                    elif options == "2":
                        c = CompareRmhBIN(rmh_folder='corpora/RMH/**/**/', proper_nouns=True)
                        c.write_to_file()

            elif data == "2":
                options = islex_choices()
                if options == "1":
                    c = CompareRmhIslex(rmh_folder='corpora/RMH/**/**/', proper_nouns=True)
                    c.write_to_file()
                elif options == "2":
                    texttype_freqs(data, "corpora/RMH/**/**/", prop_names=True)

    elif rmhpart == "2":
        if prop_names == "1":
            data = choose_data()
            if data == "1":
                base = choose_form()
                if base == "1":
                    options = bin_lemma_choices()
                    if options == "1":
                        lemma_output("corpora/RMH/CC_BY/**/", prop_names=False)
                    elif options == "2":
                        lemmabase_wordforms("corpora/RMH/CC_BY/**/", prop_names=False)
                    elif options == "3":
                        texttype_freqs(data, "corpora/RMH/CC_BY/**/", prop_names=False)

                elif base == "2":
                    options = bin_wordform_choices()
                    if options == "1":
                        wordform_output("corpora/RMH/CC_BY/**/", prop_names=False)
                    elif options == "2":
                        c = CompareRmhBIN(rmh_folder='corpora/RMH/CC_BY/**/', proper_nouns=False)
                        c.write_to_file()

            elif data == "2":
                options = islex_choices()
                if options == "1":
                    c = CompareRmhIslex(rmh_folder='corpora/RMH/CC_BY/**/', proper_nouns=False)
                    c.write_to_file()
                elif options == "2":
                    texttype_freqs(data, "corpora/RMH/CC_BY/**/", prop_names=False)

        elif prop_names=="2":
            data = choose_data()
            if data == "1":
                base = choose_form()
                if base == "1":
                    options = bin_lemma_choices()
                    if options == "1":
                        lemma_output("corpora/RMH/CC_BY/**/", prop_names=True)
                    elif options == "2":
                        lemmabase_wordforms("corpora/RMH/CC_BY/**/", prop_names=True)
                    elif options == "3":
                        texttype_freqs(data, "corpora/RMH/CC_BY/**/", prop_names=True)

                elif base == "2":
                    options = bin_wordform_choices()
                    if options == "1":
                        wordform_output("corpora/RMH/CC_BY/**/", prop_names=True)
                    elif options == "2":
                        c = CompareRmhBIN(rmh_folder='corpora/RMH/CC_BY/**/', proper_nouns=True)
                        c.write_to_file()

            elif data == "2":
                options = islex_choices()
                if options == "1":
                    c = CompareRmhIslex(rmh_folder='corpora/RMH/CC_BY/**/', proper_nouns=True)
                    c.write_to_file()
                elif options == "2":
                    texttype_freqs(data, "corpora/RMH/CC_BY/**/", prop_names=True)

    elif rmhpart == "3":
        if prop_names=="1":
            data = choose_data()
            if data == "1":
                base = choose_form()
                if base == "1":
                    options = bin_lemma_choices()
                    if options == "1":
                        lemma_output("corpora/RMH/MIM/**/", prop_names=False)
                    elif options == "2":
                        lemmabase_wordforms("corpora/RMH/MIM/**/", prop_names=False)
                    elif options == "3":
                        texttype_freqs(data, "corpora/RMH/MIM/**/", prop_names=False)

                elif base == "2":
                    options = bin_wordform_choices()
                    if options == "1":
                        wordform_output("corpora/RMH/MIM/**/", prop_names=False)
                    elif options == "2":
                        c = CompareRmhBIN(rmh_folder='corpora/RMH/MIM/**/', proper_nouns=False)
                        c.write_to_file()
            elif data == "2":
                options = islex_choices()
                if options == "1":
                    c = CompareRmhIslex(rmh_folder='corpora/RMH/MIM/**/', proper_nouns=False)
                    c.write_to_file()
                elif options == "2":
                    texttype_freqs(data, "corpora/RMH/MIM/**/", prop_names=False)

        elif prop_names=="2":
            data = choose_data()
            if data == "1":
                base = choose_form()
                if base == "1":
                    options = bin_lemma_choices()
                    if options == "1":
                        lemma_output("corpora/RMH/MIM/**/", prop_names=True)
                    elif options == "2":
                        lemmabase_wordforms("corpora/RMH/MIM/**/", prop_names=True)
                    elif options == "3":
                        texttype_freqs(data, "corpora/RMH/MIM/**/", prop_names=True)

                elif base == "2":
                    options = bin_wordform_choices()
                    if options == "1":
                        wordform_output("corpora/RMH/MIM/**/", prop_names=True)
                    elif options == "2":
                        c = CompareRmhBIN(rmh_folder='corpora/RMH/MIM/**/', proper_nouns=True)
                        c.write_to_file()
            elif data == "2":
                options = islex_choices()
                if options == "1":
                    c = CompareRmhIslex(rmh_folder='corpora/RMH/MIM/**/', proper_nouns=True)
                    c.write_to_file()
                elif options == "2":
                    texttype_freqs(data, "corpora/RMH/MIM/**/", prop_names=True)

    elif rmhpart == "4":
        prop_names = choose_propnames()
        rmhmappa = choose_rmhdir()
        data = choose_data()
        if prop_names=="1":
            if data == "1":
                base = choose_form()
                if base == "1":
                    options = bin_lemma_choices()
                    if options == "1":
                        lemma_output("corpora/"+str(rmhmappa), prop_names=False)
                    elif options == "2":
                        lemmabase_wordforms("corpora/"+str(rmhmappa), prop_names=False)
                    elif options == "3":
                        texttype_freqs(data, 'corpora/'+str(rmhmappa), prop_names=False)

                elif base == "2":
                    options = bin_wordform_choices()
                    if options == "1":
                        wordform_output("corpora/"+str(rmhmappa), prop_names=False)
                    elif options == "2":
                        c = CompareRmhBIN(rmh_folder='corpora/'+str(rmhmappa), proper_nouns=False)
                        c.write_to_file()

            elif data == "2":
                options = islex_choices()
                if options == "1":
                    c = CompareRmhIslex(rmh_folder='corpora/'+str(rmhmappa), proper_nouns=False)
                    c.write_to_file()
                elif options == "2":
                    texttype_freqs(data, 'corpora/'+str(rmhmappa), prop_names=False)

        elif prop_names=="2":
            if data == "1":
                base = choose_form()
                if base == "1":
                    options = bin_lemma_choices()
                    if options == "1":
                        lemma_output("corpora/"+str(rmhmappa), prop_names=True)
                    elif options == "2":
                        lemmabase_wordforms("corpora/"+str(rmhmappa), prop_names=True)
                    elif options == "3":
                        texttype_freqs(data, 'corpora/'+str(rmhmappa), prop_names=True)

                elif base == "2":
                    options = bin_wordform_choices()
                    if options == "1":
                        wordform_output("corpora/"+str(rmhmappa), prop_names=True)
                    elif options == "2":
                        c = CompareRmhBIN(rmh_folder='corpora/'+str(rmhmappa), proper_nouns=True)
                        c.write_to_file()

            elif data == "2":
                options = islex_choices()
                if options == "1":
                    c = CompareRmhIslex(rmh_folder='corpora/'+str(rmhmappa), proper_nouns=True)
                    c.write_to_file()
                elif options == "2":
                    texttype_freqs(data, 'corpora/'+str(rmhmappa), prop_names=True)


corpus = choose_corpus()

if corpus == "3":
    txt_corpus()
elif corpus == "2":
    tei_corpus()
elif corpus == "1":
    RMH_corpus()
