# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:19
from flask import jsonify
from . import post_bp
@post_bp.route('/')
def index():
    return jsonify(u"这是post首页")