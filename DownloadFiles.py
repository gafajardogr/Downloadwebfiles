import urllib.request, shutil
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys
import time
verbose = False
sys.setrecursionlimit(100000) ## An arbitrary number to prevent the recursion limit of python

class Logger:
    getTime = classmethod(lambda cls:  [str(i).zfill(2) for i in time.localtime()[:6]])
    info = classmethod(lambda cls,txt:  print("[{1}/{2}/{0} {3}:{4}:{5}] [INFO] {6}".format(*Logger.getTime(),txt)))
    error = classmethod(lambda cls,txt: print("[{1}/{2}/{0} {3}:{4}:{5}] [ERROR] {6}".format(*Logger.getTime(),txt),file=sys.stderr))    
    
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
    if verbose:
        Logger.info("Downloading "+webaddr)
    spath = MakePath(webaddr)
    Html = urlopen(webaddr)
    print (Html)
    soup = BeautifulSoup(Html,"html.parser")
    for links in soup.find_all('a', href=True):
        file = links.get('href')
        if file[-1:] == '/' and file[:1] != '/':
            DownloadFolder(webaddr + '/' + file)

        if (file[:1] != '?' and file[-1:] != '/' and file[:1] != '/') and not os.path.isfile(spath+'\\'+links.contents[0]):
            with urllib.request.urlopen(webaddr + '/' + file) as response, open(spath+'\\'+links.contents[0], 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        else:
            if verbose:
                Logger.error(webaddr+" not a file! (You can safely ignore this)")
            

def debug():
    global verbose
    args = sys.argv[1:]
    if '--verbose' in args:
        verbose = True
        while '--verbose' in args:
            args.remove('--verbose')
        
            
            
    if len(args)<2:
        print("ERROR! At least one web address is required")  
        sys.exit(1)
    for i in args:
        DownloadFolder(webaddr)
    


if __name__ == "__main__":
    debug()

