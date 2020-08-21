from models.Biliapi import BiliWebApi
import logging
import time, json

def getAward(cookieData):
    logging.info(f'B站直播获取领取银瓜子脚本开始为id为({cookieData["DedeUserID"]})的账户获取银瓜子')
    try:
        biliapi = BiliWebApi(cookieData)
    except Exception as e:
        logging.warning(f'获取银瓜子异常，原因为{str(e)},跳过此账户后续操作')
        return
    try:
        result = biliapi.xliveGetCurrentTask()
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
        result = biliapi.xliveGetAward()
    except Exception as e:
        logging.warning(f'打开宝箱异常，信息为({result["msg"]})，获取银瓜子失败')
        return

    if(result["code"] != 0):
        logging.warning(f'获取银瓜子失败，信息为({result["msg"]})')
        return
    logging.info(f'成功领取{result["data"]["awardSilver"]}个银瓜子')

    try:
        result = biliapi.xliveGetCurrentTask()
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

    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    for x in configData["cookieDatas"]:
        getAward(x)

if __name__=="__main__":
    main()
