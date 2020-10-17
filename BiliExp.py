# -*- coding: utf-8 -*-
import asyncio, json, time, logging, sys, re, io
from models.asyncBiliApi import asyncBiliApi
#from tasks import * #所有任务模块通过动态加载

def push_message(SCKEY=None,
                 email=None
                 ) -> None:

    log = log_stream_io.getvalue()
    import urllib
    if SCKEY:
        data_string = urllib.parse.urlencode({"text": "B站经验脚本消息推送","desp": log.replace("\n","\n\n")})
        urllib.request.urlopen(f'https://sc.ftqq.com/{SCKEY}.send', data=data_string.encode())
    if email:
        data_string = urllib.parse.urlencode({"address":email, "name": "B站经验脚本消息推送", "certno": log.replace("\n","<br>")})
        #这辣鸡接口居然还要User-Agent才能访问....
        req = urllib.request.Request(url=f'http://liuxingw.com/api/mail/api.php?{data_string}', headers={"User-Agent":"Mozilla/5.0"})
        urllib.request.urlopen(req)

async def run_user_tasks(user,           #用户配置
                        default          #默认配置
                        ) -> None:

    async with asyncBiliApi() as biliapi:
        try:
            if not await biliapi.login_by_cookie(user["cookieDatas"]):
                logging.warning(f'id为{user["cookieDatas"]["DedeUserID"]}的账户cookie失效，跳过此账户后续操作')
                return
        except Exception as e: 
            logging.warning(f'登录验证id为{user["cookieDatas"]["DedeUserID"]}的账户失败，原因为{str(e)}，跳过此账户后续操作')
            return

        tasks = []

        for task in default: #遍历任务列表，把需要运行的任务添加到tasks
            if isinstance(default[task], bool):
                if task in user["tasks"]:
                    if user["tasks"][task]:
                        task_module = __import__(f'tasks.{task}') #载入任务模块
                        task_function = getattr(getattr(task_module, task), task)#载入任务入口方法
                        tasks.append(task_function(biliapi))               #放进任务列表
                elif default[task]:
                    task_module = __import__(f'tasks.{task}')
                    task_function = getattr(getattr(task_module, task), task)
                    tasks.append(task_function(biliapi))
            elif isinstance(default[task], dict):
                if task in user["tasks"]:
                    if user["tasks"][task]["enable"]:
                        task_module = __import__(f'tasks.{task}')
                        task_function = getattr(getattr(task_module, task), task)
                        tasks.append(task_function(biliapi, user["tasks"][task]))
                elif default[task]["enable"]:
                    task_module = __import__(f'tasks.{task}')
                    task_function = getattr(getattr(task_module, task), task)
                    tasks.append(task_function(biliapi, default[task]))
        if tasks:
            await asyncio.wait(tasks)        #异步等待所有任务完成

def initlog(log_file: str, log_console: bool, log_stream: bool):
    '''初始化日志参数'''
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter1 = logging.Formatter("[%(levelname)s]; %(message)s")
    if log_console:
        console_handler = logging.StreamHandler(stream=sys.stdout) #输出到控制台
        console_handler.setFormatter(formatter1)
        logger.addHandler(console_handler)
    if log_stream:
        global log_stream_io #全局变量
        log_stream_io = io.StringIO() #用于记录日志
        strio_handler = logging.StreamHandler(stream=log_stream_io) #输出到log_stream用于消息推送
        formatter2 = logging.Formatter("%(message)s")
        strio_handler.setFormatter(formatter2)
        logger.addHandler(strio_handler)
    if log_file:
         file_handler = logging.FileHandler(log_file)#输出到日志文件
         file_handler.setFormatter(formatter1)
         logger.addHandler(file_handler)

def main(*args):
    try:
        with open('config/config.json','r',encoding='utf-8') as fp:
            configData = json.loads(re.sub(r'\/\*[\s\S]*?\/', '', fp.read()))
    except Exception as e: 
        print(f'配置加载异常，原因为{str(e)}，退出程序')
        sys.exit(6)
    
    try:
        is_push_message = bool(configData["email"] or configData["SCKEY"])
        initlog(configData["log_file"], configData["log_console"], is_push_message)
    except Exception as e: 
        print(f'日志配置异常，原因为{str(e)}')

    #启动任务
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(run_user_tasks(user, configData["default"])) for user in configData["users"]]
    loop.run_until_complete(asyncio.wait(tasks))

    if is_push_message:
        try:
            push_message(configData["SCKEY"], configData["email"])
        except Exception as e: 
            logging.error(f'消息推送异常，原因为{str(e)}')

__name__=="__main__" and main()