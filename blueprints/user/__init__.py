# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:07
from flask import Blueprint
user_bp = Blueprint("user", __name__, url_prefix="/")
from . import view

