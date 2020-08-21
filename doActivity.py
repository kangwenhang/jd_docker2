from models.Biliapi import BiliWebApi
import time, json

def do_activity(cookieData, activityData):
    try:
       biliapi = BiliWebApi(cookieData)
    except Exception as e:
       print(f'登录验证id为{cookieData["DedeUserID"]}的账户失败，原因为({str(e)})，跳过此账户后续所有操作')
       return
    print(f'id为{cookieData["DedeUserID"]}的账户开始参与活动')
    for x in activityData:
        print(f'开始参与 "{x["name"]}" 活动')
        for y in x["addTimes"]:
            try:
                biliapi.activityAddTimes(x["sid"], y) #执行增加抽奖次数操作,一般是分享转发
            except Exception as e:
                print(f'增加抽奖次数异常,原因为({str(e)})')

        try:
            times = biliapi.activityMyTimes(x["sid"])["data"]["times"]
        except Exception as e:
            print(f'获取剩余抽奖次数异常，原因为({str(e)})，在尝试执行1次抽奖')
            times = 1
        print(f'活动可参与的次数为{times}')

        for ii in range(times):
            try:
                result = biliapi.activityDo(x["sid"], 1)
                print(f'{ii + 1}.', end="")
                if result["code"]:
                    print(result["message"])
                else:
                    print(result["data"][0]["gift_name"]) #获取奖品名称，目前没发现一次中几个奖的，但是抽奖结果是数组
                    time.sleep(5.5) #抽奖延时
            except Exception as e:
                print(f'参与活动异常，原因为({str(e)})')

def main(*args):
    with open('config/config.json','r',encoding='utf-8') as fp:
        configData = json.load(fp)

    with open('config/activity.json','r',encoding='utf-8') as fp:
        activityData = json.load(fp)

    for x in configData["cookieDatas"]:
        do_activity(x, activityData)

if __name__=="__main__":
    main()