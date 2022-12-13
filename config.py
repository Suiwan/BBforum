# -*- coding: utf-8 -*-
# @Author  : Zijian li
# @Time    : 2022/10/19 14:45
import os
JSON_AS_ASCII = False
#数据库配置
HOSTNAME ='127.0.0.1'
PORT = '3306'
DATABASE = 'bbforum'
USERNAME = '########'
PASSWORD = '########'
DB_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOSTNAME,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY="20211231"
