#!/bin/sh

#删除非每日任务功能需要的模块，否则会执行失败
BiliClient_needs=("__init__.py" "asyncBiliApi.py" "asyncXliveWs.py")
params=''
for i in ${BiliClient_needs[@]};do params="$params\|$i"; done
delete_arr=(`ls ./BiliClient|grep -v ${params: 2}`)
for i in ${delete_arr[@]};do rm -rf "./BiliClient/${i}"; done
