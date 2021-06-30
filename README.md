# SpotifyAPI-ETL-Airflow-AWS
Scheduled automated system for adding random tracks to a Spotify playlist.

### **Project motivation** 
Recommendation systems try to find contents that a person might like. This structure mostly results in a system where similar results are suggested. To explore the outside of this bubble and meet with new tracks I wanted to randomize the track search. And thanks to randomize track request I have come across with new composers. Here is an example: https://www.youtube.com/watch?v=tFIIMa0hKNI.

All the tracks which randomly added to playlist during the development of project can be found here -> https://open.spotify.com/playlist/7xA9OjNeAAaBvZ2WJLHbDT

Purpose of the repository in a nutshell,
    
    - Spotify Application : (added.)
        Create a random string  
        Search this string on Spotify
        Retrieve the first 3 track of the search result
        Pick one random track
        Add this track to playlist
        Log the process
    
    - Airflow, scheduling : (added. June 30, 2021)
        Scheduling this process with airflow to run for 365 days once in a day
       
    - Amazon AWS : (will be added)
        Running on AWS instance


### **A brief example of Spotify API use case**

In order to to achieve 'Spotify Application' section, 2 API request is necessary. And these requests requires [authorization](https://developer.spotify.com/documentation/general/guides/authorization-guide/) requests. The authorization process is explained in detail in [auth.py](https://github.com/rootloginson/SpotifyAPI-ETL-Airflow-AWS/blob/master/auth.py) file.

  1. API request for [**search**](https://developer.spotify.com/documentation/web-api/reference/#endpoint-search)
  
      - Access Token for Spotify search can be obtain with [Client Credentials Flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow). For this authorization type ***client_id*** and ***client_secret*** is required which can be obtained from developer dashboard. This type of authorization does not require user confirmation of the application.
      
      
  2. API request for [**adding item to playlist**](https://developer.spotify.com/documentation/web-api/reference/#endpoint-add-tracks-to-playlist)
      - Access Token for Spotify search can be obtain with [Authorization Code Flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow). For this authorization type ***client_id***, ***client_secret*** and ***refresh token*** is required. Refresh Token is permanently valid unless authorization is deleted by the user. Refresh token can be obtain by following the processes that is defined in the docstrings of *auth.Tokens* class. In a nutshell:
      
          - Request a url. Click the url.
          - Give authorization access to application with the user account.
          - Get the redirected url and extract the **'code'** value from the url.
          - Request a refresh token with this code.
          - Use this refresh token to get 'access_token'.
          
(*! All the access tokens expires in 3600 seconds.*)

**How to use the app with minimum information?**

- To get random track, only a client_id and client_secret is needed. These can be found on Spotify Developer Dashboard. These strings will take the place of the ones in *hidden.py*. Then, track uri can be obtained by running ```demo_get_track.py``` script. (This process is "*API request for search*", as mentioned above.)


- If the application is to be used as intended, refresh token will be needed. And this process has been briefly described above. A detailed explanation and process map can be found in class docstrings and method docstrings. After getting the refresh token, user that authorized the application needs to create a public playlist and change the 'PLAYLIST_ID' global variable in spotify_app.py with the id of this playlist that is newly created.

<p>&nbsp;</p>

---
#### **Code structure**
Note: The order of execution and the description of the operations to be performed are explained in detail in the documentation of the classes and it's methods.

```python
# located in -> custom_exception_check.py
# used for request exception control, error control, logging
class CustomRequestExceptionCheck(object)

# located in -> auth.py
# used for authorizations and getting access tokens 
class Tokens(CustomRequestExceptionCheck)

# located in -> api_task_requests.py
# used for API requests, tasks like search, add item etc. 
class Spochastify(CustomRequestExceptionCheck)  
# since the track selection process is random, 
# I combined the word stochastic and the name of spotify :)

# -> hidden.py stores the client_id, client_secret and refresh token
```
*Note: lambda expressions that is used with request.get, request.post is to send the request for exception checking. 'CustomRequestExceptionCheck' class handles these checks, log processes. And writes to the log file.
It is aimed to apply the DRY principle. New Authorization Flows can be added into auth.Tokens class with similar structure. Requests like search, create playlist can be added to api_task_requests.Spochastify. Or they can be used separately depends on a need.*
    
In addition , there is an advanced library called [***Spotipy Library***](https://spotipy.readthedocs.io/en/2.18.0/).


#### **Interpreting the Logs**

Log file contains:

   - function running time: gmt +0 
   - name of the file that contains "CustomRequestExceptionCheck" class
   - request status : "SUCCESS", "ERROR" or "FAILED"
   - status_code, eg. 200, 201, 400 etc.
   - the name of the method from which it was called.

For example:

> If there is no internet connection; exception control will catch the Connection Error. Method will return **None**. run_spotify_app function will check the condition and terminate the function with return value None.
    
> If there is a valid client_id and secret_id; Tokens.get_client_credential_access_token method call will be successful. And if there is a invalid refresh token, Tokens.get_access_token_with_scope method call will cause a HTTPError.

> If there is a request from Spochastify.post_search_request more than 1 time (2 times in given case), even the request is successful, that indicates the first search request returned a empty track list.

[Python log file example of test cases](https://github.com/rootloginson/SpotifyAPI-ETL-Airflow-AWS/blob/master/spotify_app.log)

[Airflow log file of triggered spotify_app](https://raw.githubusercontent.com/rootloginson/SpotifyAPI-ETL-Airflow-AWS/master/airflow_execution_log/airflow_log_triggered_spotify_app.png)

---
<p>&nbsp;</p>

### Time Saver for developers:
For GET and POST requests, some endpoints and parameters are passed as arguments and keyword arguments. Some of them are passed as encoded url.
