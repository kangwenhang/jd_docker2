//云函数入口,需要运行什么脚本自己改名字
exports.main_handler = async (event, context, callback) => {
  try {
    delete require.cache[require.resolve('./jddj_fruit.js')];
    require('./jddj_fruit.js');
  } catch (e) {
    console.error(e)
  }
}
