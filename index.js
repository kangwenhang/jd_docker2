//'use strict';
exports.main_handler = async (event, context, callback) => {
    try {
        const SOURCE_URL = process.env
        for (const v of event["Message"].split("&")) {
            console.log(v);
            if (SOURCE_URL) { //不允许直链!!!不允许直链!!!不允许直链!!!
                const request = require('request')
                request(`${SOURCE_URL}${v}.js`, function(error, response, body) {
                    eval(response.body)
                })
            } else {
                delete require.cache[require.resolve('./' + v + '.js')];
                require('./' + v + '.js')
            }
        }
    } catch (e) {
        console.error(e)
    }
}