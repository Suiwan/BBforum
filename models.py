# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 16:20
from flask_sqlalchemy.model import Model

from app.extensions import db
from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import ForeignKey

TypeId = {
    1:"课程答疑",
    2:"资源共享",
    3:"评价反馈",
    4:"作业讨论"
}

# flask-login实现登录需要User类继承UserMixin
# class User(UserMixin):
#     def __init__(self, user):
#         self.password = user.password
#         self.id = user.id
#         self.username = user.username
#         self.role_id = user.role_id
#
#     def get(user_id):
#         """根据用户ID获取用户实体，为 login_user 方法提供支持"""
#         if not user_id:
#             return None
#         user = User.query.filter_by(id=user_id).first()
#         if user:
#             return User(user)
#         return None
#
#     def has_role(self, role_name):
#         role = Role.query.filter_by(id=self.role_id).first()
#         if role.name == role_name:
#             return True
#         else:
#             return False
#
#
# class AnonymousUser(AnonymousUserMixin):
#     def has_role(self, role_name):
#         return False


class UserModel(db.Model,UserMixin):
    __tablename__ = "user"
    id = db.Column(db.String(200), primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    # relationships
    roles = db.relationship('Role', backref=db.backref('users', lazy='dynamic'))# 身份权限
    posts = db.relationship('PostModel', backref='author',cascade="all,delete") # 发布的帖子
    topics = db.relationship('TopicModel', backref='author',cascade="all,delete")# 建立的话题
    responses = db.relationship('ResponseModel', backref='author',cascade="all,delete")# 回复
    # subscriptions = db.relationship('SubscriptionsModel',backref=db.backref('user', lazy='dynamic'),cascade="all,delete")
    # likes = db.relationship('LikesModel', backref=db.backref('user', lazy='dynamic'), cascade="all,delete")  # 点赞的帖子
    likes = db.relationship('LikesModel', backref='user', cascade="all,delete",lazy='dynamic')
    subscriptions = db.relationship('SubscriptionsModel', backref='user', cascade="all,delete",lazy='dynamic')
    notifications = db.relationship('Notification',backref='receiver',cascade="all,delete")



    def __repr__(self):
        return " %s" % self.username

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

    def subscribe(self,topic_id):
        if not self.is_subscribing(topic_id):
            sub = SubscriptionsModel(u_id = self.id,t_id = topic_id)
            db.session.add(sub)
            db.session.commit()
        return self.is_subscribing(topic_id)

    def unsubscribe(self,topic_id):
        if self.is_subscribing(topic_id):
            sub = self.subscriptions.filter_by(t_id = topic_id).first()
            db.session.delete(sub)
            db.session.commit()

    def is_subscribing(self,topic_id):
        return self.subscriptions.filter_by(t_id = topic_id).first() is not None

    def like(self,post_id):
        if not self.is_liking(post_id):
            like = LikesModel(u_id=self.id, p_id=post_id)
            db.session.add(like)
            db.session.commit()
        return self.is_liking(post_id)

    def unlike(self,post_id):
        if  self.is_liking(post_id):
            like = self.likes.filter_by(p_id = post_id).first()
            db.session.delete(like)
            db.session.commit()

    def is_liking(self,post_id):
        return self.likes.filter_by(p_id = post_id).first() is not None


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer(), primary_key=True)
    description = db.Column(db.String(255))


class TopicModel(db.Model):
    __tablename__ = "topic"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    theme = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    type_id = db.Column(db.Integer, nullable=False)
    img_urls = db.Column(db.String(200))# split: /
    video_urls = db.Column(db.String(200))# split: /
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)

    # ForeignKeys:
    author_id = db.Column(db.String(200),db.ForeignKey('user.id'),nullable=False)

    # relationships:
    posts = db.relationship('PostModel',backref='topic',cascade="all,delete")

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class PostModel(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now)
    img_urls = db.Column(db.String(200)) # split: /
    video_urls = db.Column(db.String(200))# split: /
    # ForeignKeys:
    author_id = db.Column(db.String(200), db.ForeignKey('user.id'), nullable=False)
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'), nullable=False)

    # relationships:
    responses = db.relationship('ResponseModel',backref='post',cascade="all,delete")

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class ResponseModel(db.Model):
    __tablename__ = "response"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(511), nullable=False)
    creat_time = db.Column(db.DateTime, default=datetime.now)
    img_url = db.Column(db.String(200), primary_key=True)


    # ForeignKeys:
    author_id = db.Column(db.String(200), db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'), nullable=False)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class LikesModel(db.Model):
    __tablename__="likes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    like_time =db.Column(db.DateTime, default=datetime.now)
    # ForeignKeys:
    u_id = db.Column(db.String(200), ForeignKey("user.id", ondelete="CASCADE"))
    p_id = db.Column(db.Integer, ForeignKey("post.id", ondelete="CASCADE"))
    # relationships
    post = db.relationship("PostModel",backref='user_liked') # `这条点赞对应的帖子('user_likes'代表给这个帖子点赞了的所有人)


class SubscriptionsModel(db.Model):
    __tablename__="subscription"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscribe_time =db.Column(db.DateTime, default=datetime.now)
    # ForeignKeys:
    u_id = db.Column(db.String(200), ForeignKey("user.id", ondelete="CASCADE"))
    t_id = db.Column(db.Integer, ForeignKey("topic.id", ondelete="CASCADE"))

    # relationships
    topic = db.relationship("TopicModel",backref='user_subscribed') # `这条关注对应的话题('user_subscribed'代表关注话题的所有人)


def model_to_dict(result):
    from collections import Iterable
    try:
        if isinstance(result, Iterable):
            tmp = [dict(zip(res.__dict__.keys(), res.__dict__.values())) for res in result]
            for t in tmp:
                t.pop('_sa_instance_state')
        else:
            tmp = dict(zip(result.__dict__.keys(), result.__dict__.values()))
            tmp.pop('_sa_instance_state')
        return tmp
    except BaseException as e:
        print(e.args)
        raise TypeError('Type error of parameter')


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    target_id = db.Column(db.Integer)
    type = db.Column(db.Integer)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime,default = datetime.utcnow,index=True)

    # Foreign Key
    receiver_id = db.Column(db.String(200), ForeignKey("user.id", ondelete="CASCADE"))


from datetime import datetime as cdatetime #有时候会返回datatime类型
from datetime import date,time
from sqlalchemy import DateTime,Numeric,Date,Time #有时又是DateTime



def queryToDict(models):
    if(isinstance(models,list)):
        if(isinstance(models[0],Model)):
            lst = []
            for model in models:
                gen = model_2_dict(model)
                dit = dict((g[0],g[1]) for g in gen)
                lst.append(dit)
            return lst
        else:
            res = result_to_dict(models)
            return res
    else:
        if (isinstance(models, Model)):
            gen = model_to_dict(models)
            dit = dict((g[0],g[1]) for g in gen)
            return dit
        else:
            res = dict(zip(models.keys(), models))
            find_datetime(res)
            return res


#当结果为result对象列表时，result有key()方法
def result_to_dict(results):
    res = [dict(zip(r.keys(), r)) for r in results]
    #这里r为一个字典，对象传递直接改变字典属性
    for r in res:
        find_datetime(r)
    return res


def model_2_dict(model):
    for col in model.__table__.columns:
        if isinstance(col.type, DateTime):
            value = convert_datetime(getattr(model, col.name))
        elif isinstance(col.type, Numeric):
            value = float(getattr(model, col.name))
        else:
            value = getattr(model, col.name)
        yield (col.name, value)


def find_datetime(value):
    for v in value:
        if (isinstance(value[v], cdatetime)):
            value[v] = convert_datetime(value[v])   #这里原理类似，修改的字典对象，不用返回即可修改


def convert_datetime(value):
    if value:
        if(isinstance(value,(cdatetime,DateTime))):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        elif(isinstance(value,(date,Date))):
            return value.strftime("%Y-%m-%d")
        elif(isinstance(value,(Time,time))):
            return value.strftime("%H:%M:%S")
    else:
        return ""