"""
This class does the main iterating work when comparing an input
corpus to an undefined database. 
"""

from xml.etree import ElementTree as ET
from string import punctuation
import glob
from ordtaka.sql.sql_lookup import SQLDatabase, SQLiteQuery
from ordtaka.rmh_extractor import RmhWord, RmhExtractor

class CompareRmhOther:
    """
    A class that streams words RMH files and checks
    whether they exist in the database
    """
    def __init__(self, rmh_folder=None, proper_nouns=True):
        self.rmh_folder = rmh_folder
        self.proper_nouns = proper_nouns
        self.other_candidates = {}
        # Database connection established when class instance is initalized
        self.connection = SQLDatabase(db_name='databases/ordasafn.db')
        # RmhExtractor initalized for yielding TEI content
        self.rmh = RmhExtractor(folder=rmh_folder)
        self.filters_connection = SQLDatabase(db_name='databases/filters.db')


    def _compare(self):
        """
        Checks whether word form in RMH exists in BÍN
        """
        # These part of speech tags are ignored as they won't generally be needed
        pos_to_ignore = ['e', 'c', 'v', 'as', 'to', 'tp', 'ta', 'au']
        # This creates a generator that yields a lemma and pos for every
        # single element of every single TEI file in the specified directory
        for word in self.rmh.extract(forms=False, lemmas=True, pos=True):
            if '-' in word.pos:
                continue
            if word.pos in pos_to_ignore:
                continue
            if not self.proper_nouns:
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
            filter_query = SQLiteQuery(word.word_form,
                                       'filter',
                                       'FILTER_WORD_FORMS',
                                       cursor=self.filters_connection.cursor)
            if filter_query.exists:
                continue
            else:
                # Check if word from RMH exists in the database
                query = SQLiteQuery(word.lemma, 'word_form', 'ORDASAFN_WORD',
                                    cursor=self.connection.cursor)
                # Check if word from RMH exists lowercase in the database
                query_lower = SQLiteQuery(word.lemma.lower(), 'word_form', 'ORDASAFN_WORD',
                                          cursor=self.connection.cursor)
                # If neither exists in the database, collect to seen
                if not query.exists and not query_lower.exists:
                    # If word already exists in dict
                    if word.lemma in self.other_candidates:
                        # If word is a noun
                        if word.pos[0] == 'n':
                            # If word is singular (eintala)
                            self.other_candidates[word.lemma]['freq'] += 1
                            self.other_candidates[word.lemma]['tala'][word.pos[2]] += 1
                        else:
                            self.other_candidates[word.lemma]['freq'] += 1
                            self.other_candidates[word.lemma]['tala']['annað'] += 1
                    else:
                        if word.pos[0] == 'n':
                            if word.pos[2] == 'e':
                                self.other_candidates[word.lemma] = {'freq': 0, 'tala':
                                                                        {'e': 1, 'f': 0, 'annað': 0}}
                            elif word.pos[2] == 'f':
                                self.other_candidates[word.lemma] = {'freq': 0, 'tala':
                                                                        {'e': 0, 'f': 1, 'annað': 0}}
                        else:
                            self.other_candidates[word.lemma] = {'freq': 0, 'tala':
                                                                    {'e': 0, 'f': 0, 'annað': 1}}
                        self.other_candidates[word.lemma]['freq'] = 1
        return self.other_candidates

    def write_to_file(self):
        """
        Adds words from RMH that do not exist in the database
        to other_candidates, sorts them by frequency and
        writes them to a file
        """
        if self.rmh_folder == "corpora/RMH/**/**/":
            with open(f'uttaksskjol/ordasafn/RMH_wordform_ordasafn.freq',
                      'w', encoding='utf-8') as out:
                other_candidates = self._compare()
                other_candidates = {k: v for k, v in sorted(other_candidates.items(),
                                    key=lambda item: item[1]['freq'], reverse=True)}
                for key, value in other_candidates.items():
                    out.write(key + ': ' + str(value) + '\n')

        elif self.rmh_folder == "corpora/RMH/CC_BY/**/":
            with open(f'uttaksskjol/ordasafn/CC_BY_wordform_ordasafn.freq',
                      'w', encoding='utf-8') as out:
                other_candidates = self._compare()
                other_candidates = {k: v for k, v in sorted(other_candidates.items(),
                                    key=lambda item: item[1]['freq'], reverse=True)}
                for key, value in other_candidates.items():
                    out.write(key + ': ' + str(value) + '\n')

        elif self.rmh_folder == "corpora/RMH/MIM/**/":
            with open(f'uttaksskjol/ordasafn/MIM_wordform_ordasafn.freq',
                      'w', encoding='utf-8') as out:
                other_candidates = self._compare()
                other_candidates = {k: v for k, v in sorted(other_candidates.items(),
                                    key=lambda item: item[1]['freq'], reverse=True)}
                for key, value in other_candidates.items():
                    out.write(key + ': ' + str(value) + '\n')
        else:
            self.rmh_folder = self.rmh_folder.split('/')[-1]
            with open(f'uttaksskjol/ordasafn/{self.rmh_folder}_wordform_ordasafn.freq',
                      'w', encoding='utf-8') as out:
                other_candidates = self._compare()
                other_candidates = {k: v for k, v in sorted(other_candidates.items(),
                                    key=lambda item: item[1]['freq'], reverse=True)}
                for key, value in other_candidates.items():
                    out.write(key + ': ' + str(value) + '\n')

if __name__ == '__main__':
    c = CompareRmhOther(rmh_folder='../../CC_BY/viljinn', proper_nouns=True)
    c.write_to_file()
