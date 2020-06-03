import os
import unittest
from unittest.mock import patch
from app import app 

class BasicTests(unittest.TestCase):

        def test_home(self):
                tester = app.test_client(self)
                response = tester.get('/', content_type='html/text')
                self.assertEqual(response.status_code, 200)
                self.assertNotIn(b'You\'re new url is:', response.data)
        
        # def test_home(self):
        #         tester = app.test_client(self)
        #         response = tester.get('/', content_type='html/text')
        #         self.assertEqual(response.status_code, 200)
        #         self.assertIn(b'You\'re new url is:', response.data)

        # def client():
        #         db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        #         app.config['TESTING'] = True

        #         with app.test_client() as client:
        #                 with app_context():
        #                         init_db()
        #                 yield client

        #         os.close(db_fd)
        #         os.unlink(app.config['DATABASE'])


        def test_new_url(client):
                rv = client.post('/new_url', data=dict(
                url='https://www.google.com'
                ), follow_redirects=True)
                assert b'No entries here so far' not in rv.data
                assert b'&lt;https://www.google.com&gt;' in rv.data

if __name__ == '__main__':
        unittest.main()
