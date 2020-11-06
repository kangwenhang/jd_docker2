from . import bili

class MangaDownloader(object):
    "B站漫画下载类"
    def __init__(self, comic_id=0, cookieData: dict = None):

        bili.__init__(self)
        if cookieData:
            bili.login_by_cookie(self, cookieData)

        if comic_id:
            self._manga_detail = bili.mangaDetail(self, comic_id)["data"]
            self._comic_id = self._manga_detail["id"]
            self._manga_detail["ep_list"].sort(key=lambda elem: elem["ord"])
        else:
            self._manga_detail = None

    def login_by_cookie(self, cookieData: dict) -> bool:
        '''使用cookie登录'''
        return bili.login_by_cookie(self, cookieData)

    def setComicId(comic_id: int):
        "设置当前漫画id"
        self._manga_detail = bili.mangaDetail(self, comic_id)["data"]
        self._comic_id = self._manga_detail["id"]
        self._manga_detail["ep_list"].sort(key=lambda elem: elem["ord"])

    def getIndex(self):
        "获取漫画章节列表"
        return self._manga_detail["ep_list"]

    def getTitle(self):
        "获取漫画名称"
        return self._manga_detail["title"]

    def getAuthors(self):
        "获取漫画作者名称(数组)"
        return self._manga_detail["author_name"]

    def getCover(self):
        "获取漫画封面图片链接"
        return self._manga_detail["vertical_cover"]

    def getNum(self):
        "获取漫画章节数量"
        return self._manga_detail["last_ord"]

    def getDownloadList(self, ep_id: int):
        "获取漫画章节下载列表"
        data = bili.mangaImageIndex(self, ep_id)["data"]["images"]
        url_list = [x["path"] for x in data]
        data = bili.mangaImageToken(self, url_list)["data"]
        url_list = [f'{x["url"]}?token={x["token"]}' for x in data]
        return url_list

    def download(self, ep_id: int, path: str):
        "下载一个章节"
        import os
        if not os.path.exists(path):
            os.mkdir(path)

        import requests
        _s = requests.session()

        list = self.getDownloadList(ep_id)
        n = 0
        for x in list:
            n += 1
            with open(f'{path}/{n:0>2}.jpg', 'wb') as f:
                f.write(_s.get(x).content)

    def downloadAll(self, path):
        "下载漫画所有可下载章节"
        import os
        if not os.path.exists(path):
            os.makedirs(path)
        title = self.getTitle()
        if path[-1] == '/':
            path = f'{path}{title}'
        else:
            path = f'{path}/{title}'
        if not os.path.exists(path):
            os.makedirs(path)
        
        bq = len(str(self.getNum()))
        for x in self.getIndex():
            name = x["title"]
            if name.replace(' ', '') == '':
                name = x["short_title"]
            if not x["is_locked"]:
                self.download(x['id'], f'{path}/{x["ord"]:0>{bq}}-{name}')
                print(f'{x["ord"]:0>{bq}}-{name} 下载完成')
            else:
                print(f'{x["ord"]:0>{bq}}-{name} 目前需要解锁')
