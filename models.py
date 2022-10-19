# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 16:20
from app.extensions import db
from flask_login import UserMixin, AnonymousUserMixin



# flask-login实现登录需要User类继承UserMixin
class User(UserMixin):
    def __init__(self, user):
        self.password = user.password
        self.id = user.id
        self.username = user.username
        self.role_id = user.role_id

    def get(user_id):
        """根据用户ID获取用户实体，为 login_user 方法提供支持"""
        if not user_id:
            return None
        user = User.query.filter_by(id=user_id).first()
        if user:
            return User(user)
        return None

    def has_role(self, role_name):
        role = Role.query.filter_by(id=self.role_id).first()
        if role.name == role_name:
            return True
        else:
            return False


class AnonymousUser(AnonymousUserMixin):
    def has_role(self, role_name):
        return False

class User(db.Model,UserMixin):
    __tablename__ = "user"
    id = db.Column(db.String(200), primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))
    roles = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))