# -*- coding: utf-8 -*-
from BiliClient import MangaDownloader
import os, sys
from getopt import getopt
try:
    from json5 import load
except:
    from json import load

if os.path.exists('./config.json'):
    with open('./config.json','r',encoding='utf-8-sig') as fp:
        configData = load(fp)
elif os.path.exists('./config/config.json'):
    with open('./config/config.json','r',encoding='utf-8-sig') as fp:
        configData = load(fp)
elif os.path.exists('/etc/BiliExp/config.json'):
    with open('/etc/BiliExp/config.json','r',encoding='utf-8-sig') as fp:
        configData = load(fp)
else:
    configData = None

def print_format(string, way, width, fill= ' ',ed = ''):
    count = 0
    for word in string:
        if (word >='\u4e00' and word <= '\u9fa5') or word in ['；','：','，','（','）','！','？','——','……','、','》','《']:
            count+=1
    width = width-count if width>=count else 0
    print('{0:{1}{2}{3}}'.format(string,fill,way,width),end = ed,flush=True)

def download_interactive():
    id = int(input('请输入B站漫画id(整数，不带mc前缀)：'))
    path = input('请输入保存路径(默认当前目录)：')
    pdf = input('下载后是否合并为一个pdf(y/n)：')
    if not path:
        path = os.getcwd()
    mag = MangaDownloader(id, configData["users"][0]["cookieDatas"]) if configData else MangaDownloader(id)
    print(f'开始下载漫画 "{mag.getTitle()}"')
    for ret in mag.downloadAll(path):
        print_format(ret.name, '<', 30)
        if ret.code == MangaDownloader.DownloadCode.Ok:
            print(' 下载成功')
        elif ret.code == MangaDownloader.DownloadCode.Locked:
            print(' 没有解锁')
        elif ret.code == MangaDownloader.DownloadCode.Error:
            print(' 下载失败')
    print('下载任务结束')

    if pdf.upper() == 'Y':
        import fitz, glob
        print("正在合并下载图片为pdf")
        title = mag.getTitle()
        path = os.path.join(path, title)
        doc = fitz.open()
        for name in glob.glob(os.path.join(path, "*", "*.jpg")):
            imgdoc = fitz.open(name)
            pdfbytes = imgdoc.convertToPDF()
            imgpdf = fitz.open("pdf", pdfbytes)
            doc.insertPDF(imgpdf)
        path = os.path.join(path, title + ".pdf")
        doc.save(path)
        print(f'文件保存至{path}')

def download_task(task, path: str):
    if configData:
         mag = MangaDownloader(task[0], configData["users"][0]["cookieDatas"])
    else:
         mag = MangaDownloader(task[0])

    title = mag.getTitle()
    print(f'开始下载漫画 "{title}"')
    if task[1] == 'a':
        mag.downloadAll(path)
    else:
        ep_list = mag.getIndex()
        ep_len = len(ep_list)
        ep_P = set()
        for P in task[1].split(','):
            if '-' in P:
                start, end = P.split('-')
                for i in range(int(start), int(end)+1):
                    if i <= ep_len:
                        ep_P.add(i-1)
            else:
                if int(P) <= ep_len:
                    ep_P.add(int(P)-1)

    for ret in mag.downloadIndexes(ep_P, path):
        print_format(ret.name, '<', 30)
        if ret.code == MangaDownloader.DownloadCode.Ok:
            print(' 下载成功')
        elif ret.code == MangaDownloader.DownloadCode.Locked:
            print(' 没有解锁')
        elif ret.code == MangaDownloader.DownloadCode.Error:
            print(' 下载失败')
    print('下载任务结束')

    if task[2]:
        import fitz, glob
        print("正在合并下载图片为pdf")
        path = os.path.join(path, title)
        doc = fitz.open()
        for name in glob.glob(os.path.join(path, "*", "*.jpg")):
            imgdoc = fitz.open(name)
            pdfbytes = imgdoc.convertToPDF()
            imgpdf = fitz.open("pdf", pdfbytes)
            doc.insertPDF(imgpdf)
        path = os.path.join(path, title + ".pdf")
        doc.save(path)
        print(f'文件保存至{path}')

def main(*args, **kwargs):
    if kwargs["task"][0]:
        download_task(kwargs["task"], kwargs["path"])
    else:
        download_interactive()

if __name__=="__main__":
    kwargs = {
       "task": ["", "a", False],
       "path": './'
        }
    opts, args = getopt(sys.argv[1:], "hVfm:e:p:", ["help", "version", "pdf", "manga=", "episode=", "path="])
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print('mangaDownloader -p <下载文件夹> -m <漫画> -e <章节数> -f')
            print(' -p --path      下载保存的路径，提供一个文件夹路径，没有会自动创建文件夹，默认为当前文件夹')
            print(' -m --manga     下载的漫画mc号，整数')
            print(' -e --episode   章节数，不提供默认下载所有章节，多个用逗号分隔，连续用减号分隔  -e 2,3,5-7,10 表示2,3,5,6,7,10章节，注意番外也算一个章节')
            print(' -f --pdf       下载后合并为一个pdf')
            print(' -V --version   显示版本信息')
            print(' -h --help      显示帮助信息')
            exit()
        elif opt in ('-V','--version'):
            print('B站漫画下载器 mangaDownloader v1.2.0')
            exit()
        elif opt in ('-p','--path'):
            kwargs["path"] = arg.replace(r'\\', '/')
        elif opt in ('-m','--manga'):
            kwargs["task"][0] = arg
        elif opt in ('-e','--episode'):
            kwargs["task"][1] = arg
        elif opt in ('-f','--pdf'):
            kwargs["task"][2] = True
    main(**kwargs)