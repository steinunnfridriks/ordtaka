"""
This script provides the user with a setup of the necessary
databases for the Lexicon Acquisition Tool. Two files, 'SHsnid.csv' and
'ordmyndir.txt', can be downloaded with this script but the third one,
islex_fletta_ofl.csv, as of now, is not available with an open license.
Using a command line interface, simply run this script and follow the
instructions.
"""

import sys
from pathlib import Path
from ordtaka.prepare_data import prepare_data
from ordtaka.sql.corpus_to_sql import CorpusToSQL
from ordtaka.request_file import request_file

current_python = sys.version_info[:2]
required_python = (3, 6)

if current_python < required_python:
    sys.stderr.write(f"""
    ==================================
    Þessi útgáfa af Python er of gömul
    ==================================
    Þessi hugbúnaður reiðir sig á Python {required_python[0]}.{required_python[1]}. en
    þú ert að nota Python {current_python[0]}.{current_python[1]}. Vinsamlegast upp-
    færðu Python.
""")
    sys.exit(1)


print("""
    ============================================================
    Hvaða gagnasöfn viltu setja upp?
    ============================================================

    Stimplaðu tölurnar inn með bili á milli og ýttu á ENTER.

    Til að setja upp SHsnid.csv og ordmyndir.txt stimplarðu inn:
    1 2
    ============================================================
""")

to_setup_input = input(f"""
    (1) SHsnid.csv
    (2) ordmyndir.txt
    (3) islex_fletta_ofl.csv

""")

# User input mapped to files
i_to_db = {
            '1': 'SHsnid.csv',
            '2': 'ordmyndir.txt',
            '3': 'islex_fletta_ofl.csv',
}

# Files that are valid for this package
valid_files = i_to_db.values()

# Exit if user input is not in [1, 2, 3] and therefore has no corresponding file
try:
    to_setup = [i_to_db[i] for i in to_setup_input.split()]
except KeyError as e:
    sys.stderr.write(f"""
    {e.args[0]} er ekki valmöguleiki. Valmgöguleikarnir eru: 1, 2, 3.
""")
    sys.exit(1)

# Input for setup is valid if it has at least one of [1, 2, 3] and nothing else
setup_is_valid = len(to_setup) != 0 and all(i in valid_files for i in to_setup)
# Check whether all files requested for setup exist
all_files_exist = all(Path(i).is_file() for i in to_setup)

if not setup_is_valid:
    sys.stderr.write("""
    Þú valdir ekkert.
""")
    sys.exit(1)


else:
    islex = 'islex_fletta_ofl.csv'
    sh_snid = 'SHsnid.csv'
    bin = 'ordmyndir.txt'
    filters = 'all_filters.txt'
    if not Path('databases/filters.db').is_file():
        if Path(filters).is_file():
            print('Undirbý filtera')
            prepare_data(filters)
            print('Bý til gagnagrunn fyrir filtera')
            # Creates SQL database filters_ordmyndir.db with header FILTER_WORD_FORMS
            filter_db = CorpusToSQL(corpus=filters, db_name='databases/filters')
            filter_db.create_db('FILTER_WORD_FORMS', 'filter')
        else:
            # Exit if all_filters.txt doesn't exist
            print(f'Skráin <{filters}> er ekki til. Stöðva uppsetningu.')
            sys.exit(1)
    else:
        pass
    if islex in to_setup:
        if not Path('databases/islex_lemmas.db').is_file():
            if Path(islex).is_file():
                print('Undirbý ISLEX')
                prepare_data(islex)
                print('Bý til gagnagrunn fyrir ISLEX')
                # Creates SQL database islex_lemmas.db, with header ISLEX_LEMMAS
                islex = CorpusToSQL(corpus=islex, db_name='databases/islex_lemmas')
                islex.create_db('ISLEX_LEMMAS', 'fletta')
            else:
                print(f'Skráin <{islex}> er ekki til eða á röngum stað.')
        else:
            print(f'Gagnagrunnur fyrir ISLEX er nú þegar til.')
    if bin in to_setup:
        if not Path('databases/bin_ordmyndir.db').is_file():
            if not Path(bin).is_file():
                print(f'<{sh_snid}> er ekki til. Sæki skrána.')
                request_file('https://bin.arnastofnun.is/django/api/nidurhal/?file=ordmyndir.txt.zip',
                             'ordmyndir.txt.zip', zipped=True)
            if Path(bin).is_file():
                print('Undirbý BIN')
                prepare_data(bin)
                print('Bý til gagnagrunn fyrir BÍN')
                # Creates SQL database bin_ordmyndir.db with header BIN_WORD_FORMS
                bin = CorpusToSQL(corpus=bin, db_name='databases/bin_ordmyndir')
                bin.create_db('BIN_WORD_FORMS', 'word_form')
            else:
                print(f'Skráin <{bin}> er ekki til eða á röngum stað. Sæki hana.')
                request_file('https://bin.arnastofnun.is/django/api/nidurhal/?file=ordmyndir.txt.zip',
                             'ordmyndir.txt.zip', zipped=True)
        else:
            print(f'Gagnagrunnur fyrir orðmyndir BÍN er nú þegar til.')
    if sh_snid in to_setup:
        if not Path('databases/bin_lemmas_word_forms.db').is_file():
            if not Path(sh_snid).is_file():
                print(f'<{bin}> er ekki til. Sæki skrána.')
                request_file('https://bin.arnastofnun.is/django/api/nidurhal/?file=SHsnid.csv.zip',
                             'SHsnid.csv.zip', zipped=True)
            if Path(sh_snid).is_file():
                print('Undirbý SHsnið')
                prepare_data(sh_snid)
                print('Bý til gagnagrunn fyrir SHsnið')
                # Creates SQL database bin_ordmyndir.db with header BIN_WORD_FORMS
                sh_snid = CorpusToSQL(corpus=sh_snid, db_name='databases/bin_lemmas_word_forms')
                sh_snid.create_relational_database('BIN_ELEMENT', 'lemma', 'word_form')
            else:
                print(f'Skráin <{sh_snid}> er ekki til eða á röngum stað.')
        else:
            print(f'Gagnagrunnur fyrir SHsnið er nú þegar til.')
