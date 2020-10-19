from BiliClient import asyncbili
import asyncio, logging

activity_task_lock = asyncio.Lock()
async def activity_task(biliapi: asyncbili,
                        task_config: dict
                        ) -> None:

    for x in task_config["activities"]:
        for y in range(2, 5):
            try:
                await biliapi.activityAddTimes(x["sid"], y) #执行增加抽奖次数操作,一般是分享转发
            except Exception as e:
                logging.warning(f'{biliapi.name}: 增加({x["name"]})活动抽奖次数异常,原因为({str(e)})')

        try:
            ret = await biliapi.activityMyTimes(x["sid"])
            if ret["code"] == 0:
                times = ret["data"]["times"]
            else:
                logging.info(f'{biliapi.name}: 获取({x["name"]})活动抽奖次数错误，消息为({ret["message"]})')
                continue
        except Exception as e:
            logging.warning(f'{biliapi.name}: 获取({x["name"]})活动抽奖次数异常，原因为({str(e)})，跳过参与活动')
            continue

        for ii in range(times):
            try:
                async with activity_task_lock:
                    ret = await biliapi.activityDo(x["sid"], 1)
                    if ret["code"]:
                        logging.info(f'{biliapi.name}: 参与({x["name"]})活动第({ii + 1}/{times})次，结果为({ret["message"]})')
                    else:
                        logging.info(f'{biliapi.name}: 参与({x["name"]})活动第({ii + 1}/{times})次，结果为({ret["data"][0]["gift_name"]})')
                    await asyncio.sleep(6) #抽奖延时
            except Exception as e:
                logging.warning(f'{biliapi.name}: 参与({x["name"]})活动异常，原因为({str(e)})')