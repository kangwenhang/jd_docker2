# -*- coding: utf-8 -*-
from models.Biliapi import BiliWebApi
import json, logging

auto_buy_list = {
    "8468742": "25900|1-30,35,55;25966|5,15,35-",
    "账户2uid": "同上所示"
    #这里表示为uid为8468742的账户购买漫画mc25900的第1话到30话和35话及55话，购买漫画mc25966的5话，15话 和 35话到最新话
    }
#注：配置格式为 "账号uid": "漫画mc号1{竖线}漫画章数1(支持n-m和n-格式){逗号}漫画章数2{分号}漫画mc号2{竖线}漫画章数1......"
#上述的章数与实际章数可能不一样，番外也算一话，如果要购买30章，但是前面有一章番外，那么章数请填写31
#支持多账户，每个账户以DedeUserID(uid)作区分,必须在config/config.json文件中存在

def get_need_buy_eplist(need: 'str 需要购买的话数', all_ep_list):
    '''通过所有eplist和过滤条件获得需要购买的漫画ep_id列表'''
    L1 = need.split(',')
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

def manga_buy_by_coupons(cookie, buy_list):
    '''用即将过期的漫读劵兑换漫画'''
    try:
        biliapi = BiliWebApi(cookie)
    except Exception as e: 
        logging.error(f'登录验证id为{data["DedeUserID"]}的账户失败，原因为:{str(e)}，跳过后续所有操作')
        return
    
    logging.info(f'登录账户 {biliapi.getUserName()} 成功')

    coupons_will_expire = 0
    try:
        coupons_data = biliapi.mangaGetCoupons()["data"]
        for x in coupons_data["user_coupons"]:
            if x["will_expire"] != 0:
                coupons_will_expire += x["remain_amount"]
    except Exception as e: 
        logging.error(f'获取漫读劵数量失败，原因为:{str(e)}，跳过后续所有操作')
        return
    
    if coupons_will_expire == 0:
        logging.info('没有即将过期的漫读劵，跳过购买')
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

def str2list(s_input):
    result = []
    S1 = s_input.split(';')
    for x in S1:
        if x == '':
            continue
        S2 = x.split('|')
        result.append((S2[0],S2[1]))
    return result

def main(*args):
    try:
        logging.basicConfig(filename="mangaAutoBuy.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass

    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    for x in configData["cookieDatas"]:
        if x["DedeUserID"] in auto_buy_list:
            manga_buy_by_coupons(x, str2list(auto_buy_list[x["DedeUserID"]]))

if __name__=="__main__":
    main()
