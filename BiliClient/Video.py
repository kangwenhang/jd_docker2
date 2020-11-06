# -*- coding: utf-8 -*-
from . import bili
import os, math, time

class VideoUploader(object):
    "B站视频上传类"
    videoPreupload = bili.videoPreupload
    videoUploadId = bili.videoUploadId
    videoUpload = bili.videoUpload
    videoUploadInfo = bili.videoUploadInfo
    videoRecovers = bili.videoRecovers
    videoTags = bili.videoTags
    videoAdd = bili.videoAdd
    videoPre = bili.videoPre
    videoDelete = bili.videoDelete
    #本类只继承BiliApi中与Video上传有关的方法
    def __init__(self, cookieData: dict = None, title="", desc="", dtime=0, tag=[], copyright=2, tid=174, source="", cover="",desc_format_id=0, subtitle={"open":0,"lan":""}):
        "创建一个B站视频上传类"               #简介
        bili.__init__(self, cookieData)
        if cookieData:
            bili.login_by_cookie(self, cookieData)

        self._data = {
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
        if dtime and dtime - int(time.time()) > 14400:
            self._data["dtime"] = dtime

        for i in range(len(tag)):
            if (i == len(tag) - 1):
                self._data["tag"] += tag[i]
            else:
                self._data["dynamic"] += f'{tag[i]},'
            self._data["tag"] += f'#{tag[i]}#'

    def uploadFile(self, filepath: '视频路径', fsize=8388608):
        "上传本地视频文件,返回视频信息dict"
        
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
        if self._data["title"] == "":
            self._data["title"] = self._data["videos"][0]["title"]
        retobj = self.videoAdd(self._data)
        if retobj["code"] == 0:
            self._submit = retobj["data"]
        else:
            self._submit = retobj
        return self._submit

    def delete(self):
        "立即撤销本视频的发布(会丢失硬币)"
        aid = self._submit["aid"]
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
        self._data["videos"].append(upvideo)

    def clear(self):
        "清除已经添加的视频"
        self._data["videos"] = []

    def setDtime(self, dtime: int):
        "设置延时发布时间，距离提交大于4小时，格式为10位时间戳"
        if dtime - int(time.time()) > 14400:
            self._data["dtime"] = dtime

    def setTitle(self, title: str):
        "设置标题"
        self._data["title"] = title

    def setDesc(self, desc: str):
        "设置简介"
        self._data["desc"] = desc

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

        self._data["tag"] = tagstr
        self._data["dynamic"] = dynamic

    def setCopyright(self, copyright=2):
        "设置copyright"
        self._data["copyright"] = copyright

    def setTid(self, tid=174):
        "设置视频分区"
        self._data["tid"] = tid

    def setTitle(self, tid=174):
        "设置标题"
        self._data["tid"] = tid

    def setSource(self, source=""):
        "设置转载原地址"
        self._data["source"] = source

    def setCover(self, cover=""):
        "设置视频封面url"
        self._data["cover"] = cover

    def setDescFormatId(self, desc_format_id=0):
        "设置desc_format_id"
        self._data["desc_format_id"] = desc_format_id

    def setSubtitle(self, subtitle={"open":0,"lan":""}):
        "设置subtitle"
        self._data["subtitle"] = subtitle

class _videoStream(object):
    def __init__(self, name: str,url: str, resolution: str, size: int):
        self._name = name
        self._url = url
        self._resolution = resolution
        self._size = size

    def __repr__(self):
        return f'<name={self._name};resolution={self._resolution};size={self._size};cid={self._size}>'

    def __str__(self):
        return f'filename={self._name} ; resolution={self._resolution} ; size={self._size / 1024 / 1024:0.2f}MB'

    @property
    def url(self) -> str:
        '''返回下载流url'''
        return self._url

    @property
    def fliename(self) -> str:
        '''返回下载文件名'''
        return self._name

class _videos(object):
    def __init__(self, subtitle, bvid='', cid=0, epid=''):
        self._title = subtitle.replace('/',' ')
        self._bvid = bvid
        self._cid = cid

    def __repr__(self):
        return f'<title={self._title};bvid={self._bvid};cid={self._cid}>'

    def __str__(self):
        return self._title

    def getTitle(self):
        '''获取当前视频标题'''
        return self._title

    def allStream(self, cookieData: dict = None, reverse_proxy='', force_use_proxy=False):
        '''
        获取所有视频流
        cookieData dict :包含"SESSDATA"值的字典，模拟用户登录
        reverse_proxy str :B站接口代理地址
        force_use_proxy bool :强制使用代理地址(默认请求失败才尝试代理地址)
        '''
        biliapi = bili()
        if cookieData:
            biliapi.login_by_cookie(cookieData)

        if force_use_proxy:
            RP = reverse_proxy
            data = biliapi.playerUrl(cid=self._cid, bvid=self._bvid, reverse_proxy=RP)
            if data["code"] != 0:
                raise Exception(f'解析失败，请尝试使用会员账号(错误信息：{data["message"]})')
        else:
            RP = ''
            data = biliapi.playerUrl(cid=self._cid, bvid=self._bvid, reverse_proxy=RP)
            if data["code"] != 0:
                if reverse_proxy == '':
                    raise Exception(f'解析失败，请尝试使用代理或会员账号(错误信息：{data["message"]})')
                else:
                    RP = reverse_proxy
                    data = biliapi.playerUrl(cid=self._cid, bvid=self._bvid, reverse_proxy=RP)
                    if data["code"] != 0:
                        print(self._bvid, self._cid)
                        raise Exception(f'解析失败，请尝试更换代理地区或使用会员账号(错误信息：{data["message"]})')
        
        accept_quality = data["data"]["accept_quality"]
        accept_description = data["data"]["accept_description"]
        ret = []
        for ii in range(len(accept_quality)):
            data = biliapi.playerUrl(cid=self._cid, bvid=self._bvid, qn=accept_quality[ii], reverse_proxy=RP)["data"]
            if data["quality"] != accept_quality[ii]:
                continue
            if 'flv' in data["format"]:
                ret.append(_videoStream(f'{self._title}.flv', data["durl"][0]["url"].replace('http:','https:'),accept_description[ii],data["durl"][0]["size"]))
            else:
                ret.append(_videoStream(f'{self._title}.mp4', data["durl"][0]["url"].replace('http:','https:'),accept_description[ii],data["durl"][0]["size"]))
        return ret

class VideoParser(object):
    '''B站视频解析类'''

    def __init__(self, url: str):
        self.parser(url)

    def all(self):
        '''取得当前所有视频(分P)'''
        if self._type == 1:
            list = bili.playList(self._bvid)["data"]
            return [_videos(x["part"], self._bvid, x["cid"]) for x in list]
        elif self._type == 2:
            return [_videos(x[0], x[1], x[2]) for x in self._eplist]
        else:
            return []

    def parser(self, url: str):
        '''
        解析视频
        url  str: BV，av，ep，ss号以及包含这些号的网址
        '''
        import re
        self._type = 0
        find = re.findall('(BV|av|ep|ss)([0-9 a-z A-Z]*)', url)
        if len(find):
            if find[0][0] == 'BV':
                self._bvid = f'BV{find[0][1]}'
                self._title = bili.webView(self._bvid)["data"]["title"]
                self._type = 1
            elif find[0][0] == 'av':
                self._bvid = bili.av2bv(int(find[0][1]))
                self._title = bili.webView(self._bvid)["data"]["title"]
                self._type = 1
            elif find[0][0] == 'ep' or find[0][0] == 'ss':
                data = bili.epPlayList(find[0][0] + find[0][1])
                self._title = data["mediaInfo"]["title"]
                self._eplist = [[f'{x["titleFormat"]} {x["longTitle"]}', x["bvid"], x["cid"]] for x in data["epList"]]
                self._type = 2
        else:
            raise Exception("不支持的参数")

    def getTitle(self):
        '''获取标题'''
        return self._title