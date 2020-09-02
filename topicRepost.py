# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import json, time

topiclist = ('抽奖','动态抽奖','互动抽奖')#话题列表
islike = True #转发前是否关注

now_time = int(time.time())#当前时间
end_time = now_time - (now_time + 28800) % 86400  #结束时间，为今天0点
start_time = end_time - 86400                     #开始时间，为昨天0点                    
#转发开始时间到结束时间内的所有话题动态

def bili_topic_repost(data, list, time):
    '''转发指定时间段内的话题'''
    alr = []#记录已经转发的动态用于去重
    try:
        biliapi = BiliWebApi(data)
    except Exception as e: 
        print(f'登录验证id为{data["DedeUserID"]}的账户失败，原因为{str(e)}，跳过后续所有操作')
        return
    
    for tpn in list:
        topic = biliapi.getTopicList(tpn)
        for x in topic:
            stime = x["desc"]["timestamp"]
            if(stime > time[1]):
                continue
            if(stime < time[0]):
                break
            dyid = x["desc"]["dynamic_id"]
            if dyid in alr:
                continue
            try:
                if islike and x["desc"]["is_liked"] == 0:
                    if biliapi.followed(x["desc"]["uid"])['code'] != 0:
                        print("关注异常")
                biliapi.repost(dyid)
                print(f'id为{data["DedeUserID"]}的账户转发抽奖(用户名:{x["desc"]["user_profile"]["info"]["uname"]},动态id:{dyid})成功')
            except Exception as e: 
                print(f'此次转发抽奖失败，原因为{str(e)}')
            else:
                alr.append(dyid)

def main(*args):
    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    for x in configData["cookieDatas"]:
        bili_topic_repost(x, topiclist, (start_time, end_time))

if __name__=="__main__":
    main()