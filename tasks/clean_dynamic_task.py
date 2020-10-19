from BiliClient import asyncbili
import logging, json
from .import_once import now_time

async def clean_dynamic_task(biliapi: asyncbili,
                       task_config: dict
                       ) -> None:
    try:
        async for x in biliapi.getMyDynamic():
            dyid = x["desc"]["dynamic_id"]
            card = json.loads(x["card"])

            if 'item' in card and 'miss' in card["item"] and card["item"]["miss"] == 1:
                await biliapi.removeDynamic(dyid)
                logging.info(f'{biliapi.name}: 已删除id为{dyid}的动态，原因为：动态已被原作者删除')
                continue
            
            if 'origin_extension' in card and 'lott' in card["origin_extension"]:
                lott = json.loads(card["origin_extension"]["lott"])
                if 'lottery_time' in lott and lott["lottery_time"] <=  now_time:
                    await biliapi.removeDynamic(dyid)
                    logging.info(f'{biliapi.name}: 已删除id为{dyid}的动态，原因为：过期抽奖')
                    continue

            if 'item' in card and 'orig_dy_id' in card["item"]:
                ret = (await biliapi.getLotteryNotice(card["item"]["orig_dy_id"]))["data"]
                if 'lottery_time' in ret and ret["lottery_time"] <= now_time:
                    await biliapi.removeDynamic(dyid)
                    logging.info(f'{biliapi.name}: 已删除id为{dyid}的动态，原因为：过期抽奖')
                    continue

            if 'origin' in card:
                origin = json.loads(card["origin"])
                if 'item' in origin and 'description' in origin["item"]:
                    if 'description' in card["item"]:
                        text = origin["item"]["description"]
                    elif 'content' in card["item"]:
                        text = card["item"]["content"]
                    else:
                        text = None
                    if text:
                        for x in task_config["black_keywords"]:
                            if x in text:
                                logging.info(f'{biliapi.name}: 已删除id为{dyid}的动态，原因为：包含黑名单关键字{x}')
                                continue
    except Exception as e: 
        logging.warning(f'{biliapi.name}: 获取动态列表、异常，原因为{str(e)}，跳过动态清理')