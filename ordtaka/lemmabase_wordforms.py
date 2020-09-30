from xml.etree import ElementTree as ET
from string import punctuation
import glob
from ordtaka.sql.sql_lookup import SQLDatabase, SQLiteQuery
from ordtaka.rmh_extractor import RmhWord, RmhExtractor

def lemmabase_wordforms(rmh_folder, prop_names):
    bin = SQLDatabase(db_name='databases/bin_ordmyndir.db')
    islex = SQLDatabase(db_name='databases/islex_lemmas.db')
    filters = SQLDatabase(db_name='databases/filters.db')
    pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au']
    RMH = RmhExtractor(folder=str(rmh_folder))
    freqdic = {}
    print("Les inntaksskjöl")
    for word in RMH.extract(forms=True, lemmas=True, pos=True):
        try:
            # Ignore proper nouns
            if prop_names==False:
                if word.pos.startswith('n') and word.pos.endswith('s'):
                    continue
            if word.pos in pos_to_ignore:
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
                query = SQLiteQuery(word.lemma,'word_form','BIN_WORD_FORMS', cursor = bin.cursor)
                query_lower = SQLiteQuery(word.lemma.lower(),'word_form','BIN_WORD_FORMS', cursor = bin.cursor)
                if not query.exists and not query_lower.exists:
                    if word.lemma in freqdic:
                        if word.word_form not in freqdic[word.lemma]['wordforms']:
                            freqdic[word.lemma]['wordforms'].append(word.word_form)
                        freqdic[word.lemma]['freq'] += 1
                    else:
                        freqdic[word.lemma] = {}
                        freqdic[word.lemma]['freq'] = 1
                        freqdic[word.lemma]['wordforms'] = [word.word_form]
        except IndexError:
            continue
        except ET.ParseError:
            continue

    print("Skrifar úttaksskjal")
    if not rmh_folder.startswith("corpora/RMH/"):
        namefolder = rmh_folder.partition("/")[2].partition("/")[0]
        with open('uttaksskjol/bin/'+str(namefolder)+"_lemmabase_bin.freq", mode='w+', encoding='utf8') as out:
            bin_candidates = {k: v for k, v in sorted(freqdic.items(),key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in bin_candidates.items():
                out.write(key + ': ' + str(value) + '\n')
    if rmh_folder == "corpora/RMH/**/**/":
        with open("uttaksskjol/bin/RMH_lemmabase_bin.freq", mode='w+', encoding='utf8') as out:
            bin_candidates = {k: v for k, v in sorted(freqdic.items(),key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in bin_candidates.items():
                out.write(key + ': ' + str(value) + '\n')
    elif rmh_folder == "corpora/RMH/CC_BY/**/":
        with open("uttaksskjol/bin/CC_BY_lemmabase_bin.freq", mode='w+', encoding='utf8') as out:
            bin_candidates = {k: v for k, v in sorted(freqdic.items(),key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in bin_candidates.items():
                out.write(key + ': ' + str(value) + '\n')
    elif rmh_folder == "corpora/RMH/MIM/**/":
        with open("uttaksskjol/bin/MIM_lemmabase_bin.freq", mode='w+', encoding='utf8') as out:
            bin_candidates = {k: v for k, v in sorted(freqdic.items(),key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in bin_candidates.items():
                out.write(key + ': ' + str(value) + '\n')
    elif rmh_folder.startswith("corpora/RMH/"):
        namefolder = rmh_folder.rpartition("/")[2]
        with open('uttaksskjol/bin/'+str(namefolder)+"_lemmabase_bin.freq", mode='w+', encoding='utf8') as out:
            bin_candidates = {k: v for k, v in sorted(freqdic.items(),key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in bin_candidates.items():
                out.write(key + ': ' + str(value) + '\n')

    print("Úttaksskjal tilbúið")

if __name__ == '__main__':
    pass
