import os
import os.path
import sqlite3


class _PathStore:

    def __init__(self, path):
        self._path = (path + 'dotedit.db' if path.endswith('/')
                      else path + '/dotedit.db')

        if not os.path.exists(self._path):
            self._create_db()

    def get(self, program):
        connection = sqlite3.connect(self._path)
        cursor = connection.cursor()
        cursor.execute("SELECT path from paths WHERE program=?", (program,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row is None:
            raise LookupError()

        return row[0]

    def list(self):
        connection = sqlite3.connect(self._path)
        cursor = connection.cursor()
        cursor.execute("SELECT program from paths")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        return [tup[0] for tup in rows if tup]

    def add(self, program, path):
        connection = sqlite3.connect(self._path)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO paths VALUES(?,?)", (program, path,))
        cursor.close()
        connection.commit()
        connection.close()

    def update(self, program, path):
        connection = sqlite3.connect(self._path)
        cursor = connection.cursor()
        cursor.execute("REPLACE INTO paths VALUES(?,?)", (program, path,))
        cursor.close()
        connection.commit()
        connection.close()

    def remove(self, program):
        connection = sqlite3.connect(self._path)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM paths WHERE program=?", (program,))
        cursor.close()
        connection.commit()
        connection.close()

    def _create_db(self):
        try:
            os.makedirs(os.path.dirname(self._path))
        except OSError as e:
            if e.errno != os.errno.EEXIST:
                raise

        connection = sqlite3.connect(self._path)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE paths (program text, path text)")
        cursor.close()
        connection.commit()
        connection.close()
