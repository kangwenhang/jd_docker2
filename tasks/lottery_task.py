from models.asyncBiliApi import asyncBiliApi
from tasks.import_once import now_time
import logging, json, asyncio

end_time = now_time - (now_time + 28800) % 86400 + 43200 #当天中午12点
start_time = end_time - 86400

async def lottery_task(biliapi: asyncBiliApi, 
                       task_config: dict    #配置
                       ) -> None:

    already_repost_dyid = [] #记录动态列表中自己已经转发的动态id
    try:
        async for x in biliapi.getDynamic():
            if str(x["desc"]["uid"]) == biliapi.uid and x["desc"]["pre_dy_id"]: #记录本账号转发过的动态
                already_repost_dyid.append(x["desc"]["pre_dy_id"])
                continue

            timestamp = x["desc"]["timestamp"]
            if(timestamp > end_time):
                continue
            elif(timestamp < start_time):
                break

            if 'card' in x:
                card = json.loads(x["card"])
                if 'item' in card:
                    flag = False
                    if 'description' in card["item"]:
                        text = card["item"]["description"]
                    elif 'content' in card["item"]:
                        text = card["item"]["content"]
                    else:
                        text = None
                    if text:
                        for keyword in task_config["keywords"]:
                            if keyword in text:
                                uname = x["desc"]["user_profile"]["info"]["uname"]  #动态的主人的用户名
                                dyid = x["desc"]["dynamic_id"]
                                try:
                                    oid = (await biliapi.getDynamicDetail(dyid))["data"]["card"]["desc"]["rid"]
                                    await biliapi.dynamicReplyAdd(oid, task_config["reply"])
                                    await biliapi.dynamicRepostReply(dyid, task_config["repost"])
                                    logging.info(f'{biliapi.name}: 转发关键字动态(用户名:{uname},动态id:{dyid})成功')
                                except Exception as e: 
                                    logging.warning(f'{biliapi.name}: 转发关键字动态(用户名:{uname},动态id:{dyid})异常，原因为{str(e)}')
                                flag = True
                                break
                    if flag:
                        continue

            if 'extension' in x and 'lott' in x["extension"]: #若抽奖标签存在
                uname = x["desc"]["user_profile"]["info"]["uname"]  #动态的主人的用户名
                dyid = x["desc"]["dynamic_id"]
                if dyid in already_repost_dyid: #若动态被转发过就跳过
                    continue
                try:
                    oid = (await biliapi.getDynamicDetail(dyid))["data"]["card"]["desc"]["rid"]
                    await biliapi.dynamicReplyAdd(oid, task_config["reply"])    #这里评论
                    await biliapi.dynamicRepostReply(dyid, task_config["repost"]) #这里转发到自己的动态
                    logging.info(f'{biliapi.name}: 转发抽奖动态(用户名:{uname},动态id:{dyid})成功')
                    await asyncio.sleep(5)
                except Exception as e: 
                    logging.warning(f'{biliapi.name}: 转发抽奖动态(用户名:{uname},动态id:{dyid})异常，原因为{str(e)}')

    except Exception as e: 
        logging.warning(f'{biliapi.name}: 获取动态列表、异常，原因为{str(e)}，跳过转发抽奖动态')
        return
