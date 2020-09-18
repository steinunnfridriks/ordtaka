import pandas as pd
import sqlite3

class CorpusToSQL:
    """
    This class is used to populate the three databases used in this package,
    bin_lemmas_word_forms.db, bin_ordmyndir.db, islex_lemmas.db. The first one
    is populated with create_relational_database and the other ones with create_db.
    Usage examples are commented out at the bottom of this file. CorpusToSQL is
    mostly used in setup_dbs.py.
    """
    def __init__(self, corpus=None, db_name=None, include_index=True):
        self.corpus = corpus
        self.db_name = db_name
        self.include_index = include_index
        self.connection = sqlite3.connect(f'{self.db_name}.db')

    def create_db(self, table_name, column_name):
        self.connection.execute(f"""CREATE TABLE
                                if not exists {table_name}
                                ({column_name} TEXT)""")
        if self.include_index:
            self.connection.execute(f"""CREATE INDEX word_form_id
                                    ON {table_name} ({column_name})""")

        data = pd.read_csv(self.corpus, sep=',', dtype=str)
        df = pd.DataFrame(data, columns=[column_name])
        df.to_sql(f'{table_name}', self.connection, if_exists='append', index=False)

    def create_relational_database(self, table_name, column1, column2):
        self.connection.execute(f"""CREATE TABLE
                                    if not exists {table_name}
                                    ({column1} TEXT)""")

        self.connection.execute(f"""ALTER TABLE
                                   {table_name}
                                    ADD COLUMN {column2} TEXT""")
        if self.include_index:
            self.connection.execute(f""" CREATE INDEX lemma_index
                                    ON {table_name} ({column1})
                                    """)
            self.connection.execute(f""" CREATE INDEX word_form_index
                                    ON {table_name} ({column2})
                                    """)


        data = pd.read_csv(self.corpus, sep=';', dtype=str)
        df = pd.DataFrame(data, columns=[column1, column2])
        df.to_sql(f'{table_name}', self.connection, if_exists='append', index=False)

if __name__ == '__main__':
    pass
    #new_corpus = CorpusToSQL(corpus='../SHsnid.csv', db_name='bin_lemmas_word_forms')
    #new_corpus.create_relational_database('BIN_ELEMENT', 'lemma', 'word_form')
    #new_corpus = CorpusToSQL(corpus='islex_fletta_ofl.csv', db_name='islex_lemmas')
    #new_corpus.create_db('ISLEX_LEMMAS', 'fletta')
    #new_corpus = CorpusToSQL(corpus='../ordmyndir.txt', db_name='bin_ordmyndir')
    #new_corpus.create_db('BIN_WORD_FORMS', 'word_form')
