# -*- coding: utf-8 -*-
from BiliClient import MangaDownloader
import json, re, os

with open('config/config.json','r',encoding='utf-8') as fp:
    configData = json.loads(re.sub(r'\/\*[\s\S]*?\/', '', fp.read()))

id = int(input('请输入B站漫画id(整数，不带mc前缀)：'))
path = input('请输入保存路径(默认当前目录)：')
pdf = input('下载后是否合并为一个pdf(y/n)：')

if not path:
    path = os.getcwd()

path = path.replace('\\', '/')
mag = MangaDownloader(id, configData["users"][0]["cookieDatas"])
print(f'开始下载漫画 "{mag.getTitle()}"')
mag.downloadAll(path)
print('下载任务结束')

if pdf.upper() == 'Y':
    import fitz, glob
    print("正在合并下载图片为pdf")
    title = mag.getTitle()
    if path[-1] == '/':
        path = f'{path}{title}'
    else:
        path = fr'{path}/{title}'

    doc = fitz.open()
    for name in glob.glob(f'{path}/*/*.jpg'):
        imgdoc = fitz.open(name)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(f'{path}/{title}.pdf')
    print(f'文件保存至{path}/{title}.pdf')


