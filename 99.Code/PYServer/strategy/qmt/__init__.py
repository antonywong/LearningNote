from flask import Blueprint, request, jsonify
from . import collecter, delta

bp = Blueprint('qmt', __name__, url_prefix='/v1/api/qmt')

@bp.route('/all_code', methods=['GET'])
def get_all_code():
    return jsonify(collecter.get_all_code()), 200, {'Content-Type': 'application/json; charset=utf-8'}

@bp.route('/option/code', methods=['GET'])
def get_option_code():
    return jsonify(collecter.get_option_code(request.args.get('underlying'), request.args.get('expire_month'))), 200, {'Content-Type': 'application/json; charset=utf-8'}
@bp.route('/option/code', methods=['POST'])
def post_option_code():
    return jsonify(collecter.post_option_code(request.get_json())), 200, {'Content-Type': 'application/json; charset=utf-8'}

@bp.route('/tick', methods=['POST'])
def post_tick():
    return jsonify(collecter.post_tick(request.get_json())), 200, {'Content-Type': 'application/json; charset=utf-8'}

@bp.route('/k_1m_time', methods=['POST'])
def get_k_1m_time():
    """接收一分钟K线-qmt"""
    return jsonify(collecter.get_k_1m_time(request.get_json())), 200, {'Content-Type': 'application/json; charset=utf-8'}
@bp.route('/k_1m', methods=['POST'])
def post_k_1m():
    """接收一分钟K线-qmt"""
    return jsonify(collecter.post_k_1m(request.get_json())), 200, {'Content-Type': 'application/json; charset=utf-8'}

@bp.route('/after_trading', methods=['POST'])
def post_after_trading():
    return jsonify(collecter.update_after_trading()), 200, {'Content-Type': 'application/json; charset=utf-8'}



@bp.route('/pre_delta', methods=['POST'])
def pre_delta():
    return jsonify(delta.pre(request.get_json())), 200, {'Content-Type': 'application/json; charset=utf-8'}

@bp.route('/delta', methods=['POST'])
def get_delta():
    """delta中性套利-qmt"""
    return jsonify(delta.run(request.get_json())), 200, {'Content-Type': 'application/json; charset=utf-8'}