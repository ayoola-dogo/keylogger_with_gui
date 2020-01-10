import sqlite3
import logging


def key_logger_entry(mode, _id, title, entry_text, date):

    conn = sqlite3.connect('entry_db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    try:
        cur.execute('''
                        CREATE TABLE logger_text (
                        id integer primary key,
                        title text,
                        entry_text text,
                        date timestamp)            
                    ''')

        conn.commit()
    except Exception as err:
        logging.basicConfig(filename='database.log', level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%({})s'.format(err))

    # Insert details
    def insert_details():
        # Using the python connection object representing the database as a context manager
        with conn:
            cur.execute("INSERT INTO logger_text VALUES (:id, :title, :entry_text, :date)", {'id': _id,
                                                                                             'title': title,
                                                                                             'entry_text': entry_text,
                                                                                             'date': date})

    # Retrieve details
    def retrieve_details():
        with conn:
            if _id:
                cur.execute("SELECT * FROM logger_text WHERE id=:id", {'id': _id})
            else:
                cur.execute("SELECT * FROM logger_text WHERE title=:title", {'title': title})
            return cur.fetchone()

    # Delete details
    def delete_details():
        with conn:
            if _id:
                cur.execute('DELETE FROM logger_text WHERE id=:id', {'id': _id})
            else:
                cur.execute('DELETE FROM logger_text WHERE id=:title', {'title': title})

    def delete_all():
        with conn:
            cur.execute("DELETE FROM logger_text")

    def table_layout():
        with conn:
            cur.execute("SELECT sql FROM sqlite_master WHERE type='table'")
            return cur.fetchall()

    if mode == 'i':
        try:
            insert_details()
        except Exception as e:
            logging.basicConfig(filename='database.log', level=logging.INFO,
                                format='%(asctime)s:%(levelname)s:%({})s'.format(e))
            conn.close()

    if mode == 'r':
        results = retrieve_details()
        if results:
            return results
        else:
            logging.basicConfig(filename='database.log', level=logging.INFO,
                                format='%(asctime)s:%(levelname)s:%(No text entry in the database table with that Id)s')

    if mode == 'd':
        delete_details()
        # print('This is the current content of the database: ', table_layout())

    if mode == 'd_all':
        query = input('Are you sure you want to delete all content in the database: ')
        if query in ('y', 'Y', 'yes', 'YES'):
            delete_all()
        else:
            pass

    if mode == 'c':
        return table_layout()

    if conn:
        conn.close()
        print('Connection closed')
