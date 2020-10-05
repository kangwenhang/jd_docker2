# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
from models.PushMessage import PushMessage
import json, sys

def main(*args):
    try:
        with open('config/config.json','r',encoding='utf-8') as fp:
            configData = json.load(fp)
    except:
        print('配置文件加载错误，如果在actions中运行，请检查是否正确创建了secrets(biliconfig)，如果在本地和云函数中运行，请检查config.json文件是否填写正确，')
        sys.exit(6)

    pm = PushMessage("B站经验脚本账户有效性检查", SCKEY=configData["SCKEY"], email=configData["email"])

    ii = 0
    for x in configData["cookieDatas"]:
        ii += 1
        try:
            biliapi = BiliWebApi(x)
            like = biliapi.likeCv(7793107)
            if like["code"] != 0 and like["code"] != 65006:
                print(f'{ii}.id为{x["DedeUserID"]}的账户可能账号有异常，检查bili_jct参数是否有效或账号是否被封禁({biliapi.getLevel()},{biliapi.verified})')
            else:
                print(f'{ii}.id为{x["DedeUserID"]}的账户验证有效({biliapi.getLevel()},{biliapi.verified})')
        except Exception as e: 
            pm.addMsg(f'{ii}.id为{x["DedeUserID"]}的账户登录验证失败,原因为{str(e)}。')

    msg = pm.getMsg()
    if msg:
        print(msg)
        try:
            pm.pushMessage()
        except Exception as e: 
            print(f'消息推送异常，原因为{str(e)}。')
        sys.exit(8)
    else:
        print('没有账号失效消息')

if __name__=="__main__":
    main()
