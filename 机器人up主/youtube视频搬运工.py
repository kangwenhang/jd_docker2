# -*- coding: utf-8 -*-
from models.Video import Video
from userData.userData import cookieDatas
import time
from pytube import YouTube

print("请粘贴youtube视频完整链接后按回车")
url = input()


print("开始下载youtube视频")
video = YouTube(url)
video.streams.filter(file_extension="mp4")[2].download()
filename = f'{video.title}.mp4' #下载的文件名


bilivideo = Video(cookieDatas[0]) #创建B站视频发布任务
print(f'开始将{filename}上传至B站，请耐心等待')
vd = bilivideo.uploadFile(filename) #上传视频
if vd["filename"] == "":
    print("上传失败")
    exit(0)
print(f'上传完成,即将发布，请等待最多30s')
#vd["title"] = "" #设置视频标题,默认为文件名
bilivideo.add(vd)  #添加视频
#bilivideo.setTitle("") #设置发布标题,默认为第一个添加的视频的标题
#bilivideo.setCopyright(2) #设置为非原创
bilivideo.setDesc(f'转载于：{url}') #添加简介
bilivideo.setSource(url) #添加转载地址说明
#bilivideo.setTid(174) #设置视频分区,默认为 生活，其他分区
bilivideo.setTag(["转载"]) #设置视频标签,数组,好像最多9个
pics = bilivideo.recovers(vd)["data"] #获取视频截图，刚上传的视频可能获取不到
if len(pics):
    bilivideo.setCover(pics[0]) #设置视频封面
else:
    time.sleep(25) #B站需要足够的时间来生成封面
    pics = bilivideo.recovers(vd)["data"]
    if len(pics):
        bilivideo.setCover(pics[0])
    else:
        time.sleep(10)
        pics = bilivideo.recovers(vd)["data"]
        bilivideo.setCover(pics[0])

bilivideo.submit() #提交视频发布
print("完成")