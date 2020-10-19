from BiliClient import asyncbili
from .import_once import get_ids
import logging

async def watch_task(biliapi: asyncbili) -> None:
    try:
        ret = await get_ids(biliapi)
    except Exception as e:
        logging.warning(f'{biliapi.name}: 获取B站分区视频信息异常，原因为{str(e)}，跳过模拟视频观看')
        return

    if ret["code"]:
        logging.warning(f'{biliapi.name}: 获取B站分区视频信息异常，原因为{ids["message"]}，跳过视频分享')
        return
    ids = ret["data"]["archives"]

    try:
        ret = await biliapi.report(ids[5]["aid"], ids[5]["cid"], 300)
        if ret["code"] == 0:
            logging.info(f'{biliapi.name}: 成功模拟观看av号为{ids[5]["aid"]}的视频')
        else:
            logging.warning(f'{biliapi.name}: 模拟观看av号为{ids[5]["aid"]}的视频投币失败，原因为：{ret["message"]}')
    except Exception as e: 
        logging.warning(f'{biliapi.name}: 模拟视频观看异常，原因为{str(e)}')
