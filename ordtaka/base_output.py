from xml.etree import ElementTree as ET
from string import punctuation
import glob
from ordtaka.sql.sql_lookup import SQLDatabase, SQLiteQuery
from ordtaka.rmh_extractor import RmhWord, RmhExtractor
import csv

def lemma_output(rmh_folder, data):
    bin = SQLDatabase(db_name='dbs/bin_ordmyndir.db')
    islex = SQLDatabase(db_name='dbs/islex_lemmas.db')
    filters = SQLDatabase(db_name='dbs/filters.db')
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au']
    RMH = RmhExtractor(folder=str(rmh_folder))
    freqdic = {}
    print("Les inntaksskjöl")
    for word in RMH.extract(forms=False, lemmas=True, pos=True):
        try:
            if word.pos in pos_to_ignore:
                    continue
            # Ignore proper nouns
            if word.pos.startswith('n') and word.pos.endswith('s'):
                continue
            # Ignore if not only letters or letters and hyphen
            if (not all(i.isalpha() or i == '-' for i in word.lemma)):
                continue
            if len(word.lemma) < 3:
                continue
            # Ignore words that start with '[anyLetter?]-' or end with '-'
            if '-' in [word.lemma[0], word.lemma[1], word.lemma[-1]]:
                continue
            # Ignore unwanted words, such as names, foreign words, stopwords, abbreviations
            filter_query = SQLiteQuery(word.lemma,
                                       'filter',
                                       'FILTER_WORD_FORMS',
                                       cursor=filters.cursor)
            if filter_query.exists:
                continue
            else:
                if data == "ISLEX":
                    query = SQLiteQuery(word.lemma,'fletta','ISLEX_LEMMAS', cursor = islex.cursor)
                    query_lower = SQLiteQuery(word.lemma.lower(),'fletta','ISLEX_LEMMAS', cursor = islex.cursor)
                    if not query.exists and not query_lower.exists:
                        if word.lemma not in freqdic:
                            freqdic[word.lemma] = 1
                        else:
                            freqdic[word.lemma] += 1
                elif data == "BÍN":
                    query = SQLiteQuery(word.lemma,'word_form','BIN_WORD_FORMS', cursor = bin.cursor)                  
                    query_lower = SQLiteQuery(word.lemma.lower(),'word_form','BIN_WORD_FORMS', cursor = bin.cursor)
                    if not query.exists and not query_lower.exists:
                        if word.lemma not in freqdic:
                            freqdic[word.lemma] = 1
                        else:
                            freqdic[word.lemma] += 1
        except IndexError:
            continue
        except ET.ParseError:
            continue  
    print("Skrifar úttaksskjal")
    header = ['Orð', 'Tíðni']
    namefolder = rmh_folder.rpartition("/")[2]
    with open(namefolder+"_"+data+".csv", mode='w+') as outputfile:
        csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(header)
        for i in freqdic.items():
            csvwriter.writerow(i)        
    print("Úttaksskjal tilbúið")

def wordform_output(rmh_folder):
    bin = SQLDatabase(db_name='dbs/bin_ordmyndir.db')
    filters = SQLDatabase(db_name='dbs/filters.db')
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au']
    RMH = RmhExtractor(folder=str(rmh_folder))
    freqdic = {}
    print("Les inntaksskjöl")
    for word in RMH.extract(forms=True, lemmas=False, pos=True):
        try:
            if word.pos in pos_to_ignore:
                    continue
            # Ignore proper nouns
            if word.pos.startswith('n') and word.pos.endswith('s'):
                continue
            # Ignore if not only letters or letters and hyphen
            if (not all(i.isalpha() or i == '-' for i in word.word_form)):
                continue
            if len(word.word_form) < 3:
                continue
            # Ignore words that start with '[anyLetter?]-' or end with '-'
            if '-' in [word.word_form[0], word.word_form[1], word.word_form[-1]]:
                continue
            # Ignore unwanted words, such as names, foreign words, stopwords, abbreviations
            filter_query = SQLiteQuery(word.word_form,
                                       'filter',
                                       'FILTER_WORD_FORMS',
                                       cursor=filters.cursor)
            if filter_query.exists:
                continue
            else:    
                query = SQLiteQuery(word.word_form,'word_form','BIN_WORD_FORMS', cursor = bin.cursor)                  
                query_lower = SQLiteQuery(word.word_form.lower(),'word_form','BIN_WORD_FORMS', cursor = bin.cursor)
                if not query.exists and not query_lower.exists:
                    if word.word_form not in freqdic:
                        freqdic[word.word_form] = 1
                    else:
                        freqdic[word.word_form] += 1
        except IndexError:
            continue
        except ET.ParseError:
            continue  
    print("Skrifar úttaksskjal")
    header = ['Orð', 'Tíðni']
    namefolder = rmh_folder.rpartition("/")[2]
    with open(namefolder+"_BIN.csv", mode='w+') as outputfile:
        csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(header)
        for i in freqdic.items():
            csvwriter.writerow(i)        
    print("Úttaksskjal tilbúið")