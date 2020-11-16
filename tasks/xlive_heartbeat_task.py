from BiliClient import asyncbili
import logging, asyncio, uuid, time, aiohttp

async def xlive_heartbeat_task(biliapi: asyncbili,
                               task_config: dict
                               ) -> None:

    rooms = None
    send_msg = task_config.get("send_msg", "")
    num: int = task_config.get("num", 0)
    room_id: int = task_config.get("room_id", 0)
    tasks = []

    if send_msg:
        rooms = await get_rooms(biliapi)
        tasks.append(send_msg_task(biliapi, rooms, send_msg))
    
    if num:
        if not room_id > 0:
            if not rooms:
                rooms = await get_rooms(biliapi)
            level = intimacy = 0
            for roominfo in rooms:
                if roominfo[2] > level or (level == roominfo[2] and roominfo[3] > intimacy) and roominfo[1] == 1:
                    room_id = roominfo[0]
                    level = roominfo[2]
                    intimacy = roominfo[3]

        if room_id > 0:
            tasks.append(heartbeat_task(biliapi, room_id, num))
        else:
            logging.info(f'{biliapi.name}: 没有获取到需要心跳的房间，跳过直播心跳')

    if tasks:
        await asyncio.wait(tasks)

class xliveHeartBeat:
    '''B站心跳异步迭代器，每迭代一次发送一次心跳'''

    def __init__(self, biliapi: asyncbili, buvid: str, parent_area_id: int, area_id: int, room_id: int):
        self._biliapi = biliapi
        self._data = {
            "id": [parent_area_id, area_id, 0, room_id],
            "device": [buvid, str(uuid.uuid4())]
            }
        self._secret_rule: list = None

    async def _encParam(self) -> str:
        '''加密参数'''
        urls = ('http://116.85.43.27:3000/enc', 'http://www.madliar.com:6000/enc')
        s = ''
        for url in urls:
            try:
                async with aiohttp.request("post", url=url, json={"t":self._data, "r":self._secret_rule}) as r:
                    ret = await r.json()
            except Exception as e:
                logging.warning(f'{biliapi.name}: 直播心跳获取加密参数异常，原因为{str(e)}')
            else:
                if 's' in ret:
                    s = ret["s"]
                    break
        return s

    def __aiter__(self):
        return self

    async def __anext__(self):
        
        if self._data["id"][2] == 0:   #第1次执行进入房间心跳 HeartBeatE
            ret = await self._biliapi.xliveHeartBeatE(**self._data)
            if ret["code"] == 0:
                self._data["ets"] = ret["data"]["timestamp"]
                self._data["benchmark"] = ret["data"]["secret_key"]
                self._data["time"] = ret["data"]["heartbeat_interval"]
                self._secret_rule = ret["data"]["secret_rule"]
                self._data["id"][2] += 1
            return ret["code"], ret["message"], ret["data"]["heartbeat_interval"]

        else:                          #第n>1次执行进入房间心跳 HeartBeatX
            self._data["ts"] = int(time.time() * 1000)
            self._data["s"] = await self._encParam()
            ret = await self._biliapi.xliveHeartBeatX(**self._data)
            if ret["code"] == 0:
                self._data["ets"] = ret["data"]["timestamp"]
                self._data["benchmark"] = ret["data"]["secret_key"]
                self._data["time"] = ret["data"]["heartbeat_interval"]
                self._secret_rule = ret["data"]["secret_rule"]
                self._data["id"][2] += 1
            return ret["code"], ret["message"], ret["data"]["heartbeat_interval"]

async def get_rooms(biliapi: asyncbili):
    '''获取所有勋章房间'''
    result = []
    try:
        ret = await biliapi.get_home_medals()
    except Exception as e:
        logging.warning(f'{biliapi.name}: 获取有勋章的直播间异常，原因为{str(e)}')
        return result

    if ret["code"] == 0 and ret["data"]["cnt"] > 0:
        for x in ret["data"]["list"]:
            try:
                accinfo = await biliapi.accInfo(x["target_id"])
            except Exception as e:
                logging.warning(f'{biliapi.name}: 查询up主{x["target_id"]}的信息异常，原因为{str(e)}')
            else:
                if accinfo["code"] == 0:
                    result.append((accinfo["data"]["live_room"]["roomid"], accinfo["data"]["live_room"]["liveStatus"], x["level"], x["intimacy"]))
                else:
                    logging.warning(f'{biliapi.name}: 查询up主{x["target_id"]}的信息失败，信息为{accinfo["message"]}')
    else:
        logging.info(f'{biliapi.name}: 获取有勋章的直播间失败，可能是没有勋章，{ret["message"]}')

    return result

async def send_msg_task(biliapi: asyncbili,
                        rooms: list,
                        msg: str
                        ):
    for roominfo in rooms:
        retry = 3
        while retry:
            try:
                ret = await biliapi.xliveMsgSend(roominfo[0], msg)
            except Exception as e:
                logging.warning(f'{biliapi.name}: 直播在房间{roominfo[0]}发送信息异常，原因为{str(e)}，重试')
                retry -= 1
            else:
                if ret["code"] == 0:
                    if ret["message"] == '':
                        logging.info(f'{biliapi.name}: 直播在房间{roominfo[0]}发送信息成功')
                        break
                    else:
                        logging.warning(f'{biliapi.name}: 直播在房间{roominfo[0]}发送信息，消息为{ret["message"]}，重试')
                        retry -= 1
                else:
                    logging.warning(f'{biliapi.name}: 直播在房间{roominfo[0]}发送信息失败，消息为{ret["message"]}，跳过')
                    break
            await asyncio.sleep(3)
        await asyncio.sleep(3)

async def heartbeat_task(biliapi: asyncbili,
                         room_id: int,
                         num: int
                         ):
    try:
        ret = await biliapi.xliveGetRoomInfo(room_id)
        if ret["code"] != 0:
            logging.info(f'{biliapi.name}: 直播请求房间信息失败，信息为：{ret["message"]}，跳过直播心跳')
            return
        parent_area_id = ret["data"]["room_info"]["parent_area_id"]
        area_id = ret["data"]["room_info"]["area_id"]
        room_id = ret["data"]["room_info"]["room_id"] #为了防止上面的id是短id，这里确保得到的是长id
    except Exception as e:
        logging.warning(f'{biliapi.name}: 直播请求房间信息异常，原因为{str(e)}，跳过直播心跳')
        return

    try:
        buvid = await biliapi.xliveGetBuvid()
    except Exception as e:
        logging.warning(f'{biliapi.name}: 获取直播buvid异常，原因为{str(e)}，跳过直播心跳')
        return

    ii = 0
    try:
        async for code, message, wtime in xliveHeartBeat(biliapi, buvid, parent_area_id, area_id, room_id): #每一次迭代发送一次心跳
            if code != 0:
                logging.warning(f'{biliapi.name}: 直播心跳错误，原因为{message}，跳过直播心跳')
                return
            ii += 1
            if ii < num:
                logging.info(f'{biliapi.name}: 成功在id为{room_id}的直播间发送第{ii}次心跳')
                await asyncio.sleep(wtime) #等待wtime秒进行下一次迭代
            else:
                logging.info(f'{biliapi.name}: 成功在id为{room_id}的直播间发送完{ii}次心跳，退出直播心跳')
                break
    
    except Exception as e:
        logging.warning(f'{biliapi.name}: 直播心跳异常，原因为{str(e)}，退出直播心跳')
        return