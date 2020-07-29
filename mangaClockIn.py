from models.Biliapi import BiliAppApi
import logging

access_keys = [""] #漫画app登录后的access_key，支持多账户

def mangaClockIn(access_key):
    logging.info(f'B站漫画签到脚本开始为access_key({access_key}的账户签到')
    try:
        result = BiliAppApi.mangaClockIn(access_key)
        logging.info(f'签到信息为：{str(result)}')
    except Exception as e:
        logging.warning(f'签到异常，原因为{str(e)}')

def main(*args):
    try:
        logging.basicConfig(filename="manga.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass
    for x in access_keys:
        mangaClockIn(x)

main()
