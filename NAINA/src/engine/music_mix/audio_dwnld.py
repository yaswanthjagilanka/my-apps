from __future__ import unicode_literals
import youtube_dl

def audio_download(url):
  ydl_opts = {
      'outtmpl': '/content/drive/My Drive/Audio_Mixer/%(title)s-.%(ext)s%(id)s',
      'format': 'bestaudio/best',
      'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '320',
      }],
  }
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])

def audio_cut(start,end):
    pass

def audio_rename(name):
    pass

def push_to_telgram(username,userid):
    ##push song###
    return "success"
