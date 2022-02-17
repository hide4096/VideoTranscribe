import os
import pafy
import re
import time
import ffmpeg as ff
import math as m
import speech_recognition as sr
from PIL import Image

SCALE = 2
SPTIME = 60

def ConvertYoutubeVoice2txt(url):
    print(url)
    video = pafy.new(url)
    best = video.getbestaudio()
    fpath = '/tmp/' + video.title + '.ogg'
    if not(os.path.exists(fpath)):
        best.download(fpath)
    
    srcinfo = ff.probe(fpath)
    dura = float(srcinfo['streams'][0]['duration'])
    
    ftitle = video.title + '-audio.txt'
    fp = open(ftitle,mode='w')

    for i in range(m.ceil(dura / SPTIME)):
        cnv = ff.input(fpath,ss=SPTIME*i,t=SPTIME)
        wpath = fpath + str(i) + '.wav'
        cnv = ff.output(cnv,wpath)
        if not(os.path.exists(wpath)):
            ff.run(cnv)
        print('Convert...')
        r = sr.Recognizer()
        with sr.AudioFile(wpath) as src:
            audio = r.record(src)
        text = r.recognize_google(audio,language='ja-JP')
        fp.write(text)
        fp.write('\n')
        print('Interval')
        time.sleep(3)

    fp.flush()
    fp.close()

def main():
    url = input('Youtube URL:')
    ConvertYoutubeVoice2txt(url)
    print('\nFinished')

if __name__ == '__main__':
    main()
