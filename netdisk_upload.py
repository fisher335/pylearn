#!/usr/bin/env python
# -*- coding: utf-8 -*-  @Author  : bjsasc
import os
import sys
import requests
import hashlib
import uuid
import time
import json



# rest_url = 'http://10.0.6.83:8088/NetDisk/rest/util'
# rest_share = 'http://10.0.6.83:8088/NetDisk/rest/share'
# rest_mine = 'http://10.0.6.83:8088/NetDisk/rest/mine'

rest_url = 'http://disk.bjsasc.com:8180/NetDisk/rest/util'
rest_share = 'http://disk.bjsasc.com:8180/NetDisk/rest/share'
rest_mine = 'http://disk.bjsasc.com:8180/NetDisk/rest/mine'

# 全局范围登录，保持session
params = {'method': 'login', 'loginName': 'wangyichong',
          'password': 'wangyichong', 'client': 'PCClient'}
s = requests.Session()
s.get(rest_url, params=params)

# 准备文件信息


def getMD5(filename):
    _a = hashlib.md5()
    _a.update(open(filename, 'rb').read())
    return _a.hexdigest()


def getCloudStorageURl(method=None, id=None):
    params = {'method': 'getCSAccessUrl',
              'csMethod': method, 'bucketId': 'default', 'id': id}
    r = s.get(rest_url, params=params)
    # print r.content
    return r.json()['CSAccessUrl']


def upload(file_path):
    # 准备文件
    file_size = os.path.getsize(file_path)
    filename = os.path.basename(file_path)
    md5 = getMD5(file_path)
    # file_mtime = int(os.stat('c:/pylearn/temp').st_mtime)
    _id = str(uuid.uuid4())
    id = _id.replace('-', '')
    if '.' in filename:
        ext_name = filename.rsplit('.', 1)[1]  # 获取后缀
    else:
        ext_name = ''

    print u'开始秒传检查。。获取检查的url地址。。。。begin。。。。。'
    # 秒传检查
    url_checkfile = getCloudStorageURl('checkfile')
    print url_checkfile
    params_checkfile = {'fileSize': file_size, 'fileName': filename,
                        'md5': md5}
    print params_checkfile
    result = s.get(url_checkfile, params=params_checkfile).json()
    print result
    csfileId = False if result.get('info') =='' else True
    print '秒传检查完成。。。。。cfilsid'.decode('utf-8'), csfileId

    begin = int(time.time())
    end = int(time.time())

    '如果文件不存在，开始上传，判断文件存在的方式是如果上面返回的有info，并且info里面是个文件ID，则说明文件存在，如果没有info，则说明文件不存在，那个result 永远是TRUE，没毛用'.decode('utf-8')
    if csfileId == False:
        print '文件上传开始。。。。。。'.decode('utf-8')
        url_upload = getCloudStorageURl('upload')
        print url_upload
        params_upload = {'fileSize': file_size,
                         'md5': md5, 'fileName': filename}
        files = {'file': (filename, open(file_path, 'rb'), {'Expires': '0'})}
        headers = {'content_type': 'application/octet-stream'}
        # # 开始上传文件
        begin = int(time.time())

        upload_response = s.post(url_upload, params=params_upload,
                                 files=files, headers=headers)
        upload_result = upload_response.json()

        if upload_result['result']:
            upload_info = upload_result['info']
            csfileId = json.loads(upload_info)['id']
            print '文件 '.decode('utf-8'), file_path, ' 上传成功,文件 id '.decode('utf-8'), csfileId
        else:
            print '文件上传失败'.decode('utf-8'), upload_result
        end = int(time.time())
    else:
        print '文件已存在，跳过上传，文件id'.decode('utf-8'), csfileId

    # # 写到网盘记录中
    params_mine = {'method': 'chunkOrAppendUploadFinish', 'parent': '', 'fileName': filename.decode('utf-8'),
                   'fileSize': file_size, 'fileId': csfileId, 'md5': md5, 'begin': begin, 'end': end}
    mine_result = s.get(rest_mine, params=params_mine)
    # print mine_result.url
    print mine_result.content
    mine_id = mine_result.json()[0]['info']
    if len(mine_id) > 0:
        print '写入个人网盘记录完成，记录_id = '.decode('utf-8') + mine_id
    else:
        print '插入个人网盘记录失败'.decode('utf-8')

    # # 写到分享中心记录中
    params_share = {'method': 'create', 'parent': '', 'name': filename.decode('utf-8'), 'shareId': id, 'ids': mine_id,
                    'recordType': 0, 'fileExtName': ext_name}
    share_content = s.get(rest_share, params=params_share)
    share_result = share_content.json()[0].get('success', False)
    if share_result:
        print '生成分享记录成功'.decode('utf-8')
    else:
        print '生成分享记录失败'.decode('utf-8')


if __name__ == '__main__':
    # uploade(ur'oraclehomeproperties.xml')
    # uploade(ur'C:\pylearn\pycharm-community-5.0.exe')
    upload(ur'c:\pylearn\1.ini')
