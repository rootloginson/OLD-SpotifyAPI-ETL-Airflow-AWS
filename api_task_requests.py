import requests
from custom_exception_check import CustomRequestExceptionCheck
from urllib.parse import urlencode


class Spochastify(CustomRequestExceptionCheck):

    def post_search_request(self, client_credential_access_token: str,
                            search_word: str) -> requests.models.Response:
        """
        Argument :
            client_credential_access_token (str)
            search_word (str): a string for the spotify search request

        Returns  :
            r : requests.models.Response object
                   (OK:200 - The request has succeeded.)

        """
        endpoint = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f'Bearer {client_credential_access_token}',
            "Accept": "application/json",
            "Content-Type": "application/json"
            }
        data = {'q': search_word, 'type': 'track', 'limit': '3'}
        url = endpoint + '?' + urlencode(data)
        r = self.request_call_with_exception_check(
                lambda: requests.get(url, headers=headers),
                )
        return r

    def get_list_of_tracks(self, r_search: requests.models.Response) -> list:
        """
        Argument :
            r_search (requests.models.Response object) :
                response object of the 'post_search_request' method

        Returns  :
            returned_items_list (list)  : If tracks are found in the search,
                                          returns id list of tracks
            None        (NoneType)      : If search result is empty.

        >>> r_search['tracks']
        dict_keys(['href', 'items', 'limit', 'next',
                   'offset', 'previous', 'total'])

        length of r_search['tracks']['items'] is the number of tracks retrieved.
        Each of them has track datas.
        >>> r_search['tracks']['items']
        dict_keys(['album', 'artists', 'available_markets', 'disc_number',
                   'duration_ms', 'explicit', 'external_ids',
                   'external_urls', 'href', 'id', 'is_local', 'name',
                   'popularity', 'preview_url', 'track_number',
                   'type', 'uri'])
        """
        results = r_search.json()
        returned_items_list = results['tracks']['items']
        if returned_items_list:
            return returned_items_list
        else:
            return None

    def add_track_to_playlist(self, access_token_with_scope: str,
                              track_uri: str,
                              playlist_id: str) -> requests.models.Response:
        """
        Argument :
            access_token_with_scope (str)
            track_uri (str) : track_uri of a Spotify track

        Returns  :
            r : requests.models.Response object
                    (OK:201 - The request has succeeded.)
        """
        endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token_with_scope}"
            }
        data = {"uris": track_uri}
        url = endpoint + '?' + urlencode(data)
        r = self.request_call_with_exception_check(
                lambda: requests.post(url, headers=headers),
                )
        return r

    def extract_track_info(self, random_track_item: dict) -> dict:
        """
            Argument :
                random_track_item (dict) : Information about spotify track

            Returns  :
                track_details (dict)  :
                    track_details = {
                        'artist_name': artist_name,
                        'album_name': album_name,
                        'track_name': track_name,
                        'track_external_urls': track_external_urls,
                        'track_uri': track_uri
                    }
        """
        try:
            artist_name = random_track_item['artists'][0]['name']
        except KeyError:
            artist_name = 'Not Available'

        try:
            album_name = random_track_item['album']['name']
        except KeyError:
            album_name = 'Not Available'

        try:
            track_name = random_track_item['name']
        except KeyError:
            track_name = 'Not Available'

        try:
            track_external_urls = random_track_item['external_urls']['spotify']
        except KeyError:
            track_external_urls = 'Not Available'

        try:
            track_uri = random_track_item['uri']  #to add into playlist
        except KeyError:
            track_uri = 'Not Available'

        track_details = {
            'artist_name': artist_name,
            'album_name': album_name,
            'track_name': track_name,
            'track_external_urls': track_external_urls,
            'track_uri': track_uri
            }

        return track_details

