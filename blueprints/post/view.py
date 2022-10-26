# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:19
from flask import jsonify
from . import post_bp
from flask_restful import Resource,Api,marshal_with,fields
from models import PostModel

@post_bp.route('/')
def index():
    return jsonify(u"这是post首页")


# 注册topic api
topic_api = Api(post_bp)

# 单个话题CURD
class PostView(Resource):
    def get(self, id):
        return jsonify(u"帖子查看成功")

    def delete(self,id):
        return jsonify(u"帖子删除成功")


class PostsView(Resource):
    def get(self):
        return jsonify(u"这是一个帖子集合")


topic_api.add_resource(PostView, '/<int:id>')
topic_api.add_resource(PostsView,'/')