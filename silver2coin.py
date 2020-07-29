# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
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

def silver2coin(cookieData):
   "B站直播银瓜子兑换硬币"
   logging.info(f': B站银瓜子兑换硬币脚本开始为id为{cookieData["DedeUserID"]}的用户进行兑换')
   try:
       biliapi = BiliWebApi(cookieData)
   except Exception as e: 
       logging.error(f'登录验证id为{cookieData["DedeUserID"]}的账户失败，原因为{str(e)}，跳过此账户后续所有操作')
       return

   try:
       info = biliapi.xliveGetStatus()
   except Exception as e: 
       logging.warning(f'获取瓜子信息异常，原因为{str(e)}')
   print(info)
   if(info["code"] != 0):
       logging.warning(f'获取瓜子信息失败，信息为({info["msg"]})，跳过此账户后续所有操作')
       return

   num = info["data"]["silver_2_coin_left"]
   if(num == 0):
       logging.warning(f'今日兑换额度已经用完')
       return

   try:
       info = biliapi.silver2coin()
   except Exception as e: 
       logging.warning(f'银瓜子兑换硬币异常，原因为{str(e)}，跳过此账户后续所有操作')
       return
   print(info)
   if(info["code"] != 0):
       logging.warning(f'兑换失败，信息为({info["msg"]})')
       return

   logging.warning('成功将银瓜子兑换为1个硬币')
   
def main(*args):
    try:
        logging.basicConfig(filename="silver2coin.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass
    for x in cookieDatas:
        silver2coin(x)

main()
