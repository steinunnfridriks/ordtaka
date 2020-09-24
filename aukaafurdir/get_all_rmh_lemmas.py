import glob
from xml.etree import ElementTree as ET
from string import punctuation
from rmh_extractor import RmhWord, RmhExtractor
from sys import path

class RmhLemmas:
    """
    This class is mainly used for writing all of
    RMH's lemmas to a text file.
    """
    def __init__(self):
        self.corpora = ['../../CC_BY', '../../MIM']
        self.rmh_lemmas = {}

    def _all_lemmas(self):
        """
        Keeps count of the frequency of every single lemma in RMH.
        Can easily be changed to work with subcorpora, by changing
        the elements in self.corpora.
        """
        for corpus in self.corpora:
            current_corpous = RmhExtractor(folder=corpus)
            for word in current_corpous.extract(forms=False, lemmas=True, pos=False):
                if word.lemma in self.rmh_lemmas:
                    self.rmh_lemmas[word.lemma] += 1

                else:
                    self.rmh_lemmas[word.lemma] = 1
        return self.rmh_lemmas

    def write_to_file(self):
        """
        Adds lemmas from to self.rmh_lemmas, sorts them by frequency and
        writes them to a file
        """
        with open('all_rmh2019_lemmas.freq',
                  'w', encoding='utf-8') as out:
            all_lemmas = self._all_lemmas()
            all_lemmas = {k: v for k, v in sorted(all_lemmas.items(),
                          key=lambda item: item[1], reverse=True)}
            for key, value in all_lemmas.items():
                out.write(key + ': ' + str(value) + '\n')


if __name__ == '__main__':
    rmhl = RmhLemmas()
    rmhl.write_to_file()
