import requests
import json
class PushMessage(object):
    "Server酱提供的将消息推送到微信的接口"
    def __init__(self, SCKEY, title):
        "绑定sckey"
        self.__SCKEY = SCKEY
        self.__sendUrl = f'https://sc.ftqq.com/{SCKEY}.send'
        self.__title = title
        self.__message = ""

    def sendText(self, text, desp):
        "发送消息"
        post_data = {
            "text": text,
            "desp": desp
            }
        content = requests.post(self.__sendUrl, data=post_data)
        return json.loads(content.text)

    def addMsg(self, msg, newLine=True):
        "添加要推送的消息"
        self.__message = f"{self.__message}{msg}\n" if newLine else f"{self.__message}{msg}"

    def pushMessage(self):
        "推送已经添加消息"
        return self.sendText(self.__title, self.__message)

    def setMsg(self, msg):
        "设置要推送的消息"
        self.__message = msg

    def getMsg(self):
        "获取要推送的消息"
        return self.__message

    def setTitle(self, title):
        "设置消息标题"
        self.__title = title

    def getTitle(self):
        "获取当前消息标题"
        return self.__title

