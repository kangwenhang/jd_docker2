# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import json, time
import logging

def bili_lottery(data, stime, etime):
    "抽取从stime到etime之间的抽奖，stime<etime"
    try:
        biliapi = BiliWebApi(data)
    except Exception as e: 
        logging.error(f'登录验证id为{data["DedeUserID"]}的账户失败，原因为{str(e)}，跳过后续所有操作')
        return

    try:
        biliapi.xliveUserOnlineHeart() #发两个直播在线心跳
        biliapi.xliveHeartBeat()
    except: 
        pass

    datas = biliapi.getDynamic()
    try:
        for x in datas:
            timestamp = x["desc"]["timestamp"]
            if(timestamp > etime):
                continue
            elif(timestamp < stime):
                break
            if 'extension' in x and 'lott' in x["extension"]: #若抽奖标签存在
                uname = x["desc"]["user_profile"]["info"]["uname"]  #动态的主人的用户名
                dyid = x["desc"]["dynamic_id"]
                try:
                    biliapi.dynamicRepostReply(dyid, '从未中奖，从未放弃[doge]')
                    logging.info(f'id为{data["DedeUserID"]}的账户转发抽奖(用户名:{uname},动态id:{dyid})成功')
                except Exception as e: 
                    logging.warning(f'转发抽奖失败，原因为{str(e)}')
            
    except Exception as e: 
        logging.warning(f'获取动态列表、异常，原因为{str(e)}，跳过后续所有操作')
        return

def main(*args):
    try:
        logging.basicConfig(filename="lottery.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass

    now_time = int(time.time()) + 10 #当前时间
    time1 = now_time - now_time % 600 #当前时间对10分钟取整
    time2 = time1 - 600 #再取前10分钟
    #对上一个10分钟区间内的抽奖动态进行转发，比如9:15的上一个十分钟区间为9:00--9:10

    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    for x in configData["cookieDatas"]:
        bili_lottery(x, time2, time1)

if __name__=="__main__":
    main()
