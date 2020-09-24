import json
from urllib.request import urlopen
from urllib.parse import quote

class RmhJSON:
    """
    This class represents a json object from https://malheildir.arnastofnun.is/

    To get collocations of a given word, with five surrounding words:
    >>> print([c for c in RmhJSON('hundur', 20, 5, 'lemma').get_collocations()])

    To get collocations of a given word in a specific case:
    >>> print([c for c in RmhJSON('hundi', 20, 5, 'word').get_collocations()])

    To get all forms of a word that appear within the first 100 results:
    >>> print([w for w in RmhJSON('hundur', 100, 5, 'lemma').get_word_forms().items()])

    To get all possible lemmas of a word form that appear within the first 100 results:
    >>> print(RmhJSON('er', 100, 3, 'word').get_all_possible_lemmas())
    """
    def __init__(self, query_string: str=None, count: int=100, context: int=10, type: str=None):
        # Lemma or word form, depending on self.type
        self.query_string = query_string
        # Marks query_string as lemma or word form
        # Use 'word' if grammatical case matters
        self.type = type
        # Encodes query_string for url
        self.encoded_query_string = quote(query_string)
        # N word/sentence examples
        self.count = count
        # N words surrounding query
        self.context = context
        self.url = ('https://malheildir.arnastofnun.is:4321/'
        f'query?command=query&default_context={self.context}%20'
        'words&show=sentence,paragraph,text,word,pos,lemma,'
        'pers,kyn,tala,fall,lostig,mynd,hattur,tid,lob,fsfall,'
        'tob,fnf,tof,tt,sernafn,greinir&show_struct=text_author,'
        'text_datefrom,text_dateto,text_timefrom,text_timeto,'
        'text_date,text_midill,text_wordcount,text_id_midill,'
        'text_title,text_url,text_speakerurl,text_speaker,'
        'text_thingnr,text_flokkur,text_kjordaemi,text_aldur,'
        'text_flokkar,text_stada,text_utgafuar,text_ritstjorar,'
        'text_utgefandi,text_sentencecount,text_paragraphcount,'
        f'text_translator&start=0&end={self.count}&corpus='
        'RMH2019_STOD2,RMH2019_RAS1_OG_2,RMH2019_BYLGJAN,'
        'RMH2019_SJONVARPID,RMH2019_MORGUNBLADID,'
        'RMH2019_FRETTABLADID_IS,RMH2019_KJARNINN_BLAD,RMH2019_RUV,'
        'RMH2019_VISIR,RMH2019_MBL,RMH2019_DV_IS,RMH2019_KJARNINN,'
        'RMH2019_STUNDIN,RMH2019_VILJINN,RMH2019_FRETTATIMINN,'
        'RMH2019_EYJAN,RMH2019_DOMSTOLAR,RMH2019_HAESTIRETTUR,'
        'RMH2019_LANDSRETTUR,RMH2019_ALTHINGISLOG,RMH2019_ALTHINGI,'
        'RMH2019_WIKIPEDIA,RMH2019_VISINDAVEFUR,RMH2019_SILFUREGILS,'
        'RMH2019_ANDRIKI,RMH2019_JONAS,RMH2019_HEIMUR,RMH2019_VF,'
        'RMH2019_FJARDARPOSTUR,RMH2019_DFS,RMH2019_SKESSUHORN,'
        'RMH2019_BB,RMH2019_KAFFID,RMH2019_EYJAFRETTIR,RMH2019_EYJAR,'
        'RMH2019_FJARDARFRETTIR,RMH2019_HUNI,RMH2019_KOPAVOGSBLADID,'
        'RMH2019_SIGLFIRDINGUR,RMH2019_SUNNLENSKA,RMH2019_TROLLI,'
        'RMH2019_VIKUDAGUR,RMH2019_FOTBOLTI,RMH2019_FJORIRTHRIRTHRIR,'
        'RMH2019_VF_KYLFINGUR,RMH2019_EIDFAXI,RMH2019_BONDI,'
        'RMH2019_BLEIKT,RMH2019_BBL,RMH2019_PRESSAN,'
        'RMH2019_FISKIFRETTIR,RMH2019_MANNLIF,RMH2019_VB,'
        f'RMH2019_TEXTASAFN&cqp=[{self.type}%20=%20%22{self.encoded_query_string}%22%20%c]'
        '&query_data=&context=&incremental=true&'
        'default_within=sentence&within=')

    def get_collocations(self):
        response = urlopen(self.url)
        json_data = json.loads(response.read())
        for text in json_data['kwic']:
            tokens = text['tokens']
            chunk = []
            for token in tokens:
                chunk.append(token['word'])
            yield chunk

    def get_word_forms(self):
        word_forms = {}
        response = urlopen(self.url)
        json_data = json.loads(response.read())
        for text in json_data['kwic']:
            tokens = text['tokens']
            for token in tokens:
                if token['lemma'] == self.query_string:
                    word_forms[token['word'].lower()] = token['pos']
        word_forms = {k: v for k, v in sorted(word_forms.items(), key=lambda item: item[1])}
        return word_forms

    def get_all_possible_lemmas(self):
        possible_lemmas = []
        response = urlopen(self.url)
        json_data = json.loads(response.read())
        for text in json_data['kwic']:
            tokens = text['tokens']
            for token in tokens:
                if token['word'] == self.query_string:
                    if token['lemma'] in possible_lemmas:
                        continue
                    else:
                        possible_lemmas.append(token['lemma'])
        return possible_lemmas

if __name__ == '__main__':
    print(RmhJSON('úrvalsdeild', 100, 3, 'word').get_all_possible_lemmas())
