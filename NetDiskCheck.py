#!/usr/bin/env python
# -*- coding: gbk -*-
import os
import paramiko
import time
import requests
# HOSTS_Tomcat = ['10.10.30.12', '10.10.30.13', '10.10.30.22', '10.10.30.23']
# HOSTS_Nginx = ['10.10.30.10', '10.10.30.11', '10.10.30.20', '10.10.30.21']
# HOSTS_Mongo = ['10.10.30.24', '10.10.30.25', '10.10.30.26']
#
#
# PORT = 22
# USER = 'bjsasc'
# PASSWORD = 'bjsasc'
#
# URL_page = ['http://10.10.30.10/NetDisk/','http://10.10.30.11/NetDisk/','http://10.10.30.20/CloudStorage/console/','http://10.10.30.21/CloudStorage/console/']
# URL_REST = 'http://10.10.30.10/NetDisk/rest/util'
# USER_LOGIN = 'test'
# USER_PASSWORD = 'test'


''' ���沿������Դ���ǵ��������'''
HOSTS_Tomcat = ['172.17.227.102', '172.17.227.103', '172.17.227.106', '172.17.227.107']
HOSTS_Nginx = ['172.17.227.100', '172.17.227.101', '172.17.227.104', '172.17.227.105']
HOSTS_Mongo = ['172.17.227.108', '172.17.227.109', '172.17.227.110']
HOSTS_VIP = ['172.17.227.112', '172.17.227.113']
PORT = 22
USER = 'root'
PASSWORD = 'openstack'


URL_page = ['http://172.17.227.100/NetDisk/','http://172.17.227.101/NetDisk/','http://172.17.227.104/CloudStorage/console/','http://172.17.227.105/CloudStorage/console/']
URL_REST = 'http://172.17.227.100/NetDisk/rest/util'
USER_LOGIN = 'test'
USER_PASSWORD = 'test'



def checkServerStatus():
    HOSTS = HOSTS_Mongo + HOSTS_Tomcat + HOSTS_Nginx+HOSTS_VIP
    HOSTS.sort()
    for host in HOSTS:
        time.sleep(1)
        out = os.popen('ping -n 1 ' + host)
        output = out.read()
        if str(output).upper().find("TTL") >= 0:
            print host, '������״̬ �������'
        else:
            print host, '������״̬ ����쳣��δpingͨ'


def checkTomcatStatus():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in HOSTS_Tomcat:
        time.sleep(1)
        try:
            ssh.connect(host, PORT, USER, PASSWORD,timeout=2)
            stdin, stdout, stderr = ssh.exec_command('ps -ef|grep Tomcat')
            data = stdout.read()
            # print data
            print host, 'Tomcat ����������' if data.find('_ZYWX') >= 0 else 'Tomcat ����û������'
        except:
            print host, '�����쳣���������ͷ������Ƿ�����'

    ssh.close()


def checkNginxStatus():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in HOSTS_Nginx:
        time.sleep(1)
        try:
            ssh.connect(host, PORT, USER, PASSWORD)
            stdin, stdout, stderr = ssh.exec_command('ps -ef|grep nginx')
            data = stdout.read()
            # print data
            print host, 'nginx ����������' if 'openresty' in data else 'nginx ����û������'
        except:
            print host, '�����쳣���������ͷ������Ƿ�����'

    ssh.close()


def checkMongoStatus():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in HOSTS_Mongo:
        time.sleep(1)
        try:
            ssh.connect(host, PORT, USER, PASSWORD)
            stdin, stdout, stderr = ssh.exec_command('ps -ef|grep mongo')
            data = stdout.read()
            # print data
            print host, 'Mongo���ݿ� ����������' if 'mongod' in data else 'Mongo���ݿ���� û������'
        except:
            print host, '�����쳣���������ͷ������Ƿ�����'

    ssh.close()


def checkAcess():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    for host in HOSTS_Mongo:
        time.sleep(1)
        try:
            ssh.connect(host, PORT, USER, PASSWORD)
            stdin, stdout, stderr = ssh.exec_command('ps -ef|grep mongo')
            data = stdout.read()
            # print data
            print host, 'Mongo���ݿ� ����������' if 'mongod' in data else 'Mongo���ݿ���� û������'
        except:
            print host, 'ssh�����쳣���������ͷ������Ƿ�����'

    ssh.close()


def checkAcess(URL):
    time.sleep(2)
    try:
        a = requests.get(URL)
        if a.status_code == 200 :
            print URL,'ҳ�������Ӧ����'
    except:
        print URL,'ҳ������쳣'
        # pass
    # print a.status_code
def checkVip():
    time.sleep(1)
    print '��ʼ����ip�����õķ���ҳ����'
    url_vip =  ['http://172.17.227.112/NetDisk/','http://172.17.227.113/CloudStorage/console/']
    for url_vip_page in url_vip:
        checkAcess(url_vip_page)
#
# def checkLogin():
#     time.sleep(2)
#     params = {'method': 'login', 'loginName': USER_LOGIN, 'password': USER_PASSWORD, 'client': 'PCClient'}
#     try:
#         r = requests.post(URL_REST, params=params)
#         # print r.content
#         print '�û�'+USER_LOGIN+'��¼�������' if 'success:true' in r.content else '�û���¼���ʧ��'
#     except:
#         print '�û���¼����쳣��rest�����쳣'


if __name__ == "__main__":
    '''
        ����ļ����Ե������У����������ע�͵�
    '''
    print '-----------��鿪ʼ------------'+os.linesep
    checkServerStatus() #������з������Ƿ�pingͨ
    checkTomcatStatus()#���Tomcat�ķ������Ƿ�����tomcat
    checkNginxStatus()#Ngin�������
    checkMongoStatus()#������ݿ����
    for i in URL_page:
        # print i
        checkAcess(i)#������̵�¼ҳ��
    # checkLogin()#�����û���rest��¼
    checkVip()
    print os.linesep+'-----------���м�����------------'
    time.sleep(360)