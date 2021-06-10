var dal = require('../../dal/main');
var http = require("http");
var iconv = require('iconv-lite');
var highLow = require('./high_low');

module.exports = {
    batchK_Day: () => {
        var db = new dal();
        var sql = "SELECT *,(SELECT day FROM StockK_Day kd WHERE kd.code=s.code ORDER BY day DESC LIMIT 1 OFFSET 0) AS lastK FROM Stock s ORDER BY updateDate";
        db.query(sql)
            .then((rows) => {
                console.log(rows.length);
                Stocks = rows;
                HTTPInterval = setInterval(getStockDays, 1800);
            })
            .catch((err) => { })
            .finally(() => { db.close(); });
    },
};

var HTTPInterval;
var HTTPEnd = false;
var Stocks;
var StockIndex = 0;
var KSQL = [];
var getStockDays = (code) => {
    if(!code) {
        code = Stocks[StockIndex].code;
    }

    var lastK = new Date(Stocks[StockIndex].lastK);
    var today = new Date();
    var days = parseInt((today - lastK + 1000 * 60 * 60 * 8) / 1000 / 60 / 60 / 24) + 1;
    var url = 'http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=' + code + '&scale=240&ma=1&datalen=' + days.toString();
    http.get(url, (text) => {
        var chunks = [];
        text.on("data", function (chunk) {
            chunks.push(chunk);
        })
        text.on("end", () => {
            var text = iconv.decode(Buffer.concat(chunks), 'gbk');
            var kLines = eval(text);

            for (var i = 0; i < kLines.length; i++) {
                if(new Date(kLines[i].day) > lastK) {
                    KSQL.push({ code: code, day: kLines[i].day, open: kLines[i].open, high: kLines[i].high, low: kLines[i].low, close: kLines[i].close, volume: kLines[i].volume});
                }
            }

            if(!isInserting) { insert(); }
        })
    });

    if (StockIndex >= Stocks.length - 1){
        clearInterval(HTTPInterval);
        HTTPEnd = true;
        console.log("最新数据下载完成！");
    } else {
        StockIndex++;
    }
};

var isInserting = false;
var insert = () => {
    console.log(isInserting.toString() + "----" + KSQL.length.toString());
    if(KSQL.length == 0) {
        if(HTTPEnd){
            highLow.batchStockDays();
        }
        isInserting = false;
        return; 
    }

    isInserting = true;
    var sql = "INSERT INTO StockK_Day (code,day,open,high,low,close,volume) VALUES ('"+KSQL[0].code+"','"+KSQL[0].day+"',"+KSQL[0].open+","+KSQL[0].high+","+KSQL[0].low+","+KSQL[0].close+","+KSQL[0].volume+")";
    KSQL.shift();

    for (var i = 0; i < 99; i++) {
        if(KSQL.length == 0) { break; }

        sql += ",('"+KSQL[0].code+"','"+KSQL[0].day+"',"+KSQL[0].open+","+KSQL[0].high+","+KSQL[0].low+","+KSQL[0].close+","+KSQL[0].volume+")";
        KSQL.shift();
    }
    sql += ";";

    var db = new dal();
    db.run(sql)
        .then(() => { insert(); })
        .catch((err) => { console.log(err); })
        .finally(() => { db.close(); });
};
