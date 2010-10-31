#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from trage.common.general import *

def add_user(username, realname, password):
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute('''
    INSERT INTO user
    (name, realname, password, regtime, submit_count, accept_count) VALUES
    (?, ?, ?, strftime('%s', 'now'), 0, 0)''',
    (username, realname, password))
    conn.commit()
    c.close()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def load(self):
        # Read database
        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        c.execute("SELECT realname FROM user WHERE name = ? AND password = ?", [self.username, self.password])
        row = c.fetchone()
        if row is None:
            return 1
        self.realname = row[0]
        c.close()
        return 0

    def get_username(self):
        return self.username

    def get_realname(self):
        return self.realname
