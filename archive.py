from db import MongoDB


class Archive(object):
    ''' Store all the logs and records in JSON.

    one Archive instance will store a kind of log. '''

    def __init__(self, db, table):
        self.db = db
        if isinstance(db, str):
            self.db = MongoDB(db)
        self.table = self.db[table]

    def insert_file(self, key, path):
        with open(path) as f:
            c = f.read()
            rcd = {'key': key, 'value': c}
        return self.db.insert(self.table, rcd)

    def insert_rcd(self, key, record):
        return self.db.insert(self.table, {'key': key, 'value': record})

    def query(self, key):
        return self.table.find_one({'key': key})
