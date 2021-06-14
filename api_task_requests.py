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
            tracks_uri_list (list)  : If tracks are found in the search,
                                      returns id list of tracks
            None        (NoneType)  : If search result is empty.

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
        returned_items = results['tracks']['items']
        if returned_items:
            return [item['uri'] for item in returned_items]
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
