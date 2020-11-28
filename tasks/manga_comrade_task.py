from BiliClient import asyncbili
from .push_message_task import webhook
from .import_once import taday
import logging

async def manga_comrade_task(biliapi: asyncbili,
                             task_config: dict
                             ) -> None:
    if not taday in task_config["days"]:
        return
    try:
        ret = await biliapi.mangaComrade()
        if ret["data"]["active"] == 1:
            if ret["data"]["received"] == 0:
                ret = await biliapi.mangaPayBCoin(5) #只有兑换5B币才能参加活动
                if ret["code"] == 0:
                    logging.info(f'{biliapi.name}: 成功参与站友日活动，订单号为{ret["data"]["id"]}')
                    webhook.addMsg('msg_simple', f'{biliapi.name}:参与站友日活动成功\n')
                else:
                    logging.warning(f'{biliapi.name}: 站友日活动参与失败，可能是B币不足')
                    webhook.addMsg('msg_simple', f'{biliapi.name}:参与站友日活动失败\n')
            else:
                logging.info(f'{biliapi.name}: 您貌似今天已经参与过站友日活动了')
                webhook.addMsg('msg_simple', f'{biliapi.name}:参与站友日活动失败\n')
        else:
            logging.info(f'{biliapi.name}: 站友日还未启动，请看看这月{taday}号是否是站友日')
            webhook.addMsg('msg_simple', f'{biliapi.name}:参与站友日活动失败\n')
    except Exception as e: 
        logging.warning(f'{biliapi.name}: 站友日活动参与异常,原因为：{str(e)}')
        webhook.addMsg('msg_simple', f'{biliapi.name}:参与站友日活动异常\n')