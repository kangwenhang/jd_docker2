from BiliClient import asyncbili
from .import_once import taday
import logging

async def vip_task(biliapi: asyncbili) -> None:
    if taday == 1:
        try:
            ret = await biliapi.vipPrivilegeReceive(1)
            if ret["code"] == 0:
                logging.info(f'{biliapi.name}: 成功领取大会员B币')
            else:
                logging.warning('{biliapi.name}: 领取大会员B币失败')

            ret = await biliapi.vipPrivilegeReceive(2)
            if ret["code"] == 0:
                logging.info('{biliapi.name}: 成功领取大会员优惠券')
            else:
                logging.warning('{biliapi.name}: 领取大会员优惠券失败')
        except:
            logging.warning('{biliapi.name}: 领取大会员权益异常')

    elif taday == 28:
        try:
            cbp = (await biliapi.getUserWallet())["data"]["couponBalance"] #B币劵数量
            if cbp > 0:
                cbp *= 10
                ret = await biliapi.elecPay(biliapi.uid, cbp)
                if ret["data"]["order_no"]:
                    logging.info(f'{biliapi.name}: 成功给自己充电，订单编号为{ret["data"]["order_no"]}')
                else:
                    logging.warning(f'{biliapi.name}: 给自己充电失败，信息为{ret["data"]["msg"]}')
        except Exception as e:
            logging.warning(f'{biliapi.name}: 获取账户B币劵并给自己充电失败，原因为{str(e)}')