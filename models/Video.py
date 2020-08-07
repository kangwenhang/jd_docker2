# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi

class Video(object):
    "B站视频上传类"
    videoPreupload = BiliWebApi.videoPreupload
    videoUploadId = BiliWebApi.videoUploadId
    videoUpload = BiliWebApi.videoUpload
    videoUploadInfo = BiliWebApi.videoUploadInfo
    videoRecovers = BiliWebApi.videoRecovers
    videoTags = BiliWebApi.videoTags
    videoAdd = BiliWebApi.videoAdd
    videoPre = BiliWebApi.videoPre
    videoDelete = BiliWebApi.videoDelete
    #本类只继承BiliWebApi中与Video有关的方法
    def __init__(self, cookieData, title="", desc="", tag=[], copyright=2, tid=174, source="", cover="",desc_format_id=0, subtitle={"open":0,"lan":""}):
        "创建一个B站视频类"                         #简介
        BiliWebApi.__init__(self, cookieData)
        self.__data = {
            "copyright":copyright,
            "videos":[],
            "source":source,
            "tid":tid, #分区,174为生活，其他分区
            "cover":cover, #封面图片，可由recovers方法得到视频的帧截图
            "title":title,
            "tag":"",
            "desc_format_id":desc_format_id,
            "desc":desc,
            "dynamic":"",
            "subtitle":subtitle
            }
        for i in range(len(tag)):
            if (i == len(tag) - 1):
                self.__data["tag"] += tag[i]
            else:
                self.__data["dynamic"] += f'{tag[i]},'
            self.__data["tag"] += f'#{tag[i]}#'

    def uploadFile(self, filepath: '视频路径', fsize=8388608):
        "上传本地视频文件,返回视频信息dict"
        import os, math
        path,name = os.path.split(filepath)#分离路径与文件名

        with open(filepath,'rb') as f: 
            size = f.seek(0, 2) #获取文件大小
            chunks = math.ceil(size / fsize) #获取分块数量

            retobj = self.videoPreupload(name, size) #申请上传
            auth = retobj["auth"]
            endpoint = retobj["endpoint"]
            biz_id = retobj["biz_id"]
            upos_uri = retobj["upos_uri"][6:] 
            rname = os.path.splitext(upos_uri[5:])[0]
            url = f'https:{endpoint}{upos_uri}'  #视频上传路径

            retobj = self.videoUploadId(url, auth)
            upload_id = retobj["upload_id"] #得到上传id

            #开始上传
            parts = [] #分块信息
            f.seek(0, 0)
            for i in range(chunks): #单线程分块上传，官方支持三线程
                data = f.read(fsize) #一次读取一个分块大小
                self.videoUpload(url, auth, upload_id, data, i, chunks, i*fsize, size)#上传分块
                parts.append({"partNumber":i+1,"eTag":"etag"}) #添加分块信息，partNumber从1开始
                #print(f'{i} / {chunks}')#输出上传进度

        preffix = os.path.splitext(name)[0]
        retobj = self.videoUploadInfo(url, auth, parts, name, upload_id, biz_id)
        if (retobj["OK"] == 1):
            return {"title": preffix, "filename": rname, "desc": ""}
        return {"title": preffix, "filename": "", "desc": ""}

    def submit(self):
        if self.__data["title"] == "":
            self.__data["title"] = self.__data["videos"][0]["title"]
        retobj = self.videoAdd(self.__data)
        self.__submit = retobj["data"]
        return retobj

    def delete(self):
        "立即撤销本视频的发布(会丢失硬币)"
        aid = self.__submit["aid"]
        retobj = self.videoPre()
        challenge = retobj["data"]["challenge"]
        gt = retobj["data"]["gt"]
        return (self.videoDelete(aid, challenge, gt, f'{gt}%7Cjordan')["code"] == 0)

    def recovers(self, upvideo: "由uploadFile方法返回的dict"):
        "返回官方生成的封面,刚上传可能获取不到"
        return self.videoRecovers(upvideo["filename"])

    def getTags(self, upvideo: "由uploadFile方法返回的dict"):
        "返回官方推荐的tag"
        return self.videoTags(upvideo["title"], upvideo["filename"])

    def add(self, upvideo: "由uploadFile方法返回的dict"):
        "添加已经上传的视频"
        self.__data["videos"].append(upvideo)

    def clear(self):
        "清除已经添加的视频"
        self.__data["videos"] = []

    def setTitle(self, title: str):
        "设置标题"
        self.__data["title"] = title

    def setDesc(self, desc: str):
        "设置简介"
        self.__data["desc"] = desc

    def setTag(self, tag: []):
        "设置标签，tag为数组"
        tagstr = ""
        dynamic = ""
        for i in range(len(tag)):
            if (i == len(tag) - 1):
                tagstr += tag[i]
            else:
                tagstr += f'{tag[i]},'
            dynamic += f'#{tag[i]}#'

        self.__data["tag"] = tagstr
        self.__data["dynamic"] = dynamic

    def setCopyright(self, copyright=2):
        "设置copyright"
        self.__data["copyright"] = copyright

    def setTid(self, tid=174):
        "设置视频分区"
        self.__data["tid"] = tid

    def setTitle(self, tid=174):
        "设置标题"
        self.__data["tid"] = tid

    def setSource(self, source=""):
        "设置转载原地址"
        self.__data["source"] = source

    def setCover(self, cover=""):
        "设置视频封面url"
        self.__data["cover"] = cover

    def setDescFormatId(self, desc_format_id=0):
        "设置desc_format_id"
        self.__data["desc_format_id"] = desc_format_id

    def setSubtitle(self, subtitle={"open":0,"lan":""}):
        "设置subtitle"
        self.__data["subtitle"] = subtitle