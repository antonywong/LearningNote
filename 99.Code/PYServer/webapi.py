# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from flask_cors import CORS
import option, option.qmt_collecter
import arbitrage._05.qmt

app = Flask(__name__)
CORS(app)  # 允许跨域


@app.route('/', methods=['GET'])
def health_check():
    """服务健康检查接口"""
    return jsonify({"status": "ok", "version": "1.0.0"})


@app.route('/v1/api/option/code', methods=['GET'])
def get_option_code():
    """获取期权合约代码"""
    return jsonify(option.get_option_code(request.args.get('underlying'), request.args.get('expire_month'))), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/v1/api/tick/qmt', methods=['POST'])
def qmt_collecter():
    """接收tick数据-qmt"""
    return jsonify(option.qmt_collecter.post_tick(request.get_json())), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/v1/api/_05/qmt', methods=['POST'])
def qmt_05():
    """delta中性套利-qmt"""
    return jsonify(arbitrage._05.qmt.run(request.get_json())), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)