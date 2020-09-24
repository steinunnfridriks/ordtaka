from rmh_extractor import RmhWord, RmhExtractor
import sys
sys.path.append('../sql/')
import sqlite3
from sql_lookup import SQLiteQuery, SQLDatabase
from kvistur.kvistur import Kvistur
from string import punctuation

sql = SQLDatabase(db_name='../bin_lemmas_word_forms.db')
cursor = sql.cursor

model_path = 'kvistur/kvistur.hdf5'
chars_path = 'kvistur/chars.json'
kvistur = Kvistur(model_path, chars_path)

# Choose the directory whose files should be parsed
print("Extracting files from RMH.")
RMH = RmhExtractor(folder='mbl')
words = RMH.extract(forms=True, lemmas=True, pos=True)

# Get all words from the files in the specified directory
allwords = {}
for word in words:
    if "'" in word.lemma:
        clean = word.lemma.replace("'", "")
        if clean not in allwords:
            allwords[clean] = 1
        else:
            allwords[clean] += 1
    else:
        if word.lemma not in allwords:
            allwords[word.lemma] = 1
        else:
            allwords[word.lemma] += 1

# if the vocabulary considered is more than 100.000 words, only consider the most frequent ones 
if len(allwords) > 100000:
    print("Limiting vocabulary to 100.000 most frequent words.")
    sorted_words = {k: v for k, v in sorted(allwords.items(), key=lambda item: item[1], reverse=True)[:100000]}
else:
    sorted_words = {k: v for k, v in sorted(allwords.items(), key=lambda item: item[1], reverse=True)}

# Split the compound words using Kvistur to get the binary components
print("Splitting words using Kvistur. Can take a while.")
nodes = kvistur.split(sorted_words.keys())

plain_compounds = []
inflections = []
dne = []

print("Checking if words exist in BÍN. Can take a while.")
for node in nodes:
    query = SQLiteQuery(node.form, 'lemma', 'BIN_ELEMENT', cursor=sql.cursor)
    if query.all_word_forms == None:
        query2 = SQLiteQuery(node.form.lower(), 'lemma', 'BIN_ELEMENT', cursor=sql.cursor)
        if query2.all_word_forms == None:
            if node.get_binary()[0] != None and len(node.get_binary()[0]) > 2:
                query3 = SQLiteQuery(node.get_binary()[1], 'lemma', 'BIN_ELEMENT', cursor=sql.cursor)
                compounds = []
                if query3.all_word_forms == None:
                    dne.append(node.form)
                    dne.append(node.get_binary()[1])
                else:
                    plain_compounds.append(node.form)
                    for i in query3.all_word_forms:
                        compounds.append((node.get_binary()[0]+i))
                inflections.append(compounds)

print("Generating frequencies. Can take a while.")
final1 = []
for i in plain_compounds:
    for x in sorted_words.items():
        if i == x[0]:
            final1.append(i+"   "+str(x[1]))

print("Writing output files.")
# Write an outputfile that includes the compound words plain, no inflections
with open(f"plain_compounds_{RMH.folder}.txt", 'w+', encoding='utf8') as f:
    for i in final1:
        f.write(i+'\n')

# Write an outputfile that includes all inflections of the words, seperated by a blank line
with open(f"compound_inflections_{RMH.folder}.txt", 'w+', encoding='utf8') as f:
    for i in inflections:
        for x in i:
            if len(x) > 1:
                f.write(x+'\n')
        f.write('\n')

# Write an outputfile that includes all compound words whose second half does not exist in BÍN
with open(f"compound_inflections_second_half_not_in_bin_{RMH.folder}.txt", 'w+', encoding='utf8') as out: 
    i = 0
    while i < len(dne):
        out.write(dne[i].upper() + '\n')
        i += 1
        out.write("Second component: " + dne[i].upper() + " does not exist in BÍN (in this form) \n \n")
        i += 1

print("Finished.")