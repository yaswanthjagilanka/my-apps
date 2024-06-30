"""
Python module to search gaana.com using their API.

Uses api.gaana.com to get search results.
"""

import requests

# Define the base url
base_url = "http://api.gaana.com/?type=search&subtype=search_song&key={}&token=b2e6d7fbc136547a940516e9b77e5990&format=JSON"

SONG = []
gaana_options = ['track_id', 'seokey', 'albumseokey', 'track_title', 'album_id', 'album_title', 'language', 'language_id', 'release_date', 'meta_title', 'meta_description', 'meta_keywords', 'meta_h1_tag', 'artwork', 'artwork_web', 'artwork_large', 'parental_warning', 'artist', 'gener', 'lyrics_url', 'youtube_id', 'popularity', 'rating', 'content_source', 'stream_type', 'duration', 'isrc', 'is_most_popular', 'track_format', 'rtmp', 'http', 'https', 'rtsp', 'display_global', 'mobile', 'country', 'vendor', 'is_local', 'premium_content', 'vgid', 'atw', 'vd_expiry', 'clip_videos', 'ppd', 'secondary_language', 'total_downloads', 'trivia_info', 'is_premium']


class GaanaSongs():
    """Class to store gaana song tags."""

    def __init__(self, SONG):
        """SONG is supposed to be a dict."""
        self.track_name = SONG['track_title']
        self.release_date = SONG['release_date']
        self.artist_name = SONG['artist'][0]['name']
        self.provider = "gaana"
        self.language = SONG['language']
        self.album_title = SONG['album_title']
        self.lyrics_url = SONG['lyrics_url']
        self.youtube_id = SONG['youtube_id']
        self.collection_name = SONG['album_title']
        self.primary_genre_name = SONG['gener'][0]['name']
        self.artwork_url = SONG['artwork_large']
        self.track_time = self._convert_time(SONG['duration'])

    def _convert_time(self, duration):
        in_min = int(duration)
        in_time = int(in_min / 60) + (0.01 * (in_min % 60))
        return in_time


def searchSong(querry):
    """Nanan."""
    url = base_url.format(querry)
    r = requests.get(url)
    data = r.json()
    data = data['tracks']
    SONG_TUPLE = []

    if data:
        for i in range(0, len(data)):
            song_obj = GaanaSongs(data[i])
            SONG_TUPLE.append(song_obj)
    if not SONG_TUPLE:
        data = None
    else:
        data = SONG_TUPLE[0]
    return data

if __name__ == '__main__':
    q = input("Enter the querry: ")
    dat = searchSong(q)
    print (dat.track_name)
    print (dat.release_date)
    print (dat.artist_name)
    print (dat.primary_genre_name )
    print (dat.artwork_url_100) 
    print (dat.track_time )
