#!/usr/bin/python
import unittest

class GarbanzoTestCase(unittest.TestCase):

    def setUp(self):
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()

    # def tearDown(self):
        # Turn off stuff.

    def provinces(self):
        return self.app.get('http://pythonbox/garbanzo-api/provinces', follow_redirects=True)

    def test_provinces(self):
        rv = self.provinces()
        assert b'You were logged in' in rv.data

if __name__ == '__main__':
    unittest.main()
