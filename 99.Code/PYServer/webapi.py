# -*- coding: utf-8 -*-

from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import option
import arbitrage._04.echarts
from strategy.qmt import bp as qmt_webapi_bp

app = Flask(__name__)
CORS(app)  # 允许跨域


# 注册蓝本
app.register_blueprint(qmt_webapi_bp)


@app.route('/', methods=['GET'])
def health_check():
    """服务健康检查接口"""
    return jsonify({"status": "ok", "version": "1.0.0"})


@app.route('/v1/api/tick', methods=['POST'])
def post_tick():
    """接收tick数据-qmt"""
    req = request.get_json()
    time = datetime.strptime(req["time"], "%Y-%m-%dT%H:%M:%S")
    underlying_price = float(req["underlying_price"])
    return jsonify(option.save_tick(time, req["underlying"], underlying_price, req["expire_month"], req["data"])), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/v1/api/_04/echarts', methods=['GET'])
def echarts_04():
    """VI监测-echarts"""
    return jsonify(arbitrage._04.echarts.fetch(request.args.get('underlying'))), 200, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5000, debug=True)