# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:08
from flask import jsonify
from . import user_bp
from flask_restful import Resource

@user_bp.route('/')
def index():
    return jsonify(u"这是首页")


from flask_restful import Api
user_api = Api(user_bp)


class User(Resource):
    def get(self, id):
        return 'hello {}!'.format(id)

    def delete(self,id):
        return jsonify(u"删除成功")


user_api.add_resource(User, '/hello/<string:id>')