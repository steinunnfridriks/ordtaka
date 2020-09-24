from json import loads
from urllib.request import urlopen
from urllib.parse import quote


class WordNotFound(Exception):
    """
    Raise if word does not exist in BÍN
    """
    pass


class NotInflectable(Exception):
    """
    Raise if word has only one word form
    """
    pass


class BINWordJSON:
    """
    This class represents a json object from https://bin.arnastofnun.is/api/
    """
    def __init__(self, query_string: str=None):
        # Lemma or word form, depending on self.type
        self.query_string = query_string
        # Encodes query_string for url
        self.encoded_query_string = quote(query_string)
        self.url = (f'https://bin.arnastofnun.is/api/ord/{self.encoded_query_string}')
        self.response = urlopen(self.url)
        self.json_data = loads(self.response.read())
        # Checks if words share identical lemmas
        self.n_lemmas = len(self.json_data)
        # Used if words share identical lemmas
        if not self.json_data == {'0': ''}:
            self.all_ids = [w['guid'] for w in self.json_data]
        else:
            raise WordNotFound('Word does not exist in BÍN', self.query_string)
        # Generator object with all word forms of a given lemma
        # Nested * self.n_lemmas
        self.all_forms = self.get_all_forms()

    def get_all_forms(self):
        for id in self.all_ids:
            # Temp list, used to keep words forms with different IDs separate
            temp_forms = []
            url = f'https://bin.arnastofnun.is/api/ord/{id}'
            response = urlopen(url)
            json_data = loads(response.read())
            # bmyndir = beygingarmyndir = inflected word forms
            word_forms = json_data[0]['bmyndir']
            for form in word_forms:
                try:
                    temp_forms.append(form['b'])
                # Some words, such as prepositions and conjunctions, only have a single form
                except KeyError as e:
                    if e.args[0] == 'b':
                        raise NotInflectable('Word does not inflect', self.query_string)
            yield temp_forms


if __name__ == '__main__':
    # Raises WordNotFound
    b = BINWordJSON('vera')
    print(b.all_ids)
    print([w for w in b.get_all_forms()])
    """
    Returns [
    'maður', 'maðurinn', 'mann', 'manninn',
    'manni', 'manninum', 'manns', 'mannsins',
    'menn', 'mennirnir', 'menn', 'mennina',
    'mönnum', 'mönnunum', 'manna', 'mannanna'
    ]
    """
