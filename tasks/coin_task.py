from BiliClient import asyncbili
from .import_once import get_ids
import logging, asyncio

async def coin_task(biliapi: asyncbili, 
                    task_config: dict
                    ) -> None:

    if biliapi.myexp >= task_config["target_exp"]:
        logging.info(f'{biliapi.name}: 已达到经验目标，跳过投币')
        return

    coin_num = biliapi.mycoin
    if coin_num == 0:
        logging.info(f'{biliapi.name}: 硬币不足，跳过投币')
        return

    try:
        reward = (await biliapi.getReward())["data"]
        #print(f'{biliapi.name}: 经验脚本开始前经验信息 ：{str(reward)}')
    except Exception as e: 
        logging.warning(f'{biliapi.name}: 获取账户经验信息异常，原因为{str(e)}，跳过投币')
        return

    coin_exp_num = (task_config["num"] * 10 - reward["coins_av"]) // 10
    toubi_num = coin_exp_num if coin_num > coin_exp_num else coin_num
    
    if toubi_num < 1:
        return
    else:
        try:
            ret = await get_ids(biliapi)
        except Exception as e:
            logging.warning(f'{biliapi.name}: 获取B站分区视频信息异常，原因为{str(e)}，跳过投币')
            return

        if ret["code"]:
            logging.warning(f'{biliapi.name}: 获取B站分区视频信息异常，原因为{ret["message"]}，跳过视频分享')
            return
        ids = ret["data"]["archives"]

        tasks = [asyncio.ensure_future(biliapi.coin(ids[ii]["aid"], 1, 1)) for ii in range(toubi_num)]
        for task in asyncio.as_completed(tasks):
            aid, ret = await task
            if ret["code"] == 0:
                logging.info(f'{biliapi.name}: 成功给av号为{aid}的视频投一个币')
            else:
                logging.info(f'{biliapi.name}: 给av号为{aid}的视频投币失败，原因为：{ret["message"]}')