from json_database import JsonDatabase
from flask import Flask,  request, render_template, url_for, redirect
from spotipy.oauth2 import SpotifyOAuth
from party import Party
from spotify_actions import SpotifyActions


# TODO Move these constants to config file
database_file_name = "database.json"

client_id = "53f79d1ffdbe4a2ca762790a31bceed4"
client_secret = "1605574c67e84fee959c5da3076fad02"
scope = 'user-library-read playlist-modify-public'
redirect_uri = "http://127.0.0.1:5000/sptfy_auth"

party_name_key = "party_name"
user_name_key = "user_name"
auth_code_key = "auth_code"
playlist_id_key = "playlist_id"
song_name_key = "song_name"
artist_name_key = "artist_name"


spot_actions = SpotifyActions(client_id, client_secret, scope, redirect_uri)

spau = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                    scope=scope)


app = Flask(__name__)
database = JsonDatabase(database_file_name, write_freq=1)


def _add_party_to_database(db, party):
    _dict = {playlist_id_key: party.playlist_id, user_name_key: party.user, party_name_key: party.party_name,
             auth_code_key: party.auth_code}
    db.insert(_dict)


@app.route('/')
def home():
    return render_template("home.html")


@app.route("/sptfy_auth", methods=['GET', 'POST'])
def auth():
    if request.method == "POST":
        # Create playlist and its details, along with others, to the database.
        _form = request.form
        # Create Party object using details from form
        party_ = Party(_form[party_name_key], _form[user_name_key], _form[auth_code_key])
        # Create a playlist using details from Party Objecy
        playlist_creation_details = spot_actions.create_playlist(party_)
        # Set Party object's playlist_id property to the id from the newly created playlist.
        party_.playlist_id = playlist_creation_details["id"]
        # Add Party to Database
        _add_party_to_database(database, party_)
        return redirect(url_for("home"))
    code = request.args.get("code")
    return render_template("create_party.html", auth_code_=spot_actions.get_access_token(code))


@app.route("/get_auth_code")
def get_auth():
    return redirect(spot_actions.get_authorize_url())


@app.route("/add_song", methods=['GET', 'POST'])
def add_song():
    if request.method == "POST":
        # Get Party details from database
        try:
            party_details = database.select(party_name_key, request.form[party_name_key])[0]
        except:
            return render_template("home.html")
        # Create new Party object using details pulled from database
        party_ = Party(party_details[party_name_key], party_details[user_name_key], party_details[auth_code_key],
                       party_details[playlist_id_key])
        # Get Song ID
        # song_id = spot_actions.find_song(party_, request.form[song_name_key], request.form[artist_name_key])
        # Add the song to the party playlist
        song_id = request.form["uri"]
        try:
            spot_actions.add_song_to_playlist(party_, song_id)
        except:
            return render_template("home.html")
        return render_template("home.html")

    return render_template("add_song.html")
