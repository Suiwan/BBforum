# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:08

from flask import jsonify,request
from . import user_bp
from flask_restful import Resource,marshal_with,fields,Api
from models import UserModel
from models import UserModel,LikesModel
from flask_login import login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash


@user_bp.route('/')
def index():
    return jsonify(u"这是首页")


@user_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return jsonify("您已登录，返回首页")
    if request.method == 'GET':
        return jsonify("登录页面")
    else:
        account = request.json.get('account')
        pwd = request.json.get('password')
        user = UserModel.query.filter_by(id=account).first()
        if user:
            if check_password_hash(user.password,pwd):
                login_user(user)
                return jsonify({'code':200,
                                'token':123456,
                                'msg':'login success'})
            else:
                return jsonify({
                    'code':601,
                    'msg':'wrong password'
                })
        else:
            return jsonify({
                'code':602,
                'msg':"user not exist"
            })


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({
        'code':200,
        'msg':'logout sucess'
    })


@user_bp.route('/like',methods=['POST'])
@login_required
def like():
    post_id = request.get_json()['post_id']
    if not current_user.is_liking(post_id):
        current_user.like(post_id)
        return jsonify({
            'code':200,
            'msg':'success'
        })
    return jsonify({
        'code':601,
        'msg':'Already liked!'
    })


@user_bp.route('/unlike',methods=['POST'])
@login_required
def unlike():
    post_id = request.get_json()['post_id']
    if  current_user.is_liking(post_id):
        current_user.unlike(post_id)
        return jsonify({
            'code':200,
            'msg':'success'
        })
    return jsonify({
        'code':601,
        'msg':'Have not liked yet!'
    })

@user_bp.route('/subscribe',methods=['POST'])
@login_required
def subscribe():
    topic_id = request.get_json()['topic_id']
    if not current_user.is_subscribing(topic_id):
        current_user.subscribe(topic_id)
        return jsonify({
            'code':200,
            'msg':'success'
        })
    return jsonify({
        'code':601,
        'msg':'Already subscribed!'
    })


@user_bp.route('/unsubscribe',methods=['POST'])
@login_required
def unsubscribe():
    topic_id = request.get_json()['topic_id']
    if  current_user.is_subscribing(topic_id):
        current_user.unsubscribe(topic_id)
        return jsonify({
            'code':200,
            'msg':'success'
        })
    return jsonify({
        'code':601,
        'msg':'Have not liked yet!'
    })



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

    def delete(self,id):
        return jsonify(u"删除成功")



user_api.add_resource(UserView, '/user/<int:id>')
