#!/usr/bin/env python
# -*- coding: utf-8 -*-  @Author  : bjsasc
from pymongo import MongoClient
import bson
# client = MongoClient('10.0.6.83', 27017)
# client = MongoClient('mongodb://adp_netdisk/adp_netdisk@10.0.28.253:27020')
# client = MongoClient('mongodb://10.0.6.83:27017')
client = MongoClient('mongodb://10.10.30.18:27017')
# 建立和数据库系统的连接,创建Connection时，指定host及port参数
# db_auth = client.admin
# db_auth.authenticate("admin", "bjsasc")
# #admin 数据库有帐号，连接-认证-切换库
db = client.netdisk_314
# record = db.NDPrepareRecord
# record = db.NDUserRecord
user = db.NDUser
# 连接数据库
# a = user.find({'email':None},limit = 1000)
# a = user.find({},limit = 1000)
# print a.count()

print db.collection_names()
user.find({})

# for i in a:
#     print i.get('loginName',''),i.get('mail','mail为空')
# record.remove({})

# preparerecord = db.NDPrepareRecord
# # preparerecord.remove({})
# sharerecord = db.NDShareRecord
# # sharerecord.remove({})
#
#
# a = user.find({})
# for i in  a:
#     print i
#
# config.update({{'_id': 'ptNetDiskConfig'}, {
#               '$set': {'contents.orderFileValidityDays': '2'}}})
