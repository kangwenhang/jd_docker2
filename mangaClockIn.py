from models.Biliapi import BiliWebApi
import logging
import json

def mangaClockIn(cookieData):
    logging.info(f'B站漫画签到脚本开始为id为({cookieData["DedeUserID"]})的账户签到')
    try:
        biliapi = BiliWebApi(cookieData)
    except Exception as e:
        logging.warning(f'签到异常，原因为{str(e)},跳过此账户后续操作')
        return
    try:
        result = biliapi.mangaClockIn()
        if(result["code"] == 0):
            logging.info(f'签到成功')
        else:
            logging.info(f'签到失败,信息为：{result["msg"]}')
    except Exception as e:
        logging.warning(f'签到异常，原因为{str(e)}')

def main(*args):
    try:
        logging.basicConfig(filename="manga.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass

    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    for x in configData["cookieDatas"]:
        mangaClockIn(x)

if __name__=="__main__":
    main()

