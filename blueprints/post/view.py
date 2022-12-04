# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:19
import json

from flask import jsonify,request
from flask_login import login_required

from . import post_bp
import datetime
from flask_restful import Resource,Api,marshal_with,fields
from models import PostModel, model_to_dict, ResponseModel, TopicModel,LikesModel,queryToDict
from app.extensions import db,pagination
from ..user.view import push_notification


@post_bp.route('/responses/<int:post_id>',methods=['GET'])
@login_required
def get_responses(post_id):
    post = PostModel.query.filter_by(id=post_id).first()
    responses = model_to_dict(post.responses)
    return jsonify({
        'msg':'success',
        'code':200,
        'data':responses
    })


@post_bp.route('/response',methods=['POST'])
@login_required
def post_response():
    post_id = request.get_json()['post_id']
    text= request.get_json()['text']
    img_url = request.get_json()['img_url'] if 'img_url' in request.get_json() else "null"
    author_id = request.get_json()['author_id']
    resp = ResponseModel(text=text, img_url=img_url, author_id=author_id, post_id=post_id)
    if resp:
        db.session.add(resp)
        db.session.commit()
        user = PostModel.query.filter_by(id=post_id).first().author
        push_notification(user,post_id,2)
        return jsonify({
            'code':200,
            'msg':'success'
        })
    else:
        return jsonify({
            'code':400,
            'msg':'some error occurred!'
        })


# 帖子收集功能（待完善）
@post_bp.route('/collect',methods = ['POST'])
def collect():
    # id_list = request.form.getlist('ids')
    id_list = request.get_json()['ids']
    posts = []
    for id in id_list:
        if id.isdigit():
            post = PostModel.query.get(id)
            if not post:
                return jsonify({
                         'code': 400,
                          'msg':'post not found'
                     })
            posts.append(post)
    # return posts
    return jsonify({
             'code': 200,
             'msg':'success',
             'data': {
                 'post_list': model_to_dict(posts)
             }
         })


@post_bp.route('/topic/<int:topic_id>',methods=['GET'])
@login_required
def get_posts_by_topic(topic_id):
    query = PostModel.query.filter_by(topic_id=topic_id)
    page_num = int(request.args.get('page'))

    # 分页
    totals = query.count()
    pag = pagination(page_num, totals)

    if totals != 0:
        data = query.offset(pag["offset"]).limit(pag["page_size"]).all()
        data = queryToDict(data)
        # for post in data:
        #     print(post.author.username)
    else:
        data = []
    pag['data'] = data;
    return json.dumps(data)


@post_bp.route('/like/<int:post_id>')
def like_number(post_id):
    post = PostModel.query.filter_by(id=post_id).first()
    return jsonify({
        "number": len(post.user_liked)
    })


# 注册topic api
topic_api = Api(post_bp)


# 话题CURD
class PostView(Resource):

    resource_fields = {
        'id':fields.Integer,
        'title': fields.String,
        'text':fields.String,
        'create_time':fields.DateTime,
        'update_time':fields.DateTime,
        'img_urls':fields.String,
        'video_urls':fields.String,
        'author_id':fields.String,
        'topic_id':fields.Integer,
        'author': fields.Nested({
            'username': fields.String
        })
    }

    @marshal_with(resource_fields)
    def get(self, id):
        post = PostModel.query.get(id)
        # author = topic.author
        return post

    def delete(self,id):
        post = PostModel.query.get(id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({'code':200,
                        'msg':"delete success"
                        })

    def put(self,id):
        data = request.get_json()
        data['update_time'] = datetime.datetime.now()
        post = PostModel.query.filter_by(id=id)
        post.update(data)
        db.session.commit()
        return jsonify({
            'code':200,
            'msg':'update success'
        })


class PostsView(Resource):

    post_fields = {
        'id':fields.Integer,
        'title': fields.String,
        'text':fields.String,
        'create_time':fields.DateTime,
        'update_time':fields.DateTime,
        'author_id':fields.String,
        'topic_id':fields.Integer,
        'author':fields.Nested({
            'username':fields.String
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
        "data":fields.List(fields.Nested(post_fields))
    }

    @marshal_with(resource_fields)
    def get(self):
        page_num = int(request.args.get('page'))
        query = PostModel.query

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
        title = data['title']
        text = data['text']
        topic_id = data['topic_id']
        img_urls = data['img_urls']
        video_urls = data['video_urls']
        author_id = data['author_id']
        post = PostModel(title = title,text=text,topic_id=topic_id,img_urls=img_urls,video_urls=video_urls,author_id=author_id)
        record = TopicModel.query.filter_by(id=topic_id).first().user_subscribed
        for r in record:
            user = r.user
            push_notification(user,post.id,1)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'msg':'add success',
            'code':200
        })


topic_api.add_resource(PostView, '/<int:id>')
topic_api.add_resource(PostsView,'')