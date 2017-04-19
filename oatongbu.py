#!/usr/bin/env python
# coding:utf-8
from bs4 import BeautifulSoup
import requests

from util import log

'''用于从统一用户同步用户数据，设置成定时执行'''
def syncoauser():
    params = {'method': 'login', 'loginName': 'test', 'password': 'test'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
    loginurl = 'http://disk.bjsasc.com:8180/NetDisk/rest/util'
    s = requests.Session()
    s.post(loginurl, data=params, headers=headers)  # POST帐号和密码，设置headers
    print '模拟登录test账户成功'
    url = 'http://disk.bjsasc.com:8180/NetDisk/nd/jsp/sysmgr/util/SyncFromLdap.jsp'
    print ('访问系统同步页面成功，抓取同步结果中。。。。')
    r = s.get(url)
    html = BeautifulSoup(r.content)
    # print html
    '''
    bgColor = "#78c4ac"; 忽略用户
    bgColor = "#c3c428"; 添加用户
    bgColor = "#d39c86"; 更新用户
    '''
    result_insert = html.find_all('tr', {'bgcolor': '#c3c428'})
    result_update = html.find_all('tr', {'bgcolor': '#d39c86'})
    result_insert.extend(result_update)
    result = result_insert
    print '新增用户和更新用户数量为', len(result)
    if len(result) > 0:
        log.info(str(result))
        print '记录日志到日志文件完成'


if __name__ == '__main__':
    try:
        syncoauser()
    except Exception, e:
        log.error(e.message)
