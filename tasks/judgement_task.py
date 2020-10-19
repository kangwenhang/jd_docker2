from BiliClient import asyncbili
import logging

async def judgement_task(biliapi: asyncbili, 
                         task_config: dict
                         ) -> None:
    '''风纪委员会投票任务'''
    try:
        ret = await biliapi.juryInfo()
    except Exception as e:
        logging.warning(f'{biliapi.name}: 获取风纪委员信息异常，原因为{str(e)}，跳过投票')
        return
    if ret["code"] == 25005:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，请去https://www.bilibili.com/judgement/apply申请成为风纪委员')
        return
    elif ret["code"] != 0:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，信息为：{ret["msg"]}')
        return
    if ret["data"]["status"] != 1:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，风纪委员资格失效')
        return
    rightRadio =  ret["data"]["rightRadio"]
    try:
        ret = await biliapi.juryCaseObtain()
    except Exception as e:
        logging.warning(f'{biliapi.name}: 获取风纪委员案件异常，原因为{str(e)}，跳过投票')
        return
    if ret["code"] == 25008:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，没有新案件了，当前裁决正确率为：{rightRadio}%')
        return
    elif ret["code"] == 25014:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，案件已审满，当前裁决正确率为：{rightRadio}%')
        return
    elif ret["code"] != 0:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，信息为：{ret["message"]}，当前裁决正确率为：{rightRadio}%')
        return

    cid = ret["data"]["id"]  #案件id
    params = task_config["params"]  #配置文件里的投票参数
    try:
        ret = await biliapi.juryVote(cid, **params) #将参数params展开后传参
    except Exception as e:
        logging.warning(f'{biliapi.name}: 风纪委员投票异常，原因为{str(e)}，跳过投票')
        return
    if ret["code"] == 0:
        logging.warning(f'{biliapi.name}: 风纪委员成功为id为{cid}的案件投票，当前裁决正确率为：{rightRadio}%')
    else:
        logging.warning(f'{biliapi.name}: 风纪委员投票失败，信息为：{ret["message"]}，当前裁决正确率为：{rightRadio}%')