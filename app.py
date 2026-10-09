import requests
import os
from dotenv import load_dotenv
import base64
from requests import post, get
load_dotenv()
import json
import hashlib

artistName = input("Enter the artist's name you would like to search: ")

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}



def search_tracks_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": f"artist:{artist_name}",
        "type": "track",
        "limit": 10
    }

   
    result = get(url, headers = headers, params = params)
    result.raise_for_status()
    print(result.json())

    data = result.json()
    tracks = data["tracks"]["items"]
    if len(tracks) == 0:
        print("error, could not return the songs you were looking for")
        return None
        
    else:
        track_list = []
        for track in tracks:
            artist_name = [artist["name"] for artist in track["artists"]]
            print(track["name"], "-", ", ".join(artist_name))
            track_list.append(track["name"])
        return track_list
def generateRandomString(length):
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    values = os.urandom(length)
    return "".join(possible[x % len(possible)] for x in values)

def sha256(codeString):
    data = codeString.encode("utf-8")
    hash_object = hashlib.sha256(data)
    hex_dig = hash_object.hexdigest()
    return hex_dig.digest()
    
def search_for_artist(token, userInput):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    parameters = {
        "q": f"artist: {userInput}",
        "type": "track",
        "limit": 10
        }
    result = get(url, headers = headers, params = parameters)
    status = result.raise_for_status()
    # print(status)
    # print(result.status_code)
    # print(result.text)
    data = result.json()
    tracks = data["tracks"]["items"]
    track_list = []
    for track in tracks:
        artist_names = []
        for artist in track["artists"]:
            artist_names.append(artist["name"])
        track_list.append(", ".join(artist_names) + " - " + track["name"] + " - " + track["id"])
    return track_list


            
token = get_token()
tracks = search_for_artist(token, artistName)
codeVerifier = generateRandomString(64)
hashed = sha256(codeVerifier)
code_challenge = base64.urlsafe_b64encode(hashed).decode("utf-8").rstrip("=")

print(tracks)   
