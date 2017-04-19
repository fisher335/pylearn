#!/usr/bin/env python
# -*- coding: utf-8 -*-  @Author  : bjsasc
from pymongo import MongoClient
import bson
client = MongoClient('10.0.6.83', 27017)
# 建立和数据库系统的连接,创建Connection时，指定host及port参数
# db_auth = client.admin
# db_auth.authenticate("admin", "bjsasc")
# #admin 数据库有帐号，连接-认证-切换库
db = client.cloudstorage_dev_fsm
file = db.file
# user = db.NDUser
# 连接数据库
# a = user.find({'email':None},limit = 1000)
# a = user.find({},limit = 1000)
# print a.count()

# for i in a:
#     print i.get('loginName',''),i.get('mail','mail为空')
# file.remove({})
a = file.find_one({'_id': '489fa46f5ac9404d9a7bb1a8b8b992df'})
print a

