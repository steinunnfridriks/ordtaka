"""
This script allow a user to add more filters to the filters
database, which consists of words that are ignored in the
Lexicon Acquisition Tool's output. Using a command line interface,
simply run this script and follow the instructions.

"""

from ordtaka.sql.word_to_db import WordToDB
import re
from string import punctuation

print("""
    ============================================================
    Viltu setja textaskjal (1) inn í filtera eða bæta orðum við
    af skipanalínu (2)? Stimplaðu inn tölu og ýttu á ENTER.
    ============================================================
""")

setup_type = input(f"""
    (1) Bæta við orðum af skipanalínu
    (2) Textaskjal

    ============================================================

""")

if setup_type == '1':
    input_words = input(f"""
    Skrifaðu orð með bili á milli og ýttu á ENTER
    þegar þú hefur stimplað þau öll inn:

""").split()

    for input_word in input_words:
        w = WordToDB(word=input_word, db_name='databases/filters',
                     table_name='FILTER_WORD_FORMS', column='filter')

if setup_type == '2':
    input_file = input(f"""
    Settu inn nafn skráarinnar. Athugaðu að full leið
    (e. path) að henni er nauðsynleg.

""")
    with open(input_file, 'r', encoding='utf-8') as in_file:
        read_file = in_file.read()
    input_words = re.findall(r"[\w'\-]+", read_file)
    for input_word in input_words:
        w = WordToDB(word=input_word, db_name='databases/filters',
                        table_name='FILTER_WORD_FORMS', column='filter')
    print(f"""
    ============================================================
    {len(input_words)} orðum bætt við filtera.
    Hér eftir munu þau ekki birtast í úttaksskjölum.
    ============================================================
""")
