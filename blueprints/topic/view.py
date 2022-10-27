# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:25
from flask import jsonify
from . import topic_bp
from flask_restful import Resource,Api,marshal_with,fields
from models import TopicModel
from app.extensions import db
# @topic_bp.route('/')
# def index():
#     return jsonify(u"这是topic首页")


# 注册topic api
topic_api = Api(topic_bp)

# 单个话题CURD
class TopicView(Resource):
    resource_fields = {
        'id':fields.Integer,
        'theme': fields.String,
        'description':fields.String,
        'type_id': fields.Integer,
        'create_time':fields.DateTime,
        'update_time':fields.DateTime,
        'img_urls':fields.String,
        'video_urls':fields.String,
        'author_id':fields.String
    }

    @marshal_with(resource_fields)
    def get(self, id):
        topic = TopicModel.query.get(id)
        # author = topic.author
        return topic

    def delete(self,id):
        topic = TopicModel.query.get(id)
        db.session.delete(topic)
        db.session.commit()
        return jsonify(u"话题删除成功")



class TopicsView(Resource):
    resource_fields = {
        'id':fields.Integer,
        'theme': fields.String,
        'description':fields.String,
        'type_id': fields.Integer,
        'create_time':fields.DateTime,
        'update_time':fields.DateTime,
        'img_urls':fields.String,
        'video_urls':fields.String,
        'author_id':fields.String
    }


    @marshal_with(resource_fields)
    def get(self):
        topics = TopicModel.query.all()
        return topics


topic_api.add_resource(TopicView, '/<int:id>')
topic_api.add_resource(TopicsView,'/')