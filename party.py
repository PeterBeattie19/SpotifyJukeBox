from spotipy import Spotify


class Party:
    def __init__(self, party_name, user, auth_code, playlist_id=None):
        self._party_name = party_name
        self._user = user
        self._playlist_id = playlist_id
        self._auth_code = auth_code

    @property
    def spotify(self):
        return Spotify(auth=self._auth_code)

    @property
    def user(self):
        return self._user

    @property
    def party_name(self):
        return self._party_name

    @property
    def playlist_id(self):
        return self._playlist_id

    @playlist_id.setter
    def playlist_id(self, val):
        self._playlist_id = val

    @property
    def auth_code(self):
        return self._auth_code



