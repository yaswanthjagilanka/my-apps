from __future__ import unicode_literals
import youtube_dl
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON, TRCK, TYER
from mutagen.mp3 import MP3
import os
import sys
import urllib.request
from .metadata.main import update_metadata 
# base_drive = os.getcwd() + "/Songs"
# base_drive = '/content/drive/My Drive/Songs'
base_drive='/Users/yjagilanka/Google Drive/My Drive/Audio/Songs'

def audio_process(data):
    path = base_drive +"/"+ data['genre']+ "/"+data['language'] + "/"
    #download and format change
    # print ("data",data)
    info_dict = audio_download(data['url'],path)
    print ("info_dict",info_dict['title'])
    #metadata processing - youtube and gaana
    metadata = get_meta_data(info_dict)
    #metadata attac
    filename = info_dict['title']+'.mp3'
    filename = filename.replace(":"," -")
    filename = filename.replace("\"","\'")
    filename = filename.replace("|","_")
    filename = filename.replace("__","_")
    # filename = filename.replace(" __ ","_")
    # filename = filename.replace(", ",",")
    song = setmetadata(filename,path,metadata,data)
    return filename

def audio_download(url,path):
  ydl_opts = {
      'outtmpl': os.path.join(path,'%(title)s.%(ext)s'),
    #   'outtmpl': '%(title)s.%(ext)s',
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '320',
        #   'nocheckcertificate': True,
      }],
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
      info_dict = ydl.extract_info(url, download=False)
      return info_dict

def get_meta_data(info_dict):
    song = update_metadata(info_dict)
    return song

def setmetadata(song,path,metadata,data):
    """
    Set the meta data if the passed data is mp3.
    """
    print ("setmetadata",song,path,metadata)
    SONG_PATH = os.path.join(path,song)
    if metadata:
        audio = MP3(SONG_PATH, ID3=ID3)
        data = ID3(SONG_PATH)
        urllib.request.urlretrieve(metadata.artwork_url,os.path.join(path,"art.jpg"))
        imagedata = open(os.path.join(path,"art.jpg"), 'rb').read()
        data.add(APIC(3, 'image/jpeg', 3, u'Cover', imagedata))
        os.remove(os.path.join(path,"art.jpg"))
        audio.save()
        data.add(TYER(encoding=3, text=metadata.release_date))
        data.add(TIT2(encoding=3, text=metadata.track_name))
        data.add(TPE1(encoding=3, text=metadata.artist_name))
        data.add(TALB(encoding=3, text=metadata.collection_name))
        data.add(TCON(encoding=3, text=metadata.primary_genre_name))
        # data.add(TRCK(encoding=3, text=str(metadata.track_number)))
        data.save()
        final = metadata.track_name + '.mp3'
    else:
        if data['rename']:
            final = data['rename']
        else:
            final = song.replace(".mp3","")[27] + '.mp3'
    print ("final",final)
    # # Rename the downloaded file
    os.rename(SONG_PATH, os.path.join(path,final))
    return "hello"
