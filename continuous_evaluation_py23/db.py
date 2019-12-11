import bson
from pymongo import MongoClient


class MongoDB(object):
    def __init__(self, dbname, host='localhost', port=27017):
        self.client = MongoClient(host, int(port))
        self.db = getattr(self.client, dbname)

    def all_tables(self):
        '''
        find all collection
        '''
        collist = self.db.list_collection_names()
        return collist

    def table(self, table):
        ''' table might be a string or a Mongo table object. '''
        if isinstance(table, str):
            table = getattr(self.db, table)
        return table

    # def insert_one(self, table, key, json):
    #     key['_value'] = json
    #     self.table(table).insert_one(key)
    def insert_one(self, table, record):
        self.table(table).insert_one(record)

    def remove(self, table, cond):
        self.table(table).remove(cond)

    def find_one(self, table, cond):
        '''
        Find one record.

        cond: dic
           something like {'author': 'Mike'}
        '''
        return self.table(table).find_one(cond)

    def find_sections(self, table, cond, sections, key, limit=-1):

        if limit == -1:
            return self.table(table).find(cond, sections).sort(key)
        else:
            return self.table(table).find(cond, sections).sort(key).limit(limit)

    def find(self, table, cond):
        '''
        Find records.

        cond: dic
           something like {'author': 'Mike'}
        '''
        return self.table(table).find(cond)

    def finds(self, table, cond):
        '''
        Find records.

        cond: dic
           something like {'author': 'Mike'}
        '''
        return [r for r in self.table(table).find(cond)]


if __name__ == '__main__':
    import _config
    from pprint import pprint

    db = MongoDB(_config.db_name)
    records = db.finds(_config.table_name, {'type': 'kpi'})
    pprint(records)
