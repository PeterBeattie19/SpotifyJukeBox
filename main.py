import sys
import time
import base64
from pprint import pprint
from json_database import JsonDatabase
import urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
import requests
import spotipy.oauth2 as oauth2
from flask import request
import json
from json_database import JsonDatabase


db = JsonDatabase("database.json", write_freq=1)
db.insert({"name": "joan"})


exit()

client_id = "53f79d1ffdbe4a2ca762790a31bceed4"
client_secret = "1605574c67e84fee959c5da3076fad02"
scope = 'user-library-read'
username = "peterpython"
redirect_uri = "http://127.0.0.1:5000/sptfy_auth"


def get_access_token(code, spot_oauth):
    res = spot_oauth.get_access_token(code)
    return res["access_token"]



sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope, cache_path=".cache-" + username)

auth_url = sp_oauth.get_authorize_url()
print(auth_url)
r1 = requests.get(auth_url).url
print(r1)
