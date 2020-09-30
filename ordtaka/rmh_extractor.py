"""
These two classes are responsible for iterating through the RMH corpus
and representing every single token of it.
"""

from xml.etree import ElementTree as ET
from string import punctuation
import glob
punctuation += "–„”"
from progress.bar import IncrementalBar
import sys


class RmhWord:
    def __init__(self, word_form=None, lemma=None, pos=None):
            self.word_form = word_form
            self.lemma = lemma
            self.pos = pos
            self.is_punctuation_mark = False

    def __repr__(self):
        return f'({self.word_form}, {self.lemma}, {self.pos})'

class RmhExtractor:
    def __init__(self, folder=None):
        self.folder = folder
        self.xml_files = glob.glob(f'{folder}/**/*.xml', recursive=True)


    def extract(self, forms=True, lemmas=True, pos=True):
        filebar = IncrementalBar('Inntaksskjöl lesin', max = len(self.xml_files))
        for file in self.xml_files:
            with open(file, 'r', encoding='utf-8') as content:
                try:
                    tree = ET.parse(content)
                    for element in tree.iter():
                        rmh_word = RmhWord()
                        try:
                            if element.attrib.get('lemma') is not None:
                                if forms:
                                    rmh_word.word_form = element.text
                                if lemmas:
                                    rmh_word.lemma = element.attrib.get('lemma')
                                if pos:
                                    rmh_word.pos = element.attrib.get('type')
                                yield rmh_word
                            elif element.text in punctuation:
                                rmh_word.word_form = element.text
                                rmh_word.lemma = element.text
                                rmh_word.pos = element.text
                                rmh_word.is_punctuation_mark = True
                                yield rmh_word
                        except TypeError:
                            pass
                except ET.ParseError:
                    continue
            filebar.next()
            sys.stdout.flush()
        filebar.finish()

if __name__ == '__main__':
    pass
