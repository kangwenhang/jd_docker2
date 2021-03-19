#!/bin/sh

build_crontab_file(){
  if [ ${enable_52pojie} ];then
    if [ -f "${config_52pojie}" ];then
      echo "10 13 * * *       node /AutoSignMachine/index.js 52pojie --config=${config_52pojie}" >> /var/spool/cron/crontabs/root
    else
      echo "52pojie配置文件${config_52pojie}不存在，任务跳过"
    fi
  fi

  if [ ${enable_bilibili} ];then
    if [ -f "${config_bilibili}" ];then
      echo "*/30 7-22 * * *       node /AutoSignMachine/index.js bilibili --config=${config_bilibili}" >> /var/spool/cron/crontabs/root
    else
      echo "bilibili配置文件${config_bilibili}不存在，任务跳过"
    fi
  fi

  if [ ${enable_iqiyi} ];then
    if [ -f "${config_iqiyi}" ];then
      echo "*/30 7-22 * * *       node /AutoSignMachine/index.js iqiyi --config=${config_iqiyi}" >> /var/spool/cron/crontabs/root
    else
      echo "iqiyi配置文件${config_iqiyi}不存在，任务跳过"
    fi
  fi

  if [ ${enable_unicom} ];then
    if [ -f "${config_unicom}" ];then
      echo "*/30 7-22 * * *       node /AutoSignMachine/index.js unicom --config=${config_unicom}" >> /var/spool/cron/crontabs/root
    else
      echo "unicom配置文件${config_unicom}不存在，任务跳过"
    fi
  fi

  if [ ${enable_hecaiyun} ];then
    if [ -f "${config_hecaiyun}" ];then
      echo "10 13 * * *       node /AutoSignMachine/index.js hecaiyun --config=${config_hecaiyun}" >> /var/spool/cron/crontabs/root
    else
      echo "hecaiyun配置文件${config_hecaiyun}不存在，任务跳过"
    fi
  fi
}

git_pull_update(){
  if [ ${enable_git_pull_update} ];then
    echo "将启用git pull更新"
    echo "*/30 7-22 * * *       git -C /AutoSignMachine/ fetch --all && git -C /AutoSignMachine/ reset --hard ${git_branch}"  >> /var/spool/cron/crontabs/root
  fi
}

if [ ${crontab_file} ];then
  echo "已指定计划任务配置${crontab_file}，将直接使用该文件"
  /usr/bin/crontab ${crontab_file}
else
  git_pull_update
  build_crontab_file
fi

/usr/sbin/crond -S -c /var/spool/cron/crontabs -f -L /dev/stdout