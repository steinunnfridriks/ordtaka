from ordtaka.find_texttype_freqs import texttype_freqs
from ordtaka.compare_rmh_islex import CompareRmhIslex
from ordtaka.compare_rmh_bin import CompareRmhBIN
from ordtaka.txt_to_data import txt_corpus_freq 
from ordtaka.base_output import lemma_output, wordform_output
from ordtaka.lemmabase_wordforms import lemmabase_wordforms
import os.path
from os import path

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
        choose_corpus()
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
        choose_data()
    return data

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
        choose_form()
    return base

def islex_choices():
    print("""
        ============================================================
        Veldu eitt af eftirfarandi: Tíðnilisti (lemmur og tíðni 
        þeirra) eða textagerðir (lemmur með tíðni flokkaðar eftir 
        textagerð). Athugið að textagerðir nýtast best með stökum 
        möppum úr RMH. 
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
        islex_choices()
    return options

def bin_lemma_choices():
    print("""
        ============================================================
        Veldu eitt af eftirfarandi: Tíðnilisti (lemmur og tíðni þeirra),
        lemmur með öllum mögulegum orðmyndum sínum eða textagerðir 
        (lemmur með tíðni flokkaðar eftir textagerð). 
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
        bin_lemma_choices()
    return options

def bin_wordform_choices():
    print("""
        ============================================================
        Veldu eitt af eftirfarandi: Tíðnilisti (orðmyndir og tíðni 
        þeirra) eða orðmyndir með öllum mögulegum lemmum sínum. 
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
        bin_wordform_choices()
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
        choose_rmhpart()
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
        choose_rmhdir()
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
        print(txtcorpus + " valin")
    else:
        print("Þessi slóð er ekki til. Reyndu aftur.")
        txt_corpus()

    data = choose_data()
    if data == "1":
        txt_corpus_freq(txtcorpus, "BÍN")
    elif data == "2": 
        txt_corpus_freq(txtcorpus, "ISLEX")  

def tei_corpus():

    teicorpus = input("""
    ============================================================
    Sláðu inn nafn möppunnar sem inniheldur málheildina.
    ============================================================
    Athugaðu að ef um undirmöppu er að ræða þarf að slá inn fulla 
    slóð hennar, þ.e. teimalheild/undirmappa.
    ============================================================
    """)
    print(teicorpus + " valin")
     
    data = choose_data()
    if data == "1":
        base = choose_form()        
        if base == "1":
            options = bin_lemma_choices()
            if options == "1":
                lemma_output("corpora/"+str(teicorpus)+"/**", "BÍN")
            elif options == "2":
                lemmabase_wordforms("corpora/"+str(teicorpus))
            elif options == "3":
                texttype_freqs(data, str(teicorpus)+"/**")
        elif base == "2":
            options = bin_wordform_choices()
            if options == "1":
                wordform_output("corpora/"+str(teicorpus)+"/**")
            elif options == "2":
                c = CompareRmhBIN(rmh_folder='corpora'+str(teicorpus))
                c.write_to_file()     
    elif data == "2": 
        options = islex_choices()
        if options == "1":
            lemma_output("corpora/"+str(teicorpus)+"/**", "ISLEX")
        elif options == "2":
            texttype_freqs(data, str(teicorpus)+"/**") 

def RMH_corpus():
    rmhpart = choose_rmhpart()

    if rmhpart == "1":
        data = choose_data()
        if data == "1":
            base = choose_form()
            if base == "1":
                options = bin_lemma_choices()
                if options == "1":
                    lemma_output("corpora/RMH/**/**/", "BÍN")
                elif options == "2":
                    lemmabase_wordforms("corpora/RMH/**/**/")
                elif options == "3":
                    texttype_freqs(data, "RMH/**/**/")
            
            elif base == "2":
                options = bin_wordform_choices()
                if options == "1":
                    wordform_output("corpora/RMH/**/**/")
                elif options == "2":
                    c = CompareRmhBIN(rmh_folder='corpora/RMH/**/**/')
                    c.write_to_file()  

        elif data == "2": 
            options = islex_choices()
            if options == "1":
                lemma_output("corpora/RMH/**/**/", "ISLEX")
            elif options == "2":
                texttype_freqs(data, "RMH/**/**/") 

    elif rmhpart == "2":
        data = choose_data()
        if data == "1":
            base = choose_form()
            if base == "1":
                options = bin_lemma_choices()
                if options == "1":
                    lemma_output("corpora/RMH/CC_BY/**/", "BÍN")
                elif options == "2":
                    lemmabase_wordforms("corpora/RMH/CC_BY/**/")
                elif options == "3":
                    texttype_freqs(data, "RMH/CC_BY/**/")
            
            elif base == "2":
                options = bin_wordform_choices()
                if options == "1":
                    wordform_output("corpora/RMH/CC_BY/**/")
                elif options == "2": 
                    c = CompareRmhBIN(rmh_folder='corpora/RMH/CC_BY/**/')
                    c.write_to_file()  

        elif data == "2": 
            options = islex_choices()
            if options == "1":
                lemma_output("corpora/RMH/CC_BY/**/", "ISLEX") 
            elif options == "2":
                texttype_freqs(data, "RMH/CC_BY/**/")
    
    elif rmhpart == "3":
        data = choose_data()
        if data == "1":
            base = choose_form()
            if base == "1":
                options = bin_lemma_choices()
                if options == "1":
                    lemma_output("corpora/RMH/MIM/**/", "BÍN")
                elif options == "2":
                    lemmabase_wordforms("corpora/RMH/MIM/**/")
                elif options == "3":
                    texttype_freqs(data, "RMH/MIM/**/") 

            elif base == "2":
                options = bin_wordform_choices()
                if options == "1":
                    wordform_output("corpora/RMH/MIM/**/")
                elif options == "2":
                    c = CompareRmhBIN(rmh_folder='corpora/RMH/MIM/**/')
                    c.write_to_file()   
        elif data == "2": 
            options = islex_choices()
            if options == "1":
                lemma_output("corpora/RMH/MIM/**/", "ISLEX")
            elif options == "2":
                texttype_freqs(data, "RMH/MIM/**/") 
    
    elif rmhpart == "4":
        rmhmappa = choose_rmhdir()
        data = choose_data()

        if data == "1":
            base = choose_form()
            if base == "1":
                options = bin_lemma_choices()
                if options == "1":
                    lemma_output("corpora/"+str(rmhmappa), "BÍN") 
                elif options == "2":
                    lemmabase_wordforms("corpora/"+str(rmhmappa))
                elif options == "3":
                    texttype_freqs(data, rmhmappa)
            
            elif base == "2":
                options = bin_wordform_choices()
                if options == "1":
                    wordform_output("corpora/"+str(rmhmappa))
                elif options == "2":
                    c = CompareRmhBIN(rmh_folder='corpora/'+str(rmhmappa))
                    c.write_to_file()  

        elif data == "2": 
            options = islex_choices()
            if options == "1":
                lemma_output("corpora/"+str(rmhmappa), "ISLEX")
            elif options == "2":
                texttype_freqs(data, rmhmappa) 


corpus = choose_corpus()

if corpus == "3":
    txt_corpus()
elif corpus == "2":
    tei_corpus()
elif corpus == "1":
    RMH_corpus()