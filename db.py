'''
Database handler.
'''
from pymongo import MongoClient
from bson import ObjectId


class MongoDB(object):
    def __init__(self, dbname, ip='localhost', port=27017):
        self.client = MongoClient(ip, port)
        self.db = self.client[dbname]

    def insert(self, table, record):
        ''' insert (key, value) to a table.
        table: str
        record: python object
        '''
        if isinstance(table, str):
            table = getattr(self.db, table)
        return table.insert_one(record)

    def query(self, table, cond=None, id=None):
        ''' get a record from table which matches the cond.
        table: str
        cond: python dic '''
        assert cond or id, 'either cond or id should be provided to query a record.'
        table = getattr(self.db, table)
        if cond:
            return [v for v in table.find(cond)]
        return table.find_one({'_id': ObjectId(id)})
