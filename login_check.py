#!/usr/bin/env python
# -*- coding: GBK -*-  @Author  : bjsasc
from __future__ import print_function
from util import send_mail
import requests
try:

    rest_url = 'http://disk.bjsasc.com:8180/NetDisk/rest/util'
    # rest_prepare = 'http://10.0.6.65:7080/NetDisk/rest/mine'
    # rest_prepare = 'http://10.0.6.65:7080/NetDisk/rest/prepare'
    # rest_share = 'http://10.0.6.65:7080/NetDisk/rest/share'

    # 全局范围登录，保持session
    params = {'method': 'login', 'loginName': 'test',
              'test': '1', 'client': 'PCClient'}
    s = requests.Session()
    a = s.get(rest_url, params=params)
    if a.content[10:14] == 'true':
        print('用户fengshaomin，测试登录成功')
    else:
        send_mail.send(text_content='用户登录失败，用户验证错误,登录用户test'+'\n'+a.content)
except:
    print('企业网盘用户登录失败')
    print ('用户登录失败，系统访问错误')
    send_mail.send(text_content='用户登录失败，系统访问错误')
