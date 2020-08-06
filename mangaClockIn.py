from models.Biliapi import BiliAppApi
import logging
from userData.userData import app_access_keys

def mangaClockIn(access_key):
    logging.info(f'B站漫画签到脚本开始为access_key({access_key})的账户签到')
    try:
        biliapi = BiliAppApi(access_key)
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
    for x in app_access_keys:
        mangaClockIn(x)

main()#云函数使用注释掉这一句
