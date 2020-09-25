from string import punctuation
import xml.etree.ElementTree as ET
import glob
import csv
from ordtaka.sql.sql_lookup import SQLDatabase, SQLiteQuery
from progress.bar import IncrementalBar
import sys


def texttype_freqs(corpus, folder, prop_names):
    bin = SQLDatabase(db_name='databases/bin_ordmyndir.db')
    islex = SQLDatabase(db_name='databases/islex_lemmas.db')
    filters = SQLDatabase(db_name='databases/filters.db')
    
    print("Les skjöl")
    xml_files = glob.glob(folder+'/**/*.xml', recursive=True)

    alltexttypes = []
    freqdic1 = {}
    freqdic2 = {}
    filebar = IncrementalBar('Inntaksskjöl lesin', max = len(xml_files))
    for file in xml_files:
        with open(file, 'r', encoding='utf-8') as content:
            try:
                tree = ET.parse(content)
                root = tree.getroot() 
                textClass = root[0][2][0][0][0][0]
                texttype = textClass.text
                if texttype not in alltexttypes:
                    alltexttypes.append(texttype)
                pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au']
                for word in tree.iter():
                    pos = word.attrib.get('type')
                    if pos is not None:
                        if prop_names==False:
                            if pos.startswith('n') and pos.endswith('s'):
                                continue
                        if pos in pos_to_ignore:
                            continue
                        if (not all(i.isalpha() or i == '-' for i in word.text)):
                            continue
                        if len(word.text) < 3:
                            continue
                        if word.text[-1] == '-':
                            continue
                        if word.text[0] == '-':
                            continue
                        if word.attrib.get('lemma') is not None:
                            lemma = word.attrib.get('lemma')
                            filter_query = SQLiteQuery(lemma,'filter','FILTER_WORD_FORMS', cursor=filters.cursor)
                            if filter_query.exists:
                                continue
                            else:
                                if corpus == "2":
                                    query = SQLiteQuery(lemma,'fletta','ISLEX_LEMMAS', cursor = islex.cursor)
                                    query_lower = SQLiteQuery(lemma.lower(),'fletta','ISLEX_LEMMAS', cursor = islex.cursor)
                                    if not query.exists and not query_lower.exists:
                                        if lemma not in freqdic1:
                                            freqdic1[lemma] = 1
                                        else:
                                            freqdic1[lemma] += 1
                                        if (lemma,texttype) not in freqdic2:
                                            freqdic2[(lemma,texttype)] = 1      
                                        else:
                                            freqdic2[(lemma,texttype)] += 1
                                elif corpus == "1":
                                    query = SQLiteQuery(lemma,'word_form','BIN_WORD_FORMS', cursor = bin.cursor)                  
                                    query_lower = SQLiteQuery(lemma.lower(),'word_form','BIN_WORD_FORMS', cursor = bin.cursor)
                                    if not query.exists and not query_lower.exists:
                                        if lemma not in freqdic1:
                                            freqdic1[lemma] = 1
                                        else:
                                            freqdic1[lemma] += 1
                                        if (lemma,texttype) not in freqdic2:
                                            freqdic2[(lemma,texttype)] = 1      
                                        else:
                                            freqdic2[(lemma,texttype)] += 1
            except IndexError:
                continue
            except ET.ParseError:
                continue  

        filebar.next()
        sys.stdout.flush()
    filebar.finish()
    
    print("Eftirfarandi eru allar mögulegar textagerðir:")
    print(sorted(alltexttypes))

    print("Raðar tíðni eftir textagerðum. Getur tekið þó nokkurn tíma ef skjölin eru mörg.")
    tempfinal = []
    bar1 = IncrementalBar('Framvinda', max = len(freqdic1))
    for key, value in sorted(freqdic1.items()):
        tempf = []
        tempf.append(key)
        temp = []
        for k, v in freqdic2.items():
            if k[0] == key:
                temp.append((k[1], v))
        tempf.append(temp)
        tempf.append(value)
        tempfinal.append(tempf)
        bar1.next()
        sys.stdout.flush()
    bar1.finish()
    
    print("Leggur lokahönd á ferlið")

    final = []
    bar2 = IncrementalBar('Framvinda', max = len(tempfinal))
    for i in tempfinal:
        fitemp = []
        fitemp.append(i[0])
        fitemp.append(i[2])
        for tt in alltexttypes:
            if tt in [item[0] for item in i[1]]:              
                continue
            else:
                i[1].append((tt, 0))
        for tup in sorted(i[1]):
            fitemp.append(tup[1])
        final.append(fitemp)
        bar2.next()
        sys.stdout.flush()
    bar2.finish()

    header = ['Orð', 'Heildartíðni'] + sorted(alltexttypes)
    if not folder.startswith("corpora/RMH/"):
        namefolder = folder.partition("/")[2].partition("/")[0]
        if corpus == "1":
            with open("uttaksskjol/bin/"+namefolder+"_texttypes_BIN.csv", mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)
        elif corpus == "2":
            with open("uttaksskjol/islex/"+namefolder+"_texttypes_ISLEX.csv", mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)
    
    elif folder == "corpora/RMH/**/**/":
        if corpus == "1":
            with open("uttaksskjol/bin/RMH_texttypes_BIN.csv", mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)
        elif corpus == "2":
            with open("uttaksskjol/islex/RMH_texttypes_ISLEX.csv", mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)

    elif folder == "corpora/RMH/CC_BY/**/":
        if corpus == "1":
            with open('uttaksskjol/bin/CC_BY_texttypes_BIN.csv', mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)
        elif corpus == "2":
            with open('uttaksskjol/islex/CC_BY_texttypes_ISLEX.csv', mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)
    elif folder == "corpora/RMH/MIM/**/":
        if corpus == "1":
            with open('uttaksskjol/bin/MIM_texttypes_BIN.csv', mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)
        elif corpus == "2":
            with open('uttaksskjol/islex/MIM_texttypes_ISLEX.csv', mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)
    elif folder.startswith("corpora/RMH/"):
        namefolder = folder.rpartition("/")[2]
        if corpus == "1":
            with open('uttaksskjol/bin/'+namefolder+"_texttypes_BIN.csv", mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)
        elif corpus == "2":
            with open('uttaksskjol/islex'+namefolder+"_texttypes_ISLEX.csv", mode='w+') as outputfile:
                csvwriter = csv.writer(outputfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(header)
                for i in final:
                    csvwriter.writerow(i)

    print("Úttaksskjal tilbúið")