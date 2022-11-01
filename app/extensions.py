# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 16:09
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



