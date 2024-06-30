yt_mt_options = ['id', 'uploader', 'uploader_id', 'uploader_url', 'channel_id', 'channel_url', 'upload_date', 'license', 'creator', 'title', 'alt_title', 'thumbnails', 'description', 'categories', 'tags', 'subtitles', 'automatic_captions', 'duration', 'age_limit', 'annotations', 'chapters', 'webpage_url', 'view_count', 'like_count', 'dislike_count', 'average_rating', 'formats', 'is_live', 'start_time', 'end_time', 'series', 'season_number', 'episode_number', 'track', 'artist', 'album', 'release_date', 'release_year', 'extractor', 'webpage_url_basename', 'extractor_key', 'playlist', 'playlist_index', 'thumbnail', 'display_id', 'requested_subtitles', 'format_id', 'url', 'player_url', 'ext', 'format_note', 'acodec', 'abr', 'asr', 'filesize', 'fps', 'height', 'tbr', 'width', 'vcodec', 'downloader_options', 'format', 'protocol', 'http_headers']


#song_meta.yt_tb_url = info_dict['thumbnails'][3]['url']

def yt_meta(info_dict):
    yt_meta_data = YTSongs(info_dict)
    return yt_meta_data

class YTSongs():
    """Class to store gaana song tags."""

    def __init__(self, SONG):
        """SONG is supposed to be a dict."""
        self.track_name = SONG['title'][:15]
        self.release_date = SONG['upload_date']
        self.artist_name = SONG['artist']
        self.language = None
        try:
            self.album_title = SONG['album']
        except:
            pass
        try:
            self.lyrics_url = SONG['subtitles']
        except:
            pass
        self.youtube_id = SONG['webpage_url'].split('=')[1].replace('\'',"")
        self.collection_name = SONG['title']
        self.primary_genre_name = SONG['categories'][0]
        self.artwork_url = SONG['thumbnails'][3]['url']
        self.track_time = self._convert_time(SONG['duration'])

    def _convert_time(self, duration):
        in_min = int(duration)
        in_time = int(in_min / 60) + (0.01 * (in_min % 60))
        return in_time