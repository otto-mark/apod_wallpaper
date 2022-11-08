import os
import sys
import requests
import urllib
import ctypes
from PIL import Image, ImageDraw, ImageFont

from config import *

def multilineTextSize(txt, fnt):
    lines = txt.split("\n")
    sizeX = 0
    sizeY = 0
    size = (0,0)
    for l in lines:
        size = fnt.getsize(l)
        sizeX = max(sizeX, size[0])
    sizeY = len(lines) * (size[1] + 4)
    return (sizeX, sizeY)


def insertNewLine(str, n):
    cnt = 0
    ret = ""
    for i in range(0, len(str)):
        if cnt < n:
            ret += str[i]
            cnt += 1
            continue
        if str[i] == " ":
            ret += "\n"
            cnt = 0
            continue
        ret += str[i]
    return ret
        

# params for APOD API request
params = {
    'api_key' : token,
    'hd' : True,
    'thumbs': True,
    'date' : "2022-01-01"
}



result = requests.get('https://api.nasa.gov/planetary/apod', params=params).json()

copyright=""
if "copyright" in result.keys():
    copyright = "   " + u"\u00A9" + result["copyright"]

# get image from URL; use thumbnail in case of video
url = result["url"]
if "thumbnail_url" in result:
    if not useThumbnail:
        sys.exit(0)    
    url = result["thumbnail_url"]

urllib.request.urlretrieve(url, img_path)


# get screen size to crop out a proper section without skewing the image
sX, sY = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

im = Image.open(img_path)
if add_text:
    im = im.convert("RGBA")
w, h = im.size


# crop out horizontal if img is too high, or vertical if too wide
if(w > sX):
    cW = sX * h / sY
    cH = h
else:
    cH = sY * w / sX
    cW = w
L = (int) (w/2) - (cW/2)
T = (int) (h/2) - (cH/2)
R = L + cW
B = T + cH
new = im.crop(((L, T, R, B)))
# higher resolution for text display
new = new.resize((sX, sY))

if add_text:
    # fetch title and descriptive text
    des = result["explanation"]
    des += copyright
    title = result["title"]

    # prepare fonts; insert line breaks into descriptive text
    fntDes = ImageFont.truetype("arial.ttf", fnt_size, encoding="unic")
    des = insertNewLine(des, sX // ( fnt_size))
    desSize = multilineTextSize(des, fntDes)

    fntTitle = ImageFont.truetype("arial.ttf", fnt_size_title, encoding="unic")
    titleSize = fntTitle.getsize(title)

    # define a border box for text
    overlayX = max(titleSize[0], desSize[0]) + 2 * margin
    overlayY = titleSize[1] + desSize[1] + 2 * margin


    # create new image to write on
    over = Image.new('RGBA', new.size, (0,0,0, 0))
    
    # put overlay into desired corner
    layerSize = (overlayX, overlayY)
    layerX = 0 if pos in (0, 2) else over.size[0] - layerSize[0]
    layerY = 0 if pos in (0, 1) else over.size[1] - layerSize[1]
    layerEndX = layerSize[0] if pos in (0,2) else over.size[0]
    layerEndY = layerSize[1] if pos in (0,1) else over.size[1]

    # put text on image
    draw = ImageDraw.Draw(over, "RGBA")
    draw.rectangle(((layerX, layerY), (layerEndX, layerEndY)), fill=overlay_col)
    draw.text((layerX + margin, layerY +margin), title, font=fntTitle, fill=txt_col)
    draw.text((layerX + margin, layerY+ margin + 12 + titleSize[1]), des, font=fntDes, fill=txt_col)

    # put rendered text on image
    new = Image.alpha_composite(new, over)
    new = new.convert("RGB")

new.save(img_path)

# set background
SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img_path, 3)
print(copyright)