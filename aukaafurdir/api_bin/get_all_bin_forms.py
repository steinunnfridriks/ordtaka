from sql_lookup import SQLDatabase, SQLiteQuery

class BINElement:
    def __init__(self, query_string=None, cursor=None):
        self.query_string = query_string
        self.cursor = cursor
        self.all_word_forms = self._all_word_forms()

    def _all_word_forms(self):
        all_word_forms = []
        for word in self.cursor.execute(f"""
                            SELECT word_form
                            FROM BIN_ELEMENT
                            WHERE lemma='{self.query_string}'
                            """):
                                all_word_forms.append(word[0])
        if all_word_forms == []:
            return None
        return all_word_forms

if __name__ == '__main__':
    sql = SQLDatabase(db_name='../bin_lemmas_word_forms.db')
    cursor = sql.cursor
    b = BINElement('maður', cursor=cursor)
    wordlist = ['maður']
    print(b.all_word_forms)
