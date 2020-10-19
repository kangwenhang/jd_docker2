from BiliClient import asyncbili
from .import_once import get_ids
import logging

async def share_task(biliapi: asyncbili) -> None:
    try:
        ret = await get_ids(biliapi)
    except Exception as e:
        logging.warning(f'{biliapi.name}: 获取B站分区视频信息异常，原因为{str(e)}，跳过视频分享')
        return

    if ret["code"]:
        logging.warning(f'{biliapi.name}: 获取B站分区视频信息异常，原因为{ret["message"]}，跳过视频分享')
        return
    ids = ret["data"]["archives"]

    try:
        ret = await biliapi.share(ids[5]["aid"])
        if ret["code"] == 0:
            logging.info(f'{biliapi.name}: 成功分享av号为{ids[5]["aid"]}的视频')
        else:
            logging.warning(f'{biliapi.name}: 分享av号为{ids[5]["aid"]}的视频失败，原因为：{ret["message"]}')
    except Exception as e: 
        logging.warning(f'{biliapi.name}: 分享视频异常，原因为{str(e)}')
