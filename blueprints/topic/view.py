# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:25
import datetime
from datetime import timezone
from flask import jsonify
from . import topic_bp
from flask_restful import Resource,Api,marshal_with,fields,request
from models import TopicModel,model_to_dict
from app.extensions import db


@topic_bp.route('/posts/<int:topic_id>',methods=['GET'])
def get_posts(topic_id):
    topic = TopicModel.query.filter_by(id=topic_id).first()
    posts = model_to_dict(topic.posts)
    return posts


# 注册topic api
topic_api = Api(topic_bp)


# CURD
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
        return jsonify({'code':200,
                        'msg':"delete success"
                        })

    def put(self,id):
        data = request.get_json()
        data['update_time'] = datetime.datetime.now()
        post = TopicModel.query.filter_by(id=id)
        post.update(data)
        db.session.commit()
        return jsonify({
            'code':200,
            'msg':'update success'
        })


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

    def post(self):
        data = request.get_json()
        theme = data['theme']
        description = data['description']
        type_id = data['type_id']
        img_urls = data['img_urls']
        video_urls = data['video_urls']
        author_id = data['author_id']
        topic = TopicModel(theme=theme,description=description,type_id=type_id,img_urls=img_urls,video_urls=video_urls,author_id=author_id)
        db.session.add(topic)
        db.session.commit()
        return jsonify({
            'msg': 'add success',
            'code': 200
        })


topic_api.add_resource(TopicView, '/<int:id>')
topic_api.add_resource(TopicsView,'/')