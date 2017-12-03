import urllib.request, re, os.path
import requests
from bs4 import BeautifulSoup
import re

rawurl = input('Введите адрес: ')

urlsplit = re.split(r'/', rawurl)
if urlsplit[-1] != 'en' or 'en?from=sticker':
 lang = 'en'
url = 'https://store.line.me/stickershop/product/' + str(urlsplit[-2]) + '/' + str(lang)

print('Получаю информацию о стикерах. Подождите...')
#Ищем и получаем айди первого и последнего стикера
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
for textlist in (soup.find_all(True,text=re.compile(r'ids: \[', re.I))):
 textin = textlist.parent
 idimagefirst = re.findall(r'ids: \[.*', str(textin))
 idimagesecond = re.split(r': \[', str(idimagefirst))
 idimage3 = re.split(r'\]', str(idimagesecond[1]))
 idimage4 = re.split(r',', str(idimage3[0]))
 global id1, idend
 id1 = idimage4[0]
 idend = idimage4[-1]


#Проверяем пак на анимацию, звук и получаем его имя
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
for textlist in (soup.find_all(True,text=re.compile(r'var product =', re.I))):
 global typeimage, urlformat
 intext = textlist.parent
 typeimage = re.findall(r'\'hasAnimation\':(\w+)', str(intext))
 if typeimage[0] == 'false':
    urlformat = 'sticker@2x.png'
 elif typeimage[0] != 'false':
    urlformat = 'sticker_animation@2x.png'
 soundg = re.findall(r'\'hasSound\':(\w+)', str(intext))
 sd = soundg[0]
 packnamefirst = re.findall(r'\'title\':\'.+', str(intext))
 packnamesecond = re.split(r':\'', str(packnamefirst))
 packname3 = re.split(r'\',', str(packnamesecond[1]))
 packname4 = packname3[0]
 mypath = re.sub(r'\\|:|&#39;|/', '', packname4)

urlmethod = 'iphone/'
sound = 'sticker_sound.m4a'
global urlsound, soundpath

print('Загружаю пак ' + str(mypath) + '. Подождите...')

#Загружаем стикеры и звуки при наличии
script_dir = os.path.dirname(os.path.abspath(__file__))
end_direct = os.path.join(script_dir, mypath)
try:
    os.makedirs(end_direct)
except OSError:
    pass # already exists
while int(id1) <= int(idend):
 name = os.path.join(end_direct, str(id1) + ".png")
 urlimage = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/' + str(id1) + '/' + str(urlmethod)  + str(urlformat)
 soundpath = os.path.join(end_direct, str(id1) + ".m4a")
 urlsound = 'https://stickershop.line-scdn.net/stickershop/v1/sticker/' + str(id1) + '/' + str(urlmethod) + str(sound)
 f = open(name, 'wb')
 f.write(urllib.request.urlopen(urlimage).read())
 f.close()
 if sd == 'true':
     m4a = urllib.request.URLopener()
     m4a.retrieve(urlsound, soundpath)
 else:
     pass
 id1 = int(id1) + 1

print('Загрузка пака ' + mypath + ' завершена.')
