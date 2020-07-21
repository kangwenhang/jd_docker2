#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Biliapi import Biliapi
import logging

cookieDatas = [{
    "SESSDATA": "",
    "bili_jct": "",
    "DedeUserID": "",
    },  #支持多账户，单账户只填写一组cookie就行
    {
    "SESSDATA": "",
    "bili_jct": "",
    "DedeUserID": "",
    }]

def bili_exp(cookieData):
   "B站直播签到，投币分享获取经验，模拟观看一个视频"
   logging.info(f': B站经验脚本开始为id为{cookieData["DedeUserID"]}的用户进行直播签到，投币点赞分享并观看一个首页视频')
   try:
       biliapi = Biliapi(cookieData)
   except Exception as e: 
       logging.error(f'登录验证id为{cookieData["DedeUserID"]}的账户失败，原因为{str(e)}，跳过此账户后续所有操作')
       return

   try:
       xliveInfo = biliapi.xliveSign()
       logging.info(f'bilibili直播签到信息：{str(xliveInfo)}')
   except Exception as e: 
       logging.warning(f'直播签到异常，原因为{str(e)}')

   try:
       reward = biliapi.getReward()
       logging.info(f'经验脚本开始前经验信息 ：{str(reward)}')
   except Exception as e: 
       logging.warning(f'获取账户经验信息异常，原因为{str(e)}，跳过此账户后续所有操作')
       return

   try:
       coin_num = biliapi.getCoin()
   except Exception as e: 
       logging.warning(f'获取账户剩余硬币数异常，原因为{str(e)}')
       coin_num = 0

   coin_exp_num = (50 - reward["coins_av"]) // 10
   toubi_num = coin_exp_num if coin_num > coin_exp_num else coin_num

   try:
       datas = biliapi.getRegions()
   except Exception as e: 
       logging.warning(f'获取B站分区视频信息异常，原因为{str(e)}，跳过此账户后续所有操作')
       return

   if(toubi_num > 0):
       for i in range(toubi_num):
           try:
               info = biliapi.coin(datas[i]["aid"], 1, 1)
               logging.info(f'投币信息 ：{str(info)}')
           except Exception as e: 
               logging.warning(f'投币异常，原因为{str(e)}')

   try:
       info = biliapi.report(datas[5]["aid"], datas[5]["cid"], 300)
       logging.info(f'模拟视频观看进度上报：{str(info)}')
   except Exception as e: 
       logging.warning(f'模拟视频观看异常，原因为{str(e)}')

   try:
       info = biliapi.share(datas[5]["aid"])
       logging.info(f'分享视频结果：{str(info)}')
   except Exception as e: 
       logging.warning(f'分享视频异常，原因为{str(e)}')

   logging.info(f'id为{cookieData["DedeUserID"]}的账户操作全部完成')

def main(*args):
    try:
        logging.basicConfig(filename="exp.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass
    for x in cookieDatas:
        bili_exp(x)

main()
 
