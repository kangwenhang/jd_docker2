# -*- coding: utf-8 -*-
import requests
import json
import re
class Biliapi(object):
    "B站API操作"
    __headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
            "Referer": "https://www.bilibili.com/",
            }
    def __init__(self, cookieData):
        #创建session
        self.__session = requests.session()
        #添加cookie
        requests.utils.add_dict_to_cookiejar(self.__session.cookies, cookieData)
        #设置header
        self.__session.headers.update(Biliapi.__headers)

        self.__bili_jct = cookieData["bili_jct"]
        self.__uid = cookieData["DedeUserID"]

        content = self.__session.get("https://account.bilibili.com/home/reward")
        if json.loads(content.text)["code"] != 0:
            raise Exception("参数验证失败")


    def getReward(self):
        "取B站经验信息"
        url = "https://account.bilibili.com/home/reward"
        content = self.__session.get(url)
        return json.loads(content.text)["data"]

    @staticmethod
    def getId(url):
        "取B站指定视频链接的aid和cid号"
        content = requests.get(url, headers=Biliapi.__headers)
        match = re.search( 'https:\/\/www.bilibili.com\/video\/av(.*?)\/\">', content.text, 0)
        aid = match.group(1)
        match = re.search( '\"cid\":(.*?),', content.text, 0)
        cid = match.group(1)
        return {"aid": aid, "cid": cid}

    def getCoin(self):
        "获取剩余硬币数"
        url = "https://api.bilibili.com/x/web-interface/nav?build=0&mobi_app=web"
        content = self.__session.get(url)
        return int(json.loads(content.text)["data"]["money"])

    def coin(self, aid, num, select_like):
        "给指定av号视频投币"
        url = "https://api.bilibili.com/x/web-interface/coin/add"
        post_data = {
            "aid": aid,
            "multiply": num,
            "select_like": select_like,
            "cross_domain": "true",
            "csrf": self.__bili_jct
            }
        content = self.__session.post(url, post_data)
        return json.loads(content.text)

    def share(self, aid):
        "分享指定av号视频"
        url = "https://api.bilibili.com/x/web-interface/share/add"
        post_data = {
            "aid": aid,
            "csrf": self.__bili_jct
            }
        content = self.__session.post(url, post_data)
        return json.loads(content.text)

    def report(self, aid, cid, progres):
        "B站上报观看进度"
        url = "http://api.bilibili.com/x/v2/history/report"
        post_data = {
            "aid": aid,
            "cid": cid,
            "progres": progres,
            "csrf": self.__bili_jct
            }
        content = self.__session.post(url, post_data)
        return json.loads(content.text)

    def getHomePageUrls(self):
        "取B站首页推荐视频地址列表"
        url = "https://www.bilibili.com"
        content = self.__session.get(url)
        match = re.findall( '<div class=\"info-box\"><a href=\"(.*?)\" target=\"_blank\">', content.text, 0)
        match = ["https:" + x for x in match]
        return match

    @staticmethod
    def getRegions(rid=1, num=6):
        "获取B站分区视频信息"
        url = "https://api.bilibili.com/x/web-interface/dynamic/region?ps=" + str(num) + "&rid=" + str(rid)
        content = requests.get(url, headers=Biliapi.__headers)
        datas = json.loads(content.text)["data"]["archives"]
        ids = []
        for x in datas:
            ids.append({"title": x["title"], "aid": x["aid"], "bvid": x["bvid"], "cid": x["cid"]})
        return ids

    @staticmethod
    def getRankings(rid=1, day=3):
        "获取B站分区排行榜视频信息"
        url = "https://api.bilibili.com/x/web-interface/ranking?rid=" + str(rid) + "&day=" + str(day)
        content = requests.get(url, headers=Biliapi.__headers)
        datas = json.loads(content.text)["data"]["list"]
        ids = []
        for x in datas:
            ids.append({"title": x["title"], "aid": x["aid"], "bvid": x["bvid"], "cid": x["cid"], "coins": x["coins"], "play": x["play"]})
        return ids

    def repost(self, dynamic_id, content="", extension='{"emoji_type":1}'):
        "转发B站动态"
        url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost"
        post_data = {
            "uid": self.__uid,
            "dynamic_id": dynamic_id,
            "content": content,
            "extension": extension,
            #"at_uids": "",
            #"ctrl": "[]",
            "csrf_token": self.__bili_jct
            }
        content = self.__session.post(url, post_data)
        return json.loads(content.text)

    def getDynamicNew(self, type_list='268435455'):
        "取B站用户动态数据"
        url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?uid=" + self.__uid + "&type_list=" + type_list
        content = self.__session.get(url)
        return json.loads(content.text)

    @staticmethod
    def mangaClockIn(access_key, platform="android"):
        "模拟B站漫画客户端签到"
        url = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
        headers = {
            "User-Agent": "Mozilla/5.0 BiliComic/3.0.0",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
        post_data = {
            "access_key": access_key,
            "platform": platform
            }
        content = requests.post(url, data=post_data, headers=headers)
        return json.loads(content.text)

    def xliveSign(self):
        "B站直播签到"
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
        content = self.__session.get(url)
        return json.loads(content.text)