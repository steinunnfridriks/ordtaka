"""
This script creates necessary databases for lookups in BÍN, ISLEX and SH_snid
Make sure ordmyndir.txt, islex.csv and SH_snid.csv are in the same directory as this script
ordmyndir.txt and SH_snid.csv can be downloaded at: https://bin.arnastofnun.is/gogn/mimisbrunnur/
"""


def prepare_data(file):
    """
    Prepares the argument file for SQL insertion
    """
    with open(file, 'r', encoding='utf-8') as infile:
        infile = infile.read().splitlines()
        if file == 'islex_fletta_ofl.csv':
            pass
        elif file == 'ordmyndir.txt':
            if infile[0] != 'word_form':
                infile = ['word_form'] + infile
            else:
                pass
        elif file == 'SHsnid.csv':
            if infile[0] != ['lemma;id;gender;type;word_form;pos']:
                infile = ['lemma;id;gender;type;word_form;pos'] + infile
        elif file == 'all_filters.txt':
            if infile[0] != 'filter':
                infile = ['filter'] + infile
            else:
                pass
        with open(file, 'w', encoding='utf-8') as outfile:
            if file == 'SHsnid.csv':
                for row in infile:
                    outfile.write(row + '\n')
            else:
                for row in infile:
                    if row in ['"háls-, nef- og eyrnalæknir","n m"',
                               '"fóta-, handa- og munnveiki","n f"',
                               '"einn, tveir og þrír","adv"']:
                               continue
                    data = row.replace('"', '')
                    outfile.write(data + '\n')

if __name__ == '__main__':
    pass
