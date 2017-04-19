#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-10-19 10:49:56
import logging
import os
import sys
import time
import paramiko
import datetime
from collections import OrderedDict
from xml.etree import ElementTree as ET

reload(sys)
sys.setdefaultencoding('UTF-8')
logging.basicConfig(
    filename='netdisk_start.log',
    level=logging.INFO,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
)

path = os.path.join(os.getcwd(), 'config.xml')


def checkfile(path):
    """
    检查配置文件是否存在，如果不存在就创建一个初始文件
    :param path:
    """
    if not os.path.exists(path):
        with open(path, 'w') as f:  # 如果配置文件不存在，那么就写一个初始配置的
            f.write('''<?xml version="1.0" encoding="UTF-8" ?>
<!-- 第一层为一级命令，例如start，stop。第二层为服务名称,可以配置多个服务，第三层才是具体的命令参数 -->
<root>
    <start>
        <netdisk>
            <ip>10.0.6.83</ip>
            <port>22</port>
            <user>bjsasc</user>
            <password>bjsasc</password>
            <cmd>cd /home/bjsasc/ADP_NetDisk/bin; ./startup.sh</cmd>
        </netdisk>
        <mongo>
            <ip>10.0.6.83</ip>
            <port>22</port>
            <user>root</user>
            <password>111111</password>
            <cmd>/usr/local/mongodb/bin/mongod -f /usr/local/mongodb/master.conf</cmd>
        </mongo>
    </start>
    <stop>
        <netdisk>
            <ip>10.0.6.83</ip>
            <port>22</port>
            <user>bjsasc</user>
            <password>bjsasc</password>
            <cmd>cd /home/bjsasc/ADP_NetDisk/bin; ./stop.sh</cmd>
        </netdisk>
        <mongo>
            <ip>10.0.6.83</ip>
            <port>22</port>
            <user>root</user>
            <password>111111</password>
            <cmd><![CDATA[kill -9 `pgrep mongo`]]></cmd>
        </mongo>
    </stop>
</root>''')
            f.close()
        print (u'检查配置文件不存在，已经初始化配置例子在当前目录下'.decode('UTF-8'))
        b = raw_input(u'请按回车键结束程序'.decode('UTF-8').encode('GBK') + os.linesep)
        sys.exit()
    else:
        print (u'检查配置文件已存在'.decode('UTF-8'))

def getconfig(service='start'):
    """
    执行启动或者停止服务命令，star为启动服务命令，stop为停止服务命令
    :param service: start or stop
    :return:
    """
    dom = ET.parse(path)
    root = dom.getroot()
    servic_cmd = root.find(service)
    dic_sevice = OrderedDict()
    for i in servic_cmd:
        d_config = {}
        for j in i:
            # print j.tag,j.text
            d_config[j.tag.strip()] = j.text.strip()
            # print d_config
        dic_sevice[i.tag] = d_config
    return dic_sevice


def exec_cmd(service_name, ip, port, user, password, cmd):
    """
    :param service_name: 服务名称，netdisk fastdfs monggo zookper
    :param ip: SSH的ip地址
    :param port: SSH的端口，一般默认为22
    :param user: 登录的用户名
    :param password: 登录的口令，paramiko支持用证书的方式来登录，不过这个程序中只采用了用户名和口令登录，如果有证书登录再具体分析
    :param cmd:执行的命令，多行命令中间用‘；’隔开，
    """
    try:
        print '''=================================================='''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, user, password, timeout=150)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        out = stdout.readlines()
        # for i in out:
        #     print i
        logging.info(out)
        logging.info(u'{}\t{}\t{}\t执行成功!!\n'.format(ip, service_name, cmd).decode('UTF-8'))
        print u'{}\t{}\t{}\t执行成功!!\n'.format(ip, service_name, cmd).decode('UTF-8')
    except:
        logging.info(u'{}\t{}\t{}\t 执行失败!!\n'.format(ip, service_name, cmd).decode('UTF-8'))
        print u'{}\t{}\t{}\t 执行失败!!\n'.format(ip, service_name, cmd).decode('UTF-8')
    finally:
        ssh.close()


def exec_service(service):
    """
    读取xml中的数据，平凑出符合执行条件的参数。
    :param service: xml中，一级命令也就是第一层tag的名称，例如start或者stop
    """
    xml = getconfig(service=service)
    print xml
    for service_name in xml.keys():
        config = xml[service_name]
        ip = config['ip']

        port = int(config['port'])
        user = config['user']
        password = config['password']
        cmd = config['cmd']

        print config
        exec_cmd('-'.join([service, service_name]), ip, port, user, password, cmd)


if __name__ == '__main__':
    print (u'本脚本用于执行神软企业网盘启动服务命令'.decode('UTF-8'))
    time.sleep(1)
    print (u'检查配置文件是否存在'.decode('UTF-8'))
    checkfile(path)
    time.sleep(1)
    cmd_input = raw_input(u'''请输入xml中的一级命令,默认为start和stop，然后按回车键盘，不输入缺省为start,'''.decode('UTF-8').encode('GBK') + os.linesep)
    if cmd_input.strip() == '':
        cmd_input = 'start'
    logging.info(os.linesep+os.linesep+cmd_input + ' 网盘服务 *****************************************************************任务开始')
    exec_service(cmd_input.strip())
    logging.info(cmd_input + ' 网盘服务  ****************************************************************任务结束')
    print (u'程序执行完成，本窗口将在15秒钟后关闭，具体日志可参考当前目录下的日志文件，'.decode('UTF-8'))
    # a = raw_input(u'请按回车键结束程序'.decode('UTF-8').encode('GBK') + os.linesep)
