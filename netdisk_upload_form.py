#!/usr/bin/env python
# -*- coding: utf-8 -*-  @Author  : bjsasc
"""本脚本用于直接执行上传文件到神软网盘上，然后自动分享到分享中心，此脚本模拟浏览器表单进行上传，性能有限，最好用网盘客户端来上传。"""
import os
import requests
import re
import platform
import time
from bs4 import BeautifulSoup
import logging
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logging.basicConfig(
    filename='log.log',
    level=logging.WARNING,
    format='%(asctime)s  %(filename)s  [line:%(lineno)d]   %(levelname)s  %(message)s', )

rest_url = 'http://disk.bjsasc.com:8180/NetDisk/rest/util'
rest_share = 'http://disk.bjsasc.com:8180/NetDisk/rest/share'
rest_mine = 'http://disk.bjsasc.com:8180/NetDisk/rest/mine'
user_name = 'fengshaomin'
password = '1'
# 全局范围登录，保持session
data = {'loginName': user_name,
        'password': password, 'client': 'PCClient'}
s = requests.Session()
r = s.post(rest_url, data=data, params={'method': 'login'})


def createFolder(foldername):
    foldername = foldername.decode('utf-8')
    params_createfolder = {'method': 'createFolder'}
    data_create_folder = {'parent': '', 'folderName': foldername}
    # # 开始上传文件
    headers = {'content_type': 'application/x-www-form-urlencoded; charset=UTF-8'}
    s.post(rest_mine, params=params_createfolder, data=data_create_folder, headers=headers)
    params_fileid = {'method': 'list',
                     'option': 'option', 'parent': ''}
    data_fileid = {'sortName': 'CREATETIME', 'sortOrder': 'desc', 'sort': 'CREATETIME', 'dir': 'desc', 'start': 0,
                   'limit': 15}
    response_getfolderid = s.post(rest_mine, params=params_fileid, data=data_fileid)
    # rsp_rows = json.loads(response_getfileid.content)
    rsp_dic= response_getfolderid.json()['rows']
    # rsp_dic = rsp_rows['rows']
    fileid = None
    for i in rsp_dic:
        if i['NAME'].strip() == foldername.strip():
            fileid = i['ID']
            print('获取文档记录ID---------%s ' % fileid)
            return fileid
    if fileid is None:
        logging.warning('获取文件夹 %s ID失败' % foldername)


def upload(file_path):
    # 准备文件信息，包括文件名称和文件后缀名
    filename = os.path.basename(file_path)
    # print filename
    if '.' in filename:
        ext_name = filename.rsplit('.', 1)[1]  # 获取后缀
    else:
        ext_name = ''
    filename = filename.decode('utf-8')
    file_path = file_path.decode('utf-8')
    # 开始表单上传
    params_upload = {'method': 'formUpload', 'parentFolderId': '', 'fileName': filename}
    files = {'file': (filename, open(file_path, 'rb'), {'Expires': '0'})}
    # files = {'file':  open(file_path, 'rb')}
    headers = {'content_type': 'application/octet-stream'}
    # # 开始上传文件
    print '%s 上传开始，请等待，----- '.decode('utf-8') % filename
    logging.info('%s 上传开始，请等待，----- ' % filename)
    response_upload = s.post(rest_mine, files=files, params=params_upload, headers=headers, timeout=36000, stream=True)
    if response_upload.status_code == 200:
        print '%s 上传成功' % filename
        logging.warn('%s 上传成功'.decode('utf-8') % filename)
    else:
        logging.warn(' %s 上传失败' % filename)
        raise SystemExit
    # 获取文档记录id
    params_fileid = {'method': 'list',
                     'option': 'option', 'parent': ''}
    data_fileid = {'sortName': 'CREATETIME', 'sortOrder': 'desc', 'sort': 'CREATETIME', 'dir': 'desc', 'start': 0,
                   'limit': 15}
    response_getfileid = s.post(rest_mine, params=params_fileid, data=data_fileid)
    # rsp_rows = json.loads(response_getfileid.content)
    rsp_dic= response_getfileid.json()['rows']
    # rsp_dic = rsp_rows['rows']
    fileid = None
    for i in rsp_dic:
        if i['NAME'].strip() == filename.strip():
            fileid = i['ID']
            print('获取文档记录ID---------%s ' % fileid)
    if fileid is None:
        logging.warning('获取文件 %s ID失败' % filename)

    # 获取文档分享shareid
    params_shareid = {'method': 'generateShareId'}
    data_shareid = {'ids': fileid, 'name': filename, 'recordType': 0, 'fileExtName': ext_name}
    response_getshareid = s.post(rest_share, params=params_shareid, data=data_shareid)
    shareid = response_getshareid.json()[0]['info']
    print '获取文档分享记录ID ---------%s '.decode('utf-8') % shareid

    # 文档分享到分享中心
    params_shareid = {'method': 'create'}
    data_shareid = {'shareId': shareid, 'ids': fileid, 'name': filename, 'recordType': 0, 'fileExtName': ext_name,
                    'password': '', 'sharedays': '', 'description': u'由' + platform.node() + u'自动上传分享'}
    # log.info data_shareid
    response_share = s.post(rest_share, params=params_shareid, data=data_shareid)
    if response_share.json()[0]['success']:
        print ' %s 分享成功' % filename
        logging.warn(' %s 分享成功'.decode('utf-8') % filename)
    else:
        print ' %s 分享失败，原因如下 %s ' % (filename, response_share.json()[0]['info'])
        logging.warn(' %s 分享失败，原因如下 %s '.decode('utf-8') % (filename, response_share.json()[0]['info']))



if __name__ == '__main__':
    # path = raw_input(u"input the file abspath,or the filename in currutdir" + os.linesep)
    print __doc__
    path = ur'D:\工作软件\vc++运行环境_x64.exe'
    if os.path.exists(path):
        print path
        try:
            upload(path)
        except:
            print '%s 上传异常，请检查处理' % path
    else:
        print '路径输入有错误'
