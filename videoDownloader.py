# -*- coding: utf-8 -*-
from BiliClient import (VideoParser, Downloader)
import sys, json, re, time, curses, os
is_win = os.name == 'nt'

ReverseProxy = 'http://biliapi.8box.top/playerproxy' #解析接口代理

with open('config/config.json','r',encoding='utf-8') as fp:
    configData = json.loads(re.sub(r'\/\*[\s\S]*?\/', '', fp.read()))

def get_input_tasks() -> list:
    '''通过控制台输入获得下载任务'''
    ret = []
    reverse = input('是否使用内部代理(可下载港澳台)(y/n)：').upper() == 'Y'
    add_another = True
    while add_another:
        url = input('请输入视频链接(或者av,bv号)：')
        video_parser = VideoParser(url)
        print(f'当前视频标题为：{video_parser.getTitle()}')
        video_list = video_parser.all()
        if len(video_list) == 1:
            video = video_list[0]
        else:
            for ii in range(len(video_list)):
                print(f'{ii+1}. {video_list[ii]}')
            P = int(input('请输入要下载的分P序号：'))
            video = video_list[P-1]

        if reverse:
            video_stream_list = video.allStream(configData["users"][0]["cookieDatas"], reverse_proxy=ReverseProxy)
        else:
            video_stream_list = video.allStream(configData["users"][0]["cookieDatas"])

        for ii in range(len(video_stream_list)):
            print(f'{ii+1}. {video_stream_list[ii]}')

        P = int(input('请输入要下载的视频流序号：'))
        video_stream = video_stream_list[P-1]
        ret.append(video_stream)
        print('成功添加一个下载任务.....')
        add_another = input('是否再添加一个任务(y:再添加一个/n:立即开始下载)：').upper() == 'Y'
    return ret

def downloader_put_tasks(downloader, tasks):
    '''将下载任务放进下载器'''
    for xx in tasks:
        downloader.add(url=xx.url, dst=xx.fliename, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)","Referer":"https://www.bilibili.com/"})

def show(stdscr, tasklist: list, tasknum: tuple or list) -> None:
    stdscr.clear()
    if is_win:
        for ii in range(len(tasklist)):
            stdscr.addstr(ii*3, 0, ' '.join(f'正在下载:{tasklist[ii]["dst"]}'))
            per = tasklist[ii]["completedLength"] / tasklist[ii]["totalLength"]
            perlen = int(per * 40)
            stdscr.addstr(ii*3+1, 0, f"进 度 : [{'*' * perlen}{' ' * (40 - perlen)}] {per*100:.2f}%")
        stdscr.addstr(ii*3+3, 0, f'任 务 总 数 {tasknum[0]}个 ,正 在 下 载 {tasknum[1]}个 ,等 待 中 {tasknum[2]}个 ,下 载 完 成 {tasknum[3]}个 ,失 败 任 务 {tasknum[4]}个 ')
    else:
        for ii in range(len(tasklist)):
            stdscr.addstr(ii*2, 5, f'正在下载: {tasklist[ii]["dst"]}')
            per = tasklist[ii]["completedLength"] / tasklist[ii]["totalLength"]
            perlen = int(per * 40)
            stdscr.addstr(ii*2+1, 0, f"进度: [{'*' * perlen}{' ' * (40 - perlen)}] {per*100:.2f}%")
        stdscr.addstr(ii*2+2, 0, f'任务总数{tasknum[0]}个,正在下载{tasknum[1]}个,等待中{tasknum[2]}个,下载完成{tasknum[3]}个,失败任务{tasknum[4]}个')
    stdscr.refresh()

def queryDownloaderInfo(downloader):
    task_nums = [0, 0, 0, 0, 0]
    active_task = []
    for x in downloader.queryAll():
        task_nums[0] += 1
        if x["status"] == "active":
            task_nums[1] += 1
            active_task.append(x)
        elif x["status"] == "waiting":
            task_nums[2] += 1
        elif x["status"] == "over":
            task_nums[3] += 1
        elif x["status"] == "failed":
            task_nums[4] += 1

    return active_task, task_nums

def display(downloader) -> None:
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    while True:
        time.sleep(2)
        active_task, task_nums = queryDownloaderInfo(downloader)
        if not (task_nums[1] or task_nums[2]):
            break
        show(stdscr, active_task, task_nums)
    curses.endwin()

def main(*args):
    tasks = get_input_tasks()
    downloader = Downloader()
    downloader_put_tasks(downloader, tasks)
    downloader.startAll()
    display(downloader)
    print("下载结束")

if __name__=="__main__":
    main()