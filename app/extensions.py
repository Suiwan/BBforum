# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 16:09
import math

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()
cors = CORS()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id): # 调用current_user时会调用load_user，若已经登录会返回user实例，否则返回内置的AnonymousUserMixin对象
    from models import UserModel
    user = UserModel.query.filter_by(id=user_id).first()
    return user


def pagination(page_num,totals):
    ret = {"prev_page": page_num - 1,  # 上一页
           "next_page": page_num + 1,  # 下一页
           "current_page": 0,          # 当前页
           "total_pages": 0,           # 总页数
           "max_page": 0,              # 最大页
           "page_size": 10,            # 每页数据条数
           "totals": totals,           # 数据总条数
           "offset": 0,                # 偏移量
           "page_range": None          # 页码范围
           }

    ret["total_pages"] = math.ceil(totals / ret["page_size"])
    ret["max_page"] = ret["total_pages"]


    if page_num <= 1:
        page_num = 1
        ret["prev_page"] = 1
    if page_num >= ret["max_page"]:
        page_num = ret["max_page"]
        ret["next_page"] = ret["max_page"]

    ret["current_page"] = page_num

    if totals == 0:
        ret["offset"] = 0
    else:
        ret["offset"] = (ret["current_page"] - 1) * ret["page_size"]

    page_range = []
    for i in range(1,ret["max_page"]+1):
        page_range.append(i)
    ret["page_range"] = page_range

    return ret
