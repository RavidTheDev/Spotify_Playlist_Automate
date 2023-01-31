import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import  SpotifyOAuth
import os


CLIENT_ID= os.environ['CLIENT_ID']
CLIENT_SECRET=os.environ['CLIENT_SECRET']
URI="https://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
year_selection= "2012-08-15" #input("Which year do you want to travel? YYY-MM-DD format. ")

#webbrowser.open(f"https://www.billboard.com/charts/hot-100/{year_selection}")//debuging purpuse

response=requests.get(f"https://www.billboard.com/charts/hot-100/{year_selection}")

list_page=response.text
soup=BeautifulSoup(list_page,"html.parser")

# songs = soup.find_all("h3", "a-no-trucate")
# song_names = [song.getText(strip=True) for song in songs]
songs_names=[song.getText(strip=True) for song in soup.find_all("h3", "a-no-trucate")]


song_uris = []
year = year_selection.split("-")[0]
for song in songs_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{year_selection} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print(songs_names)


