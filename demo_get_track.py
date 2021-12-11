import random
import auth
import api_task_requests
from custom_exception_check import trigger_starttime_log


def random_string() -> str:
    consonants = "bcçdfgğhjklmnpqrstvwxyz"
    vowels = "aeıioöuü"
    word_len = random.randint(2, 5)
    word = []
    for i in range(word_len):
        if random.random() < 0.5:
            word.append(random.choice(vowels))
        else:
            word.append(random.choice(consonants))
    return ''.join(word)


def run_spotify_app():
    # instance for api requests and helper methods
    spochastify = api_task_requests.Spochastify()
    # instance for access token requests
    token = auth.Tokens()
    client_credential_access_token = ''

    r = None                 # requests.models.Response object
    r_search = None          # requests.models.Response object
    search_word = ''         # word for track search request
    tracks_uri_list = []     # track list retrieved due to search request
    random_track_uri = None  # track to add to playlist

    # adds approximate function call time(GMT 0:00 format) to log file.
    _ = trigger_starttime_log()

    # 'ACCESS TOKEN' REQUESTS
    # requesting client credential access token
    r = token.get_client_credential_access_token()
    if r is None:   # exception contol such as Connection Error
        return None
    # 200: OK - The request has succeeded.
    elif r.status_code == 200:
        # 'Access Token' is received
        client_credential_access_token = r.json()['access_token']
    else:
        return r

    # 'SEARCH' REQUEST
    # range(5) is; number of attempts if track list is empty.
    for i in range(5):
        # get a random search string
        search_word = random_string()
        # Requesting random track search
        r_search = spochastify.post_search_request(
                        client_credential_access_token,
                        search_word
                        )
        if r_search is None:   # exception contol such as Connection Error
            return None
        # 200: OK - The request has succeeded.
        elif r_search.status_code == 200:
            tracks_uri_list = spochastify.get_list_of_tracks(r_search)
        else:
            return r_search
        # if there is track in track list, pick a random track
        if tracks_uri_list:
            random_track_uri = random.choice(tracks_uri_list)
            return random_track_uri
    else:
        print("Failed to retrieve any tracks list")
        return None


if __name__ == '__main__':
    res = run_spotify_app()
    print(res)
