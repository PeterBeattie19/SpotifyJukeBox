from spotipy.oauth2 import SpotifyOAuth


class SpotifyActions:
    def __init__(self, client_id, client_secret, scope, redirect_uri):
        self.sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                                     scope=scope)

    @staticmethod
    def create_playlist(party):
        sp = party.spotify
        return sp.user_playlist_create(user=party.user, name=party.party_name)

    @staticmethod
    def add_song_to_playlist(party, song_id):
        sp = party.spotify
        sp.user_playlist_add_tracks(user=party.user, playlist_id=party.playlist_id, tracks=[song_id])

    @staticmethod
    def get_playlist(party):
        sp = party.spotify
        return sp.user_playlist(user=party.user, playlist_id=party.playlist_id)

    @staticmethod
    def get_current_track(party):
        sp = party.spotify
        user = party.user
        return user.currently_playing()

    def get_authorize_url(self):
        return self.sp_oauth.get_authorize_url()

    def get_access_token(self, code):
        return self.sp_oauth.get_access_token(code)["access_token"]

    @staticmethod
    def find_song(party, song_name, filter, artist_name=None):
        sp = party.spotify
        search_results = sp.search(song_name)
        if artist_name:
            song_dict = list(filter(lambda x: x['album']['artists'][0]['name'] == artist_name,
                                    search_results['tracks']['items']))[0]
            return song_dict['id']
        return search_results['tracks']["items"][0]["id"]

    @staticmethod
    def parse_link_to_uri(link):
        start = link.rindex('/')+1
        stop = link.index('?')
        track = link[start:stop]
        spotify_uri = "spotify:track:{}".format(track)
        return spotify_uri
