from BiliClient import asyncbili
from .push_message_task import webhook
import logging, asyncio, uuid, time, aiohttp

async def xlive_anchor_task(biliapi: asyncbili,
                            task_config: dict
                            ) -> None:
    room_task = [anchor_task(biliapi, x, task_config) for x in task_config["rooms_id"]]
    if room_task:
        await asyncio.wait(room_task)

async def anchor_task(biliapi: asyncbili,
                      roomid: int,
                      task_config: dict
                      ):
    time = 0
    while task_config["times"] > time:
        try:
            ret = await biliapi.xliveAnchorCheck(roomid)
        except Exception as e:
            logging.warning(f'{biliapi.name}: 获取直播间{roomid}天选时刻信息异常，原因为{str(e)}')
            await asyncio.sleep(task_config["delay"])
        else:
            if ret["data"]:
                if ret["data"]["time"] > 0:
                    try:
                        rret = await biliapi.xliveAnchorJoin(ret["data"]["id"], ret["data"]["gift_id"], ret["data"]["gift_num"])
                    except Exception as e:
                        logging.warning(f'{biliapi.name}: 直播间{roomid}参与天选时刻{ret["data"]["id"]}异常，原因为{str(e)}')
                        await asyncio.sleep(ret["data"]["time"])
                    else:
                        if rret["code"] == 0:
                            logging.info(f'{biliapi.name}: 参与直播间{roomid}天选时刻{ret["data"]["id"]}成功')
                        else:
                            logging.warning(f'{biliapi.name}: 参与直播间{roomid}天选时刻{ret["data"]["id"]}失败，原因为{rret["message"]}')
                        await asyncio.sleep(ret["data"]["time"])
                else:
                    if biliapi.uid in [x["uid"] for x in ret["data"]["award_users"]]:
                        logging.info(f'{biliapi.name}: 直播间{roomid}天选时刻{ret["data"]["id"]}中奖')
                        webhook.addMsg('msg_simple', f'{biliapi.name}:天选时刻中奖\n')
                    else:
                        logging.info(f'{biliapi.name}: 直播间{roomid}天选时刻{ret["data"]["id"]}没有中奖')
                    await asyncio.sleep(ret["data"]["goaway_time"]+2)
            else:
                await asyncio.sleep(task_config["delay"])

        time += 1