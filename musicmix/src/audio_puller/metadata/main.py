"""

Script where the metadata gets finalised:


"""
from .gaana import searchSong as gaana_meta
from .saavn import search_query as saavn_meta
from .ytmt import yt_meta

SONG = []
options = ["gaana"] #saavn WIP

class MetaData:

    def __init__(self, SONG,provider):
        """SONG is supposed to be a dict."""
        self.track_name = SONG.track_name
        self.release_date = SONG.release_date
        self.artist_name = SONG.artist_name
        self.provider = provider
        self.lanugage = SONG.language
        try:
            self.album_title = SONG.album_title
        except:
            pass
        try:
            self.lyrics_url = SONG.lyrics_url
        except:
            pass
        self.youtube_id = SONG.youtube_id
        self.collection_name = SONG.collection_name
        self.primary_genre_name = SONG.primary_genre_name
        self.artwork_url = SONG.artwork_url
        self.track_time = SONG.track_time


def update_metadata(info_dict):
    meta_data = get_metadata(info_dict,6)
    if not meta_data.artist_name : 
        meta_data = get_metadata(info_dict,4)
        if not meta_data.artist_name:
            meta_data = get_metadata(info_dict,2)
            return meta_data
        else:
            return meta_data
    else:
        return meta_data


def get_metadata(info_dict,n):
        #title process before meta collection
        query = query_preprocess(info_dict['title'],n)
        print ("query is {}".format(query))
        #meta process yt
        yt_meta_data = yt_meta(info_dict)
        #meta process gaana
        gaana_meta_data = None
        try : 
            gaana_meta_data = gaana_meta(query)
        except:
            print ("pass")
        # if not gaana_meta_data:
        saavn_meta_data = None
        try: 
            saavn_meta_data = saavn_meta(query)
        except:
            print ("pass")
        # else:
            # saavn_meta_data = None
        #final meta collection
        final_meta = meta_final(yt_meta_data,saavn_meta_data,gaana_meta_data)
        #return song_meta
        return final_meta

def query_preprocess(querry,n):
    querry = querry.replace("#","")
    querry = querry.replace("\"","")
    querry = querry.replace("\'","")
    querry = querry.replace(":","")
    querry = querry.replace("|","")
    querry = querry.replace("(","")
    querry = querry.replace(")","")
    querry = querry.replace(" _ ","")
    querry = querry.replace(" -","")
    querry = querry.replace("| ","")
    querry = querry.replace("  ","")
    querry = querry.replace("Video ","")
    querry = querry.replace("Video ","")
    querry = querry.replace("video ","")
    querry = querry.replace("song ","")
    querry = querry.replace("Song ","")
    querry = querry.replace("Songs","")
    querry = querry.replace("Movie ","")
    querry = querry.replace("FULL ","")
    querry = querry.replace("AUDIO ","")
    querry = querry.replace("Full","")
    querry = querry.replace("HD ","")
    query = querry.split(" ")
    query = query[:n]
    query = " ".join(query)
    return query

def meta_final(yt_meta_data,saavn_meta_data,gaana_meta_data):
    if gaana_meta_data:
        meta_final = MetaData(gaana_meta_data,"gaana")
        print ("gaana")
    elif saavn_meta_data:
        meta_final = MetaData(saavn_meta_data,"saavn")
        print ("saavn")
    else:
        meta_final= MetaData(yt_meta_data,"yt")
        print ("yt")
    return meta_final