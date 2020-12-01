from BiliClient import asyncbili
from aiohttp.client_exceptions import ServerDisconnectedError
from .push_message_task import webhook
from .import_once import now_time
from random import randint
import logging, json, asyncio, re, aiohttp

end_time = now_time - (now_time + 28800) % 86400 + 43200 #当天中午12点
start_time = end_time - 86400

async def lottery_task(biliapi: asyncbili, 
                       task_config: dict    #配置
                       ) -> None:
    if 'repost_by_others' in task_config and task_config["repost_by_others"]:
        await repost_task_E(biliapi, task_config)
    else:
        await repost_task_X(biliapi, task_config)

async def get_dynamic(biliapi: asyncbili) -> dict:
    '''取B站用户动态数据，异步生成器'''
    offset = 0
    hasnext = True
    retry = 3 #连续失败重试次数
    while hasnext:
        try:
            ret = await biliapi.getDynamic(offset)
        except ServerDisconnectedError: 
            logging.warning(f'{biliapi.name}: 获取动态列表时服务器强制断开连接，尝试重试动态列表获取')
        except Exception as e: 
            if retry:
                retry -= 1
                logging.warning(f'{biliapi.name}: 获取动态列表异常，原因为{str(e)}，重试动态列表获取')
            else:
                logging.warning(f'{biliapi.name}: 获取动态列表异常，原因为{str(e)}，跳过获取')
                break
        else:
            retry = 3
            if ret["code"] == 0:
                if "has_more" in ret["data"]:
                    hasnext = (ret["data"]["has_more"] == 1)
                if not "cards" in ret["data"]:
                    break
                cards = ret["data"]["cards"]
                if not len(cards):
                    break
                offset = cards[-1]["desc"]["dynamic_id"]
                for x in cards:
                    yield x
            else:
                logging.warning(f'{biliapi.name}: 获取动态列表失败，原因为{ret["message"]}，跳过转发抽奖动态')
                break

async def get_space_dynamic(biliapi: asyncbili,
                            uid: int,
                            ) -> dict:
    '''取B站空间动态数据，异步生成器'''
    offset = ''
    hasnext = True
    retry = 3 #连续失败重试次数
    while hasnext:
        try:
            ret = await biliapi.getSpaceDynamic(uid, offset)
        except ServerDisconnectedError: 
            logging.warning(f'{biliapi.name}: 获取空间动态时服务器强制断开连接，尝试重试空间动态获取')
        except Exception as e: 
            if retry:
                retry -= 1
                logging.warning(f'{biliapi.name}: 获取空间动态列表异常，原因为{str(e)}，重试空间动态列表获取')
            else:
                logging.warning(f'{biliapi.name}: 获取空间动态列表异常，原因为{str(e)}，跳过获取')
                break
        else:
            if ret["code"] == 0 and ret["data"]:
                hasnext = (ret["data"]["has_more"] == 1)
                if 'cards' in ret["data"] and ret["data"]["cards"]:
                    for x in ret["data"]["cards"]:
                        yield x
                    offset = x["desc"]["dynamic_id_str"]
                    retry = 3
                else:
                    retry -= 1
            else:
                retry -= 1
                logging.warning(f'{biliapi.name}: 获取空间动态列表失败，信息为{ret["message"]}，重试获取')

            if not retry:
                logging.warning(f'{biliapi.name}: 获取空间动态列表失败次数太多，跳过获取')
                break

async def repost_task_E(biliapi: asyncbili, 
                       task_config: dict
                       ) -> None:
    '''跟踪转发模式'''
    force_follow = task_config.get("force_follow", False)
    users = set()
    su1 = su2 = er1 = er2 = 0
    for uid in task_config["repost_by_others"]:
        async for x in get_space_dynamic(biliapi, uid):
            timestamp = x["desc"]["timestamp"]
            if(timestamp > end_time):
                continue
            elif(timestamp < start_time):
                break

            if 'previous' in x["desc"]:
                dyid = x["desc"]["previous"]["dynamic_id_str"]
                oid, type = dyid, 17
                uid = x["desc"]["previous"]["uid"]
            elif 'origin' in x["desc"]:
                dyid = x["desc"]["origin"]["dynamic_id_str"]
                if x["desc"]["origin"]["type"] == 8: #x[desc][orig_type]
                    oid, type = x["desc"]["origin"]["rid_str"], 1
                elif x["desc"]["origin"]["type"] == 4 or x["desc"]["origin"]["type"] == 1:
                    oid, type = x["desc"]["origin"]["dynamic_id_str"], 17
                else:
                    oid, type = x["desc"]["origin"]["rid_str"], 11
                uid = x["desc"]["origin"]["uid"]
            else:
                continue

            if 'card' in x:
                card = json.loads(x["card"])
                if 'origin_user' in card and 'info' in card["origin_user"] and 'uname' in card["origin_user"]["info"]:
                    name = card["origin_user"]["info"]["uname"]
                else:
                    name = '未知用户'

            if isinstance(task_config["repost"], list):
                if len(task_config["repost"]) > 0:
                    repost: str = task_config["repost"][randint(0, len(task_config["repost"]) - 1)] #取随机评论
                else:
                    repost: str = ''
            else:
                repost: str = task_config["repost"]

            if isinstance(task_config["reply"], list):
                if len(task_config["reply"]) > 0:
                    reply: str = task_config["reply"][randint(0, len(task_config["reply"]) - 1)]
                else:
                    reply: str = ''
            else:
                reply: str = task_config["reply"]

            try:
                ret = await biliapi.dynamicReplyAdd(oid, reply, type)
            except Exception as e: 
                logging.warning(f'{biliapi.name}: 评论动态(用户:{name},动态id:{dyid})失败，原因为({str(e)})')
                er1 += 1
            else:
                if ret["code"] == 0:
                    logging.info(f'{biliapi.name}: 评论动态(用户:{name},动态id:{dyid})成功')
                    su1 += 1
                else:
                    logging.warning(f'{biliapi.name}: 评论动态(用户:{name},动态id:{dyid})失败，信息为{ret["message"]}')
                    er1 += 1

            try:
                ret = await biliapi.dynamicRepostReply(dyid, repost)
            except Exception as e: 
                logging.warning(f'{biliapi.name}: 转发动态(用户:{name},动态id:{dyid})失败，原因为({str(e)})')
                er2 += 1
            else:
                if ret["code"] == 0:
                    logging.info(f'{biliapi.name}: 转发动态(用户:{name},动态id:{dyid})成功')
                    su2 += 1
                else:
                    logging.warning(f'{biliapi.name}: 转发动态(用户:{name},动态id:{dyid})失败，信息为{ret["message"]}')
                    er2 += 1

            try:
                ret = await biliapi.dynamicLike(dyid)
            except Exception as e: 
                logging.warning(f'{biliapi.name}: 点赞动态(用户:{name},动态id:{dyid})异常，原因为({str(e)})')
            else:
                if ret["code"] == 0:
                    logging.info(f'{biliapi.name}: 点赞动态(用户:{name},动态id:{dyid})成功')
                else:
                    logging.warning(f'{biliapi.name}: 点赞动态(用户:{name},动态id:{dyid})失败，信息为{ret["message"]}')

            if force_follow and not uid in users:
                try:
                    ret = await biliapi.followUser(uid)
                except Exception as e: 
                    logging.warning(f'{biliapi.name}: 关注用户{uid}异常，原因为({str(e)})')
                else:
                    if ret["code"] == 0:
                        logging.info(f'{biliapi.name}:  关注用户{uid}成功')
                        users.add(x["desc"]["uid"])
                    else:
                        logging.warning(f'{biliapi.name}:  关注用户{uid}失败，原因为{ret["message"]}')

            if "delay" in task_config:
                await asyncio.sleep(randint(task_config["delay"][0], task_config["delay"][1]))
            else:
                await asyncio.sleep(3)

    if er1 or er2:
        webhook.addMsg('msg_simple', f'{biliapi.name}:抽奖转发成功{su1}个,失败{er1}个,评论成功{su2}个,失败{er2}个\n')

tag_rex = re.compile(r'.*?(#.*?#)')
async def repost_task_X(biliapi: asyncbili, 
                       task_config: dict
                       ) -> None:
    '''转发互动抽奖，关键字抽奖'''
    already_repost_dyid = set() #记录动态列表中自己已经转发的动态id
    su1 = su2 = er1 = er2 = 0
    rexs = [re.compile(x, re.S) for x in task_config["keywords"]]
    async for x in get_dynamic(biliapi):
        if x["desc"]["uid"] == biliapi.uid and x["desc"]["pre_dy_id_str"] != '0':
            already_repost_dyid.add(int(x["desc"]["pre_dy_id_str"]))
            continue
            
        timestamp = x["desc"]["timestamp"]
        if(timestamp > end_time):
            continue
        elif(timestamp < start_time):
            break

        dyid = x["desc"]["dynamic_id"]
        if dyid in already_repost_dyid: #若动态被转发过就跳过
            continue

        find = False
        fixs = None
        if 'card' in x:
            card = json.loads(x["card"])
            if 'item' in card:
                if 'description' in card["item"]:
                    text = card["item"]["description"]
                elif 'content' in card["item"]:
                    text = card["item"]["content"]
                else:
                    text = None
                if text:
                    for rex in rexs:
                        if re.match(rex, text):
                            find = True
                            if 'repost_with_tag' in task_config:
                                fixs = re.findall(tag_rex, text)
                                for fix in fixs:
                                    for ept in task_config["repost_with_tag"]["except"]:
                                        if ept in fix:
                                            fixs.remove(fix)

        if not find:
            find = 'extension' in x and 'lott' in x["extension"] #若抽奖标签存在

        if find:
            dyid: str = x["desc"]["dynamic_id_str"]
            if x["desc"]["type"] == 8:
                oid, type = x["desc"]["rid_str"], 1
            elif x["desc"]["type"] == 4:
                oid, type = dyid, 17
            elif x["desc"]["type"] == 2:
                oid, type = x["desc"]["rid_str"], 11
            else:
                oid, type = dyid, 17

            if "uname" in x["desc"]["user_profile"]["info"]:
                uname = x["desc"]["user_profile"]["info"]["uname"]
            elif "name" in x["desc"]["user_profile"]["info"]:
                uname = x["desc"]["user_profile"]["info"]["name"]
            else:
                uname = '未知用户'

            if isinstance(task_config["repost"], list):
                if len(task_config["repost"]) > 0:
                    repost: str = task_config["repost"][randint(0, len(task_config["repost"]) - 1)] #取随机评论
                else:
                    repost: str = ''
            else:
                repost: str = task_config["repost"]

            if isinstance(task_config["reply"], list):
                if len(task_config["reply"]) > 0:
                    reply: str = task_config["reply"][randint(0, len(task_config["reply"]) - 1)]
                else:
                    reply: str = ''
            else:
                reply: str = task_config["reply"]

            if fixs:
                if task_config["repost_with_tag"]["fix"] == 1:
                    repost = repost + ','.join(fixs)
                    if task_config["repost_with_tag"]["reply_with_tag"]:
                        reply = reply + ','.join(fixs)
                else:
                    repost = ','.join(fixs) + repost
                    if task_config["repost_with_tag"]["reply_with_tag"]:
                        reply = ','.join(fixs) + reply

            try:
                ret = await biliapi.dynamicReplyAdd(oid, reply, type)
            except Exception as e: 
                logging.warning(f'{biliapi.name}: 评论动态(用户:{uname},动态id:{dyid})异常，原因为({str(e)})')
                er1 += 1
            else:
                if ret["code"] == 0:
                    logging.info(f'{biliapi.name}: 评论动态(用户:{uname},动态id:{dyid})成功')
                    su1 += 1
                else:
                    logging.warning(f'{biliapi.name}: 评论动态(用户:{uname},动态id:{dyid})失败，信息为{ret["message"]}')
                    er1 += 1

            try:
                ret = await biliapi.dynamicRepostReply(dyid, repost)
            except Exception as e: 
                logging.warning(f'{biliapi.name}: 转发动态(用户:{uname},动态id:{dyid})异常，原因为({str(e)})')
                er2 += 1
            else:
                if ret["code"] == 0:
                    logging.info(f'{biliapi.name}: 转发动态(用户:{uname},动态id:{dyid})成功')
                    su2 += 1
                else:
                    logging.warning(f'{biliapi.name}: 转发动态(用户:{uname},动态id:{dyid})失败，信息为{ret["message"]}')
                    er2 += 1

            try:
                ret = await biliapi.dynamicLike(dyid)
            except Exception as e: 
                logging.warning(f'{biliapi.name}: 点赞动态(用户:{uname},动态id:{dyid})异常，原因为({str(e)})')
            else:
                if ret["code"] == 0:
                    logging.info(f'{biliapi.name}: 点赞动态(用户:{uname},动态id:{dyid})成功')
                else:
                    logging.warning(f'{biliapi.name}: 点赞动态(用户:{uname},动态id:{dyid})失败，信息为{ret["message"]}')

            if "delay" in task_config:
                await asyncio.sleep(randint(task_config["delay"][0], task_config["delay"][1]))
            else:
                await asyncio.sleep(3)

    if er1 or er2:
        webhook.addMsg('msg_simple', f'{biliapi.name}:抽奖转发成功{su1}个,失败{er1}个,评论成功{su2}个,失败{er2}个\n')