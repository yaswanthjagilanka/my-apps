"""
This module is taken from the repo `https://github.com/cyberboysumanjay/JioSaavnAPI`

author: cyberboysumanjay (https://github.com/cyberboysumanjay)
"""

import urllib3
import re
from traceback import print_exc
import ast
import json
from pyDes import *
import os
import base64
from bs4 import BeautifulSoup
import requests


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

des_cipher = des(b"38346591", ECB, b"\0\0\0\0\0\0\0\0",
                 pad=None, padmode=PAD_PKCS5)
base_url = 'https://h.saavncdn.com'
json_decoder = json.JSONDecoder()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
}

saavn_options = []

def search_from_song_id(song_id):
    song_base_url = "https://www.jiosaavn.com/api.php?cc=in&_marker=0%3F_marker%3D0&_format=json&model=Redmi_5A&__call=song.getDetails&pids=" + \
        str(song_id)
    song_response = requests.get(song_base_url)
    songs_json = list(filter(lambda x: x.startswith(
        "{"), song_response.text.splitlines()))[0]
    songs_json = json.loads(songs_json)
    try:
        songs_json[song_id]['media_url'] = generate_media_url(
            songs_json[song_id]['media_preview_url'])
    except KeyError:
        songs_json[song_id]['media_url'] = decrypt_url(
            songs_json[song_id]['encrypted_media_url'])
    songs_json[song_id]['image'] = fix_image_url(songs_json[song_id]['image'])
    songs_json[song_id]['song'] = fix_title(songs_json[song_id]['song'])
    songs_json[song_id]['album'] = fix_title(songs_json[song_id]['album'])
    return songs_json[song_id]


def search_from_query(query):
    query = query[:30]
    base_url = f"https://www.saavn.com/api.php?__call=autocomplete.get&_marker=0&query={query}&ctx=android&_format=json&_marker=0"
    response = requests.get(base_url)
    songs_json = list(filter(lambda x: x.startswith(
        "{"), response.text.splitlines()))[0]
    songs_json = json.loads(songs_json)
    songs_data = songs_json['songs']['data']
    # songs_data=[songs_data[0]]
    songs = []
    for song in songs_data:
        song_id = song['id']
        song_base_url = "https://www.jiosaavn.com/api.php?cc=in&_marker=0%3F_marker%3D0&_format=json&model=Redmi_5A&__call=song.getDetails&pids="+song_id
        song_response = requests.get(song_base_url)
        songs_json = list(filter(lambda x: x.startswith(
            "{"), song_response.text.splitlines()))[0]
        songs_json = json.loads(songs_json)
        try:
            songs_json[song_id]['media_url'] = generate_media_url(
                songs_json[song_id]['media_preview_url'])
        except KeyError:
            songs_json[song_id]['media_url'] = decrypt_url(
                songs_json[song_id]['encrypted_media_url'])
        songs_json[song_id]['image'] = fix_image_url(
            songs_json[song_id]['image'])
        songs_json[song_id]['song'] = fix_title(songs_json[song_id]['song'])

        songs_json[song_id]['album'] = fix_title(songs_json[song_id]['album'])
        songs_json[song_id]['media_url'] = check_media_url(
            songs_json[song_id]['media_url'])
        songs.append(songs_json[song_id])
    return songs


class SaavnSong():
    """Class to store saavn song tags."""

    def __init__(self, SONG):
        """SONG is supposed to be a dict."""
        self.track_name = SONG['song']
        self.release_date = self._get_proper_date(SONG['release_date'])
        self.artist_name = SONG['primary_artists']
        self.language = SONG['language']
        self.album_title =  SONG['album']
        self.lyrics_url = "None"
        self.youtube_id = "None"
        self.collection_name = SONG['album']
        self.primary_genre_name = SONG['language']
        self.artwork_url = self._get_proper_img_url(SONG['image'])
        self.track_time = self._convert_time(SONG['duration'])
        # self.album_title = SONG['album_title']
        # self.lyrics_url = SONG['lyrics_url']
        # self.youtube_id = SONG['youtube_id']

    def _convert_time(self, duration):
        in_min = int(duration)
        in_time = int(in_min / 60) + (0.01 * (in_min % 60))
        return in_time

    def _get_proper_date(self, date):
        """
        The passed date will be of the form
        YYYY-MM-DD

        We need to convert it to a timezone aware
        form.
        Preferably YYYY-MM-DDTHH:MM:SSZ
        """
        return date + 'T00:00:00Z'

    def _get_proper_img_url(self, url):
        """
        The URL provided by Saavn will be a 500x500

        We need to return it in 100x100
        """
        # return url.replace("500x500", "100x100")
        return url


def search_query(query):
    """
    Just a wrapper over the search_from_query method

    This method will return the data in the format Ytmdl wants it
    in. This will have the same attributes that all the other results
    of ytmdl meta providers have.
    """
    # results = [SaavnSong(song) for song in search_from_query(query[:29])]
    result = search_from_query(query[:29])
    if result : 
        result = SaavnSong(result[0])
    else:
        result = None 
    return result
    


def generate_media_url(url):
    url = url.replace("preview", "h")
    url = url.replace("_96_p.mp4", "_320.mp3")
    return url


def get_song_id(query):
    url = query
    songs = []
    try:
        res = requests.get(url, headers=headers, data=[('bitrate', '320')])
        id = res.text.split('"song":{"type":"')[1].split('","image":')[0].split('"id":"')[-1]
        return id
    except Exception as e:
        print_exc()
    return None


def getAlbum(albumId):
    songs_json = []
    try:
        response = requests.get(
            'https://www.jiosaavn.com/api.php?_format=json&__call=content.getAlbumDetails&albumid={0}'.format(albumId), verify=False)
        if response.status_code == 200:
            songs_json = list(filter(lambda x: x.startswith(
                "{"), response.text.splitlines()))[0]
            songs_json = json.loads(songs_json)
            songs_json['name'] = fix_title(songs_json['name'])
            songs_json['image'] = fix_image_url(songs_json['image'])
            for songs in songs_json['songs']:
                try:
                    songs['media_url'] = generate_media_url(
                        songs['media_preview_url'])
                except KeyError:
                    songs['media_url'] = decrypt_url(
                        songs['encrypted_media_url'])
                songs['image'] = fix_image_url(songs['image'])
                songs['song'] = fix_title(songs['song'])
                songs['album'] = fix_title(songs['album'])
            return songs_json
    except Exception as e:
        print_exc()
        return None


def AlbumId(input_url):
    try:
        headers = setProxy()
        res = requests.get(input_url, headers=headers)
        if 'internal error' in res.text:
            return None
        else:
            id = res.text.split('"album_id":"')[1].split('"')[0]
            return id
    except Exception:
        print_exc()
        return None


def setProxy():
    base_url = 'https://h.saavncdn.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }
    return headers


def getPlayList(listId):
    try:
        response = requests.get(
            'https://www.jiosaavn.com/api.php?listid={0}&_format=json&__call=playlist.getDetails'.format(listId), verify=False)
        if response.status_code == 200:
            response_text = (response.text.splitlines())
            songs_json = list(
                filter(lambda x: x.endswith("}"), response_text))[0]
            songs_json = json.loads(songs_json)
            songs_json['firstname'] = fix_title(songs_json['firstname'])
            songs_json['listname'] = fix_title(songs_json['listname'])
            songs_json['image'] = fix_image_url(songs_json['image'])
            for songs in songs_json['songs']:
                songs['image'] = fix_image_url(songs['image'])
                songs['song'] = fix_title(songs['song'])
                songs['album'] = fix_title(songs['album'])
                try:
                    songs['media_url'] = generate_media_url(
                        songs['media_preview_url'])
                except KeyError:
                    songs['media_url'] = decrypt_url(
                        songs['encrypted_media_url'])
            return songs_json
        return None
    except Exception:
        print_exc()
        return None


def getListId(input_url):
    headers = setProxy()
    res = requests.get(input_url, headers=headers).text
    return res.split('"type":"playlist","id":"')[1].split('"')[0]


def getSongsJSON(listId):
    url = 'https://www.jiosaavn.com/api.php?listid=' + \
        str(listId)+'&_format=json&__call=playlist.getDetails'
    response_json = requests.get(url).text
    struct = {}
    try:  # try parsing to dict
        dataform = str(response_json).split('-->')[-1]
        struct = json.loads(dataform)
    except Exception:
        print_exc()
        return None
    return struct


def decrypt_url(url):
    enc_url = base64.b64decode(url.strip())
    dec_url = des_cipher.decrypt(enc_url, padmode=PAD_PKCS5).decode('utf-8')
    dec_url = dec_url.replace("_96.mp4", "_320.mp3")
    return dec_url


def fix_title(title):
    title = title.replace('&quot;', '')
    return title


def fix_image_url(url):
    url = str(url)
    if 'http://' in url:
        url = url.replace("http://", "https://")
    url = url.replace('150x150', '500x500')
    return url


def get_lyrics(link):
    try:
        if '/song/' in link:
            link = link.replace("/song/", '/lyrics/')
            link_ = link.split('/')
            link_[-2] = link_[-2]+'-lyrics'
            link = '/'.join(link_)
            source = requests.get(link).text
            soup = BeautifulSoup(source, 'lxml')
            res = soup.find(class_='u-disable-select')
            lyrics = str(res).replace("<span>", "")
            lyrics = lyrics.replace("</span>", "")
            lyrics = lyrics.replace("<br/>", "\n")
            lyrics = lyrics.replace('<p class="lyrics"> ', '')
            lyrics = lyrics.replace("</p>", '')
            lyrics = lyrics.split("<p>")[1]
            return (lyrics)
    except Exception:
        print_exc()
        return None


def expand_url(url):
    try:
        session = requests.Session()
        resp = session.head(url, allow_redirects=True)
        return(resp.url)
    except Exception as e:
        print("URL Redirect Error: ", e)
        return url


def check_media_url(dec_url):
    ex_dec_url = expand_url(dec_url)
    r = requests.head(ex_dec_url)
    if r.status_code != 200:
        fixed_dec_url = dec_url.replace(".mp3", '.mp4')
        fixed_dec_url = expand_url(fixed_dec_url)
        return fixed_dec_url
    return ex_dec_url

if __name__ == '__main__':
    q = input("Enter the querry: ")
    q=q[:29]
    print (q)
    dat = search_query(q)
    # dat = dat[0]
    print (dat)
    print (dat.track_name)
    print (dat.release_date)
    print (dat.artist_name)
    print (dat.primary_genre_name )
    print (dat.artwork_url) 
    print (dat.track_time )