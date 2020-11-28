from BiliClient import asyncbili
from .push_message_task import webhook
import logging, aiohttp

voteInfo = ("未投票", "封禁", "否认", "弃权", "删除")

async def judgement_task(biliapi: asyncbili, 
                         task_config: dict
                         ) -> None:
    '''风纪委员会投票任务'''
    try:
        ret = await biliapi.juryInfo()
    except Exception as e:
        logging.warning(f'{biliapi.name}: 获取风纪委员信息异常，原因为{str(e)}，跳过投票')
        webhook.addMsg('msg_simple', f'{biliapi.name}:风纪委投票失败\n')
        return
    if ret["code"] == 25005:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，请去https://www.bilibili.com/judgement/apply 申请成为风纪委员')
        webhook.addMsg('msg_simple', f'{biliapi.name}:不是风纪委\n')
        return
    elif ret["code"] != 0:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，信息为：{ret["msg"]}')
        webhook.addMsg('msg_simple', f'{biliapi.name}:风纪委投票失败\n')
        return
    if ret["data"]["status"] != 1:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，风纪委员资格失效')
        webhook.addMsg('msg_simple', f'{biliapi.name}:风纪委资格失效\n')
        return
    rightRadio =  ret["data"]["rightRadio"]
    su, er = 0, 0
    while True:
        try:
            ret = await biliapi.juryCaseObtain()
        except Exception as e:
            logging.warning(f'{biliapi.name}: 获取风纪委员案件异常，原因为{str(e)}，跳过投票')
            er += 1
            break
        if ret["code"] == 25008:
            logging.warning(f'{biliapi.name}: 风纪委员投票失败，没有新案件了，当前裁决正确率为：{rightRadio}%')
            break
        elif ret["code"] == 25014:
            logging.warning(f'{biliapi.name}: 风纪委员投票失败，案件已审满，当前裁决正确率为：{rightRadio}%')
            break
        elif ret["code"] != 0:
            logging.warning(f'{biliapi.name}: 风纪委员投票失败，信息为：{ret["message"]}，当前裁决正确率为：{rightRadio}%')
            er += 1
            break

        cid = ret["data"]["id"]  #案件id
        params = task_config["params"] #获取默认投票参数

        if 'baiduNLP' in task_config and task_config["baiduNLP"]["confidence"] > 0:
            try:
                ret = await biliapi.juryCaseInfo(cid)
            except Exception as e:
                logging.warning(f'{biliapi.name}: 获取id为{cid}的案件信息异常，原因为{str(e)}，使用默认投票参数')
            else:
                if ret["code"] != 0:
                    logging.warning(f'{biliapi.name}: 获取id为{cid}的案件信息失败，原因为{ret["message"]}，使用默认投票参数')
                else:
                    try:
                        ret = await baiduNLP(ret["data"]["originContent"][0:255])
                    except Exception as e:
                        logging.warning(f'{biliapi.name}: 百度NLP接口异常，原因为{str(e)}，使用默认投票参数')
                    else:
                        if ret["errno"] != 0:
                            logging.warning(f'{biliapi.name}: 调用百度NLP接口失败，原因为{ret["msg"]}，使用默认投票参数')
                        elif ret["data"]["items"][0]["confidence"] > task_config["baiduNLP"]["confidence"]:
                            params = params.copy()
                            if ret["data"]["items"][0]["negative_prob"] > task_config["baiduNLP"]["negative_prob"]:
                                params["vote"] = params["vote"] if 'vote' in params and params["vote"] in (1, 4) else 4
                            elif ret["data"]["items"][0]["positive_prob"] > task_config["baiduNLP"]["positive_prob"]:
                                params["vote"] = 2
                            else:
                                params["vote"] = 3
        try:
            ret = await biliapi.juryVote(cid, **params) #将参数params展开后传参
        except Exception as e:
            logging.warning(f'{biliapi.name}: 风纪委员投票id为{cid}的案件异常，原因为{str(e)}，跳过投票')
            er += 1
            continue
        if ret["code"] == 0:
            logging.info(f'{biliapi.name}: 风纪委员成功为id为{cid}的案件投({voteInfo[params["vote"]]})票，当前裁决正确率为：{rightRadio}%')
            su += 1
        else:
            logging.warning(f'{biliapi.name}: 风纪委员投票id为{cid}的案件失败，信息为：{ret["message"]}，当前裁决正确率为：{rightRadio}%')
            er += 1
    if er > 0:
        webhook.addMsg('msg_simple', f'{biliapi.name}:风纪委投票成功{su}次,失败或异常{er}次裁决正确率{rightRadio}%\n')

async def baiduNLP(text: str) -> dict:
    '''百度NLP语言情感识别'''
    async with aiohttp.request("post",
                               url='https://ai.baidu.com/aidemo', 
                               data={"apiType": "nlp", "type": "sentimentClassify", "t1": text}, 
                               headers={"Cookie": "BAIDUID=0"}
                               ) as r:
        ret = await r.json(content_type=None)
    return ret
