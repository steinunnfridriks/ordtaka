from sys import path
path.append('..')
from xml.etree import ElementTree as ET
from string import punctuation
import glob
from sql.sql_lookup import SQLDatabase, SQLiteQuery
from rmh_extractor import RmhWord, RmhExtractor


class CompareRmhBIN:
    """
    A class that streams words RMH files and checks
    whether they exist in BÍN
    """
    def __init__(self, rmh_folder=None, proper_nouns=True):
        # Shortens full dir path
        self.rmh_folder = rmh_folder.split('/')[-1]
        self.proper_nouns = proper_nouns
        self.bin_candidates = {}
        # Database connections established when class instance is initalized
        self.connection = SQLDatabase(db_name='../databases/bin_ordmyndir.db')
        self.filters_connection = SQLDatabase(db_name='../databases/filters.db')
        # RmhExtractor initalized for yielding TEI content
        print('Les inntaksskjöl')
        self.rmh = RmhExtractor(folder=rmh_folder)

    def _compare(self):
        """
        Checks whether word form in RMH exists in BÍN
        """
        # These part of speech tags are ignored as they won't generally be needed
        pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au']
        # This creates a generator that yields a word form, lemma and pos for every
        # single element of every single TEI file in the specified directory
        print('Ber saman inntak og gagnagrunn BÍN')
        for word in self.rmh.extract(forms=True, lemmas=True, pos=True):
            if word.pos in pos_to_ignore:
                continue
            # Proper nouns are ignored if proper_nouns == False
            if not self.proper_nouns:
                if word.pos.startswith('n') and word.pos.endswith('s'):
                    continue
            # Ignore if not only letters or letters and hyphen
            if (not all(i.isalpha() or i == '-' for i in word.word_form)):
                continue
            # Ignore words consisting of only 1 or 2 characters
            if len(word.word_form) < 3:
                continue
            # Ignore words that start with '[anyLetter?]-' or end with '-'
            if '-' in [word.word_form[0], word.word_form[1], word.word_form[-1]]:
                continue
            # Ignore unwanted words, such as names, foreign words, stopwords, abbreviations
            filter_query = SQLiteQuery(word.word_form,
                                       'filter',
                                       'FILTER_WORD_FORMS',
                                       cursor=self.filters_connection.cursor)
            if filter_query.exists:
                continue
            else:
                # Check if word from RMH exists in BIN
                query = SQLiteQuery(word.word_form,
                                    'word_form',
                                    'BIN_WORD_FORMS',
                                    cursor=self.connection.cursor)
                # Check if word from RMH exists lowercase in BIN
                query_lower = SQLiteQuery(word.word_form.lower(),
                                          'word_form',
                                          'BIN_WORD_FORMS',
                                          cursor=self.connection.cursor)
                # If neither exists in BIN, collect to seen
                if not query.exists and not query_lower.exists:
                    if word.word_form in self.bin_candidates:
                        if word.lemma not in self.bin_candidates[word.word_form]['lemmas']:
                            self.bin_candidates[word.word_form]['lemmas'].append(word.lemma)
                        self.bin_candidates[word.word_form]['freq'] += 1
                    else:
                        self.bin_candidates[word.word_form] = {}
                        self.bin_candidates[word.word_form]['freq'] = 1
                        self.bin_candidates[word.word_form]['lemmas'] = [word.lemma]
        return self.bin_candidates

    def write_to_file(self):
        """
        Adds words from RMH that do not exist in BÍN
        to bin_candidates, sorts them by frequency and
        writes them to a file
        """
        with open(f'../uttaksskjol/bin/{self.rmh_folder}_not_in_bin.freq',
                  'w', encoding='utf-8') as out:
            bin_candidates = self._compare()
            bin_candidates = {k: v for k, v in sorted(bin_candidates.items(),
                              key=lambda item: item[1]['freq'], reverse=True)}
            for key, value in bin_candidates.items():
                out.write(key + ': ' + str(value) + '\n')
        print('Úttaksskjal tilbúið')

if __name__ == '__main__':
    c = CompareRmhBIN(rmh_folder='../../CC_BY/frettabladid_is')
    c.write_to_file()
