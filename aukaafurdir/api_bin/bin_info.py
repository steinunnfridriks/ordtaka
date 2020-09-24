from reynir.bincompress import BIN_Compressed
bin = BIN_Compressed()

class BINElement:
    """
    A class that represents a lookup in BIN_Compressed
    """
    def __init__(self, lookup_string):
        self.lookup_string = lookup_string
        self.all_results = bin.lookup(lookup_string)
        self.is_in_bin = self.all_results != []
        self.possible_lemmas = (set(element[0] for element in self.all_results))
        self.exists_as_lemma = any([lookup_string == lemma for lemma in self.possible_lemmas])
        self.n_lemmas = len(set(element[1] for element in self.all_results))

if __name__ == '__main__':
    word_list = ['geimfari']
    for word in word_list:
        b = BINElement(word)
        print('Lookup string:', '\t' * 2, b.lookup_string)
        print('Is in BÍN:', ('\t' * 2), b.is_in_bin)
        print('Possible lemmas:', '\t', b.possible_lemmas)
        print('Exists as lemma:', '\t', b.exists_as_lemma)
        print('N possible lemmas:', '\t', b.n_lemmas)
        print()
        print('All results:', '\t', b.all_results)
