import urllib.request, shutil
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen

def MakePath(webaddr):
    key = os.path.abspath(__file__)
    dirPath = os.path.dirname(key)
    spath = webaddr.replace('www','')
    spath = spath.replace('.','_')
    spath = spath.replace('http:','')
    spath = spath.replace('https:','')
    spath = spath.replace('/','\\')
    spath = spath.replace('\\\\','\\')
    if not os.path.exists(dirPath + spath):
        os.makedirs(dirPath + spath)
    return dirPath + spath


def DownloadFolder(webaddr):
    spath = MakePath(webaddr)
    Html = urlopen(webaddr)
    print (Html)
    soup = BeautifulSoup(Html,"html.parser")
    for links in soup.find_all('a', href=True):
        file = links.get('href')
        if file[-1:] == '/' and file[:1] != '/':
            DownloadFolder(webaddr + '/' + file)

        if (file[:1] != '?' and file[-1:] != '/' and file[:1] != '/'):
            if not os.path.isfile(spath+'\\'+links.contents[0]):
                with urllib.request.urlopen(webaddr + '/' + file) as response, open(spath+'\\'+links.contents[0], 'wb') as out_file:
                    print(links.contents[0])
                    shutil.copyfileobj(response, out_file)

def debug():
    webaddr = 'https://info.stylee32.net/instaoldfagkit/zpron/'
    DownloadFolder(webaddr)


if __name__ == "__main__":
    debug()

