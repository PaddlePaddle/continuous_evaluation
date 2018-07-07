from db import RedisDB, escape_bstr
import unittest


class RedisDBTester(unittest.TestCase):

    def setUp(self):
        self.db = RedisDB(test=True)

    def test_set_get(self):
        self.db.set('name', 'xxx0')
        rcd = self.db.get('name').decode('ascii')
        self.assertEqual(rcd, 'xxx0')

    def test_not_found(self):
        res = self.db.get('no-key')
        self.assertEqual(res, None)

    def test_subscribe_publish(self):
        '''
        Test Redis subscribe and publish.
        '''
        p = self.db.new_subpub()
        p.subscribe('channel0')
        datas = ['hello', 'world']
        for data in datas:
            self.db.publish_message('channel0', data)

        message = p.get_message()
        num_messages = message['data']
        for i in range(num_messages):
            message = p.get_message()
            self.assertEqual(message['type'], 'message')
            self.assertEqual(escape_bstr(message['data']), datas[i])

if __name__ == '__main__':
    unittest.main()