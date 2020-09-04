#!/usr/bin/python3

import requests, os, bs4, threading

url = 'https://xkcd.com/'
os.makedirs('xkcd', exist_ok=True)

def downloadXkcd(startComic, endComic):
    for urlNumber in range(startComic, endComic):
        imageUrl = url + str(urlNumber)
        print('[+] Downloadong page ' + imageUrl + '...')
        res = requests.get(imageUrl)
        res.raise_for_status()
        soup= bs4.BeautifulSoup(res.text, 'html.parser')
        comicElem = soup.select('#comic img')
        if comicElem == []:
            print('[-] Could not find images...')
        else:
            comicUrl = 'https:' + comicElem[0].get('src')
            print('[+] Downloading image ' + comicUrl + '...')
            res = requests.get(comicUrl)
            res.raise_for_status()
            imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)),'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()

downloadThreads = []
for i in range(0, 140, 10):
    start = i
    end = i + 10
    if start == 0:
        start = 1
    downloadThread = threading.Thread(target=downloadXkcd, args=(start, end))
    downloadThreads.append(downloadThread)
    downloadThread.start()

for downloadThread in downloadThreads:
    downloadThread.join()
print('[+] Done.')
