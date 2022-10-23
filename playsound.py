import time
from pygame import mixer
import pygame as pg
import os.path

delta = 4000

def playSound(filename, endPlayTime = 0):
    print(filename)
    if os.path.exists(filename):
        from mutagen.mp3 import MP3
        audio = MP3(filename)
        mp3_length = int(audio.info.length * 1000)
        cMilliseconds = int(time.time() * 1000)
        compare = endPlayTime + mp3_length + delta
        print(f"{cMilliseconds} - {compare}")
        if compare < cMilliseconds or endPlayTime == 0:
            endPlayTime = cMilliseconds + mp3_length + delta
            mixer.init()
            mixer.music.load(filename)
            mixer.music.play()
            mixer.music.set_volume(1)
            while mixer.music.get_busy():
                time.sleep(1)
    return endPlayTime


if __name__ == "__main__":
    while True:
        filename = ".\\photo\\KudzhSA.mp3"
        playSound(filename)
        time.sleep(0.5)

