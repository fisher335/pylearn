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

    # ȫ�ַ�Χ��¼������session
    params = {'method': 'login', 'loginName': 'test',
              'test': '1', 'client': 'PCClient'}
    s = requests.Session()
    a = s.get(rest_url, params=params)
    if a.content[10:14] == 'true':
        print('�û�fengshaomin�����Ե�¼�ɹ�')
    else:
        send_mail.send(text_content='�û���¼ʧ�ܣ��û���֤����,��¼�û�test'+'\n'+a.content)
except:
    print('��ҵ�����û���¼ʧ��')
    print ('�û���¼ʧ�ܣ�ϵͳ���ʴ���')
    send_mail.send(text_content='�û���¼ʧ�ܣ�ϵͳ���ʴ���')
