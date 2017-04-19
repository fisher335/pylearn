#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os 
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages'))


import swiftclient
from util import log
# authurl = 'http://10.0.28.164:35357/v3'
# authurl = 'http://10.0.28.164:12345/auth/v2.0/'
authurl = 'http://10.0.28.164:35357/v3'
user = 'admin'
key = 'ADMIN_PASS'
# auth = swiftclient.Connection(authurl=authurl, key=key, user=user, tenant_name='admin',
#                               auth_version="3", os_options={'project_name': 'admin'})
auth = swiftclient.client.Connection(authurl=authurl, key=key, user=user, tenant_name='admin',
                                  auth_version="3")

swift_url, token = auth.get_auth()
print swift_url, token
print auth.get_account()

# print auth.get_container('fsm')