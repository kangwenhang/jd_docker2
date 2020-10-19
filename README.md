<div align="center"> 
<h1 align="center">
BiliExp
</h1>

[![](https://img.shields.io/badge/author-%E6%98%9F%E8%BE%B0-red "作者")](https://github.com/happy888888/ )
![](https://img.shields.io/badge/dynamic/json?label=GitHub%20Followers&query=%24.data.totalSubs&url=https%3A%2F%2Fapi.spencerwoo.com%2Fsubstats%2F%3Fsource%3Dgithub%26queryKey%3Dhappy888888&labelColor=282c34&color=181717&logo=github&longCache=true "关注数量")
![](https://img.shields.io/github/stars/happy888888/BiliExp.svg?style=plastic&logo=appveyor "Star数量")
![](https://img.shields.io/github/forks/happy888888/BiliExp.svg?style=plastic&logo=stackshare "Fork数量")
[![](https://img.shields.io/badge/LICENCE-SATA-BLUE.svg?style=plastic "协议")](https://github.com/zTrix/sata-license)
![](https://img.shields.io/badge/python->=3.6-GREEN.svg?style=social "python版本")
![](https://img.shields.io/github/contributors/happy888888/BiliExp "贡献者")

</div>

## 主要功能
**一、B站自动操作脚本**

* [x] 自动获取经验(投币、点赞、分享视频) 
* [x] 自动转发互动抽奖并评论(自己关注的up主,目前没有自动关注功能,需要可以提issue)
* [x] 参与官方转盘抽奖活动(activity，目前没有自动搜集活动的功能,需要在config/activity.json里面手动指定)
* [x] 直播辅助(直播签到，~~直播挂机~~，直播自动送出快过期礼物) 
* [x] 自动兑换银瓜子为硬币 
* [x] 自动领取大会员每月权益(B币劵，优惠券)(每月1号) 
* [x] 自动将大会员B币劵给自己账户充电。(每月28号)
* [x] 漫画辅助脚本(漫画APP签到，自动花费即将过期漫读劵，自动积分兑换漫画福利券，自动领取大会员每月福利劵，自动参加每月"站友日"活动) 
* [x] 定时清理无效动态(转发的过期抽奖，失效动态) 
* [ ] ~~直播开启宝箱领取银瓜子(本活动已结束，不知道B站以后会不会再启动)~~ 
* [x] 风纪委员投票(处于功能测试状态，目前每次执行只投一次票)
</br>

```
如有其他功能需求请发issue，本部分的最新功能将在BiliExp-Actions分支更新，稳定后合并到本主分支
```

**二、脚本up主系列**
* 专栏的编写，排版和发表
* 视频稿件的上传和发布
(例子参考"机器人up主"文件夹)
</br>

**三、B站漫画下载**支持合并为单个pdf文件,允许使用账号cookie下载已解锁部分
* [x] 使用账号cookie下载已解锁部分
* [x] 合并为单个pdf文件
</br>

**四、B站视频下载(需要aria2)**
* [x] 使用账号cookie下载大会员视频
* [x] 支持下载港澳台番剧(内置一个反向代理接口，接口源码见"player_proxy"文件夹，支持云函数部署此接口)
</br>

# 目录

- [主要功能](#主要功能)
- [目录](#目录)
- [使用说明(仅自动操作脚本部分)](#使用方式仅自动操作脚本部分)
  - [一、只使用Actions(推荐)](#方式一推荐只使用github-actions)
  - [二、使用腾讯云函数(Actions部署)](#方式二使用腾讯云函数)
  - [三、使用阿里云函数(Actions部署)(不推荐)](#方式三不推荐使用阿里云函数)
  - [四、windows本地部署(依靠任务计划启动)](#方式四windows本地部署)
  - [五、linux本地部署(依靠crontab启动,shell自动下载安装)](#方式五linux本地部署)
- [更新日志](#更新日志)
- [获得B站账户cookies方法](#获得cookies方法)

</br>

## 使用方式(仅自动操作脚本部分)

### 方式一(推荐)、只使用github Actions
* 请转至本项目的"<a href="https://github.com/happy888888/BiliExp/tree/BiliExp-Actions" title="B站经验脚本纯Actions版">BiliExp-Actions</a>"分支，请区分此分支的Actions与本主分支的不同，不要使用本主分支的Actions。
* 为避免我收到大量无用的Actions消息，故不将此Actions添加到master主分支内。
* fork后切换分支的方法如下
![image](https://user-images.githubusercontent.com/67217225/94278277-34336600-ff7d-11ea-8cb5-d49e5e6884fc.png)


### 方式二、使用腾讯云函数

详细图文教程可以参考[博客文章](https://my-hexo-bucket-1251971143.cos-website.ap-guangzhou.myqcloud.com/2020/09/30/bilibili/) 。

##### 1. 准备
* 1.1开通云函数 SCF 的腾讯云账号，在[访问秘钥页面](https://console.cloud.tencent.com/cam/capi)获取账号的 TENCENT_SECRET_ID，TENCENT_SECRET_KEY
> 注意！为了确保权限足够，获取这两个参数时不要使用子账户！此外，腾讯云账户需要[实名认证](https://console.cloud.tencent.com/developer/auth)。
* 1.2依次登录 [SCF 云函数控制台](https://console.cloud.tencent.com/scf) 和 [SLS 控制台](https://console.cloud.tencent.com/sls) 开通相关服务，确保您已开通服务并创建相应[服务角色](https://console.cloud.tencent.com/cam/role) **SCF_QcsRole、SLS_QcsRole**
* 1.3一个或多个B站账号，以及登录后获取的SESSDATA，bili_jct，DedeUserID (获取方式见最下方示意图),可选：SCKEY，email用于微信或邮箱的消息推送
* 1.4fork本项目
##### 2. 部署
*  2.1 在fork后的github仓库的 “Settings” --》“Secrets” 中添加"Secrets"，name和value分别为：
    *  2.1.1 name为"TENCENT_SECRET_ID"           value为腾讯云用户SecretID(需要主账户，子账户可能没权限)
    *  2.1.2 name为"TENCENT_SECRET_KEY"        value为腾讯云账户SecretKey
    *  2.1.3 name为"biliconfig"           value为B站账号登录信息，格式如下
		```
        SESSDATA
        bili_jct
        uid
        ```
        例如下面这样
        ```
        e1272654%vfdawi241825%2C8dc06*a1
        0a9081cc53856314783d195f5ddbadf3
        203953353
        ```
		![image](https://user-images.githubusercontent.com/67217225/95849036-77654580-0d81-11eb-8125-9adcd23ec25a.png)

*  2.2 添加完上面 3 个"Secrets"后，进入"Actions"(上面那个不是Secrets下面那个) --》"deploy for tencentyun"，点击右边的"Run workflow"即可部署至腾讯云函数(如果出错请在红叉右边点击"deploy for tencentyun"查看部署任务的输出信息找出错误原因)
    *  2.2.1 首次fork可能要去actions里面同意使用actions条款，如果"Actions"里面没有"deploy for tencentyun"，点一下右上角的"star"，"deploy for tencentyun"就会出现在"Actions"里面

```
    注: 默认并没有开启所有功能，部署到云函数后可以去/config/config.json文件进行更加详细的配置
	1. 自定义功能开启与关闭
	2. 投币功能自定义投币数量
	3. 抽奖动态转发自定义评论内容，默认评论为(从未中奖，从未放弃[doge])
	4. 漫画辅助功能的启用与详细配置，默认不启用此功能
	5. 风纪委员投票功能的启用与详细配置，默认不启用此功能
	6. 多账户的支持(支持50个以上的B站账号)，默认只能单账号
```

### 方式三(不推荐)、使用阿里云函数

目前有发现在Actions内无法ping通阿里云函数的域名，部署可能出现超时现象

* 1.准备
    *  1.1开通云函数计算的阿里云账号，以及账号的ACCOUNT_ID，ACCESS_KEY_ID，ACCESS_KEY_SECRET(**注意**！！获取后面两个参数时**不**要使用**子账户**！！会没有权限创建新的函数，请提前开启云函数服务)
    *  1.2一个或多个B站账号，以及登录后获取的SESSDATA，bili_jct，DedeUserID (获取方式见最下方示意图),可选：SCKEY，email用于微信或邮箱的消息推送
    *  1.3fork本项目

* 2.部署
    *  2.1在fork后的github仓库的 “Settings” --》“Secrets” 中添加"Secrets"，name和value分别为：
        *  2.1.1 name为"ACCOUNT_ID"           value为阿里云用户的账号ID
        *  2.1.2 name为"ACCESS_KEY_ID"        value为阿里云账户AccessKeyID(需要主账户，子账户可能没权限)
        *  2.1.3 name为"ACCESS_KEY_SECRET"    value为阿里云账户accessKeySecret
        *  2.1.4 name为"biliconfig"           value为B站账号登录信息，同上面腾讯云函数的部署步骤2.1.3

    *  2.2添加完上面4个"Secrets"后，进入"Actions" --》"deploy for aliyun"，点击右边的"Run workflow"即可部署至阿里云函数(如果出错请在红叉右边点击"deploy for aliyun"查看部署任务的输出信息找出错误原因)
        *  2.2.1 首次fork可能要去actions里面同意使用actions条款，如果"Actions"里面没有"deploy for aliyun"，点一下右上角的"star"，"deploy for aliyun"就会出现在"Actions"里面

### 方式四、windows本地部署

* 1.准备
    *  1.1一个或多个B站账号，以及登录后获取的SESSDATA，bili_jct，DedeUserID (获取方式见最下方示意图),可选：SCKEY，email用于微信或邮箱的消息推送
    *  1.2进入右边的release,下载BiliExp-win32_64开头的压缩包

* 2.部署
    *  2.1解压步骤1.2下载的压缩包，并放置到合适位置(比如E:\Program Files)
    *  2.2进入解压后产生的config文件夹，配置config.json文件(包含功能的启用和账号cookie的配置)
    *  2.3退出config文件夹返回上层，运行setup_for_windows.bat文件(需要管理员权限)，按照提示即可完成安装。脚本将会在每天12:00启动(依赖于计划任务)。
	
### 方式五、linux本地部署

* 1.准备
    *  1.1一个或多个B站账号，以及登录后获取的SESSDATA，bili_jct，DedeUserID (获取方式见最下方示意图),可选：SCKEY，email用于微信或邮箱的消息推送

* 2.部署
    *  2.1执行如下命令，并按照提示安装
	      ```
		  wget https://glare.now.sh/happy888888/BiliExp/BiliExp-Linux-64 && mv BiliExp-Linux-64* BiliExp.tar && tar xvf BiliExp.tar && cd BiliExp && sudo chmod 755 setup_for_linux.sh && sudo ./setup_for_linux.sh
		  ```
    *  2.2安装成功后，可去/etc/BiliExp/config.json文件中进行详细配置，脚本将会在每天12:00启动(依赖于crontab)。

</br></br></br>

## 更新日志

### 2020/10/20更新

* 1.发布release版

</br></br>

### 2020/10/16更新

* 1.将云函数部分与BiliExp-Actions分支合并，重构这部分所有代码，并调整文件结构

</br></br>

### 2020/10/1更新

* 1.B站漫画增加自动领取每月大会员赠送的漫读劵。
* 2.B站漫画增加自动参与站友日活动(默认关闭)。
* 3.增加每月28号自动将没有使用的B币劵充电给自己的账户。

</br></br>

### 2020/09/27更新

* 1.互动抽奖方式改为转发并评论(听说能提高中奖率🤑🤩)。

</br></br>

### 2020/09/26更新

* 1.增加email推送。

</br></br>

### 2020/09/24更新

* 1.移除云函数脚本中的doActivity.py和其配置文件。

</br></br>

### 2020/09/23更新

* 1.更新Actions，部署前执行账号检查，应对有的人账号配置错误部署后脚本执行失败且找不出原因的情况。
* 2.新增分支BiliExp-Actions，使依赖于云函数的功能只需要github Actions就能使用，不需要使用云函数。

</br></br>

### 2020/09/22更新

* 1.更新BiliExp.py直接自动获取每月大会员权益(B币劵，优惠券)功能
* 2.增加mangaTask.py自动用即将过期的漫读劵兑换漫画(自动购买追漫列表(默认)或者手动指定购买列表),自动用积分兑换福利券(默认关闭),合并以前的mangaClockIn.py文件到此文件
* 3.彻底将直播开启宝箱领取银瓜子的功能从云函数中移除。

</br></br>

### 2020/09/17更新

* 1.更新BiliLottery.py转发抽奖的逻辑，避免动态太多导致抽奖动态转发的遗漏
* 2.增加videoDownloader.py下载B站视频
* 3.增加models/aria2py.py用于B站视频的下载
* 4.增加/player_proxy/player_proxy.js用于代理B站视频解析接口(需要部署到阿里云函数港澳台服务器)

</br></br>

### 2020/09/02更新

* 1.增加topicRepost.py转发话题列表(抽奖话题)(不包含在云函数内)
* 2.增加cancelAttention.py一键取关所有up主(不包含在云函数内)
* 3.增加mangaDownloader.py下载B站漫画，支持合并转pdf
* 3.删除四个已经失效的活动，现在几乎没有可以白嫖B站的官方抽奖活动了，参加(官方抽奖)活动的功能可能会取消

</br></br>

### 2020/08/28更新

* 1.截至今天，B站直播开时间宝箱领取银瓜子的活动已经结束
* 2.B站官方活动里面的 "夏日不宅宣言" 活动和 "新星计划-暑假赛" 活动已经结束，新增加"最强安利王"活动

</br></br>
### 2020/08/25更新

* 1.增加送出即将过期的直播礼物的功能
* 2.增加直播心跳维持在线状态的功能(非大老爷用户在线时长并不能加经验)

</br></br>
### 2020/08/22更新

* 1.使用Actions实现脚本自动部署到阿里云，代替本文最下方的手动部署方式(已删除)


</br></br>
### 2020/08/21更新

* 1.增加doActivity.py用于参加B站官方活动(抽奖类) 活动列表 https://www.bilibili.com/blackboard/x/act_list/
    *  活动列表(抽奖类)存放在config/activity.json中
        *  每个活动都有过期时间(目前的大部分活动都将在8.30日前过期)，活动中抽奖也有参与次数限制
        *  有的活动每天固定赠送抽奖次数，有的活动需要转发，还有的活动需要关注投币点赞甚至投稿才能获得抽奖次数，本脚本只能做每天固定赠送抽奖次数，和转发获得抽奖次数的活动
        *  活动过期或添加新活动均需手动更新activity.json，有新活动或者活动是否过期都可以在上面活动列表网址查看
    * 本人首次在"舞见大合集"活动中抽中一个"小电视抱枕"，第一次在B站中抽中实物，记录一下☺️
* 2.增加cleanDynamic.py用于清理转发的动态
    *  清理的转发动态包括:①互动抽奖过期的动态；②两个月前带#互动抽奖#标签的动态；③被原up主删除的动态
* 3.用户配置文件仅需要cookies，不需要再获取客户端的access_key，access_key从用户配置文件移除，用户配置文件由userData/userData.py改为config/config.json，账户检查脚本由userData/check.py移动到check.py


</br></br>
### 2020/08/07更新

* 1.增加B站视频上传api
* 2.增加一个自动转载视频并发布的例子(youtube一键转B站)

</br></br>
### 2020/08/06更新

* 1.发现B站app的access_key与漫画app通用，调整了app相关api的结构
* 2.新增加Article类实现专栏的自动发表,Article.Content类实现B站专栏内容的排版(支持插入B站所有标签)
* 3.增加两个自动发表B站专栏的例子(1.收集自己动态里的抽奖内容并发表到专栏；2.自动收集P站图片并转载到专栏(此脚本发表的图片通不过B站审核))
* 4.利用B站专栏的图片上传接口可能能实现把B站当做免费图床？(大雾)？

</br></br>

#### 获得cookies方法
B站操作需要的cookie数据可以按照以下方式获取
浏览器打开B站主页--》按F12打开开发者工具--》application--》cookies
<div align="center"><img src="https://s1.ax1x.com/2020/09/23/wjM09e.png" width="800" height="450" title="获取cookies示例"></div>
