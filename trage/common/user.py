#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
from trage.common.general import *

def add_user(username, realname, password):
    conn = sqlite3.connect(db_location)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''SELECT id FROM user WHERE name = ?''', [username])
    if c.fetchone():
        return 1
    c.execute('''
    INSERT INTO user
    (name, realname, password, regtime, submit_count, accept_count) VALUES
    (?, ?, ?, strftime('%s', 'now'), 0, 0)''',
    (username, realname, password))
    conn.commit()
    c.close()

def get_code_list(user_id):
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute("SELECT prob_id, time, filename FROM code WHERE user_id = ? ORDER BY id DESC", [user_id])
    code_list = []
    for row in c:
        code_list.append({
            'prob_id': row[0],
            'time': row[1],
            'filename': row[2]
        })
    c.close()
    return code_list

class User:
    def __init__(self, username, password = '', root = False):
        self.username = username
        self.password = password
        self.root = False
        if password == root_password or root:
			self.root = True

    def load(self):
        # Read database
        conn = sqlite3.connect(db_location)
        conn.text_factory = str
        c = conn.cursor()
        query = "SELECT id, realname, submit_count, accept_count FROM user "
        if self.root:
            c.execute(query + "WHERE name = ?", [self.username])
        else:
            c.execute(query + "WHERE name = ? AND password = ?", [self.username, self.password])
        row = c.fetchone()
        if row is None:
            return 1
        self.id = row[0]
        self.realname = row[1]
        self.submit_count = row[2]
        self.accept_count = row[3]
        if not self.root:
			c.execute("UPDATE user SET lastlogin = strftime('%s', 'now') WHERE id = ?", [self.id])
        conn.commit()
        c.close()
        return 0

    def set_password(self, password):
        conn = sqlite3.connect(db_location)
        conn.text_factory = str
        c = conn.cursor()
        c.execute("UPDATE user SET password = ? WHERE id = ?", [password, self.id])
        conn.commit()
        c.close()

    def get_id(self):
        return self.id

    def get_username(self):
        return self.username

    def get_realname(self):
        return self.realname

    def get_accept_count(self):
        return self.accept_count

    def get_submit_count(self):
        return self.submit_count

    def get_accept_rate(self):
        if self.submit_count == 0:
            return 0
        return int(float(self.accept_count) / float(self.submit_count) * 100)
