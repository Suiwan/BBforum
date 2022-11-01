# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 19:19
from flask import jsonify,request
from . import post_bp
import datetime
from flask_restful import Resource,Api,marshal_with,fields
from models import PostModel,model_to_dict
from app.extensions import db


# 帖子收集功能（待完善）
@post_bp.route('/post_list',methods = ['POST'])
def post_list():
    # id_list = request.form.getlist('ids')
    id_list = request.get_json()['ids']
    print(type(id_list))
    print(list(id_list))
    posts = []
    for id in id_list:
        print(id)
        # post = PostModel.query.get(id)
        # posts.append(post)
    return id_list
    # return jsonify({
    #          'code': 200,
    #          'msg':'success',
    #          'data': {
    #              'post_list': model_to_dict(posts)
    #          }
    #      })

# 注册topic api
topic_api = Api(post_bp)


# 话题CURD
class PostView(Resource):

    resource_fields = {
        'id':fields.Integer,
        'title': fields.String,
        'text':fields.String,
        'type_id': fields.Integer,
        'create_time':fields.DateTime,
        'update_time':fields.DateTime,
        'img_urls':fields.String,
        'video_urls':fields.String,
        'author_id':fields.String,
        'topic_id':fields.Integer
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
    resource_fields = {
        'id':fields.Integer,
        'title': fields.String,
        'text':fields.String,
        'create_time':fields.DateTime,
        'update_time':fields.DateTime,
        'img_urls':fields.String,
        'video_urls':fields.String,
        'author_id':fields.String,
        'topic_id':fields.Integer
    }

    @marshal_with(resource_fields)
    def get(self):
        posts = PostModel.query.all()
        return posts

    def post(self):
        data = request.get_json()
        title = data['title']
        text = data['text']
        topic_id = data['topic_id']
        img_urls = data['img_urls']
        video_urls = data['video_urls']
        author_id = data['author_id']
        post = PostModel(title = title,text=text,topic_id=topic_id,img_urls=img_urls,video_urls=video_urls,author_id=author_id)
        db.session.add(post)
        db.session.commit()
        return jsonify({
            'msg':'add success',
            'code':200
        })


topic_api.add_resource(PostView, '/<int:id>')
topic_api.add_resource(PostsView,'/')