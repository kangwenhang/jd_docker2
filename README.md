# BiliExp
B站自动操作脚本(投币、点赞、分享视频，直播签到，自动转发抽奖，漫画APP签到)

B站操作需要的cookie数据可以按照以下方式获取
浏览器打开B站主页--》按F12打开开发者工具--》application--》cookies
![Image not found](https://github.com/happy888888/BiliExp/raw/master/tip.png)
# BiliExp
B站自动操作脚本(投币、点赞、分享视频，直播签到，自动转发抽奖，漫画APP签到)


##BiliExp主要文件及功能？

* BiliExp.py：B站直播签到，投币点赞分享，模拟观看视频，一键获取经验
    *  需要将用户SESSDATA，bili_jct，DedeUserID三个cookie填入脚本内
    *  支持多账户
    *  支持云函数每日执行
    *  支持微信消息推送脚本运行结果(感谢server酱提供的推送微信消息服务，详情见http://sc.ftqq.com/)

* BiliLottery.py：B站动态一键抽奖
    *  需要将用户SESSDATA，bili_jct，DedeUserID三个cookie填入脚本内
    *  已抽奖动态id保存在Lottery.db这个数据库文件中
    *  建议每隔10分钟运行一次

* silver2coin.py：一键将银瓜子兑换成硬币
    *  需要将用户SESSDATA，bili_jct，DedeUserID三个cookie填入脚本内
    *  支持多账户
    *  支持云函数每日执行
    *  每天只能执行不超过一次

* SilverAward.py：B站直播领取时间宝箱获取银瓜子
    *  需要将B站app登录后获得的access_key填入脚本
    *  支持多账户
    *  支持云函数执行
          *  普通用户每天可领取三轮，建议云函数触发器cron表达式为0 0,3,9,18,21,27,36,39,45,54 2 \* \* \* \*
          *  大老爷用户每天可领取五轮，建议在普通用户的基础上增加一个云函数触发器cron表达式为0 0,6,15,18,24,33 3 \* \* \* \*

* mangaClockIn.py：一键签到B站漫画客户端，获得积分和漫读劵(连续一周)
    *  需要将B站漫画app登录后获得的access_key填入脚本
    *  支持多账户
    *  支持云函数每日执行

B站操作需要的cookie数据可以按照以下方式获取
浏览器打开B站主页--》按F12打开开发者工具--》application--》cookies
![Image not found](https://github.com/happy888888/BiliExp/raw/master/tip.png)
