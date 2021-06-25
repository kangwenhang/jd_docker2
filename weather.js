/*
自用的小玩意儿,不需要的禁用
[task_local]
0 8 * * * https://raw.githubusercontent.com/passerby-b/JDDJ/main/weather.js
[Script]
cron "0 8 * * *" script-path=https://raw.githubusercontent.com/passerby-b/JDDJ/main/weather.js,tag=今日天气
*/

console.log("天气脚本开始!");
const $ = new API();

let city = 'beijing/beijing';//环境变量WEATHERCITY

!(async () => {

    if (process.env.WEATHERCITY) city = process.env.WEATHERCITY;
    await $.http.get({ url: "https://tianqi.moji.com/weather/china/" + city }).then(async response => {
        let d = response.body;
        if (d) {
            var index = d.indexOf('description') + 22;
            var index2 = d.indexOf("keywords") - 24;

            var msg = d.substring(index, index2).replace(/ /g, "");
            //console.log(msg);

            var icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w0.png";
            if (msg.indexOf("多云") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w1.png";
            if (msg.indexOf("阴") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w2.png";
            if (msg.indexOf("雨") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w8.png";
            if (msg.indexOf("阵雨") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w3.png";
            if (msg.indexOf("雷") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w4.png";
            if (msg.indexOf("雨夹雪") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w6.png";
            if (msg.indexOf("小雨") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w7.png";
            if (msg.indexOf("中雨") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w8.png";
            if (msg.indexOf("大雨") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w9.png";
            if (msg.indexOf("暴雨") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w10.png";
            if (msg.indexOf("雪") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w15.png";
            if (msg.indexOf("小雪") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w14.png";
            if (msg.indexOf("中雪") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w15.png";
            if (msg.indexOf("大雪") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w16.png";
            if (msg.indexOf("暴雪") > -1) icon = "https://h5tq.moji.com/tianqi/assets/images/weather/w17.png";

            if ($.env.isNode) {
                const sendMsg = require('./sendNotify');
                const cheerio = require('cheerio');

                let html = cheerio.load(d);
                let ul = html('.forecast.clearfix>ul:eq(1)');
                let li1 = html(ul).find('li:eq(1)').text().replace(/\n/g, '').replace(/ /g, '');
                let li2 = html(ul).find('li:eq(2)').text().replace(/\n/g, '').replace(/ /g, '');
                let li3 = html(ul).find('li:eq(3)').text().replace(/\n/g, '').replace(/ /g, '');
                let li4 = html(ul).find('li:eq(4)').text().replace(/\n/g, '').replace(/ /g, '');
                let tomorrow = '\n明日天气: ' + li1 + ' ' + li2 + ' ' + li3 + ' 空气' + li4;

                await sendMsg.sendNotify('今日天气', msg + tomorrow);
            }

            msg = msg.split('。');
            if (msg.length > 0) {
                $.notify(msg[0], msg[1], msg[2], { "url": "https://tianqi.moji.com/weather/china/" + city, "img": icon });
            }
            else {
                $.notify("错误", "错误", d.substring(index, index2).replace(/ /g, ""));
            }
        }
        else {
            $.notify("返回空", "错误", d);
        }

    });

    console.log("执行完成!!!!");
    $.done();
})().catch(async (e) => {
    console.log('', '❌失败! 原因:' + e + '!', '');
}).finally(() => {
    $.done();
});



/*********************************** API *************************************/
function ENV() { const e = "undefined" != typeof $task, t = "undefined" != typeof $loon, s = "undefined" != typeof $httpClient && !t, i = "function" == typeof require && "undefined" != typeof $jsbox; return { isQX: e, isLoon: t, isSurge: s, isNode: "function" == typeof require && !i, isJSBox: i, isRequest: "undefined" != typeof $request, isScriptable: "undefined" != typeof importModule } } function HTTP(e = { baseURL: "" }) { const { isQX: t, isLoon: s, isSurge: i, isScriptable: n, isNode: o } = ENV(), r = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)/; const u = {}; return ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"].forEach(l => u[l.toLowerCase()] = (u => (function (u, l) { l = "string" == typeof l ? { url: l } : l; const h = e.baseURL; h && !r.test(l.url || "") && (l.url = h ? h + l.url : l.url); const a = (l = { ...e, ...l }).timeout, c = { onRequest: () => { }, onResponse: e => e, onTimeout: () => { }, ...l.events }; let f, d; if (c.onRequest(u, l), t) f = $task.fetch({ method: u, ...l }); else if (s || i || o) f = new Promise((e, t) => { (o ? require("request") : $httpClient)[u.toLowerCase()](l, (s, i, n) => { s ? t(s) : e({ statusCode: i.status || i.statusCode, headers: i.headers, body: n }) }) }); else if (n) { const e = new Request(l.url); e.method = u, e.headers = l.headers, e.body = l.body, f = new Promise((t, s) => { e.loadString().then(s => { t({ statusCode: e.response.statusCode, headers: e.response.headers, body: s }) }).catch(e => s(e)) }) } const p = a ? new Promise((e, t) => { d = setTimeout(() => (c.onTimeout(), t(`${u} URL: ${l.url} exceeds the timeout ${a} ms`)), a) }) : null; return (p ? Promise.race([p, f]).then(e => (clearTimeout(d), e)) : f).then(e => c.onResponse(e)) })(l, u))), u } function API(e = "untitled", t = !1) { const { isQX: s, isLoon: i, isSurge: n, isNode: o, isJSBox: r, isScriptable: u } = ENV(); return new class { constructor(e, t) { this.name = e, this.debug = t, this.http = HTTP(), this.env = ENV(), this.node = (() => { if (o) { return { fs: require("fs") } } return null })(), this.initCache(); Promise.prototype.delay = function (e) { return this.then(function (t) { return ((e, t) => new Promise(function (s) { setTimeout(s.bind(null, t), e) }))(e, t) }) } } initCache() { if (s && (this.cache = JSON.parse($prefs.valueForKey(this.name) || "{}")), (i || n) && (this.cache = JSON.parse($persistentStore.read(this.name) || "{}")), o) { let e = "root.json"; this.node.fs.existsSync(e) || this.node.fs.writeFileSync(e, JSON.stringify({}), { flag: "wx" }, e => console.log(e)), this.root = {}, e = `${this.name}.json`, this.node.fs.existsSync(e) ? this.cache = JSON.parse(this.node.fs.readFileSync(`${this.name}.json`)) : (this.node.fs.writeFileSync(e, JSON.stringify({}), { flag: "wx" }, e => console.log(e)), this.cache = {}) } } persistCache() { const e = JSON.stringify(this.cache, null, 2); s && $prefs.setValueForKey(e, this.name), (i || n) && $persistentStore.write(e, this.name), o && (this.node.fs.writeFileSync(`${this.name}.json`, e, { flag: "w" }, e => console.log(e)), this.node.fs.writeFileSync("root.json", JSON.stringify(this.root, null, 2), { flag: "w" }, e => console.log(e))) } write(e, t) { if (this.log(`SET ${t}`), -1 !== t.indexOf("#")) { if (t = t.substr(1), n || i) return $persistentStore.write(e, t); if (s) return $prefs.setValueForKey(e, t); o && (this.root[t] = e) } else this.cache[t] = e; this.persistCache() } read(e) { return this.log(`READ ${e}`), -1 === e.indexOf("#") ? this.cache[e] : (e = e.substr(1), n || i ? $persistentStore.read(e) : s ? $prefs.valueForKey(e) : o ? this.root[e] : void 0) } delete(e) { if (this.log(`DELETE ${e}`), -1 !== e.indexOf("#")) { if (e = e.substr(1), n || i) return $persistentStore.write(null, e); if (s) return $prefs.removeValueForKey(e); o && delete this.root[e] } else delete this.cache[e]; this.persistCache() } notify(e, t = "", l = "", h = {}) { const a = h["open-url"], c = h["media-url"]; if (s && $notify(e, t, l, h), n && $notification.post(e, t, l + `${c ? "\n多媒体:" + c : ""}`, { url: a }), i) { let s = {}; a && (s.openUrl = a), c && (s.mediaUrl = c), "{}" === JSON.stringify(s) ? $notification.post(e, t, l) : $notification.post(e, t, l, s) } if (o || u) { const s = l + (a ? `\n点击跳转: ${a}` : "") + (c ? `\n多媒体: ${c}` : ""); if (r) { require("push").schedule({ title: e, body: (t ? t + "\n" : "") + s }) } else console.log(`${e}\n${t}\n${s}\n\n`) } } log(e) { this.debug && console.log(`[${this.name}] LOG: ${this.stringify(e)}`) } info(e) { console.log(`[${this.name}] INFO: ${this.stringify(e)}`) } error(e) { console.log(`[${this.name}] ERROR: ${this.stringify(e)}`) } wait(e) { return new Promise(t => setTimeout(t, e)) } done(e = {}) { console.log('done!'); s || i || n ? $done(e) : o && !r && "undefined" != typeof $context && ($context.headers = e.headers, $context.statusCode = e.statusCode, $context.body = e.body) } stringify(e) { if ("string" == typeof e || e instanceof String) return e; try { return JSON.stringify(e, null, 2) } catch (e) { return "[object Object]" } } }(e, t) }
/*****************************************************************************/
