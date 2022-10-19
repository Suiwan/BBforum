# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 15:21
from flask import Flask
from flask_migrate import Migrate

import config



def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    # 注册蓝图
    register_blueprints(app)
    # 注册扩展
    register_extensions(app)
    # 注册数据库
    register_database(app)
    return app


def register_logging(app):
    pass


def register_blueprints(app):
    from blueprints.user import user_bp
    app.register_blueprint(user_bp)
    from blueprints.post import post_bp
    app.register_blueprint(post_bp)
    from blueprints.topic import topic_bp
    app.register_blueprint(topic_bp)


def register_database(app):
    from app.extensions import db
    migrate = Migrate(app, db) # 数据库迁移
    db.init_app(app)


def register_errors(app):
    pass

def register_extensions(app):
    from app.extensions import cors
    cors.init_app(app,resources={r'/*': {'origins': '*'}})# 跨域资源请求