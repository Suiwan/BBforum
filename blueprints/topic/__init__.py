# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:24
from flask import Blueprint
topic_bp = Blueprint("topic",__name__,url_prefix='/topic')
from . import view