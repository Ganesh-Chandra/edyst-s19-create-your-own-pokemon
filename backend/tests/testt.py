import os
import sys
import simplejson as json
import unittest
import requests
import sqlite3
from flask import jsonify
sys.path.append('../') # path to import app

from app import app

TEST_DB = 'test.sqlite'


class Pokemon_Test_Methods(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        
    @classmethod 
    def tearDownClass(self):
        pass
        

    def test_create_pokemon(self):
        print("---------------------------- testing create pokemon  ----------------------------")

        reqdata = { "pokemon": { "name": "charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }
        
        resdata = { "pokemon": { "id": 1, "name": "charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }
        
        res = self.app.post("http://127.0.0.1:8006/api/pokemon", data = json.dumps(reqdata), content_type='application/json')
        code=res.status_code
        res = json.loads(res.data)
        self.assertEqual(resdata,res)
        self.assertEqual(code, 200)
    
        print("---------------------------- create pokemon  test pass ----------------------------")
    
    def test_get_pokemon(self):
        print("---------------------------- testing get pokemon ----------------------------")
        
        check = { "pokemon": { "id": 1, "name": "charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }

        res = self.app.get("http://127.0.0.1:8006/api/pokemon/1")
        code=res.status_code
        res = json.loads(res.data)
        self.assertEqual(check, res)
        self.assertEqual(code, 200)
    
        print("----------------------------Get pokemon  test pass ----------------------------")

    
    def test_update_pokemon(self):
        print("----------------------------testing update pokemon ----------------------------")
        
        updata = { "pokemon": { "name": "updated_charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }

        resdata = { "pokemon": { "id": 1, "name": "updated_charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }

        res = self.app.patch("http://127.0.0.1:8006/api/pokemon/1", data = json.dumps(updata), content_type='application/json')
        code=res.status_code
        res = json.loads(res.data)

        self.assertEqual(resdata, res)
        self.assertEqual(code, 200)

        print("----------------------------Update pokemon test pass ----------------------------")


    
    def test_zzzdelete_pokemon(self):
        print("----------------------------testing delete pokemon ----------------------------")
        
        resdata = { "pokemon": { "id": 1, "name": "updated_charmander", "sprite": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "cardColours": {"fg":"#eeeeee", "bg": "#3e3e3e", "desc": "#111111" } } }

        res = self.app.delete("http://127.0.0.1:8006/api/pokemon/1")
        code=res.status_code
        res = json.loads(res.data)

        self.assertEqual(resdata, res)
        self.assertEqual(code, 200)

        print("----------------------------Delete pokemon test pass ----------------------------")


if __name__ == '__main__':
    unittest.main()
