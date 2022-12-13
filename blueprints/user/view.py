# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:08

from flask import jsonify, request, Response
from sqlalchemy import func
from models import model_to_dict

from app.extensions import db
from . import user_bp
from flask_restful import Resource, marshal_with, fields, Api
from models import UserModel, Notification, PostModel, TopicModel, queryToDict, LikesModel
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


@user_bp.route('/')
def index():
    return jsonify(u"这是首页")


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({
            'code': 203,
            'msg': "Already logged in"
        })
    if request.method == 'GET':
        return jsonify("登录页面")
    else:
        account = request.json.get('account')
        pwd = request.json.get('password')
        user = UserModel.query.filter_by(id=account).first()
        if user:
            if check_password_hash(user.password, pwd):
                login_user(user)
                return jsonify({'code': 200,
                                'token': 123456,
                                'msg': 'login success'})
            else:
                return jsonify({
                    'code': 601,
                    'msg': 'wrong password'
                })
        else:
            return jsonify({
                'code': 602,
                'msg': "user not exist"
            })


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({
        'code': 200,
        'msg': 'logout sucess'
    })


@user_bp.route('/like', methods=['POST'])
@login_required
def like():
    post_id = request.get_json()['post_id']
    if not current_user.is_liking(post_id):
        current_user.like(post_id)
        user = PostModel.query.filter_by(id=post_id).first().author
        push_notification(receiver=user, target_id=post_id, type=3)
        return jsonify({
            'code': 200,
            'msg': 'success'
        })
    return jsonify({
        'code': 601,
        'msg': 'Already liked!'
    })


@user_bp.route('/unlike', methods=['POST'])
@login_required
def unlike():
    post_id = request.get_json()['post_id']
    if current_user.is_liking(post_id):
        current_user.unlike(post_id)
        return jsonify({
            'code': 200,
            'msg': 'success'
        })
    return jsonify({
        'code': 601,
        'msg': 'Have not liked yet!'
    })


# 需要分页吗
@user_bp.route('/subscription',methods=['GET'])
@login_required
def my_subscription():
    data = list(map(lambda x: x.topic,current_user.subscriptions.all()))
    return jsonify(data=queryToDict(data))



@user_bp.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    topic_id = request.get_json()['topic_id']
    if not current_user.is_subscribing(topic_id):
        current_user.subscribe(topic_id)
        return jsonify({
            'code': 200,
            'msg': 'success'
        })
    return jsonify({
        'code': 601,
        'msg': 'Already subscribed!'
    })


@user_bp.route('/unsubscribe', methods=['POST'])
@login_required
def unsubscribe():
    topic_id = request.get_json()['topic_id']
    if current_user.is_subscribing(topic_id):
        current_user.unsubscribe(topic_id)
        return jsonify({
            'code': 200,
            'msg': 'success'
        })
    return jsonify({
        'code': 601,
        'msg': 'Have not liked yet!'
    })


# type=1 -> 关注话题有新帖子, type=2 -> 发布的帖子有回复, type=3 -> 发布的帖子被点赞
def push_notification(receiver, target_id, type):
    notification = Notification(receiver=receiver, target_id=target_id, type=type)
    db.session.add(notification)
    db.session.commit()


# param:filter
# value: read | unread
# 如果后面优化时可以做分页
@user_bp.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    notifications = Notification.query.with_parent(current_user)
    filter_rule = request.args.get('filter')  # 选择查看已读还是未读
    if filter_rule == 'unread':
        notifications = notifications.filter_by(is_read=False)
    update_notifications = notifications.filter_by(type=1).order_by(Notification.timestamp.desc()).all()
    response_notifications = notifications.filter_by(type=2).order_by(Notification.timestamp.desc()).all()
    like_notifications = notifications.filter_by(type=3).order_by(Notification.timestamp.desc()).all()
    print(update_notifications if update_notifications else "empty")
    print(response_notifications)
    print(like_notifications)
    return jsonify(
        {
            "update_notifications": queryToDict(update_notifications) if update_notifications else [],
            "response_notifications": queryToDict(response_notifications) if response_notifications else [],
            "like_notifications": queryToDict(like_notifications) if like_notifications else []
        })


@user_bp.route('/notifications_count', methods=['GET'])
@login_required
def notifications_count():
    notification = Notification.query.with_parent(current_user).filter_by(is_read=False)
    update_notification_number = notification.filter_by(type=1).count()
    response_notification_number = notification.filter_by(type=2).count()
    like_notification_number = notification.filter_by(type=3).count()
    data = jsonify({
        "update_notification_number": update_notification_number,
        "response_notification_number": response_notification_number,
        "like_notification_number": like_notification_number
    })
    return data


@user_bp.route('/notification/read/<int:id>', methods=['POST'])
@login_required
def read_notification(id):
    notification = Notification.query.get(id)
    if notification:
        if notification.receiver == current_user:
            notification.is_read = True
            db.session.commit()
            return jsonify({
                "code": 200,
                'msg': "success"
            })
        else:
            return jsonify({
                "code": 403,
                'msg': "receiver incorrect"
            })
    else:
        return jsonify({
            'code': 400,
            'msg': "notification not exist"
        })


@user_bp.route('/notification/read/all', methods=['POST'])
@login_required
def read_all_notification():
    for note in current_user.notifications:
        note.is_read = True
    db.session.commit()
    return jsonify({
        "code": 200,
        'msg': "success"
    })


@user_bp.route('/test/<int:topic_id>')
def test(topic_id):
    record = TopicModel.query.filter_by(id=topic_id).first().user_subscribed
    receivers = []
    for r in record:
        receivers.append(r.user)
    print(receivers)
    return "testing"


@user_bp.route('/images/pic/<string:name>')
def get_picture(name):
    with open('static/images/'+name,'rb') as f:
        data = f.read()

        resp = Response(data,mimetype='image/jpg')
        return resp


# 获得词云图
@user_bp.route('/wordcloud/<string:name>')
def get_wordcloud(name):
    with open('static/wc/'+name,'rb') as f:
        data = f.read()

        resp = Response(data,mimetype='image/png')
        return resp


user_api = Api(user_bp)


class UserView(Resource):
    resource_fields = {
        'username': fields.String,
        'id': fields.String,
        'role_id': fields.Integer
        # 'subscriptions':fields.List,
        # 'likes':fields.List
    }

    @marshal_with(resource_fields)
    def get(self, id):
        user = UserModel.query.get(id)
        return user

    def delete(self, id):
        return jsonify(u"删除成功")


user_api.add_resource(UserView, '/user/<int:id>')
