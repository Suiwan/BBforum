# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:25
import datetime,json
from flask import jsonify
from flask_login import login_required

from . import topic_bp
from flask_restful import Resource,Api,marshal_with,fields,request
from models import TopicModel,model_to_dict
from app.extensions import db, pagination


@topic_bp.route('/posts/<int:topic_id>',methods=['GET'])
@login_required
def get_posts_by_topic(topic_id):
    topic = TopicModel.query.filter_by(id=topic_id).first()
    posts = model_to_dict(topic.posts)
    return jsonify({
        'msg':'success',
        'code':200,
        'data':posts
    })


@topic_bp.route('/type/<int:type_id>',methods=['GET'])
@login_required
def get_posts_by_type(type_id):
    topics = TopicModel.query.filter_by(type_id=type_id).all()
    return jsonify({
        'msg':'success',
        'code':200,
        'data':model_to_dict(topics)
    })


# 项目实战
@topic_bp.route('/subscription')
def subscription_number():
    pass



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
    topic_fields = {
        'id':fields.Integer,
        'theme': fields.String,
        'description':fields.String,
        'type_id': fields.Integer,
        'create_time':fields.DateTime,
        'update_time':fields.DateTime,
        'img_urls':fields.String,
        'video_urls':fields.String,
        'author_id':fields.String,
        'author': fields.Nested({
            'username': fields.String
        })
    }

    resource_fields = {
        "prev_page": fields.Integer,  # 上一页
        "next_page": fields.Integer,  # 下一页
        "current_page": fields.Integer,  # 当前页
        "total_pages": fields.Integer,  # 总页数
        "max_page": fields.Integer,  # 最大页
        "page_size": fields.Integer,  # 每页数据条数
        "totals": fields.Integer,  # 数据总条数
        "offset": fields.Integer,  # 偏移量
        "page_range": fields.List(fields.Integer),  # 页码范围
        "data":fields.List(fields.Nested(topic_fields))
    }


    @marshal_with(resource_fields)
    def get(self):
        page_num = int(request.args.get('page'))
        query = TopicModel.query

        # 分页
        totals = query.count()
        pag = pagination(page_num,totals)

        if totals!=0:
            data = query.offset(pag["offset"]).limit(pag["page_size"]).all()
            # for post in data:
            #     print(post.author.username)
        else:
            data = []
        pag['data'] = data;
        return pag

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