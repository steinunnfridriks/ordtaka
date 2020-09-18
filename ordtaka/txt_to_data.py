import glob
import csv
from ordtaka.sql.sql_lookup import SQLDatabase, SQLiteQuery
import re

def txt_corpus_freq(folder, corpus):
    bin = SQLDatabase(db_name='dbs/bin_ordmyndir.db')
    islex = SQLDatabase(db_name='dbs/islex_lemmas.db')
    filters = SQLDatabase(db_name='dbs/filters.db')
    txt_files = glob.glob(f'../../corpora/'+folder+'/**/*.txt', recursive=True)
    outdict = {}
    
    i = 1
    for file in txt_files:
        with open(file, 'r', encoding='utf-8') as content:
            f = content.read()
            words = f.split()
            for w in words:
                if w[-1] == '-':
                    continue
                if w[0] == '-':
                    continue
                if (not all(i.isalpha() or i == '-' for i in w)):
                    continue
                filter_query = SQLiteQuery(w,'filter','FILTER_WORD_FORMS', cursor=filters.cursor)
                if filter_query.exists:
                    continue
                else:
                    if corpus == "ISLEX":
                        query = SQLiteQuery(w,'fletta','ISLEX_LEMMAS', cursor = islex.cursor)
                        query_lower = SQLiteQuery(w.lower(),'fletta','ISLEX_LEMMAS', cursor = islex.cursor)
                        if not query.exists and not query_lower.exists:
                            if len(w) > 1:
                                if w in outdict:
                                    outdict[w] += 1
                                else:
                                    outdict[w] = 1
                    elif corpus == "BÍN":
                        query = SQLiteQuery(w,'word_form','BIN_WORD_FORMS', cursor = bin.cursor)                  
                        query_lower = SQLiteQuery(w.lower(),'word_form','BIN_WORD_FORMS', cursor = bin.cursor)
                        if not query.exists and not query_lower.exists:
                            if len(w) > 1:
                                if w in outdict:
                                    outdict[w] += 1
                                else:
                                    outdict[w] = 1
            print("Skjal ", i, "af ", len(txt_files))
            i += 1
    print("Skrifar úttaksskjal")
    header = ['Orð', 'Tíðni']
    with open("txtcorpus_"+str(corpus)+".csv", 'w', encoding='utf-8') as out:
        csvwriter = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(header)
        for i in sorted(outdict.items(), key=lambda x: x[1], reverse=True):
            csvwriter.writerow(i)
            
    print("Úttaksskjal tilbúið")