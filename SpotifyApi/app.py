#first we need flask then we need to get urls right.so we use url_for #redirect for redirect
#to run flask give .py path(where it is actually)$env:FLASK_APP="YOUR FULL PATH to the  file"
from flask import Flask, request, url_for, session, redirect

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
app = Flask(__name__)

app.secret_key = 'lolol1337hehehehe'
app.config['SESSION_COOKIE_NAME'] = 'Ahanafs Cookie'
token_key= "token_info"

@app.route('/')
def indexLogin():#creat spotify auth and url
    spotify_auth = create_spotify_oauth()
    auth_url = spotify_auth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():#use different name than route name
    spotify_auth = create_spotify_oauth()
    session.clear() #clearing previous sessions
    code = request.args.get('code')#because flask doesnt take arg so we do it this way
    token_info = spotify_auth.get_access_token(code)#getting access token from spotify
    session[token_key] = token_info #replacing the token with spotify token and saving it
    return redirect(url_for('getTracks', _external=True))#now that we have access token so we can redirect the user to getTracks


@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not signed in")
        return(redirect(url_for('indexLogin',_external=False)))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_song = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50, offset=iter * 50)['items']
        iter += 1
        all_song += items
        if len(items)<50:#base case
            break
    return(len(all_song))
     

    
def get_token():
    token_info = session.get(token_key, None) #getiing info from the saved token if none just pretend None
    if not token_info:#if there is no token then we redrirect the user to the homepage
        raise "exception"
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    #lets just get a new one
    if (is_expired):
        spotify_auth = create_spotify_oauth()
        token_info = spotify_auth.refresh_access_token(token_info['refresh_token'])
    return token_info
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id ='754dfee3671c4623ba0996b9ee34b830',
        client_secret ='848f234c1e654926ba163416d724c421',
        redirect_uri =url_for('redirectPage', _external=True),#url for to get url ez way then the function name
        scope="user-library-read"
    )

