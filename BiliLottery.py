from models.Biliapi import BiliWebApi
import sqlite3

cookieData = {
    "SESSDATA": "",
    "bili_jct": "",
    "DedeUserID": "",
}

def update(dynamic_id):
    conn = sqlite3.connect('lottery.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM lottery WHERE dynamic_id=?", (dynamic_id,))
    result = True if cursor.fetchone() else False
    if not result:
        cursor.execute("SELECT id FROM lottery ORDER BY date ASC LIMIT 0,1")
        id = cursor.fetchone()[0]
        cursor.execute("UPDATE lottery SET dynamic_id=? WHERE id=?", (dynamic_id, id))
    cursor.close()
    conn.commit()
    conn.close()
    return result

def bili_lottery(data):

    try:
        biliapi = BiliWebApi(data)
    except Exception as e: 
        logging.error(f'登录验证id为{data["DedeUserID"]}的账户失败，原因为{str(e)}，跳过后续所有操作')
        return

    try:
        datas = biliapi.getDynamicNew()["data"]["cards"]
    except Exception as e: 
        logging.warning(f'获取动态列表异常，原因为{str(e)}，跳过后续所有操作')
        return

    for x in datas:
        if x.__contains__("extension") and x["extension"].__contains__("lott"):
            uname = x["desc"]["user_profile"]["info"]["uname"]
            dynamic_id = x["desc"]["dynamic_id"]
            if not update(dynamic_id):
                try:
                    biliapi.repost(dynamic_id)
                    logging.info(f'转发抽奖(用户名:{uname},dynamic_id:{str(dynamic_id)})成功')
                except Exception as e: 
                    logging.warning(f'此次转发抽奖失败，原因为{str(e)}')

def main(*args):
    try:
        logging.basicConfig(filename="lottery.log", filemode='a', level=logging.INFO, format="%(asctime)s: %(levelname)s, %(message)s", datefmt="%Y/%d/%m %H:%M:%S")
    except:
        pass
    bili_lottery(cookieData)

main()