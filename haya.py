import cv2
import os
import pafy
import pyocr
import re
from PIL import Image

SCALE = 2

def ConvertYoutube2txt(url):
    print(url)
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture(best.url)
    fps = cap.get(cv2.CAP_PROP_FPS)

    tools = pyocr.get_available_tools()
    tool = tools[0]
    maxframe = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    count = 0

    ftitle = video.title + '.txt'
    fp = open(ftitle,mode='w')

    while(cap.isOpened()):
        if(count%int(fps*2) == 0):
            ret,frame = cap.read()

            if(ret == False):
                break

            img = frame.copy()
            img = cv2.resize(img, (img.shape[1]*SCALE, img.shape[0]*SCALE), interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            img = Image.fromarray(img)
            res = tool.image_to_string(img,lang='jpn')
            res = res.replace('\n{2,}','')
            fp.write('\n##########' +'{:.1f}s'.format(count/fps) + '##########\n')
            fp.write(res)
            fp.flush()
            print('\r' + '{:.2f}'.format(count/maxframe*100) + '%',end='')
        else:
            ret = cap.grab()
            if(ret == False):
                break

        count+=1

    cap.release()
    fp.flush()
    fp.close()

def main():
    url = input('Youtube URL:')
    ConvertYoutube2txt(url)
    print('\nFinished')

if __name__ == '__main__':
    main()
