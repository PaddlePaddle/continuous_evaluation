import bson
from pymongo import MongoClient
import redis
from utils import log


class RedisDB(object):
    ''' An higher interface for the Redis database. '''

    def __init__(self, host='localhost', port=6379, db=0, test=False):
        db = 15 if test else db
        self.test = test
        self.rd = redis.StrictRedis(host=host, port=port, db=db)
        log.warn('Connect DB in %s:%d, id: %d' % (host, port, db))
        if test:
            log.warn('Run DB in testing mode.')

    def set(self, key, value):
        '''
        Set a record.
        :param key(str): the id of this record.
        :param value(str): the value of this record
        :return: bool(whether succeed)
        '''
        self.rd.set(key, value)

    def get(self, key):
        '''
        Query a record.

        :param key(str): id of the record
        :return: str or None
        '''
        return self.rd.get(key)

    def delete(self, *keys):
        '''
        Delete one or more records.

        :param key(str): id of the record.
        :return: bool (succeed)
        '''
        return self.rd.delete(*keys)

    def publish_message(self, channel, message):
        '''
        Publish a message to a channel.

        :param channel(str: name of a channel.
        :param message(str): content of a message.
        :return:
          - int: number of channels it sends to.
        '''
        return self.rd.publish(channel, message)

    def new_subpub(self):
        '''
        Create a new publish subscribe pattern.
        '''
        return self.rd.pubsub()

def escape_bstr(s, code='ascii'):
    '''
    Escape binary string.
    :param s(binary string)
    :return: str
    '''
    return s.decode(code)

class MongoDB(object):
    def __init__(self, dbname, host='localhost', port=27017):
        log.warn('The MongoDB interface is deprecated. The current DB is Redis.')
        self.client = MongoClient(host, port)
        self.db = getattr(self.client, dbname)

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

    def find_sections(self, table, cond, sections, key):

        return self.table(table).find(cond, sections).sort(key)

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
