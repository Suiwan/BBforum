# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:08
from flask import jsonify
from . import user_bp
from flask_restful import Resource
from models import UserModel
from models import UserModel,LikesModel
@user_bp.route('/')
def index():
    return jsonify(u"这是首页")


from flask_restful import Api
user_api = Api(user_bp)

@user_bp.route('/like')
def like():
    u_id = "123456"
    user = UserModel.query.filter_by(id=u_id).first()
    return jsonify(user.likes)



class User(Resource):
    def get(self, id):
        return 'hello {}!'.format(id)

    def delete(self,id):
        return jsonify(u"删除成功")



user_api.add_resource(User, '/hello/<string:id>')