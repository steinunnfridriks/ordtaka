from parse_json import RmhJSON
from tokenizer import split_into_sentences
from argparse import ArgumentParser

parser = ArgumentParser(description='Input: textfile.')
parser.add_argument('-f', '--file', metavar='', required=True)
args = parser.parse_args()

class TextFile:
    def __init__(self):
        self.file = args.file
        self.tokens = self._tokenize_file(self.file)

    def _tokenize_file(self, file):
        with open(file, 'r', encoding='utf-8') as infile:
            sentences = split_into_sentences(infile.read())
        # Returns a flat list of all tokens in the text file
        return [item for s in sentences for item in s.split()]


if __name__ == '__main__':
    """
    Usage example
    """
    file = TextFile()
    for t in file.tokens:
        print(t.upper())
        json = RmhJSON(query_string=t, count=1000, context=3, type='word')
        for possible_lemma in json.get_all_possible_lemmas():
            print(possible_lemma)
        print('==========================')
