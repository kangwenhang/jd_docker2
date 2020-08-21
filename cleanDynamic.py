# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import time
from userData.userData import cookieDatas
import json

endTime = 0  #结束时间戳(10位)，默认为当前时间
startTime = 0 #开始时间戳(10位)，默认为0
#遍历从startTime到endTime(startTime<endTime)之间的所有动态，删除符合条件的动态

keywords = ("#抽奖#","#互动抽奖#") #包含此关键字且在2个月前的动态会满足删除条件




nowTime = int(time.time())
endTime = nowTime if endTime == 0 else endTime

def filterB(biliapi, card, timestamp):
    "判断是否是抽奖过期动态"
    if 'origin_extension' in card and 'lott' in card["origin_extension"]:
        lott = json.loads(card["origin_extension"]["lott"])
        if 'lottery_time' in lott and lott["lottery_time"] <=  nowTime:
            return True
    else:
        return False
    dyid = card["item"]["orig_dy_id"]
    etime = biliapi.getLotteryNotice(dyid)["data"]["lottery_time"]
    
    if etime <= nowTime:
        return True
    return False

def filterC(biliapi, card, timestamp):
    "判断是否是动态是否含有关键字"
    if timestamp > nowTime - 5184000:
        return False
    if 'origin' in card:
        origin = json.loads(card["origin"])
        text = origin["item"]["description"]
        for x in keywords:
            if x in text:
                return True
    return False

def filterD(biliapi, card, timestamp):
    "判断动态是否被删除"
    if 'item' in card and 'miss' in card["item"] and card["item"]["miss"] == 1:
        return True
    return False

def filter(filters, *args):
    for x in filters:
        if x(*args):
            return True
    return False

def cleanDynamic(cookieData, filters):
    biliapi = BiliWebApi(cookieData)
    print(f'开始为id为{cookieData["DedeUserID"]}的账户清理动态')
    datas = biliapi.getMyDynamic()
    for x in datas:
        timestamp = x["desc"]["timestamp"]
        if(timestamp > endTime):
            continue
        if(timestamp < startTime):
            break
        dynamic_id = x["desc"]["dynamic_id"]
        card = json.loads(x["card"])
        if filter(filters, biliapi, card, timestamp):
            biliapi.removeDynamic(dynamic_id)
            print(f'已删除id为{dynamic_id}的动态')

def main(*args):
    filters = (filterB,filterC,filterD)
    for x in cookieDatas:
        cleanDynamic(x, filters)
    
if __name__=="__main__":
    main()
