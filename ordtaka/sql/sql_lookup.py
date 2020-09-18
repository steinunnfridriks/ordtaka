import sqlite3

class SQLDatabase:
    """
    This class represents a connection to a SQLite3 database.
    """
    def __init__(self, db_name=None, table_name=None, column_name=None):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()


class SQLiteQuery:
    """
    This class is used to look up various info in the three databases,
    bin_lemmas_word_forms.db, bin_ordmyndir.db, islex_lemmas.db.
    """
    def __init__(self, word=None, lookup_type=None, table_name=None, cursor=None):
        self.word = word
        self.lookup_type = lookup_type
        self.cursor = cursor
        self.table_name = table_name
        #self.all_word_forms = self._all_word_forms()
        self.exists = self.exists()

    def _all_word_forms(self):
        """
        This method is intended to be used with bin_lemmas_word_forms.db.
        It returns a list of all word forms of a given lemma (self.word) if
        it exists.
        """
        all_word_forms = []
        for word in self.cursor.execute(f"""
                            SELECT word_form
                            FROM {self.table_name}
                            WHERE lemma='{self.word}'
                            """):
                                all_word_forms.append(word[0])
        if all_word_forms == []:
            return None
        return all_word_forms


    def exists(self):
        """
        This method is intended to be used with bin_ordmyndir.db and/or
        islex_lemmas.db. It returns True if a word forms exists in the former
        or a lemma exists in the latter. Else it returns False.
        """
        self.cursor.execute(f"""
                        SELECT 1
                        FROM {self.table_name}
                        WHERE {self.lookup_type}='{self.word}'
                        """)
        return True if self.cursor.fetchone() else False

if __name__ == '__main__':
    pass
