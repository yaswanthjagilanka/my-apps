from gtts import gTTS
import pyttsx
import time





def gtts_speak(jarvis_speech):
    tts = gTTS(text=jarvis_speech, lang='en')
    tts.save('jarvis_speech.mp3')
    mixer.init()
    mixer.music.load('jarvis_speech.mp3')
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(1)


def offline_speak(jarvis_speech):
    engine = pyttsx.init()
    engine.say(jarvis_speech)
    engine.runAndWait()