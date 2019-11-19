from pprint import pprint
from json_database import JsonDatabase
from flask import Flask,  request, render_template, url_for, redirect
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify


database_file_name = "database.json"
client_id = "53f79d1ffdbe4a2ca762790a31bceed4"
client_secret = "1605574c67e84fee959c5da3076fad02"
scope = 'user-library-read playlist-modify-public'
redirect_uri = "http://127.0.0.1:5000/sptfy_auth"
spau = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                    scope=scope)


app = Flask(__name__)
database = JsonDatabase(database_file_name, write_freq=1)


# TODO Maybe these 2 methods can be implemented in a SpotifyActions class
def get_access_token(code, spot_oauth):
    res = spot_oauth.get_access_token(code)
    return res["access_token"]


def get_authorize_url(spot_oauth):
    return spot_oauth.get_authorize_url()


def _add_party_to_database(db, playlist_id, user_name, party_name, auth_code, password):
    # TODO I don't like how the field names are hard coded here, ideally there should be some sort of Party object.
    _dict = {"playlist_id": playlist_id, "user_name": user_name, "party_name": party_name, "auth_code": auth_code,
             "password": password}
    db.insert(_dict)


# TODO this should ideally call a method from a SpotifyActions object, mentioned above.
def _create_party(user_name, party_name, auth_token):
    sp = Spotify(auth=auth_token)
    playlist_details = sp.user_playlist_create(user=user_name, name=party_name)
    return playlist_details


# TODO again; these next 2 methods should be in Spotify actions and should interact with a Party object or something
def _find_song(song_name, artist_name, sp):
    search_results = sp.search(song_name)
    if artist_name:
        song_dict = list(filter(lambda x: x['album']['artists'][0]['name'] == artist_name,
                                search_results['tracks']['items']))[0]
        pprint(song_dict['uri'])
        return song_dict['id']
    return search_results['tracks']["items"][0]["id"]


def _add_song_to_party(party_dict, song_id, sp):
    sp.user_playlist_add_tracks(party_dict["user_name"], party_dict["playlist_id"], [song_id])


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/sptfy_auth", methods=['GET', 'POST'])
def auth():
    if request.method == "POST":
        # Create playlist and its details, along with others, to the database.
        _form = request.form
        playlist_creation_details = _create_party(_form["user_name"], _form["party_name"], _form["auth_code"])
        _add_party_to_database(database, playlist_creation_details["id"], _form["user_name"], _form["party_name"],
                               _form["auth_code"], _form["party_password"])
        return redirect(url_for("home"))
    code = request.args.get("code")
    return render_template("create_party.html", auth_code_=get_access_token(code, spau))


@app.route("/get_auth_code")
def get_auth():
    return redirect(get_authorize_url(spau))


@app.route("/add_song", methods=['GET', 'POST'])
def add_song():
    if request.method == "POST":
        print(request.form)
        # Find Songs and add it to the party playlist
        party_details = database.select("party_name", request.form["party_name"])[0]
        sp = Spotify(auth=party_details["auth_code"])
        song_id = _find_song(request.form["song_name"], request.form["artist_name"], sp)
        _add_song_to_party(party_details, song_id, sp)
        return render_template("home.html")

    return render_template("add_song.html")
