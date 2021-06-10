var dal = require('../../dal/main');
var http = require("http");
var iconv = require('iconv-lite');

module.exports = {
    batchStockDays: () => {
        var db = new dal();
        var sql = "SELECT * FROM StockK_Day order by code,day";
        db.query(sql)
            .then((rows) => {
                var lastCode = rows[0].code;
                var lastDays = [ rows[0] ];
                for (var i = 1; i < rows.length; i++) {
                    if (rows[i].code != lastCode){
                        StockDays.push({ code: lastCode, days: lastDays});
                        lastCode = rows[i].code;
                        lastDays = [ rows[i] ];
                    } else {
                        lastDays.push(rows[i])
                    }
                }
                StockDays.push({ code: lastCode, days: lastDays});
                calHighLow();
            })
            .catch((err) => { })
            .finally(() => { db.close(); });
    },
};

var StockDays = [];
var StockDaysIndex = 0;
var calHighLow = () => {
    var code = StockDays[StockDaysIndex].code;
    var days = StockDays[StockDaysIndex].days;

    var today = days[days.length - 1].day;

    var oldHighDays = 1;
    var oldHigh = parseFloat(days[days.length - 2].high);
    for (var i = 1; i < days.length; i++) {
        var day = days[days.length - 1 - i];
        if(oldHigh < parseFloat(day.high)){
            oldHighDays = i - 1;
            break;
        } else {
            continue;
        }
    }

    var highDays = 1;
    var todayHigh = parseFloat(days[days.length - 1].high);
    for (var i = 0; i < days.length; i++) {
        var day = days[days.length - 1 - i];
        if(todayHigh < parseFloat(day.high)){
            highDays = i;
            break;
        } else {
            continue;
        }
    }

    var oldLowDays = 1;
    var oldLow = parseFloat(days[days.length - 2].low);
    for (var i = 1; i < days.length; i++) {
        var day = days[days.length - 1 - i];
        if(parseFloat(day.low) < oldLow){
            oldLowDays = i - 1;
            break;
        } else {
            continue;
        }
    }

    var lowDays = 1;
    var todayLow = parseFloat(days[days.length - 1].low);
    for (var i = 0; i < days.length; i++) {
        var day = days[days.length - 1 - i];
        if(parseFloat(day.low) < todayLow){
            lowDays = i;
            break;
        } else {
            continue;
        }
    }
    console.log(code + "----" + oldHighDays + "----" + highDays + "----" + oldLowDays + "----" + lowDays)

    var db = new dal();
    var sql = "UPDATE Stock SET oldHighDays="+oldHighDays+",newHighDays="+highDays+",oldLowDays="+oldLowDays+",newLowDays="+lowDays+",updateDate='"+today+"' WHERE code='"+code+"'";
    db.run(sql).then(() => {
        if (StockDaysIndex >= StockDays.length - 1){
            console.log("高低值计算完成");
        } else {
            StockDaysIndex++;
            calHighLow();
        }
    }).catch((err) => { }).finally(() => { db.close(); });
};