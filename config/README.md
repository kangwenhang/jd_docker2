config
====  
##### 这里是BiliExp的进阶配置文件

* 1.config.json(功能及账户配置文件)
    此文件配置完成后请复制到secrets(advconfig)中，与简单部署中的secrets(biliconfig)冲突，这里有更高优先级
    <table border=0 cellpadding=0 cellspacing=0 width=799 style='border-collapse:
     collapse;table-layout:fixed;width:597pt'>
     <col width=64 style='width:48pt'>
     <col width=147 style='mso-width-source:userset;mso-width-alt:5233;width:110pt'>
     <col width=95 style='mso-width-source:userset;mso-width-alt:3384;width:71pt'>
     <col width=106 style='mso-width-source:userset;mso-width-alt:3754;width:79pt'>
     <col width=102 style='mso-width-source:userset;mso-width-alt:3612;width:76pt'>
     <col width=94 style='mso-width-source:userset;mso-width-alt:3328;width:70pt'>
     <col width=63 style='mso-width-source:userset;mso-width-alt:2247;width:47pt'>
     <col width=64 span=2 style='width:48pt'>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 width=64 style='height:13.8pt;width:48pt'>主配置项</td>
      <td class=xl6527348 width=147 style='width:110pt'>子配置项</td>
      <td colspan=2 class=xl6527348 width=201 style='width:150pt'>值</td>
      <td colspan=3 class=xl6627348 width=259 style='width:193pt'>说明</td>
     </tr>
     <tr height=18 style='mso-height-source:userset;height:13.8pt'>
      <td height=18 class=xl1527348 style='height:13.8pt'></td>
      <td class=xl6527348>/</td>
      <td colspan=2 class=xl6527348>/</td>
      <td class=xl6627348 width=102 style='width:76pt'>值</td>
      <td class=xl6627348 width=94 style='width:70pt'>子配置项</td>
      <td class=xl6727348 width=63 style='width:47pt'>主配置项</td>
     </tr>
     <tr height=101 style='mso-height-source:userset;height:75.6pt'>
      <td rowspan=25 height=1248 class=xl6527348 style='height:937.2pt'>default</td>
      <td class=xl6527348>vip_task</td>
      <td colspan=2 class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td class=xl6727348 width=94 style='width:70pt'>每月1号领取大会员权益，28号用领取的B币劵给自己充电</td>
      <td rowspan=25 class=xl6627348 width=63 style='width:47pt'>全局默认配置</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 style='height:13.8pt'>xliveSign_task</td>
      <td colspan=2 class=xl6527348>true(默认)/false</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td class=xl6627348 width=94 style='width:70pt'>直播签到</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 style='height:13.8pt'>xlive_bag_send_task</td>
      <td colspan=2 class=xl6527348>true/false(默认)</td>
      <td colspan=2 class=xl6627348 width=196 style='width:146pt'>送出即将到期的礼物</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td rowspan=3 height=290 class=xl6527348 style='height:217.8pt'>coin_task</td>
      <td class=xl6527348>enable</td>
      <td class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td rowspan=3 class=xl6627348 width=94 style='width:70pt'>每日投币任务</td>
     </tr>
     <tr height=134 style='mso-height-source:userset;height:100.2pt'>
      <td height=134 class=xl6527348 style='height:100.2pt'>num</td>
      <td class=xl6527348>整数</td>
      <td class=xl6627348 width=102 style='width:76pt'>投币数量，如果当天已经投币超过这个数量则不会继续投币，取值范围为0-5</td>
     </tr>
     <tr height=138 style='mso-height-source:userset;height:103.8pt'>
      <td height=138 class=xl6527348 style='height:103.8pt'>target_exp</td>
      <td class=xl6527348>整数</td>
      <td class=xl6627348 width=102 style='width:76pt'>达到目标经验值停止投币，如果当天投币后达到经验值第二天及以后就不会投币</td>
     </tr>
     <tr height=37 style='height:27.6pt'>
      <td height=37 class=xl6527348 style='height:27.6pt'>watch_task</td>
      <td colspan=2 class=xl6527348>true(默认)/false</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td class=xl6627348 width=94 style='width:70pt'>模拟观看一个随机视频</td>
     </tr>
     <tr height=37 style='height:27.6pt'>
      <td height=37 class=xl6527348 style='height:27.6pt'>share_task</td>
      <td colspan=2 class=xl6527348>true(默认)/false</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td class=xl6627348 width=94 style='width:70pt'>模拟分享一个随机视频</td>
     </tr>
     <tr height=37 style='height:27.6pt'>
      <td height=37 class=xl6527348 style='height:27.6pt'>silver2coin_task</td>
      <td colspan=2 class=xl6527348>true(默认)/false</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td class=xl6627348 width=94 style='width:70pt'>每日银瓜子兑换硬币</td>
     </tr>
     <tr height=110 style='height:82.8pt'>
      <td height=110 class=xl6527348 style='height:82.8pt'>activity_task</td>
      <td colspan=2 class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td class=xl6627348 width=94 style='width:70pt'>B站转盘抽奖活动(具体活动参考本文件夹下activity.json文件)</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td rowspan=3 height=94 class=xl6527348 style='height:71.4pt'>lottery_task</td>
      <td class=xl6527348>enable</td>
      <td class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td rowspan=3 class=xl6627348 width=94 style='width:70pt'>转发当天12点到昨天12点动态里的所有抽奖</td>
     </tr>
     <tr height=38 style='mso-height-source:userset;height:28.8pt'>
      <td height=38 class=xl6527348 style='height:28.8pt'>reply</td>
      <td class=xl6527348>字符串</td>
      <td class=xl6627348 width=102 style='width:76pt'>回复原动态评论</td>
     </tr>
     <tr height=38 style='mso-height-source:userset;height:28.8pt'>
      <td height=38 class=xl6527348 style='height:28.8pt'>repost</td>
      <td class=xl6527348>字符串</td>
      <td class=xl6627348 width=102 style='width:76pt'>转到自己动态的评论</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td rowspan=2 height=96 class=xl6527348 style='height:72.0pt'>clean_dynamic_task</td>
      <td class=xl6527348>enable</td>
      <td class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td rowspan=2 class=xl6627348 width=94 style='width:70pt'>清理自己的动态(包括过期抽奖，失效动态)</td>
     </tr>
     <tr height=78 style='mso-height-source:userset;height:58.2pt'>
      <td height=78 class=xl6527348 style='height:58.2pt'>black_keywords</td>
      <td class=xl6527348>字符串数组</td>
      <td class=xl6627348 width=102 style='width:76pt'>一个或多个黑名单关键字，包含关键字的动态会删除</td>
     </tr>
     <tr height=18 style='mso-height-source:userset;height:13.2pt'>
      <td height=18 class=xl6527348 style='height:13.2pt'>manga_sign_task</td>
      <td colspan=2 class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td class=xl6627348 width=94 style='width:70pt'>每日漫画签到</td>
     </tr>
     <tr height=36 style='mso-height-source:userset;height:27.0pt'>
      <td rowspan=2 height=72 class=xl6527348 style='height:54.0pt'>exchangeCoupons_task</td>
      <td class=xl6527348>enable</td>
      <td class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td rowspan=2 class=xl6627348 width=94 style='width:70pt'>漫画积分兑换福利券，请保证程序在中午12点整启动</td>
     </tr>
     <tr height=36 style='mso-height-source:userset;height:27.0pt'>
      <td height=36 class=xl6527348 style='height:27.0pt'>num</td>
      <td class=xl6527348>整数</td>
      <td class=xl6627348 width=102 style='width:76pt'>兑换数量</td>
     </tr>
     <tr height=22 style='mso-height-source:userset;height:16.2pt'>
      <td rowspan=2 height=55 class=xl6527348 style='height:40.8pt'>manga_vip_reward_task</td>
      <td class=xl6527348>enable</td>
      <td class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td rowspan=2 class=xl6627348 width=94 style='width:70pt'>领取每月大会员漫画权益(漫读劵)</td>
     </tr>
     <tr height=33 style='mso-height-source:userset;height:24.6pt'>
      <td height=33 class=xl6527348 style='height:24.6pt'>days</td>
      <td class=xl6527348>整数数组</td>
      <td class=xl6627348 width=102 style='width:76pt'>执行的日期</td>
     </tr>
     <tr height=21 style='mso-height-source:userset;height:15.6pt'>
      <td rowspan=2 height=45 class=xl6527348 style='height:33.6pt'>manga_comrade_task</td>
      <td class=xl6527348>enable</td>
      <td class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td rowspan=2 class=xl6627348 width=94 style='width:70pt'>参加每月站友日活动</td>
     </tr>
     <tr height=24 style='mso-height-source:userset;height:18.0pt'>
      <td height=24 class=xl6527348 style='height:18.0pt'>days</td>
      <td class=xl6527348>整数数组</td>
      <td class=xl6627348 width=102 style='width:76pt'>执行的日期</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td rowspan=3 height=220 class=xl6527348 style='height:165.6pt'>manga_auto_buy_task</td>
      <td class=xl6527348>enable</td>
      <td class=xl6527348>true/false(默认)</td>
      <td class=xl6627348 width=102 style='width:76pt'>是否启用</td>
      <td class=xl6627348 width=94 style='width:70pt'></td>
     </tr>
     <tr height=92 style='height:69.0pt'>
      <td height=92 class=xl6527348 style='height:69.0pt'>mode</td>
      <td class=xl6527348>整数</td>
      <td class=xl6627348 width=102 style='width:76pt'>执行模式(1，自动购买追漫列表的漫画；2，参见下面filter参数)</td>
      <td rowspan=2 class=xl6627348 width=94 style='width:70pt'>自动花费即将过期的漫读劵</td>
     </tr>
     <tr height=110 style='height:82.8pt'>
      <td height=110 class=xl6527348 style='height:82.8pt'>filter</td>
      <td class=xl6527348>字符串</td>
      <td class=xl6627348 width=102 style='width:76pt'>购买指定的漫画，格式为&quot;mc号1|章节1,章节2,章节3;mc号2|章节1,章节2,章节3&quot;</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 style='height:13.8pt'>email</td>
      <td class=xl6527348>/</td>
      <td colspan=2 class=xl6527348>字符串(默认空)</td>
      <td colspan=3 class=xl6627348 width=259 style='width:193pt'>推送用的电子邮件(可选)</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 style='height:13.8pt'>SCKEY</td>
      <td class=xl6527348>/</td>
      <td colspan=2 class=xl6527348>字符串(默认空)</td>
      <td colspan=3 class=xl6627348 width=259 style='width:193pt'>微信推送用的SCKEY(可选)</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td rowspan=7 height=145 class=xl6527348 style='height:110.4pt'>users</td>
      <td class=xl6527348>······</td>
      <td class=xl6527348>······</td>
      <td class=xl6527348>······</td>
      <td class=xl6627348 width=102 style='width:76pt'>······</td>
      <td class=xl6627348 width=94 style='width:70pt'>······</td>
      <td rowspan=7 class=xl6627348 width=63 style='width:47pt'>账户配置(数组)</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td rowspan=3 height=54 class=xl6527348 style='height:41.4pt'>cookieDatas</td>
      <td class=xl6527348>SESSDATA</td>
      <td class=xl6527348>字符串</td>
      <td class=xl6527348>账户SESSDATA</td>
      <td rowspan=3 class=xl6627348 width=94 style='width:70pt'>账户cookie</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 style='height:13.8pt'>bili_jct</td>
      <td class=xl6527348>字符串</td>
      <td class=xl6527348>账户bili_jct</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 style='height:13.8pt'>DedeUserID</td>
      <td class=xl6527348>字符串</td>
      <td class=xl6527348>账户uid</td>
     </tr>
     <tr height=37 style='height:27.6pt'>
      <td height=37 class=xl6527348 style='height:27.6pt'>tasks</td>
      <td colspan=2 class=xl6527348>同主配置项default</td>
      <td class=xl6627348 width=102 style='width:76pt'>同主配置项default</td>
      <td class=xl6627348 width=94 style='width:70pt'>账户独立配置</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 style='height:13.8pt'>······</td>
      <td class=xl6527348>······</td>
      <td class=xl6527348>······</td>
      <td class=xl6627348 width=102 style='width:76pt'>······</td>
      <td rowspan=2 class=xl6627348 width=94 style='width:70pt'>无限扩展多账户</td>
     </tr>
     <tr height=18 style='height:13.8pt'>
      <td height=18 class=xl6527348 style='height:13.8pt'>······</td>
      <td class=xl6527348>······</td>
      <td class=xl6527348>······</td>
      <td class=xl6627348 width=102 style='width:76pt'>······</td>
     </tr>
    </table>