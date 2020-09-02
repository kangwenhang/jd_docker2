# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import json

def remove_all_followed(data):
    '''取关所有关注的up主'''
    try:
        biliapi = BiliWebApi(data)
    except Exception as e: 
        print(f'登录验证id为{data["DedeUserID"]}的账户失败，原因为{str(e)}，跳过后续所有操作')
        return
    
    pn=1
    ps=50
    while True:
        try:
            list = biliapi.getFollowed(pn=pn, ps=ps)["data"]["list"]
        except Exception as e: 
            print(f'获取关注up主列表失败，原因为{str(e)}，跳过后续所有操作')
            break

        for x in list:
            try:
                biliapi.followedModify(x["mid"], 2)
            except:
                print(f'取关({x["uname"]})失败，原因为{str(e)}，跳过后续所有操作')
            else:
                print(f'已取关({x["uname"]})')

        if len(list) < ps:
            break

        pn += 1

def main(*args):
    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    input("请确认您确实要取关所有up主")

    for x in configData["cookieDatas"]:
        remove_all_followed(x)

if __name__=="__main__":
    main()