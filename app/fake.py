# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/27 9:53
# 生成虚拟数据
import random

from faker import Faker
from models import TopicModel,PostModel,UserModel
from app.extensions import db
fake = Faker()


def fake_posts(count=30):
    for i in range(count):
        post = PostModel(
            title=fake.sentence(),
            text=fake.text(30),
            topic_id=random.randint(1,TopicModel.query.count()),
            author_id="admin"
        )
        db.session.add(post)
    db.session.commit()


def fake_topics(count=5):
    for i in range(count):
        topic = TopicModel(
            theme=fake.sentence(),
            description=fake.text(30),
            type_id=random.randint(1, 4),
            author_id= "admin"
        )
        db.session.add(topic)
    db.session.commit()


def fake_responses(count=5):
    pass