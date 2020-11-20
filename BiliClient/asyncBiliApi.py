# -*- coding: utf-8 -*-
from aiohttp import ClientSession
import time

class asyncBiliApi(object):
    '''B站异步接口类'''
    def __init__(self):

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/63.0.3239.108","Referer": "https://www.bilibili.com/",'Connection': 'keep-alive'}
        self._islogin = False
        self._show_name = None
        self._session = ClientSession(
                headers = headers
                )
    
    async def login_by_cookie(self, cookieData, checkBanned=True) -> bool:
        '''
        登录并获取账户信息
        cookieData dict 账户cookie
        '''
        self._session.cookie_jar.update_cookies(cookieData)
        await self.refreshInfo()
        if not self._islogin:
            return False

        if 'bili_jct' in cookieData:
            self._bili_jct = cookieData["bili_jct"]
        else:
            self._bili_jct = ''

        self._isBanned = None
        if checkBanned:
            code = (await self.likeCv(7793107))["code"]
            if code != 0 and code != 65006 and code != -404:
                self._isBanned = True
                import warnings
                warnings.warn(f'{self._name}:账号异常，请检查bili_jct参数是否有效或本账号是否被封禁')
            else:
                self._isBanned = False

        return True

    @property
    def banned(self):
        '''是否账号被异常封禁'''
        return self._isBanned

    @property
    def islogin(self):
        '''是否登录'''
        return self._islogin

    @property
    def myexp(self) -> int:
        '''获取登录的账户的经验'''
        return self._exp

    @property
    def mycoin(self) -> int:
        '''获取登录的账户的硬币数量'''
        return self._coin

    @property
    def vipType(self) -> int:
        '''获取登录的账户的vip类型'''
        return self._vip
    
    @property
    def name(self) -> str:
        '''获取用于显示的用户名'''
        return self._show_name

    @name.setter
    def name(self, name: str) -> None:
        '''设置用于显示的用户名'''
        self._show_name = name

    @property
    def username(self) -> str:
        '''获取登录的账户用户名'''
        return self._name

    @property
    def uid(self) -> int:
        '''获取登录的账户uid'''
        return self._uid

    async def refreshInfo(self) -> None:
        '''刷新账户信息(需要先登录)'''
        ret = await self.getWebNav()
        if ret["code"] != 0:
            self._islogin = False
            return

        self._islogin = True
        self._name = ret["data"]["uname"]
        self._uid = ret["data"]["mid"]
        self._vip = ret["data"]["vipType"]
        self._level = ret["data"]["level_info"]["current_level"]
        self._verified = ret["data"]["mobile_verified"]
        self._coin = ret["data"]["money"]
        self._exp = ret["data"]["level_info"]["current_exp"]
        if not self._show_name:
            self._show_name = self._name

    def refreshCookie(self) -> None:
        '''刷新cookie(需要先登录)'''
        cookies = {}
        keys = ("SESSDATA","bili_jct","DedeUserID","LIVE_BUVID")
        for x in self._session.cookie_jar:
            if x.key in keys:
                cookies[x.key] = x.value
        self._session.cookie_jar.clear()
        self._session.cookie_jar.update_cookies(cookies)

    async def getFollowings(self, 
                            uid: int = None, 
                            pn: int = 1, 
                            ps: int = 50, 
                            order: str = 'desc', 
                            order_type: str = 'attention'
                            ) -> dict:
        '''
        获取指定用户关注的up主
        uid int 账户uid，默认为本账户，非登录账户只能获取20个*5页
        pn int 页码，默认第一页
        ps int 每页数量，默认50
        order str 排序方式，默认desc
        order_type 排序类型，默认attention
        '''
        if not uid:
            uid = self._uid
        url = f'https://api.bilibili.com/x/relation/followings?vmid={uid}&pn={pn}&ps={ps}&order={order}&order_type={order_type}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def spaceArticle(self, 
                            uid: int = None,
                            pn: int = 1, 
                            ps: int = 30, 
                            sort: str = 'publish_time', 
                            ) -> dict:
        '''
        获取指定up主空间专栏投稿信息
        uid int 账户uid，默认为本账户
        pn int 页码，默认第一页
        ps int 每页数量，默认50
        sort str 排序方式，默认publish_time
        '''
        if not uid:
            uid = self._uid
        url = f'https://api.bilibili.com/x/space/article?mid={uid}&pn={pn}&ps={ps}&sort={sort}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def spaceArcSearch(self, 
                          uid: int = None,
                          pn: int = 1, 
                          ps: int = 100, 
                          tid: int = 0,
                          order: str = 'pubdate', 
                          keyword: str = ''
                          ) -> dict:
        '''
        获取指定up主空间视频投稿信息
        uid int 账户uid，默认为本账户
        pn int 页码，默认第一页
        ps int 每页数量，默认50
        tid int 分区 默认为0(所有分区)
        order str 排序方式，默认pubdate
        keyword str 关键字，默认为空
        '''
        if not uid:
            uid = self._uid
        url = f'https://api.bilibili.com/x/space/arc/search?mid={uid}&pn={pn}&ps={ps}&tid={tid}&order={order}&keyword={keyword}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def search(self, 
                     keyword: str = '',
                     context: str = '',
                     page: int = 1,
                     tids: int = 0,
                     order: str = '', 
                     duration: int = 0,
                     search_type: str = 'video'
                     ) -> dict:
        '''
        获取指定视频投稿信息
        keyword str 关键字
        context str 未知
        page int 页码，默认第一页
        tids int 分区 默认为0(所有分区)
        order str 排序方式，默认为空(综合排序)
        duration int 时长过滤，默认0(所有时长)
        search_type str 搜索类型，默认video(视频)
        '''
        params = {
            "keyword": keyword,
            "context": context,
            "page": page,
            "tids": tids,
            "order": order,
            "duration": duration,
            "search_type": search_type,
            "single_column": 0,
            "__refresh__": "true",
            "tids_2": '',
            "_extra": ''
            }
        url = 'https://api.bilibili.com/x/web-interface/search/type'
        async with self._session.get(url, params=params, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def followUser(self, 
                         followid: int, 
                         type: int = 1
                         ):
        '''
        关注或取关up主
        followid int 要操作up主的uid
        type int 操作类型 1关注 0取关
        '''
        url = "https://api.vc.bilibili.com/feed/v1/feed/SetUserFollow"
        post_data = {
            "type": type,
            "follow": followid,
            "csrf_token": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getRelationTags(self) -> dict:
        '''取关注用户分组列表'''
        url = "https://api.bilibili.com/x/relation/tags"
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getRelationByUid(self,
                          uid: int
                          ) -> dict:
        '''
        判断与某个up关系
        是否关注，关注时间，是否拉黑.....
        uid int up主uid
        '''
        url = f"https://api.bilibili.com/x/relation?fid={uid}"
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getRelation(self,
                          tagid: int = 0,
                          pn: int = 1,
                          ps: int = 50
                          )-> dict:
        '''
        取关注分组内up主列表
        tagid int 分组id
        '''
        url = f"https://api.bilibili.com/x/relation/tag?tagid={tagid}&pn={pn}&ps={ps}"
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getWebNav(self) -> dict:
        '''取导航信息'''
        url = "https://api.bilibili.com/x/web-interface/nav"
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getReward(self) -> dict:
        '''取B站经验信息'''
        url = "https://account.bilibili.com/home/reward"
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret
    
    async def likeCv(self, 
                     cvid: int, 
                     type=1) -> dict:
        '''
        点赞专栏
        cvid int 专栏id
        type int 类型
        '''
        url = 'https://api.bilibili.com/x/article/like'
        post_data = {
            "id": cvid,
            "type": type,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def vipPrivilegeReceive(self, 
                                  type: int = 1
                                  ) -> dict:
        '''
        领取B站大会员权益
        type int 权益类型，1为B币劵，2为优惠券
        '''
        url = 'https://api.bilibili.com/x/vip/privilege/receive'
        post_data = {
            "type": type,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getUserWallet(self, 
                            platformType: int = 3
                            ) -> dict:
        '''
        获取账户钱包信息
        platformType int 平台类型
        '''
        url = 'https://pay.bilibili.com/paywallet/wallet/getUserWallet'
        post_data = {
            "platformType": platformType
            }
        async with self._session.post(url, json=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def elecPay(self, 
                      uid: int, 
                      num: int = 50
                      ) -> dict:
        '''
        用B币给up主充电
        uid int up主uid
        num int 充电电池数量
        '''
        url = 'https://api.bilibili.com/x/ugcpay/trade/elec/pay/quick'
        post_data = {
            "elec_num": num,
            "up_mid": uid,
            "otype": 'up',
            "oid": uid,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveFansMedal(self, 
                           page: int = 1,
                           pageSize: int = 10,
                           ) -> dict:
        '''
        获取粉丝牌
        page int 直播间id
        pageSize int 字体颜色
        '''
        url = f'https://api.live.bilibili.com/fans_medal/v5/live_fans_medal/iApiMedal?page={page}&pageSize={pageSize}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveAnchorCheck(self,
                               roomid: int
                               ) -> dict:
        '''
        查询直播天选时刻
        roomid int 真实房间id，非短id
        '''
        url = f'https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Check?roomid={roomid}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveAnchorJoin(self,
                              id: int,
                              gift_id: int,
                              gift_num: int,
                              platform: str = 'pc'
                              ) -> dict:
        '''
        参与直播天选时刻
        id int 天选时刻id
        gift_id int 礼物id
        gift_num int 礼物数量
        '''
        url = 'https://api.live.bilibili.com/xlive/lottery-interface/v1/Anchor/Join'
        post_data = {
            "id": id,
            "gift_id": gift_id,
            "gift_num": gift_num,
            "platform": platform,
            "csrf_token": self._bili_jct,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        #{"code":400,"data":null,"message":"余额不足","msg":"余额不足"}
        return ret

    async def xliveFeedHeartBeat(self) -> dict:
        '''直播心跳 feed'''
        url = 'https://api.live.bilibili.com/relation/v1/Feed/heartBeat'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        #{"code":0,"msg":"success","message":"success","data":{"open":1,"has_new":0,"count":0}}
        return ret

    async def xliveMsgSend(self, 
                           roomid: int,
                           msg: str,
                           color: int = 16777215,
                           fontsize: int = 25,
                           mode: int = 1,
                           bubble: int = 0,
                           ) -> dict:
        '''
        直播间发送消息
        roomid int 直播间id
        msg str 要发送的消息
        color int 字体颜色
        fontsize int 字体大小
        mode int 发送模式，应该是控制滚动，底部这些
        bubble int 未知
        '''
        url = 'https://api.live.bilibili.com/msg/send'
        post_data = {
            "color": color,
            "fontsize": fontsize,
            "mode": mode,
            "msg": msg,
            "rnd": int(time.time()),
            "roomid": roomid,
            "bubble": bubble,
            "csrf_token": self._bili_jct,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveBp2Gold(self, 
                           num: int = 5, 
                           platform: str = 'pc'
                           ) -> dict:
        '''
        B币劵购买金瓜子
        num int 花费B币劵数量，目前1B币=1000金瓜子
        platform str 平台
        '''
        #此接口抓包于网页https://link.bilibili.com/p/center/index中金瓜子购买
        url = 'https://api.live.bilibili.com/xlive/revenue/v1/order/createOrder'
        post_data = {
            "platform": platform,
            "pay_bp": num * 1000, #兑换瓜子数量，目前1B币=1000金瓜子
            "context_id": 1, #未知作用
            "context_type": 11, #未知作用
            "goods_id": 1, #商品id
            "goods_num": num, #商品数量，这里是B币数量
            #"csrf_token": self._bili_jct,
            #"visit_id": 'acq5hn53owg0',#这两个不需要也能请求成功，csrf_token与csrf一致
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        #返回示例{"code":1300014,"message":"b币余额不足","ttl":1,"data":null}
        #{"code":0,"message":"0","ttl":1,"data":{"status":2,"order_id":"2011042258413961167422787","gold":0,"bp":0}}
        return ret

    async def xliveSign(self) -> dict:
        '''B站直播签到'''
        url = "https://api.live.bilibili.com/xlive/web-ucenter/v1/sign/DoSign"
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveGetRecommendList(self) -> dict:
        '''B站直播获取首页前10条直播'''
        url = f'https://api.live.bilibili.com/relation/v1/AppWeb/getRecommendList'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveGetRoomInfo(self,
                               room_id: int
                               ) -> dict:
        '''
        B站直播获取房间信息
        room_id int 房间id
        '''
        url = f'https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id={room_id}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveGiftBagList(self) -> dict:
        '''B站直播获取背包礼物'''
        url = 'https://api.live.bilibili.com/xlive/web-room/v1/gift/bag_list'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveBagSend(self,
                           biz_id,
                           ruid,
                           bag_id, 
                           gift_id, 
                           gift_num, 
                           storm_beat_id=0, 
                           price=0, 
                           platform="pc"
                           ) -> dict:
        '''
        B站直播送出背包礼物
        biz_id int 房间号
        ruid int up主的uid
        bag_id int 背包id
        gift_id int 背包里的礼物id
        gift_num int 送礼物的数量
        storm_beat_id int
        price int 礼物价格
        platform str 平台
        '''
        url = 'https://api.live.bilibili.com/gift/v2/live/bag_send'
        post_data = {
            "uid": self._uid,
            "gift_id": gift_id,
            "ruid": ruid,
            "send_ruid": 0,
            "gift_num": gift_num,
            "bag_id": bag_id,
            "platform": platform,
            "biz_code": "live",
            "biz_id": biz_id,
            #"rnd": rnd, #直播开始时间
            "storm_beat_id": storm_beat_id,
            "price": price,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def coin(self, 
                   aid: int, 
                   num: int = 1, 
                   select_like: int = 1
                   ) -> dict:
        '''
        给指定av号视频投币
        aid int 视频av号
        num int 投币数量
        select_like int 是否点赞
        '''
        url = "https://api.bilibili.com/x/web-interface/coin/add"
        post_data = {
            "aid": aid,
            "multiply": num,
            "select_like": select_like,
            "cross_domain": "true",
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def coinCv(self,
                    cvid: int, 
                    num: int = 1, 
                    upid: int = 0, 
                    select_like: int = 1
                    ) -> dict:
        '''
        给指定cv号专栏投币
        cvid int 专栏id
        num int 投币数量
        upid int 专栏up主uid
        select_like int 是否点赞
        '''
        url = "https://api.bilibili.com/x/web-interface/coin/add"
        if upid == 0: #up主id不能为空，需要先请求一下专栏的up主
            info = await self.articleViewInfo(cvid)
            upid = info["data"]["mid"]
        post_data = {
            "aid": cvid,
            "multiply": num,
            "select_like": select_like,
            "upid": upid,
            "avtype": 2,#专栏必为2，否则投到视频上面去了
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def articleViewInfo(self, 
                              cvid: int
                              ) -> dict:
        '''
        获取专栏信息
        cvid int 专栏id
        '''
        url = f'https://api.bilibili.com/x/article/viewinfo?id={cvid}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveWebHeartBeat(self, 
                     hb: str = None, 
                     pf: str = None
                     ) -> dict:
        '''
        B站直播间心跳
        hb str 请求信息(base64编码) "{周期}|{uid}|1|0"
        pf str 平台 "web"
        '''
        params = {}
        if hb:
            params["hb"] = hb
        if pf:
            params["pf"] = pf
        url = 'https://live-trace.bilibili.com/xlive/rdata-interface/v1/heartbeat/webHeartBeat'
        async with self._session.get(url, params=params, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveGetBuvid(self) -> str:
        '''获得B站直播buvid参数'''
        #先查找cookie
        for x in self._session.cookie_jar:
            if x.key == 'LIVE_BUVID':
                return x.value
        #cookie中找不到，则请求一次直播页面
        url = 'https://live.bilibili.com/3'
        async with self._session.head(url, verify_ssl=False) as r:
            cookies = r.cookies['LIVE_BUVID']
        return str(cookies)[23:43]

    async def xliveHeartBeatX(self, 
                     id: list, 
                     device: list,
                     ts: int,
                     ets: int,
                     benchmark: str,
                     time: int,
                     s: str
                     ) -> dict:
        '''
        B站直播间内部心跳
        id List[int] 整数数组[大分区,小分区,轮次,长位直播间]
        device List[str] 字符串数组[bvuid, uuid]
        ts int 时间戳
        ets int 上次心跳时间戳timestamp
        benchmark str 上次心跳秘钥secret_key
        time int 上次心跳时间间隔
        s str 加密字符串，由id, device, ets, ts, benchmark, time等参数计算出
        '''
        post_data = {
            "id": f'[{id[0]},{id[1]},{id[2]},{id[3]}]',
            "device": f'["{device[0]}","{device[1]}"]',
            "ts": ts,
            "ets": ets,
            "benchmark": benchmark,
            "time": time,
            "ua": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/63.0.3239.108',
            "csrf_token": self._bili_jct,
            "csrf": self._bili_jct,
            "s": s
            }
        url = 'https://live-trace.bilibili.com/xlive/data-interface/v1/x25Kn/X'
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveHeartBeatE(self, 
                     id: list, 
                     device: list
                     ) -> dict:
        '''
        B站进入直播间心跳
        id List[int] 整数数组[大分区,小分区,轮次,长位直播间]
        device List[str] 字符串数组[bvuid, uuid]
        '''
        post_data = {
            "id": f'[{id[0]},{id[1]},{id[2]},{id[3]}]',
            "device": f'["{device[0]}","{device[1]}"]',
            "ts": int(time.time() * 1000),
            "is_patch": 0, 
            "heart_beat": [], #短时间多次进入直播间，is_patch为1，heart_beat传入xliveHeartBeatX所需要的所有数据
            "ua": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/63.0.3239.108',
            "csrf_token": self._bili_jct,
            "csrf": self._bili_jct
            }
        url = 'https://live-trace.bilibili.com/xlive/data-interface/v1/x25Kn/E'
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def get_home_medals(self) -> dict:
        '''获得佩戴的勋章'''
        url = "https://api.live.bilibili.com/fans_medal/v1/fans_medal/get_home_medals"
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def report(self, 
                     aid: int, 
                     cid: int, 
                     progres: int
                     ) -> dict:
        '''
        B站上报视频观看进度
        aid int 视频av号
        cid int 视频cid号
        progres int 观看秒数
        '''
        url = "http://api.bilibili.com/x/v2/history/report"
        post_data = {
            "aid": aid,
            "cid": cid,
            "progres": progres,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def share(self, 
                    aid
                    ) -> dict:
        '''
        分享指定av号视频
        aid int 视频av号
        '''
        url = "https://api.bilibili.com/x/web-interface/share/add"
        post_data = {
            "aid": aid,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def xliveGetStatus(self) -> dict:
        '''B站直播获取金银瓜子状态'''
        url = "https://api.live.bilibili.com/pay/v1/Exchange/getStatus"
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def silver2coin(self) -> dict:
        '''银瓜子兑换硬币'''
        url = "https://api.live.bilibili.com/pay/v1/Exchange/silver2coin"
        post_data = {
            "csrf_token": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getRegions(self, 
                         rid=1, 
                         num=6
                         ) -> dict:
        '''
        获取B站分区视频信息
        rid int 分区号
        num int 获取视频数量
        '''
        url = "https://api.bilibili.com/x/web-interface/dynamic/region?ps=" + str(num) + "&rid=" + str(rid)
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaClockIn(self, 
                     platform="android"
                     ) -> dict:
        '''
        模拟B站漫画客户端签到
        platform str 平台
        '''
        url = "https://manga.bilibili.com/twirp/activity.v1.Activity/ClockIn"
        post_data = {
            "platform": platform
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaGetPoint(self) -> dict:
        '''获取漫画积分'''
        url = f'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/GetUserPoint'
        async with self._session.post(url, json={}, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaShopExchange(self, 
                                product_id: int, 
                                point: int, 
                                product_num=1) -> dict:
        '''
        漫画积分商城兑换
        product_id int 商品id
        point int 商品需要积分数量
        product_num int 兑换商品数
        '''
        url = f'https://manga.bilibili.com/twirp/pointshop.v1.Pointshop/Exchange'
        post_data = {
            "product_id": product_id,
            "point": point,
            "product_num": product_num
            }
        async with self._session.post(url, json=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaGetVipReward(self) -> dict:
        '''获取漫画大会员福利'''
        url = 'https://manga.bilibili.com/twirp/user.v1.User/GetVipReward'
        async with self._session.post(url, json={"reason_id":1}, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaComrade(self, 
                           platform="web"
                           ) -> dict:
        '''
        站友日漫画卷兑换查询
        platform str 平台
        '''
        url = f'https://manga.bilibili.com/twirp/activity.v1.Activity/Comrade?platform={platform}'
        async with self._session.post(url, json={}, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaPayBCoin(self, 
                            pay_amount: int, 
                            product_id=1, 
                            platform='web'
                            ) -> dict:
        '''
        B币购买漫画
        pay_amount int 购买数量
        product_id int 购买商品id
        platform str 平台
        '''
        url = f'https://manga.bilibili.com/twirp/pay.v1.Pay/PayBCoin?platform={platform}'
        post_data = {
            "pay_amount": pay_amount,
            "product_id": product_id
            }
        async with self._session.post(url, json=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaGetCoupons(self, 
                              not_expired=True, 
                              page_num=1, 
                              page_size=50, 
                              tab_type=1,
                              platform="web"
                              ) -> dict:
        '''
        获取账户中的漫读劵信息
        not_expired bool
        page_num int 页数
        page_size int 每页大小
        tab_type int
        platform str 平台
        '''
        url = f'https://manga.bilibili.com/twirp/user.v1.User/GetCoupons?platform={platform}'
        post_data = {
            "not_expired": not_expired,
            "page_num": page_num,
            "page_size": page_size,
            "tab_type": tab_type
            }
        async with self._session.post(url, json=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaListFavorite(self, 
                                page_num=1, 
                                page_size=50, 
                                order=1, 
                                wait_free=0, 
                                platform='web'
                                ) -> dict:
        '''
        B站漫画追漫列表
        page_num int 页数
        page_size int 每页大小
        order int 排序方式
        wait_free int 显示等免漫画
        platform str 平台
        '''
        url = 'https://manga.bilibili.com/twirp/bookshelf.v1.Bookshelf/ListFavorite?platform={platform}'
        post_data = {
            "page_num": page_num,
            "page_size": page_size,
            "order": order,
            "wait_free": wait_free
            }
        async with self._session.post(url, json=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaDetail(self, 
                          comic_id: int, 
                          device='pc', 
                          platform='web'
                          ) -> dict:
        '''
        获取漫画信息
        comic_id int 漫画id
        device str 设备
        platform str 平台
        '''
        url = f'https://manga.bilibili.com/twirp/comic.v1.Comic/ComicDetail?device={device}&platform={platform}'
        post_data = {
            "comic_id": comic_id
            }
        async with self._session.post(url, json=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaGetEpisodeBuyInfo(self, 
                               ep_id: int, 
                               platform="web"
                               ) -> dict:
        '''
        获取漫画购买信息
        ep_id int 漫画章节id
        platform str 平台
        '''
        url = f'https://manga.bilibili.com/twirp/comic.v1.Comic/GetEpisodeBuyInfo?platform={platform}'
        post_data = {
            "ep_id": ep_id
            }
        async with self._session.post(url, json=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def mangaBuyEpisode(self, 
                        ep_id: int, 
                        buy_method=1, 
                        coupon_id=0, 
                        auto_pay_gold_status=0, 
                        platform="web"
                        ) -> dict:
        '''
        购买漫画
        ep_id int 漫画章节id
        buy_method int 购买参数
        coupon_id int 漫读劵id
        auto_pay_gold_status int 自动购买
        platform str 平台
        '''
        url = f'https://manga.bilibili.com/twirp/comic.v1.Comic/BuyEpisode?&platform={platform}'
        post_data = {
            "buy_method": buy_method,
            "ep_id": ep_id
            }
        if coupon_id:
            post_data["coupon_id"] = coupon_id
        if auto_pay_gold_status:
            post_data["auto_pay_gold_status"] = auto_pay_gold_status

        async with self._session.post(url, json=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def activityAddTimes(self, 
                               sid: str, 
                               action_type: int
                               ) -> dict:
        '''
        增加B站活动的参与次数
        sid str 活动的id
        action_type int 操作类型
        '''
        url = 'https://api.bilibili.com/x/activity/lottery/addtimes'
        post_data = {
            "sid": sid,
            "action_type": action_type,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def activityDo(self, 
                         sid: str, 
                         type: int
                         ) -> dict:
        '''
        参与B站活动
        sid str 活动的id
        type int 操作类型
        '''
        url = 'https://api.bilibili.com/x/activity/lottery/do'
        post_data = {
            "sid": sid,
            "type": type,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def activityMyTimes(self, 
                              sid: str
                              ) -> dict:
        '''
        获取B站活动次数
        sid str 活动的id
        '''
        url = f'https://api.bilibili.com/x/activity/lottery/mytimes?sid={sid}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getDynamic(self, 
                         offset_dynamic_id: int = 0,
                         type_list=268435455
                         ) -> dict:
        '''取B站用户动态数据'''
        if offset_dynamic_id:
            url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_history?uid={self._uid}&offset_dynamic_id={offset_dynamic_id}&type={type_list}'
        else:
            url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/dynamic_new?uid={self._uid}&type_list={type_list}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getDynamicDetail(self, 
                         dynamic_id: int
                         ) -> dict:
        '''
        获取动态内容
        dynamic_id int 动态id
        '''
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id={dynamic_id}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def dynamicReplyAdd(self, 
                              oid: int, 
                              message="", 
                              type=11, 
                              plat=1
                              ) -> dict:
        '''
        评论动态
        oid int 动态id
        message str 评论信息
        type int 评论类型，动态时原创则填11，非原创填17
        plat int 平台
        '''
        url = "https://api.bilibili.com/x/v2/reply/add"
        post_data = {
            "oid": oid,
            "plat": plat,
            "type": type,
            "message": message,
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def dynamicRepost(self, 
                            dynamic_id: int, 
                            content="", 
                            extension='{"emoji_type":1}'
                            ) -> dict:
        '''
        转发动态
        dynamic_id int 动态id
        content str 转发评论内容
        extension str_json
        '''
        url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost"
        post_data = {
            "uid": self._uid,
            "dynamic_id": dynamic_id,
            "content": content,
            "at_uids": '',
            "ctrl": '[]',
            "extension": extension,
            "csrf": self._bili_jct,
            "csrf_token": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        #{"code":0,"msg":"","message":"","data":{"result":0,"errmsg":"符合条件，允许发布","_gt_":0}}
        return ret

    async def dynamicRepostReply(self, 
                                 rid: int, 
                                 content="", 
                                 type=1, 
                                 repost_code=3000, 
                                 From="create.comment", 
                                 extension='{"emoji_type":1}'
                                 ) -> dict:
        '''
        转发动态
        rid int 动态id
        content str 转发评论内容
        type int 类型
        repost_code int 转发代码
        From str 转发来自
        extension str_json
        '''
        url = "https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/reply"
        post_data = {
            "uid": self._uid,
            "rid": rid,
            "type": type,
            "content": content,
            "extension": extension,
            "repost_code": repost_code,
            "from": From,
            "csrf_token": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getSpaceDynamic(self, 
                              uid: int = 0,
                              offset_dynamic_id: int = ''
                              ) -> 'dict':
        '''
        取B站空间的动态列表
        uid int B站用户uid
        '''
        if uid == 0:
            uid = self._uid
        url = f'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}&need_top=0&offset_dynamic_id={offset_dynamic_id}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def removeDynamic(self, 
                            dynamic_id: int
                            ) -> dict:
        '''
        删除自己的动态
        dynamic_id int 动态id
        '''
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/rm_dynamic'
        post_data = {
            "dynamic_id": dynamic_id,
            "csrf_token": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def getLotteryNotice(self, 
                               dynamic_id: int
                               ) -> dict:
        '''
        取指定抽奖信息
        dynamic_id int 抽奖动态id
        '''
        url = f'https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice?dynamic_id={dynamic_id}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def juryInfo(self) -> dict:
        '''
        取当前账户风纪委员状态
        '''
        url = 'https://api.bilibili.com/x/credit/jury/jury'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def juryCaseObtain(self) -> dict:
        '''
        拉取一个案件用于风纪委员投票
        '''
        url = 'https://api.bilibili.com/x/credit/jury/caseObtain'
        post_data = {
            "csrf": self._bili_jct
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def juryCaseInfo(self,
                           cid: int
                           ) -> dict:
        '''
        获取风纪委员案件详细信息
        '''
        url = f'https://api.bilibili.com/x/credit/jury/caseInfo?cid={cid}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def juryVote(self,
                       cid: int,
                       **kwargs #非必选参数太多以可变参数列表传入
                       ) -> dict:
        '''
        风纪委员投票
        cid int 案件ID
        以下为可选参数，如果需要必须用参数名称的方式调用本函数
        vote int 投票类型 0 未投票；1 封禁；2 否；3 弃权；4 删除
        content str 理由
        likes list[int] 整数数组，支持的观点
        hates list[int] 整数数组，反对的观点
        attr int 是否匿名 0 匿名；1 不匿名
        apply_type int 是否更改原因 0 保持原来原因；1 投票给新原因
        origin_reason int 原始原因
        apply_reason int 新原因
            1 刷屏
            2 抢楼
            3 发布色情低俗信息
            4 发布赌博诈骗信息
            5 发布违禁相关信息
            6 发布垃圾广告信息
            7 发布人身攻击言论
            8 发布侵犯他人隐私信息
            9 发布引战言论
            10 发布剧透信息
            11 恶意添加无关标签
            12 恶意删除他人标签
            13 发布色情信息
            14 发布低俗信息
            15 发布暴力血腥信息
            16 涉及恶意投稿行为
            17 发布非法网站信息
            18 发布传播不实信息
            19 发布怂恿教唆信息
            20 恶意刷屏
            21 账号违规
            22 恶意抄袭
            23 冒充自制原创
            24 发布青少年不良内容
            25 破坏网络安全
            26 发布虚假误导信息
            27 仿冒官方认证账号
            28 发布不适宜内容
            29 违反运营规则
            30 恶意创建话题
            31 发布违规抽奖
            32 恶意冒充他人
        '''
        url = 'https://api.bilibili.com/x/credit/jury/vote'
        post_data = {
            "cid": cid,
            "csrf": self._bili_jct,
            **kwargs #所有可选参数
            }
        async with self._session.post(url, data=post_data, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def accInfo(self,
                      uid: int
                      ) -> None:
        '''
        获取指定用户的空间个人信息
        uid int 用户uid
        '''
        url = f'https://api.bilibili.com/x/space/acc/info?mid={uid}'
        async with self._session.get(url, verify_ssl=False) as r:
            ret = await r.json()
        return ret

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc) -> None:
        await self.close()

    async def close(self) -> None:
        await self._session.close()


