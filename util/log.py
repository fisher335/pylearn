#!/usr/bin/env python
# -*- coding: utf-8 -*-  @Author  : bjsasc
import logging

logging.basicConfig(
    filename='log.log',
    level=logging.INFO,
    format='%(asctime)s  %(filename)s  [line:%(lineno)d]   %(levelname)s  %(message)s',
    #datefmt='%a, %d %b %Y %H:%M:%S',
)


def debug(msg):
    logging.debug(msg=msg)


def info(msg):
    logging.info(msg=msg)


def warning(msg):
    logging.warning(msg=msg)


def error(msg):
    logging.error(msg=msg)


def exception(msg):
    logging.exception(msg=msg)


if __name__ == '__main__':
    logging.info('loging test')
