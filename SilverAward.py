from models.Biliapi import BiliAppApi
import logging
import time
from userData.userData import app_access_keys

'''
腾讯云函数cron表达式例子
1. 0 0,3,9,18,21,27,36,39,45,54 2 * * *
2. 0 0,6,15,18,24,33 3 * * *
表达式1表示凌晨2点在0,3,9,18,21,27,36,39,45,54分钟时执行脚本，表达式2同理

非大老爷，每天可以领3轮银瓜子，只需要添加一个触发器，触发周期自定义，cron用表达式1就行
大老爷，每天可以领5轮银瓜子，需要添加两个触发器，第二个触发器用表达式2
'''

def getAward(access_key):
    logging.info(f'B站直播获取领取银瓜子脚本开始为access_key({access_key})的账户获取银瓜子')
    try:
        result = BiliAppApi.xliveGetCurrentTask(access_key)
    except Exception as e:
        logging.warning(f'获取本次宝箱信息异常，原因为({str(e)})，跳过本账户后续操作')
        return

    if(result["code"] != 0):
        if(result["code"] == -10017):
            logging.warning(f'获取本次宝箱信息失败，信息为({result["msg"]})，今日内请不要再对此账户执行脚本')
        else:
            logging.warning(f'获取本次宝箱信息失败，信息为({result["msg"]})，跳过本账户后续操作')
        return

    #result["data"]["minute"]为等待开宝箱的时间(分钟)，在3,6,9这三个值中循环取得
    #result["data"]["silver"]为这次任务完成后可以获得的银瓜子数目
    #result["data"]["time_start"]为这次任务的开始时间(时间戳)，也就是上面获取宝箱信息的时间
    #result["data"]["time_end"]为这次任务的结束时间(时间戳)，也就是开始时间加等待时间，超过这个时间才可以执行下面的打开宝箱
    
    timeEnd = time.strftime("%Y/%d/%m %H:%M:%S", time.localtime(result["data"]["time_end"]))
    logging.info(f'本次宝箱领取成功，在{timeEnd}后就可以领取{result["data"]["silver"]}个银瓜子')
    
    time_difference = result["data"]["time_end"] - int(time.time()) #取时间差
    if(time_difference > 0): #还没到开宝箱时间
        if(time_difference < 11): #距离开宝箱时间在10s内，等待开宝箱，超过10s则立即退出，目的是修正领取宝箱的时间误差
            time.sleep(time_difference)
        else:
            logging.warning(f'还没有到开宝箱的时间，跳过开启宝箱')
            return

    try:
        result = BiliAppApi.xliveGetAward(access_key)
    except Exception as e:
        logging.warning(f'打开宝箱异常，信息为({result["msg"]})，获取银瓜子失败')
        return

    if(result["code"] != 0):
        logging.warning(f'获取银瓜子失败，信息为({result["msg"]})')
        return
    logging.info(f'成功领取{result["data"]["awardSilver"]}个银瓜子')

    try:
        result = BiliAppApi.xliveGetCurrentTask(access_key)
    except Exception as e:
        logging.warning(f'获取下次宝箱信息异常，原因为({str(e)})，跳过本账户后续操作')
        return

    if(result["code"] != 0):
        logging.warning(f'获取下次宝箱信息失败，信息为({result["msg"]})')
        return

    timeEnd = time.strftime("%Y/%d/%m %H:%M:%S", time.localtime(result["data"]["time_end"]))
    logging.info(f'下次宝箱领取成功，在{timeEnd}后就可以领取{result["data"]["silver"]}个银瓜子')

def main(*args):
    try:
        logging.basicConfig(filename="SilverAward.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass
    for x in app_access_keys:
        getAward(x)

main()
