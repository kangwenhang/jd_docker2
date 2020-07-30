# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import logging
from userData.userData import cookieDatas

def bili_lottery(data):
    try:
        biliapi = BiliWebApi(data)
    except Exception as e: 
        logging.error(f'登录验证id为{data["DedeUserID"]}的账户失败，原因为{str(e)}，跳过后续所有操作')
        return

    try:
        datas = biliapi.getDynamicNew()["data"]["cards"] #获取"当前"的动态列表，不追溯历史动态
    except Exception as e: 
        logging.warning(f'获取动态列表异常，原因为{str(e)}，跳过后续所有操作')
        return
    
    already_repost_dyid = [] #记录动态列表中自己已经转发的动态id
    for x in datas:
        if str(x["desc"]["uid"]) == data["DedeUserID"] and x["desc"]["pre_dy_id"]: 
            already_repost_dyid.append(x["desc"]["pre_dy_id"])
            continue

        if x.__contains__("extension") and x["extension"].__contains__("lott"): #若抽奖标签存在
            uname = x["desc"]["user_profile"]["info"]["uname"]  #动态的主人的用户名
            dynamic_id = x["desc"]["dynamic_id"]  #动态id
            if not dynamic_id in already_repost_dyid: #若动态没被转发过
                try:
                    biliapi.repost(dynamic_id)
                    logging.info(f'id为{data["DedeUserID"]}的账户转发抽奖(用户名:{uname},动态id:{str(dynamic_id)})成功')
                except Exception as e: 
                    logging.warning(f'此次转发抽奖失败，原因为{str(e)}')

def main(*args):
    try:
        logging.basicConfig(filename="lottery.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass

    for x in cookieDatas:
        bili_lottery(x)

main()