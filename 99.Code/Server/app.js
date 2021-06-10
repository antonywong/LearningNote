var express = require('express');
var bodyParser = require('body-parser');

var app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

//设置允许跨域访问该服务.
app.all('*', function (req, res, next) {
  res.header('Access-Control-Allow-Origin', '*');
  //Access-Control-Allow-Headers ,可根据浏览器的F12查看,把对应的粘贴在这里就行
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  res.header('Access-Control-Allow-Methods', '*');
  res.header('Content-Type', 'application/json;charset=utf-8');
  next();
});

var bizUser = require('./biz/user/main');
app.post('/signin', bizUser.singin);
app.post('/amount', bizUser.postAmount);

var bizStock = require('./biz/stock/main');
var bizStockK_day = require('./biz/stock/k_day');
var bizStock_HighLow = require('./biz/stock/high_low');
app.get('/stocks', bizStock.getStocks);
app.get('/stockPrice', bizStock.getStockPrice);
app.post('/stock', bizStock.addStock);
app.delete('/stock', bizStock.deleteStock);
app.post('/quantity', bizStock.postQuantity);
app.post('/shareRate', bizStock.postShareRate);
app.post('/leverage', bizStock.postLeverage);
app.post('/lock', bizStock.postLock);

var server = app.listen(8081, function (a) {
  console.log(process.argv);
  var host = server.address().address
  var port = server.address().port
  console.log("应用实例，访问地址为 http://%s:%s\n\n", host, port)

  // bizStockK_day.batchK_Day();
  // bizStock_HighLow.batchStockDays();
})
