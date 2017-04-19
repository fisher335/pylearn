# coding:utf-8
import requests
import time
import  json
import xmltodict
URL_NetDisk =  'http://10.10.30.10/NetDisk/'
URL_CloudStorage = 'http://10.10.30.20/CloudStorage/console/login.jsp'
URL_REST = 'http://10.10.30.10/NetDisk/rest/util'
USER = 'test'
USER_PASSWORD = 'test'

def checkAcess(URL):
    time.sleep(2)
    a = requests.get(URL)
    # print a.status_code
    if a.status_code == 200 :
        print URL,'页面访问响应正常'

def checkLogin():
    time.sleep(2)
    params = {'method': 'login', 'loginName': USER, 'password': USER_PASSWORD, 'client': 'PCClient'}
    r = requests.post(URL_REST, params=params)
    # print r.content
    print '用户'+USER+'登录检查正常' if 'success:true' in r.content else '用户登录检查失败'


if __name__ == '__main__':
    checkAcess(URL_NetDisk)
    checkAcess(URL_CloudStorage)
    checkLogin()