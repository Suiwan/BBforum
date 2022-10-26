# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:25
from flask import jsonify
from . import topic_bp
from flask_restful import Resource,Api,marshal_with,fields
from models import TopicModel
# @topic_bp.route('/')
# def index():
#     return jsonify(u"这是topic首页")


# 注册topic api
topic_api = Api(topic_bp)

# 单个话题CURD
class TopicView(Resource):
    def get(self, id):
        return jsonify(u"话题查看成功")

    def delete(self,id):
        return jsonify(u"话题删除成功")


class TopicsView(Resource):
    def get(self):
        return jsonify(u"这是一个话题组")


topic_api.add_resource(TopicView, '/<int:id>')
topic_api.add_resource(TopicsView,'/')