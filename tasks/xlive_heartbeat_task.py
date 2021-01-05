from BiliClient import asyncbili
from .push_message_task import webhook
import logging, asyncio, uuid, time, aiohttp

async def xlive_heartbeat_task(biliapi: asyncbili,
                               task_config: dict
                               ) -> None:

    rooms = None
    send_msg = task_config.get("send_msg", "")
    num: int = task_config.get("num", 0)
    max_time: float = task_config.get("time", 25)
    room_id = task_config.get("room_id", 0)
    if isinstance(room_id, int):
        if room_id:
            room_id = [room_id]
        else:
            room_id = []
    tasks = []

    if send_msg:
        rooms = await get_rooms(biliapi)
        if rooms:
            tasks.append(send_msg_task(biliapi, rooms, send_msg))
    
    if num:
        if not room_id:
            if not rooms:
                rooms = await get_rooms(biliapi)
            rid = level = intimacy = 0
            for roominfo in rooms:
                if roominfo[2] > level or (level == roominfo[2] and roominfo[3] > intimacy) and roominfo[1] == 1:
                    rid = roominfo[0]
                    level = roominfo[2]
                    intimacy = roominfo[3]
            if rid:
                tasks.append(heartbeat_task(biliapi, rid, num, max_time * 60))
            else:
                logging.info(f'{biliapi.name}: 没有获取到需要心跳的房间，跳过直播心跳')
                webhook.addMsg('msg_simple', f'{biliapi.name}:直播心跳失败\n')
        else:
            tasks.extend([heartbeat_task(biliapi, x, num, max_time * 60) for x in room_id])

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

    def reset(self):
        '''重新进入房间心跳'''
        data = {
            "id": self._data["id"],
            "device": self._data["device"]
            }
        data["id"][2] = 0
        self._data = data

    async def _encParam(self) -> str:
        '''加密参数'''
        urls = ('http://116.85.43.27:3000/enc', 'http://www.madliar.com:6000/enc')
        s = ''
        for url in urls:
            try:
                async with aiohttp.request("post", url=url, json={"t":self._data, "r":self._secret_rule}) as r:
                    ret = await r.json()
            except Exception as e:
                logging.warning(f'{self._biliapi.name}: 直播心跳获取加密参数异常，原因为{str(e)}')
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
    page = 1
    while True:
        try:
            ret = await biliapi.xliveFansMedal(page, 50)
        except Exception as e:
            logging.warning(f'{biliapi.name}: 获取有勋章的直播间异常，原因为{str(e)}')
            break
        else:
            if ret["code"] == 0:
                if not ret["data"]["fansMedalList"]:
                    break
                for medal in ret["data"]["fansMedalList"]:
                    if 'roomid' in medal:
                        result.append((medal["roomid"], medal["status"], medal["level"], medal["intimacy"], medal["is_lighted"]))
            else:
                logging.warning(f'{biliapi.name}: 获取有勋章的直播间失败，信息为{ret["message"]}')
                break
            page += 1

    return result

async def send_msg_task(biliapi: asyncbili,
                        rooms: list,
                        msg: str
                        ):
    su = 0
    for roominfo in rooms:
        if roominfo[4] == 1:
            continue
        retry = 3
        while retry:
            await asyncio.sleep(3)
            try:
                ret = await biliapi.xliveMsgSend(roominfo[0], msg)
            except Exception as e:
                logging.warning(f'{biliapi.name}: 直播在房间{roominfo[0]}发送信息异常，原因为{str(e)}，重试')
                retry -= 1
            else:
                if ret["code"] == 0:
                    if ret["message"] == '':
                        logging.info(f'{biliapi.name}: 直播在房间{roominfo[0]}发送信息成功')
                        su += 1
                        break
                    else:
                        logging.warning(f'{biliapi.name}: 直播在房间{roominfo[0]}发送信息，消息为{ret["message"]}，重试')
                        retry -= 1
                else:
                    logging.warning(f'{biliapi.name}: 直播在房间{roominfo[0]}发送信息失败，消息为{ret["message"]}，跳过')
                    break
    webhook.addMsg('msg_simple', f'{biliapi.name}:直播成功在{su}个房间发送消息\n')

async def heartbeat_task(biliapi: asyncbili,
                         room_id: int,
                         num: int,
                         max_time: float
                         ):
    try:
        ret = await biliapi.xliveGetRoomInfo(room_id)
        if ret["code"] != 0:
            logging.info(f'{biliapi.name}: 直播请求房间信息失败，信息为：{ret["message"]}，跳过直播心跳')
            webhook.addMsg('msg_simple', f'{biliapi.name}:直播心跳失败\n')
            return
        parent_area_id = ret["data"]["room_info"]["parent_area_id"]
        area_id = ret["data"]["room_info"]["area_id"]
        room_id = ret["data"]["room_info"]["room_id"] #为了防止上面的id是短id，这里确保得到的是长id
    except Exception as e:
        logging.warning(f'{biliapi.name}: 直播请求房间信息异常，原因为{str(e)}，跳过直播心跳')
        webhook.addMsg('msg_simple', f'{biliapi.name}:直播心跳失败\n')
        return

    try:
        buvid = await biliapi.xliveGetBuvid()
    except Exception as e:
        logging.warning(f'{biliapi.name}: 获取直播buvid异常，原因为{str(e)}，跳过直播心跳')
        webhook.addMsg('msg_simple', f'{biliapi.name}:直播心跳失败\n')
        return

    ii = 0
    ltime = 0
    retry = 2
    try:
        heart_beat = xliveHeartBeat(biliapi, buvid, parent_area_id, area_id, room_id)
        async for code, message, wtime in heart_beat: #每一次迭代发送一次心跳
            if code != 0:
                if retry:
                    logging.warning(f'{biliapi.name}: 直播心跳错误，原因为{message}，重新进入房间')
                    heart_beat.reset()
                    retry -= 1
                    continue
                else:
                    logging.warning(f'{biliapi.name}: 直播心跳错误，原因为{message}，跳过')
                    break
            
            ii += 1
            ltime += wtime
            if ii >= num:
                logging.info(f'{biliapi.name}: 成功在id为{room_id}的直播间发送完{ii}次心跳，退出直播心跳(达到最大心跳次数)')
                break
            elif ltime >= max_time:
                ltime -= wtime
                logging.info(f'{biliapi.name}: 成功在id为{room_id}的直播间发送完{ii}次心跳，退出直播心跳(达到最大心跳时间)')
                break
            else:
                logging.info(f'{biliapi.name}: 成功在id为{room_id}的直播间发送第{ii}次心跳')
                await asyncio.sleep(wtime) #等待wtime秒进行下一次迭代
    
    except Exception as e:
        logging.warning(f'{biliapi.name}: 直播心跳异常，原因为{str(e)}，退出直播心跳')

    webhook.addMsg('msg_simple', f'{biliapi.name}:直播心跳{ltime}秒,一共{ii}次\n')