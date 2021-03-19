# jd-base
如果您是第一次安装，请等待1-2分钟后执行：docker exec -it jd bash git_pull，如你是旁路由，请把-p 5678:5678 \替换成--network host，食用方法a↓：
 ```
 docker run -dit \
	-v /安装目录/jd/config:/jd/config `# 冒号左边是配置文件存放的目录` \
	-v /安装目录/jd/log:/jd/log `# 日志保存目录` \
	-p 5678:5678 \
	-e ENABLE_HANGUP=true \
	-e ENABLE_WEB_PANEL=true \
	--name jd \
	--hostname jd \
	--restart always \
	noobx/jd:py
```
如需映射脚本出来直接在上面加一行：
```
-v /安装目录/jd/scripts:/jd/scripts \ `# 此为lxk大佬脚本目录` 
```
```
-v /安装目录/jd/scripts2:/jd/scripts2 \ `# 此为py脚本目录 若需要加py脚本请添加至此目录`
```
```
-v /安装目录/jd/scripts3:/jd/scripts3 \ `# 此为其他js脚本目录`
```
运行py脚本的方式
```
docker exce -it jd bash jd xxx py
具体请看sample中的docker.list.sample的cron的运行方式
```

# 此镜像为分支项目，不定期开发，并不能保证及时更新，如有bug，请先反馈，然后切换至主项目版本。
# 注意：此项目更新内容与主项目并不同步，介意者请勿使用。
# 主项目↓
 ```
 docker run -dit \
	-v /安装目录/jd/config:/jd/config \
	-v /安装目录/jd/log:/jd/log \
	-p 5678:5678 \
	-e ENABLE_HANGUP=true \
	-e ENABLE_WEB_PANEL=true \
	--name jd \
	--hostname jd \
	--restart always \
	noobx/jd:gitee
项目地址：https://github.com/dockere/jd-base
```
