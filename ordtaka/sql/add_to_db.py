import sqlite3

class WordToDB:
    """
    Whenever this class is initalized properly, it adds a row (word) to a  given
    column in a given table.
    """
    def __init__(self, word=None, db_name=None, table_name=None, column=None):
        self.word = word
        self.db_name = db_name
        self.table_name = table_name
        self.column = column
        self.connection = sqlite3.connect(f'{self.db_name}.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute(f"""
                             INSERT OR REPLACE INTO {self.table_name}({self.column})
                             VALUES ('{self.word}')
                             """)
        self.connection.commit()

if __name__ == '__main__':
    w = WordToDB(word='blabla', db_name='../bin_ordmyndir',
                 table_name='BIN_WORD_FORMS', column='word_form')
