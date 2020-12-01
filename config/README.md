
# config.json进阶配置文件详解

这里是配置文件的详细解释，建议设置config.json文件前先阅读一遍本文。
注意本文中所有必选参数都是在特定条件下必须在配置文件中存在的参数(无论可不可为空都必须存在)
所有可选参数都建议不用时从配置文件中删除

## 目录

- [说明](#config.json进阶配置文件详解)
- [目录](#目录)
- [正文内容](#正文内容)
  - [一、json文件格式](#一json文件格式)
  - [二、配置文件详解](#二配置文件详解)
    - [default(默认任务配置)](#default默认任务配置)
	  - [vip_task(领取主站大会员权益，可选)](#vip_task领取主站大会员权益可选)
	    - [enable(必选)](#enable(必选))
	    - [BpCharge(花费B币劵方式，可选)](#BpCharge花费B币劵方式可选)
	  - [xliveSign_task(直播签到，可选)](#xliveSign_task直播签到可选)
	  - [xlive_bag_send_task(送出直播礼物，可选)](#xlive_bag_send_task送出直播礼物可选)
	    - [enable(必选)](#enable必选)
	    - [room_id(房间号，必选)](#room_id房间号必选)
	    - [expire(过期时间，可选)](#expire过期时间可选)
	  - [xlive_heartbeat_task(直播心跳，可选)](#xlive_heartbeat_task直播心跳可选)
	    - [enable(必选)](#enable必选)
	    - [room_id(房间号，可选)](#room_id房间号可选)
	    - [num(次数，可选)](#num次数可选)
	    - [time(最大心跳时间，可选)](#time最大心跳时间可选)
	    - [send_msg(发送消息，可选)](#send_msg发送消息可选)
	  - [xlive_anchor_task(直播天选时刻，可选)](#xlive_anchor_task直播天选时刻可选)
	    - [enable(必选)](#enable必选)
	    - [rooms_id(房间号，必选)](#rooms_id房间号必选)
	    - [times(次数，必选)](#times次数必选)
	    - [delay(延时，必选)](#delay延时必选)
	  - [coin_task(投币任务，可选)](#coin_task投币任务可选)
	    - [enable(必选)](#enable必选)
	    - [num(最大投币数量，必选)](#num最大投币数量必选)
	    - [target_exp(目标经验，必选)](#target_exp目标经验必选)
	    - [do_task(投币模式，可选)](#do_task投币模式可选)
	    - [coin(投币顺序，do_task包含2必选)](#coin投币顺序do_task包含2必选)
	    - [groupTag(up主分组，do_task包含2可选)](#groupTagup主分组do_task包含2可选)
	    - [search(搜索关键字，do_task包含3必选)](#search搜索关键字do_task包含3必选)
	  - [watch_task(模拟观看视频，可选)](#watch_task模拟观看视频可选)
	  - [share_task(模拟分享视频，可选)](#share_task模拟分享视频可选)
	  - [silver2coin_task(银瓜子兑换硬币，可选)](#silver2coin_task银瓜子兑换硬币可选)
	  - [lottery_task(转发抽奖动态，可选)](#lottery_task转发抽奖动态可选)
	    - [enable(必选)](#enable必选)
	    - [reply(评论，必选)](#reply评论必选)
	    - [repost(转发，必选)](#repost转发必选)
	    - [keywords(匹配关键字，非跟踪转发模式必选)](#keywords匹配关键字非跟踪转发模式必选)
		- [repost_with_tag(带标签转发，可选)](#repost_with_tag带标签转发可选)
	    - [delay(延时，可选)](#delay延时可选)
	    - [repost_by_others(跟踪转发，可选)](#repost_by_others跟踪转发可选)
	    - [force_follow(强制关注，跟踪转发模式下可选)](#force_follow强制关注跟踪转发模式下可选)
	  - [clean_dynamic_task(动态清理任务，可选)](#clean_dynamic_task动态清理任务可选)
	    - [enable(必选)](#enable必选)
	    - [black_keywords(黑名单关键字，必选)](#black_keywords黑名单关键字必选)
	    - [unfollowed(取消关注，可选)](#unfollowed取消关注可选)
	  - [manga_sign_task(漫画签到，可选)](#manga_sign_task漫画签到可选)
	  - [exchangeCoupons_task(兑换漫画福利券，可选)](#exchangeCoupons_task兑换漫画福利券可选)
	    - [enable(必选)](#enable必选)
	    - [num(兑换数量，必选)](#num兑换数量必选)
	  - [manga_vip_reward_task(领取大会员漫画权益，可选)](#manga_vip_reward_task领取大会员漫画权益可选)
	    - [enable(必选)](#enable必选)
	    - [days(领取日期，必选)](#days领取日期必选)
	  - [manga_comrade_task(漫画站友日活动，可选)](#manga_comrade_task漫画站友日活动可选)
	    - [enable(必选)](#enable必选)
	    - [days(参与日期，必选)](#days参与日期必选)
	  - [manga_auto_buy_task(漫读劵花费，可选)](#manga_auto_buy_task漫读劵花费可选)
	    - [enable(必选)](#enable必选)
	    - [mode(花费模式，必选)](#mode花费模式必选)
	    - [filter(漫画过滤器，mode为2必选)](#filter漫画过滤器mode为2必选)
	  - [judgement_task(风纪委员投票，可选)](#judgement_task风纪委员投票可选)
	    - [enable(必选)](#enable必选)
	    - [baiduNLP(百度语言情感分析，可选)](#baiduNLP百度语言情感分析可选)
	    - [params(默认参数，必选)](#params默认参数必选)
	  - [activity_task(B站转盘抽奖活动，可选)](#activity_taskB站转盘抽奖活动可选)
	    - [enable(必选)](#enable必选)
		- [path(活动列表文件路径，可选)](#path可选)
	    - [activities(活动列表，必选)](#activities活动列表必选)
    - [webhook(消息推送，可选)](#webhook消息推送可选)
	    - [http_header(http头部，必选)](#http_headerhttp头部必选)
	    - [variable(变量定义，必选)](#variable变量定义必选)
	    - [hooks(推送接口列表，必选)](#hooks推送接口列表必选)
    - [log_file(日志文件,必选)](#log_file日志文件必选)
    - [log_console(日志输出到控制台,必选)](#log_console日志输出到控制台必选)
    - [users(账户配置,必选)](#users账户配置必选)

</br>

## 正文内容

### 一、json文件格式
* 建议学习一下 [菜鸟教程](https://www.runoob.com/json/json-tutorial.html) 掌握json基本知识
### 二、配置文件详解

#### default(默认任务配置)
此项配置下存放默认所有执行的任务，同时控制每个任务的默认执行顺序，即在前面的任务先执行(可自行调整)。

##### vip_task(领取主站大会员权益，可选)
1号领取大会员B币劵，优惠券，28号花费剩余B币劵
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### BpCharge(花费B币劵方式，可选)
每月28号花费剩余B币劵，以下参数至少选择一项
* charge(可选)
整数，给自己充电的数量
* Bp2Gold(可选)
整数，转化为金瓜子的数量

##### xliveSign_task(直播签到，可选)
功能开关，true为启动,false为关闭

##### xlive_bag_send_task(送出直播礼物，可选)
送出直播即将过期的礼物
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### room_id(房间号，必选)
整数，取0为随机选择房间送出<br>
请使用长房间号而不是短房间号，例如`https://live.bilibili.com/22528847`这个直播间,房间号是22528847
###### expire(过期时间，可选)
整数，如果礼物将在这个时间内过期则会被送出,默认为172800即两天

##### xlive_heartbeat_task(直播心跳，可选)
B站直播心跳，可获得小心心，点亮粉丝牌
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### room_id(房间号，可选)
整数数组，心跳的房间号<br>
请使用长房间号而不是短房间号，例如`https://live.bilibili.com/22528847`这个直播间,房间号是22528847
取空[]，则为自动寻找拥有粉丝牌的房间，等级高，亲密度高的优先
###### num(次数，可选)
整数，发出心跳的总次数，每次心跳的时间不定(由官方决定),每心跳5分钟可以获得1个小心心(每天最高24个小心心)
###### time(最大心跳时间，可选)
数字(单位分钟)，发出心跳的最大时长，超过这个时长会停止心跳
###### send_msg(发送消息，可选)
字符串，给所有有粉丝牌的直播间发送一条消息，为空则不发送

##### xlive_anchor_task(直播天选时刻，可选)
参与B站直播天选时刻活动
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### rooms_id(房间号，必选)
整数数组，请使用长房间号而不是短房间号，例如`https://live.bilibili.com/22528847`这个直播间,房间号是22528847
可取多个房间号，比如 `[3742025, 5441]` 则为 3742025和5441两个房间
###### times(次数，必选)
整数，查询每个房间天选时刻的总次数
###### delay(延时，必选)
整数，每次查询间隔，仅当直播间还没有天选时刻时有用

##### coin_task(投币任务，可选)
每天投币获取经验
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### num(最大投币数量，必选)
整数1-5，每天投币不会超过这个数量，如果已经投x个币，程序会接着投num-x个币
###### target_exp(目标经验，必选)
整数，达到目标经验值停止投币
###### do_task(投币模式，可选)
整数数组，每个数字代表一个投币模式
模式1:随机抽取视频投币
模式2:从账号的关注列表或下面up参数获取up主，对up主视频(专栏)投币
模式3:搜索特定关键字得到视频进行投币
取值例子 `"do_task": [1]` 随机抽取视频投币
取值例子 `"do_task": [3, 2, 1]` 先执行模式3，当币没有投够，执行模式2，还没有投够，执行模式1
###### coin(投币顺序，do_task包含2必选)
以下两个参数至少有一个存在，可以改变这两个参数的顺序
* article(可选)
整数，抽取专栏的数量，没有投够币执行下一个video参数
* video(可选)
整数，抽取视频的数量，没有投够币抽取下一个up主执行上一个article参数
###### groupTag(up主分组，do_task包含2可选)
字符串，抽取up主的关注分组名称，默认为`默认分组`，也可选`特别关注`或其他自定义分组名
与下面up参数最多提供一个，不能两个同时提供
###### up(up主id，do_task包含2可选)
整数数组，只给特定up主投币，例如`"up": [203984353, 67141]`，就只给uid为203984353和67141的up主投币
与上面groupTag参数最多提供一个，不能两个同时提供
###### search(搜索关键字，do_task包含3必选)
可提供多个关键字，按顺序搜索
* 关键字1(可选)
    * num 整数(可选)，搜索数量上限
    * order 整数(可选)，排序规则,0综合排序(默认取值),1最多点击,2最新发布,3最多弹幕,4最多收藏
    * duration 整数(可选)，时长规则,0全部时长(默认取值),1十分钟以下,2三十分钟以下,3六十分钟以下,4以上
    * tids 整数(可选)，0全部分区(默认取值),1动画,13番剧,167国创,3音乐,129舞蹈(分区太多篇幅有限不列举了)
* 关键字n(可选)
同关键字1

##### watch_task(模拟观看视频，可选)
观看一个视频获取经验，true为启动,false为关闭

##### share_task(模拟分享视频，可选)
分享一个视频获取经验，true为启动,false为关闭

##### silver2coin_task(银瓜子兑换硬币，可选)
每天将700银瓜子兑换为1个硬币，true为启动,false为关闭

##### lottery_task(转发抽奖动态，可选)
转发抽奖动态，支持互动抽奖转发，关键字转发(正则匹配)，跟踪转发
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### reply(评论，必选)
字符串或者字符串数组，用于转发时评论源动态，若是数组则随机抽取一个
取值例子 `"reply": ["从未中奖，从未放弃[doge]", "支持支持"]`
###### repost(转发，必选)
字符串或者字符串数组，用于转发时评论自己的动态，若是数组则随机抽取一个
取值例子 `"repost": ["从未中奖，从未放弃[doge]", "支持支持"]`
###### keywords(匹配关键字，非跟踪转发模式必选)
字符串数组，正则表达式数组，匹配上表达式的动态则转发
取值例子 `"keywords": ["#互动抽奖#", "#抽奖#", ".*(转|抽|评).*(转|抽|评).*(转|抽|评).*"]`
###### repost_with_tag(带标签转发，可选)
转发时带上原动态的标签，如果原动态带有`#哈哈#`这类标签,转发时也带上这种标签转发,本项不存在时不带标签转发
* fix(必选) 整数，取0为将标签加在首部,取1为加在尾部
* except 字符串数组(必选)，排除包含关键字的标签
* reply_with_tag bool(必选)，false为回复原动态不带标签,true为带上标签回复

###### delay(延时，可选)
整数数组，`[x, y]` 每次转发后随机延时x到y秒，x>y
###### repost_by_others(跟踪转发，可选)
整数数组，长度大于0时启用跟踪转发模式，keywords参数无效
跟随指定用户转发相同的动态，此模式用于:
1. 大号转发了抽奖动态，小号使用此模式跟着转
2. 跟着其他大量抽奖的用户转
不建议跟踪多个用户
###### force_follow(强制关注，跟踪转发模式下可选)
转发动态时强制关注动态的源up主，true为启动,false为关闭，此项不存在为关闭

##### clean_dynamic_task(动态清理任务，可选)
清理无效动态，过期抽奖，关键字动态
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### black_keywords(黑名单关键字，必选)
字符串数组，动态中出现关键字将会被删除
###### unfollowed(取消关注，可选)
删除动态时取消关注源up主，true为启动,false为关闭

##### manga_sign_task(漫画签到，可选)
每日签到漫画，true为启动,false为关闭

##### exchangeCoupons_task(兑换漫画福利券，可选)
漫画积分兑换福利券，请保证程序在北京时间中午12点启动
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### num(兑换数量，必选)
整数，每次兑换数量

##### manga_vip_reward_task(领取大会员漫画权益，可选)
领取每月大会员漫读劵(月度会员5张，年度会员10张/月)
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### days(领取日期，必选)
整数数组，尝试领取日期

##### manga_comrade_task(漫画站友日活动，可选)
参加每月站友日活动(站友日可5B币兑换15张漫读劵，普通购买只能1B币兑换2张)
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### days(参与日期，必选)
整数数组，尝试参与活动的日期，指定多个会参与多次，一般站友日为每月1-3号，官方可能改变

##### manga_auto_buy_task(漫读劵花费，可选)
自动花费即将过期的漫读劵
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### mode(花费模式，必选)
整数，1为自动购买追漫列表里面的漫画，2为自定义购买，参见下面filter参数
###### filter(漫画过滤器，mode为2必选)
字符串，格式为`漫画mc号1|章节1,章节2,章节n;漫画mc号2|章节1,章节2,章节n;...`
取值例子 `"filter": "25900|1-30,35,55;25966|5,15,35-"` 购买漫画id为25900漫画的1-30章，35章和55章；购买漫画id为25966的漫画5章，15章，35章到最后一章。

##### judgement_task(风纪委员投票，可选)
自动参与风纪委员投票，每次运行投当前所有案件
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### baiduNLP(百度语言情感分析，可选)
百度语言情感分析，直接影响下面params参数中vote值
* confidence(必选)
小数0-1，置信系数门限，0为完全相信百度情感分析的判断，1为完全不相信
只有可信系数高于设置的值才会采纳百度的判断，否则投默认参数
* negative_prob(必选)
小数0-1，消极概率门限，文本的消极度超过此值，则投赞成删除票或赞成封禁票，否则判断下面positive_prob参数
* positive_prob(必选)
小数0-1，积极概率门限，文本的积极度超过此值，则投反对删除票，否则投默认参数
###### params(默认参数，必选)
默认投票参数，所有参数均为可选参数，vote不提供则弃权
* vote(可选)
整数 投票类型 0 未投票；1 封禁；2 否；3 弃权；4 删除
* content(可选)
字符串 理由
* likes(可选)
整数数组，支持的观点，参见下面 原因列表取值
* hates(可选)
整数数组，反对的观点，参见下面 原因列表取值
* attr(可选)
整数 是否匿名 0 匿名；1 不匿名
* apply_type(可选)
整数 是否更改原因 0 保持原来原因；1 投票给新原因
* origin_reason(可选)
整数 原始原因，参见下面 原因列表取值
* apply_reason(可选)
整数 新原因，参见下面 原因列表取值
```
原因列表取值
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
```

##### activity_task(B站转盘抽奖活动，可选)
参与B站转盘抽奖活动(需要手动搜集和设置活动列表)
###### enable(必选)
功能开关，true为启动,false为关闭，关闭后以下参数不用提供
###### path(可选)
活动列表的json文件路径,也可以将活动列表放到下面activities参数中
###### activities(活动列表，必选)
活动数组，每个活动包括
* name(必选)
字符串 活动名称，仅影响日志推送，可任意取值
* sid(必选)
字符串，活动id，获取方法如下
    * 1. 找到一个有转盘抽奖的活动页面，例如`https://www.bilibili.com/blackboard/thebestremaker_pc.html`
	     ![image](https://user-images.githubusercontent.com/67217225/99223090-d1dd4000-281e-11eb-84f7-84a80e51836c.png)
    * 2. 按F12打开开发者工具，点击`console`
	     ![image](https://user-images.githubusercontent.com/67217225/99223254-208ada00-281f-11eb-8d24-66f344acc50a.png)
    * 3. 输入`window.__initialState['pc-lottery-new'][0]['lotteryId']`(手机版页面是`window.__initialState['h5-lottery-new'][0]['lotteryId']`)后，回车，即可看到sid
	     ![image](https://user-images.githubusercontent.com/67217225/99223641-dc4c0980-281f-11eb-90c7-d3cfeae858ea.png)

#### webhook(消息推送，可选)
用于自定义消息推送接口(只支持http/https,不支持websocket),不提供则不推送
##### http_header(http头部，必选)
这里提供推送消息时携带的http头部字段
##### variable(变量定义，必选)
这里提供推送消息时可用于url字段和params字段的变量,可以用大括号`{变量名}`引用在这里声明的变量<br>
`msg_simple和msg_raw`两个变量为内部变量，分别代表简化的推送消息和完整的推送消息(和日志一致),在这里声明后才能使用(值为null)<br>
其余变量可自定义(不可声明`msg_`开头的变量)
##### hooks(推送接口列表，必选)
数组，定义所有推送接口,每个接口包含以下字段
* enable(可选) true为启用,false为禁用,不存在默认启用
* name(必选) 字符串,接口名,在日志中使用
* http_header(可选) 同上面的http_header,不过这里只应用于本接口,而上面应用于所有接口
* variable(可选) variable,不过这里只应用于本接口,而上面应用于所有接口
* msg_separ(可选) 每条日志消息的分割符,默认为换行`\n`
* method(必选) 整数,请求方式,0为get,1为post,2为以json方式post
* url(必选) 字符串,请求链接,可用`{变量名}`方式引用上面variable变量中定义的变量(不可引用`msg_simple和msg_raw`)
* params(必选) 自定义请求参数,可用`{变量名}`方式引用上面variable变量中定义的变量

附: 微信推送server酱SCKEY获取方式如下:
* 1.进入`http://sc.ftqq.com/3.version`，点击`登入`，绑定github账号
    ![image](https://user-images.githubusercontent.com/67217225/99224324-179b0800-2821-11eb-822d-d2fa99bfec23.png)
	![image](https://user-images.githubusercontent.com/67217225/99224667-baec1d00-2821-11eb-8eab-a880965e6a3d.png)
* 2.点击`微信推送`，`开始绑定`，微信扫码登录
    ![image](https://user-images.githubusercontent.com/67217225/99225143-8a58b300-2822-11eb-8e53-5ad3a0f8eaa6.png)
* 3.在`发送消息`选项卡就能看到自己的SCKEY
    ![image](https://user-images.githubusercontent.com/67217225/99225266-ba07bb00-2822-11eb-9e50-71648f11dadd.png)

#### log_file(日志文件,必选)
输出日志文件位置，不带路径为当前运行目录，为空则不输出日志

#### log_console(日志输出到控制台,必选)
true为输出到控制台,false为关闭输出

#### users(账户配置,必选)
账户数组，每个账户包括
* cookieDatas(必选)
    * SESSDATA(必选) 字符串，账号的SESSDATA
    * bili_jct(必选) 字符串，账号的bili_jct
    * DedeUserID(可选) 字符串，账号的uid，如果不提供则必须保证账号有效，建议提供
* show_name(可选) 账户在日志或消息中的昵称，不提供则为B站账户昵称
* tasks(必选) 参考上面default参数下的所有内容，可将其中任意部分复制到本参数下来提供每个账户的差异化配置，此配置中不存在的项则默认使用default参数下的配置，default参数下不存在的配置不能在本参数中使用

获取cookie方式:`浏览器打开B站主页--》按F12打开开发者工具--》application--》cookies`
<div align="center"><img src="https://s1.ax1x.com/2020/09/23/wjM09e.png" width="800" height="450" title="获取cookies示例"></div>