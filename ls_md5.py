#!/usr/bin/env python
# -*- coding: utf-8 -*-  @Author  : bjsasc
import os
import hashlib

a = hashlib.md5(open('ip_scaner.py', 'rb').read())
print a.hexdigest().upper()
