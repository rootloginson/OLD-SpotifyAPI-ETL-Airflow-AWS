import hidden
import requests
import base64
from urllib.parse import urlencode
from custom_exception_check import CustomRequestExceptionCheck


class Tokens(CustomRequestExceptionCheck):
    """
    The tokens in the Token class :

        1. Access Token for "Client Credentials Flow"
        2. Authorization Code Flow (abbrv. is acf)
            i)   Authorization access url
            ii)  Refresh Token via (i)
            iii) Access Token with scope via (i) > (ii)
                    > access token for adding tracks to playlist

    Requires :
        client_id     : Developer's client id
        client_secret : Developer's client secret
        redirect_uri  : This is defined by the developer.
                        *** It is not the redirected url ***


    A refresh token is required for requests that require user permission.

    How to obtain a token to make track search and receive datas from Spotify:

        -> Call get_client_credential_access_token method
                Returns a header that contains access token.


    How to obtain a token to add track into user's playlist:

        -> Call "get_user_authorization_url" method.
            Important !! Scope of the token is defined in this method.

            -> Through this link user will authorize the application.
               After the authorization, Spotify will direct the user to a
               different link. In this link there is an code variable.
               *** Obtain the code value. ***

        -> Call "get_refresh_token method" with the code value.
            -> method returns a request_object.
               request_object.header has access token.
               To obtain refresh_token use,
               request_object.json()headers['access_token']

        -> Call "get_access_token_with_scope" method.
           Refresh token is defined in the method as an object and imported
           from different module.
           This method will return
           a request_object. headers['access_token'] has the access token.
           !! Only this token can be used to add tracks into playlist.

    """

    def get_base64encoded(self, client_id=hidden.client_id,
                          client_secret=hidden.client_secret) -> str:
        """
        Arguments :
            client_id     (str) : Developer's client_id
            client_secret (str) : Developer's client_secret

        Returns :
            Authorization Value : Basic <base64 encoded client_id:client_secret>
        """
        auth_value = f"{client_id}:{client_secret}"
        auth_value_conversion = base64.b64encode(auth_value.encode())
        return auth_value_conversion.decode()

    def get_client_credential_access_token(self) -> requests.models.Response:
        """
        Purpose :
            Getting the "Access Token"
            to make search requiest in spotify and retrieve search results.

        Spotify API, Client Credentials Flow
        Section 1 ->   Have your application request authorization

                ! Does not require user's authorization for access.

        Requires :
            Authorization Value : Basic <base64 encoded client_id:client_secret>

        Returns :
            {
                "access_token": "NgCXRKc...MzYjw",
                "token_type": "bearer",
                "expires_in": 3600,
            }
        """
        endpoint = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "client_credentials"
            }
        headers = {
            "Authorization": f"Basic {self.get_base64encoded()}"
            }
        r = self.request_call_with_exception_check(
                lambda: requests.post(endpoint, data=data, headers=headers),
                )
        return r

    # Authorization Code Flow, authorize the account, get redirected link
    def get_user_authorization_url(self) -> str:
        """
        Purpose :
            Getting the url address in order to authorize the application by user.
            Authorization for adding tracks to user's playlist.

        Spotify API, Authorization Code Flow,
        Section 1. ->   Have your application request authorization;
                        the user logs in and authorizes


                **** Check Class Docstring for "Requires" references ****

        Requires :
            client_id: Developer's client id

        Returns :
            url adress: A url adress for the user to give authorazation access
                        in order to obtain the access token that requires for
                        adding tracks to playlist of the user.
        """
        endpoint = "https://accounts.spotify.com/authorize"
        data = {
            "client_id": hidden.client_id,
            "response_type": "code",
            "redirect_uri": "https://www.spotify.com/callback",
            "scope": "playlist-modify-public"
            }
        url = endpoint + "?" + urlencode(data)
        r = self.request_call_with_exception_check(
                lambda: requests.get(url),
                )
        return r.url

    # Authorization Code Flow, get refresh token
    def get_refresh_token(self, code: str) -> requests.models.Response:
        """
        Purpose :
            Getting the "Refresh Token"
            to obtain the access token which allows to add tracks into playlist.

        Spotify API, Authorization Code Flow,
        Section 2. ->   Have your application request refresh and access tokens; 
                        Spotify returns access and refresh tokens


                **** Check Class Docstring for "Requires" references ****

        Requires :
            Access Token        : Authorization Code Flow > i
            code                : (code value that redirected url contains)
                                  The code value returned from the initial
                                  request to the Account
                (
                    ! redirected url adress can be obtained after authorizing
                    the access of application via the link that is provide by
                    clicking the <Tokens.get_redirected_url> method.
                    Inside of the url there is -> code="asdfsf" section.
                )

            Authorization Value : Basic <base64 encoded client_id:client_secret>

        Arguments :
            code : code value that redirected url contains

        Returns :
            {
                "access_token": "NgCXRK...MzYjw",
                "token_type": "Bearer",
                "scope": "user-read-private user-read-email",
                "expires_in": 3600,
                "refresh_token": "NgAagA...Um_SHo"
            }
        """
        endpoint = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "https://www.spotify.com/callback"
            }
        headers = {
            "Authorization": f"Basic {self.get_base64encoded()}"
            }
        r = self.request_call_with_exception_check(
                lambda: requests.post(endpoint, data=data, headers=headers),
                )
        return r

    # access token needed for adding track to playlist
    # ! The access token expires in 1 hour.
    def get_access_token_with_scope(self) -> requests.models.Response:
        """
        Purpose :
            Getting the authorized "Access Token"
            to add tracks into playlist. The access token expires in 1 hour.


        Scope: "playlist-modify-public"
            (scope is defined in get_user_authorization_url method)

        Spotify API, Authorization Code Flow,
        Section 4. ->   Requesting a refreshed access token;
                        Spotify returns a new access token to your app


                **** Check Class Docstring for "Requires" references ****

        Requires :
            Refresh Token       : Authorization Code Flow > i > ii
            Authorization Value : Basic <base64 encoded client_id:client_secret>

        Returns :
            {
                 "access_token": "NgA6ZcYI...ixn8bUQ",
                 "token_type": "Bearer",
                 "scope": "user-read-private user-read-email",
                 "expires_in": 3600
            }
        """
        endpoint = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "refresh_token",
            "refresh_token": hidden.refresh_token
            }
        headers = {
            "Authorization": f"Basic {self.get_base64encoded()}"
            }
        r = self.request_call_with_exception_check(
                lambda: requests.post(endpoint, data=data, headers=headers),
                )
        return r
