# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:19
from flask import Blueprint
post_bp = Blueprint("post", __name__, url_prefix="/post")
from . import view

