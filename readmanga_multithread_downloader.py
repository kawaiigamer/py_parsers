from concurrent.futures import ThreadPoolExecutor
import os,sys,urllib.request,re,socket


def RemoteContentHttpDownload(s):
 return urllib.request.urlopen( s,timeout = 10).read()

def input_check(ar,s,d,m):
     if len(sys.argv) > ar :
         return int(sys.argv[ar])
     else:
         _ = input(s + " ->(" + str(d) + ") ")
         return int(_) if len(_) > 0 and int(_) > 0 and int(_) < m else d
        
def ConcurrentMangaChapterDownload(task):
    _ = task.split("/" )
    _ = _manga_name + "\\" +(_[len(_)-2]+"_"+_[len(_)-1])
    os.makedirs(_,exist_ok=True)
    raw = str(RemoteContentHttpDownload(_url_base + task + "?mature=1"))
    ImgLinks = re.findall("\'(.+?)'..(.+?)'.\"(.+?)\"",raw[raw.index('.init'):][:5500])
    for i in range(len(ImgLinks)):
        url  = ImgLinks[i][1] + ImgLinks[i][0] + ImgLinks[i][2]
        while True:
             try:
                 urllib.request.urlretrieve(url[1:].replace("\\","") , _ + "\\" + url.split('/')[-1])
             except Exception as e:
                 print (str(e), url[1:].replace("\\",""))
                 continue
             break

socket.setdefaulttimeout(30)     
_url = sys.argv[1] if len(sys.argv) > 1  else  input("url -> ") # "http://readmanga.me/bleach_"
_url_base = _url[:_url.rindex('/')]
_manga_name = _url[_url.rindex('/'):]
rawCatalog = RemoteContentHttpDownload(_url)
print("Downloaded:",len(rawCatalog),"bytes")
chapterList = re.compile("<a href=\"(" + _manga_name + "/vol\d+/\d+)", re.M).findall(str(rawCatalog))
_manga_name = _manga_name[1:]
print("Found:",len(chapterList),"chapters")
_from = input_check(2,"start from",0,len(chapterList))
_to = input_check(3,"stop at",len(chapterList),len(chapterList))
_threads = input_check(4,"threads",10,1000)
os.makedirs(_manga_name,exist_ok=True)
print("creating new folder :",_manga_name)
with ThreadPoolExecutor(max_workers=_threads) as executor:
    i = _from
    while i < _to:
        executor.submit(ConcurrentMangaChapterDownload, chapterList[i])
        i += 1
    executor.shutdown()
print("(ξ^∇^ξ) ホホホホホホホホホ")
if len(sys.argv) == 1:
    input("Press Enter to continue...")
    



