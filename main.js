/*
原生nodejs运行方式,不需要面板,下面配置好脚本和运行时间,在pm2挂在该主要程序脚本,
安装pm2命令:npm install pm2 -g
挂载主程序命令:pm2 start main.js --name myserver

*/
var cronJob = require("cron").CronJob;

//在此处配置定时和脚本
cron('*/20 * * * * *', './111.js');
cron('*/20 * * * * *', './222.js');



function cron(time, file) {
    new cronJob(time, () => {
        try {
            delete require.cache[require.resolve(file)];
            require(file);
        } catch (error) {
            console.log('\r\n ' + file + "_erro:" + error);
        }
    }, null, true);
}
