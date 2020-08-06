# -*- coding: utf-8 -*-
from models.Biliapi import *
from models.PushMessage import PushMessage
try: #兼容本地目录和云函数目录
    from userData.userData import *
except:
    from userData import *

def main(*args):
    pm = PushMessage(SCKEY, "B站经验脚本账户有效性检查")

    for x in cookieDatas:
        try:
            biliapi = BiliWebApi(x)
            print(f'id为{x["DedeUserID"]}的账户验证有效')
        except Exception as e: 
            pm.addMsg(f'id为{x["DedeUserID"]}的账户登录验证失败,原因为{str(e)}。')

    for x in app_access_keys:
        try:
            if BiliAppApi.isValid(x):
                print(f'B站客户端access_key为({x})的账户验证有效')
            else:
                pm.addMsg(f'B站客户端access_key为({x})的账户登录失效。')
        except Exception as e: 
            pm.addMsg(f'B站客户端access_key为({x})的账户登录验证失败,原因为{str(e)}。')

    msg = pm.getMsg()
    if msg:
        print(msg)
        try:
            info = pm.pushMessage()
            print(f'消息推送信息为{str(info)}')
        except Exception as e: 
            print(f'消息推送异常，原因为{str(e)}。')
    else:
        print(f'没有账号失效消息')

main()#云函数使用注释掉这一句