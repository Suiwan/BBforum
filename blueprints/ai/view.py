# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/12/4 16:19
from . import ai_bp
from flask import jsonify
from flask_login import login_required
from models import *
from config import x_header,emotion_url,key_url
import urllib.request
import urllib.parse
import json



@ai_bp.route('/topic/emotion/<int:topic_id>', methods=['POST'])
@login_required
def topic_emotion_analysis(topic_id):
    topic = TopicModel.query.get(topic_id)
    posts = topic.posts
    positive_num = 0
    negative_num = 0
    neutral_num = 0
    for r in posts:
        if emotion(r.text) == "positive":
            positive_num += 1
        elif emotion(r.text) == "negative":
            negative_num += 1
        else:
            neutral_num += 1
    return jsonify({
        "positive_num": positive_num,
        "negative_num": negative_num,
        "neutral_num": neutral_num
    })


@ai_bp.route('/topic/key_summary/<int:topic_id>', methods=['POST'])
@login_required
def topic_summary_key(topic_id):
    topic = TopicModel.query.get(topic_id)
    posts = topic.posts
    text = ""
    for p in posts:
        text+= " "+p.text
        text+=p.title
    return key_summary(text)


@ai_bp.route('/topic/wordcloud/<int:topic_id>', methods=['POST'])
@login_required
def topic_wordcloud(topic_id):
    topic = TopicModel.query.get(topic_id)
    posts = topic.posts
    text = ""
    for r in posts:
        text += " " + r.text
        text += r.title
    wc_name = "wc_topic_" + str(topic_id)
    wordcloud(text, wc_name)

    return jsonify({
        'name': wc_name
    })


@ai_bp.route('/post/emotion/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_emotion_analysis(post_id):
    post = PostModel.query.get(post_id)
    responses = post.responses
    positive_num = 0
    negative_num = 0
    neutral_num = 0
    for r in responses:
        if emotion(r.text) == "positive":
            positive_num += 1
        elif emotion(r.text) == "negative":
            negative_num += 1
        else:
            neutral_num += 1
    return jsonify({
        "positive_num":positive_num,
        "negative_num":negative_num,
        "neutral_num":neutral_num
    })



@ai_bp.route('/post/key_summary/<int:post_id>', methods=['POST'])
@login_required
def post_key_summary(post_id):
    post = PostModel.query.get(post_id)
    responses = post.responses
    text = ""
    for r in responses:
        text+= " "+r.text
    # print(text)
    # wc_name = "wc_post_"+str(post_id)
    # wordcloud(text,wc_name)
    return key_summary(text)



@ai_bp.route('/post/wordcloud/<int:post_id>', methods=['POST'])
@login_required
def post_wordcloud(post_id):
    post = PostModel.query.get(post_id)
    responses = post.responses
    text = ""
    for r in responses:
        text+= " "+r.text
    # print(text)
    wc_name = "wc_post_"+str(post_id)
    wordcloud(text,wc_name)

    return jsonify({
        'name':wc_name
    })



def wordcloud(data,wc_name):
    import jieba
    import collections
    import re
    from wordcloud import WordCloud

    # 文本预处理，提取中文
    new_data = re.findall('[\u4e00 -\u9fa5]+', data, re.S)
    new_data = " ".join(new_data)

    seg_list_exact = jieba.cut(new_data, cut_all=True)

    # 开始分词
    result_list = []
    with open('stop_words.txt', encoding='utf-8') as f:
        con = f.readlines()
    stop_words = set()
    for i in con:
        i = i.replace("\n", "")  # 去掉读取每一行数据的\n
        stop_words.add(i)
        for word in seg_list_exact:
            # 设置停用词并去除单个词
            if word not in stop_words and len(word) > 1:
                result_list.append(word)
        # print(result_list)

    word_counts = collections.Counter(result_list)

    word_counts_top10 = word_counts.most_common(10)
    # print(word_counts_top10)

    my_cloud = WordCloud(
        background_color='white',  # 设置背景颜色 默认是black
        width = 900, height = 600,
        max_words = 100,  # 词云显示的最大词语数量
        font_path ='simhei.ttf',  # 设置字体 显示中文
        max_font_size = 99,  # 设置字体最大值
        min_font_size = 16,  # 设置子图最小值
         random_state = 50  # 设置随机生成状态，即多少种配色方案
    ).generate_from_frequencies(word_counts)

    my_cloud.to_file("static\wc\\"+wc_name+'.png')


def key_summary(text):
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')
    req = urllib.request.Request(key_url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    json_data = json.loads(result.decode('utf-8'))
    print(json_data)
    if json_data['code'] == "0":
        return json_data['data']['ke']
    else:
        print("key summary failed!")
        return "key summary failed!"


def emotion(text):
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')
    req = urllib.request.Request(emotion_url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    json_data = json.loads(result.decode('utf-8'))
    if json_data['code'] == "0":
        if json_data['data']['sentiment'] == 1:
            return "positive"
        elif json_data['data']['sentiment'] == 0:
            return "neutral"
        elif json_data['data']['sentiment'] == -1:
            return "negative"
        else:
            print("unknown Error!")
            return "unknown Error!"
    else:
        print("emotion analysis failed!")
        return "emotion analysis failed!"

