# -*- coding: utf-8 -*-
from models.Manga import Manga
import json

id = int(input('请输入B站漫画id(整数，不带mc前缀)：'))
path = input('请输入保存路径：')
co = input('是否加载cookie以用户身份登录(y/n)：')
pdf = input('下载后是否合并为一个pdf(需要安装pymupdf模块)(y/n)：')

path = path.replace('\\', '/')

if co.upper() == 'Y':
    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)
    mag = Manga(id, configData["users"][0]["cookieDatas"])
else:
    mag = Manga(id)

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


