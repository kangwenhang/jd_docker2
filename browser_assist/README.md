# 这里是一些用于B站的浏览器辅助脚本

脚本需要以一下方式执行
浏览器打开B站指定页面--》按F12打开开发者工具--》console--》粘贴脚本，回车

* 所有过期抽奖动态删除
    *  适用页面为 B站主页--》右上角"动态"--》左边头像下方"动态"(`https://space.bilibili.com/xxxxxx/dynamic`)
    *  脚本内容如下
          *  `(function(){if(!window.location.href.match(/https:\/\/space.bilibili.com\/[0-9]*\/dynamic.*/g)){console.log("本脚本只能在B站个人动态页面执行！");return}var i=0;function dellott(){var a=$("span.dynamic-link-hover-bg").eq(i);if(a.length==0){$(document).scrollTop($(document).height()-$(window).height());setTimeout(function(){dellott()},1500);return}var ids=a.attr("click-href").match(/.*business_id=([0-9]*)&.*/);if(ids){var bid=ids[1]}else{setTimeout(function(){i++;dellott()},500);return}$.get("https://api.vc.bilibili.com/lottery_svr/v1/lottery_svr/lottery_notice",{"dynamic_id":bid},function(data){if("lottery_result" in data["data"]){a.parents("div.card").find(".child-button")[1].click();setTimeout(function(){$(".bp-popup-ctnr").find(".bl-button--size")[0].click();dellott()},1000)}else{i++;dellott()}})}dellott()})();`

* B站专栏不可复制破解
    *  适用页面为 所有不可复制的专栏
    *  脚本内容如下
          *  `(function(){var a=document.querySelector("div.article-holder");a.classList.remove("unable-reprint");a.addEventListener("copy",function(e){e.clipboardData.setData("text",window.getSelection().toString())})})();`

* 清空所有动态
    *  适用页面为 B站主页--》右上角"动态"--》左边头像下方"动态"(`https://space.bilibili.com/xxxxxx/dynamic`)
    *  脚本内容如下
          *  `setInterval(function(){$(".child-button")[1].click();$(".bp-popup-ctnr").find(".bl-button--size")[0].click();},500);`

* 删除关注的up主(慎用)
    *  适用页面为 B站主页--》点击头像--》右边"关注数"(`https://space.bilibili.com/xxxxxx/fans/follow`)
    *  脚本内容如下(一次只能删除一页)
          *  `$(".be-dropdown-item:contains('取消关注')").click()`

* 删除互粉的粉丝(慎用)
    *  适用页面为 B站主页--》点击头像--》右边"粉丝数"(`https://space.bilibili.com/xxxxxx/fans/fans`)
    *  脚本内容如下(一次只能删除一页)
          *  `$(".be-dropdown-item:contains('取消关注')").click()`
