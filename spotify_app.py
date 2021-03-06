import random
import auth
import api_task_requests
from custom_exception_check import trigger_starttime_log
import database_update
from datetime import datetime, timezone


def get_playlist_id():
    playlist_id = '7xA9OjNeAAaBvZ2WJLHbDT'
    return playlist_id


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
    access_token_with_scope = ''

    r = None               # requests.models.Response object
    r_search = None        # requests.models.Response object
    r_add_track = None     # requests.models.Response object
    search_word = ''           # word for track search request
    returned_items_list = []   # track list retrieved due to search request
    random_track_uri = None    # track to add to playlist
    track_details = None       # information about the track

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

    # Requesting access token with scope
    r = token.get_access_token_with_scope()
    if r is None:   # exception contol such as Connection Error
        return None
    # 200: OK - The request has succeeded.
    if r.status_code == 200:
        # 'Access Token with scope' is received
        access_token_with_scope = r.json()['access_token']
    else:
        return r

    # 'SEARCH' and 'ADD ITEM' REQUESTS
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
            returned_items_list = spochastify.get_list_of_tracks(r_search)
        else:
            return r_search
        # if there is track in track list, pick a random track
        if returned_items_list:
            # pick one of the returned items
            random_track_item = random.choice(returned_items_list)
            track_details = spochastify.extract_track_info(random_track_item)
            random_track_uri = track_details['track_uri']
            break
    else:
        # Failed to retrieve any tracks list
        return (r_search, search_word)

    # requesting item add into the playlist
    r_add_track = spochastify.add_track_to_playlist(
                          access_token_with_scope,
                          random_track_uri,
                          get_playlist_id()
                          )
    if r_add_track is None:   # exception contol such as Connection Error
        return None
    # 201: OK - The request has succeeded.
    elif r_add_track.status_code == 201:
        # playlist add time. UTC +0
        dt_now = datetime.now(timezone.utc)
        # add track details into sql database
        database_update.update_db(track_details, dt_now)
        return random_track_uri, search_word
    else:
        return r_add_track
    # successful exit code
    return 0
