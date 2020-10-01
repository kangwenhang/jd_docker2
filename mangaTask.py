# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import json, logging

inner_config = {
    "mode": 0,
    "filter": {
        "8467742": "25900|1-30,35,55;25966|5,15,35-",
#这里表示为uid为8468742的账户用即将过期漫读劵购买漫画mc25900的第1话到30话和35话及55话，购买漫画mc25966的5话，15话 和 35话到最新话
        "账户2uid": "格式同上所示" #依次类推更多账号,uid(DedeUserID)必须在config/config.json文件中存在
        },
    "exchangeCoupons": 0,  #积分商城抢购积分兑换福利劵数量,0为关闭兑换
    "vip_reward_day": [1], #尝试获取大会员漫读劵权益的日期,[1,2]为指定每月1号和2号尝试获取
    "comrade_day": []      #尝试参加站友日活动的日期,[1]为每月1号,[1,2]为每月1号和2号，指定多天为每天都尝试参与，为空则不参与
    }
#注:当mode为0时，"filter"参数无效，脚本自动购买追漫列表里的漫画(默认)，当mode为1时，请手动在"filter"下设置每个账户购买的漫画列表
#filter格式为 "账号uid": "漫画mc号1{竖线}漫画章数1(支持n-m和n-格式){逗号}漫画章数2{分号}漫画mc号2{竖线}漫画章数1......"
#上述的章数与实际章数可能不一样，番外也算一话，如果要购买30章，但是前面有一章番外，那么章数请填写31


def get_need_buy_eplist(filter: 'str 需要购买的话数', all_ep_list):
    '''通过所有eplist和过滤条件获得需要购买的漫画ep_id列表'''
    L1 = filter.split(',')
    length = len(all_ep_list)
    if length == 0:
        return  []
    nums = []
    for x in L1:
        if '-' in x:
            L2 = x.split('-')
            if L2[1] == '':
                nums.extend(list(range(int(L2[0]),length)))
            else:
                nums.extend(list(range(int(L2[0]),int(L2[1]))))
        else:
            nums.append(int(x))
    result = []
    for ii in range(length-1,-1,-1):
        if all_ep_list[ii]["ord"] in nums and all_ep_list[ii]["is_locked"]:
            result.append([all_ep_list[ii]["id"], all_ep_list[ii]["ord"], f'{all_ep_list[ii]["short_title"]} {all_ep_list[ii]["title"]}'])

    return result

def buy_manga_by_coupon(biliapi: 'BiliWebApi b站api接口实例', ep_id: 'int 漫画章节id'):
    '''通过漫读劵买漫画'''
    data = biliapi.mangaGetEpisodeBuyInfo(ep_id)["data"] #获取购买信息
    if not data["allow_coupon"]:
        raise Exception('本漫画不允许漫读劵购买')
    if data["recommend_coupon_id"] == 0:
        raise Exception('可能没有足够的漫读劵了')
    if not data["is_locked"]:
        raise Exception('漫画没有锁定，不用购买')
    data = biliapi.mangaBuyEpisode(ep_id, 2, data["recommend_coupon_id"])
    if data["code"] != 0:
        raise Exception(data["msg"])

def filter2list(filter):
    result = []
    S1 = filter.split(';')
    for x in S1:
        if x == '':
            continue
        S2 = x.split('|')
        result.append((S2[0],S2[1]))
    return result

def get_filter_by_favorite(biliapi: 'BiliWebApi b站api接口实例'):
    '''通过漫画关注列表获取filter字符串'''
    List = biliapi.mangaListFavorite()["data"]
    result = ''
    for x in List:
        result = f'{result};{x["comic_id"]}|1-'
    return result

def exchange_coupons(biliapi: 'BiliWebApi b站api接口实例', num):
    '''积分兑换福利劵'''
    now_point = biliapi.mangaGetPoint()["data"]["point"]
    buy_num = int(now_point) // 100
    if buy_num < num:
        num = buy_num
    if num == 0:
        raise Exception('积分不足')
    data = biliapi.mangaShopExchange(195, 100, num)
    if data["code"] != 0:
        if data["code"] == 9:
            raise Exception('手速太慢，库存不够了')
        raise Exception(data["msg"])
    return num

def manga_task(cookie, filter=''):
    '''用即将过期的漫读劵兑换漫画，兑换福利券，自动签到'''
    try:
        biliapi = BiliWebApi(cookie)
    except Exception as e: 
        logging.error(f'登录验证id为{data["DedeUserID"]}的账户失败，原因为:{str(e)}，跳过漫画兑换')
        return
    
    logging.info(f'登录账户 {biliapi.getUserName()} 成功')

    if inner_config["exchangeCoupons"] > 0:
        try:
            _n = exchange_coupons(biliapi, inner_config["exchangeCoupons"])
            logging.info(f'成功兑换福利劵 {_n} 张')
        except Exception as e: 
            logging.error(f'兑换福利劵失败，原因为:{str(e)}')
            pass

    try:
        _ret = biliapi.mangaClockIn()
        if(_ret["code"] == 0):
            logging.info(f'漫画签到成功')
        else:
            logging.error(f'漫画签到失败,信息为：{_ret["msg"]}')
    except Exception as e: 
        logging.error(f'漫画签到异常,原因为：{str(e)}')

    now_day = time.localtime(time.time() + 28800 + time.timezone).tm_mday #获取今天是几号
                                            #上面用于修正时区差
    if now_day in inner_config["vip_reward_day"]:
        try:
            _ret = biliapi.mangaGetVipReward()
            if _ret["code"] == 0:
                logging.info(f'大会员成功领取{_ret["data"]["amount"]}张漫读劵')
            else:
                logging.error(f'大会员权益领取失败,信息为：{_ret["msg"]}')
        except Exception as e: 
            logging.error(f'漫画大会员权益领取异常,原因为：{str(e)}')

    if now_day in inner_config["comrade_day"]:
        try:
            _ret = biliapi.mangaComrade()
            if _ret["data"]["active"] == 1:
                if _ret["data"]["received"] == 0:
                    _ret = biliapi.mangaPayBCoin(5) #只有兑换5B币才能参加活动
                    if _ret["code"] == 0:
                        logging.info(f'成功参与站友日活动，订单号为{_ret["data"]["id"]}')
                    else:
                        logging.error(f'站友日活动参与失败，可能是B币不足')
                else:
                    logging.info('您貌似今天已经参与过站友日活动了')
            else:
                logging.info(f'站友日还未启动，请看看这月{now_day}号是否是站友日')
        except Exception as e: 
            logging.error(f'站友日活动参与异常,原因为：{str(e)}')

    coupons_will_expire = 0
    try:
        coupons_data = biliapi.mangaGetCoupons()["data"]
        for x in coupons_data["user_coupons"]:
            if x["will_expire"] != 0:
                coupons_will_expire += x["remain_amount"]
    except Exception as e: 
        logging.error(f'获取漫读劵数量失败，原因为:{str(e)}，跳过漫画兑换')
        return
    
    if coupons_will_expire == 0:
        logging.info('没有即将过期的漫读劵，跳过购买')
        return

    if filter:
        buy_list = filter2list(filter)
    else:
        try:
            buy_list = filter2list(get_filter_by_favorite(biliapi))
        except Exception as e: 
            logging.error('获取追漫列表失败，原因为:{str(e)}，跳过漫画兑换')
            return

    for x in buy_list:
        try:
            manga_detail = biliapi.mangaDetail(x[0])["data"]
        except Exception as e: 
            logging.error(f'获取mc为{x[0]} 的漫画信息失败，原因为:{str(e)}')
            continue
        logging.info(f'开始购买漫画 ({manga_detail["title"]})')

        list_need_buy = get_need_buy_eplist(x[1], manga_detail["ep_list"])
        if len(list_need_buy) == 0:
            logging.info('此漫画没有需要购买的话数')
            continue
        for y in list_need_buy:
            try:
                buy_manga_by_coupon(biliapi, y[0])
                coupons_will_expire -= 1
                logging.info(f'购买章节 ({y[2]}) 成功')
            except Exception as e: 
                logging.info(f'购买章节 ({y[2]}) 失败，原因为:{str(e)}')
            if not coupons_will_expire > 0:
                break
        if not coupons_will_expire > 0:
            break

    logging.info('购买任务结束')

def main(*args):
    try:
        logging.basicConfig(filename="manga.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass

    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    if inner_config["mode"] == 0:
        for x in configData["cookieDatas"]:
            manga_task(x)
    else:
        for x in configData["cookieDatas"]:
            if x["DedeUserID"] in inner_config["filter"]:
                manga_task(x, inner_config["filter"][x["DedeUserID"]])

if __name__=="__main__":
    main()
