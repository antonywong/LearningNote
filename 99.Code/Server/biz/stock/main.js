var dal = require('../../dal/main');
var http = require("http");
var iconv = require('iconv-lite');

module.exports = {
    getStocks: (req, res) => {
        var db = new dal();
        var userId = req.query.userId;
        var sql = "select * from MyStock where fkUserID=" + userId + " order by code";
        db.query(sql)
            .then((rows) => {
                res.send(rows);
                res.end();
            })
            .catch((err) => { res.send(err); res.end(); })
            .finally(() => { db.close(); });
    },
    getStockPrice: (req, res) => {
        getStockInfo(req.query.code).then((json) => {
            res.send(json);
            res.end();
        });
    },
    addStock: (req, res) => {
        var code = req.body.code;
        getStockInfo(code).then((json) => {
            if (json) {
                var db = new dal();
                var sql = "INSERT INTO MyStock (fkUserId,code,name) VALUES ('" + req.body.userId + "','" + code + "','" + json.name + "')";
                db.run(sql)
                    .then(() => { res.end(); })
                    .catch((err) => { res.send(err); res.end(); })
                    .finally(() => { db.close(); });
            }
            res.end();
        });
    },
    deleteStock: (req, res) => {
        var db = new dal();
        var sql = "delete from MyStock where id=" + req.query.id;
        db.query(sql)
            .then((rows) => {
                res.send(rows);
                res.end();
            })
            .catch((err) => { res.send(err); res.end(); })
            .finally(() => { db.close(); });
    },
    postQuantity: (req, res) => {
        save(res, "quantity", req.body.quantity, req.body.id);
    },
    postShareRate: (req, res) => {
        save(res, "shareRate", req.body.shareRate, req.body.id);
    },
    postLeverage: (req, res) => {
        save(res, "leverage", req.body.leverage, req.body.id);
    },
    postLock: (req, res) => {
        save(res, "isLock", req.query.isLock, req.query.id);
    },
};
var save = (res, column, value, id) => {
    var db = new dal();
    var sql = "update MyStock set " + column + "=" + value + " where id=" + id;
    db.run(sql)
        .then(() => { res.end(); })
        .catch((err) => { res.send(err); res.end(); })
        .finally(() => { db.close(); });
};
var getStockInfo = (code) => {
    return new Promise((resolve, reject) => {
        http.get('http://hq.sinajs.cn/?format=json&list=' + code, (text) => {
            var chunks = [];
            text.on("data", function (chunk) {
                chunks.push(chunk);
            })
            text.on("end", () => {
                var text = iconv.decode(Buffer.concat(chunks), 'gbk');
                var info = text.split('=');
                if (info.length > 1 && info[1] != "null") {
                    info = info[1].split(',');
                    resolve({ code: code, name: info[0], price: info[3] });
                }
                reject();
            })
        });
    });
};