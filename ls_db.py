#!/usr/bin/env python
# -*- coding: utf-8 -*- '2016/11/3 0003' 'fengshaomin'
import sqlite3
with sqlite3.connect('1.db') as db:
    db.execute("DROP TABLE 'fsm'")
    db.execute("create table 'fsm' ('nane','age')")