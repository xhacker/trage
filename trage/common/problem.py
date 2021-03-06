#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sqlite3
from trage.common.general import *

def update_status(user_id, prob_id, AC):
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute('''SELECT id FROM accepted WHERE user_id = ? AND prob_id = ?''', [user_id, prob_id])
    if c.fetchone():
        if AC:
            c.execute('''UPDATE accepted SET time = strftime('%s', 'now') WHERE user_id = ? AND prob_id = ?''', [user_id, prob_id])
    else:
        if AC:
            c.execute('''
            INSERT INTO accepted
            (user_id, prob_id, time) VALUES
            (?, ?, strftime('%s', 'now'))''',
            [user_id, prob_id])
            c.execute('''UPDATE problem SET submit_count = submit_count + 1, accept_count = accept_count + 1 WHERE id = ?''', [prob_id])
            c.execute('''UPDATE user SET submit_count = submit_count + 1, accept_count = accept_count + 1 WHERE id = ?''', [user_id])
        else:
            c.execute('''UPDATE problem SET submit_count = submit_count + 1 WHERE id = ?''', [prob_id])
            c.execute('''UPDATE user SET submit_count = submit_count + 1 WHERE id = ?''', [user_id])
    conn.commit()
    c.close()

def store_code(user_id, prob_id, filename):
    from time import strftime
    from shutil import copy
    newname = str(strftime("%s")) + os.path.basename(filename)
    copy(filename, os.path.join(code_dir, newname))
    conn = sqlite3.connect(db_location)
    conn.text_factory = str
    c = conn.cursor()
    c.execute('''
    INSERT INTO code
    (user_id, prob_id, time, filename) VALUES
    (?, ?, strftime('%s', 'now'), ?)''',
    [user_id, prob_id, newname])
    conn.commit()
    c.close()

def clean_code(filename):
    os.remove(os.path.join(tmp_dir, filename))

def get_status(user_id, prob_id):
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute('''SELECT id FROM accepted WHERE user_id = ? AND prob_id = ?''', [user_id, prob_id])
    if c.fetchone():
        c.close()
        return True
    c.close()
    return False

def get_problist():
    conn = sqlite3.connect(db_location)
    c = conn.cursor()
    c.execute("SELECT id, name, title, difficulty FROM problem")
    problist = []
    for row in c:
        problist.append({
            'id': str(row[0]),
            'name': row[1],
            'title': row[2],
            'difficulty': row[3]
        })
    c.close()
    return problist

def get_io(io, prob_id, tp_id):
    ext = '.in' if io == 'input' else '.ans'
    filename = os.path.join(prob_root_dir, prob_id, tp_id + ext)
    return open(filename).read()

def get_std(prob_id):
    cfile = os.path.join(prob_root_dir, prob_id, 'std.c')
    cppfile = os.path.join(prob_root_dir, prob_id, 'std.cpp')
    std = {'c': None, 'cpp': None}
    if os.path.exists(cfile):
        std['c'] = open(cfile).read()
    if os.path.exists(cppfile):
        std['cpp'] = open(cppfile).read()
    return std

def get_usercode(filename):
    file = os.path.join(code_dir, filename)
    return open(file).read()

def get_img(prob_id, img_id):
    prob_dir = os.path.join(prob_root_dir, prob_id)
    file = os.path.join(prob_dir, img_id + ".png")
    if (not os.path.exists(file)):
        file = os.path.join(prob_dir, img_id + ".jpg")
    return open(file).read()

class Problem:
    def __init__(self, id):
        self.id = str(id)

    def load(self):
        '''读取题目配置文件及数据库'''
        # Get directory path
        prob_dir = os.path.join(prob_root_dir, self.id)

        # Read database
        conn = sqlite3.connect(db_location)
        c = conn.cursor()
        c.execute("SELECT name, title, info_main, info_hint, info_input, info_output, example_input, example_output, difficulty, accept_count, submit_count FROM problem WHERE id = ?", [self.id])
        row = c.fetchone()
        self.name = row[0]
        self.title = row[1]
        self.info_main = row[2]
        self.info_hint = row[3]
        self.info_input = row[4]
        self.info_output = row[5]
        self.example_input = row[6]
        self.example_output = row[7]
        self.difficulty = row[8]
        self.accept_count = row[9]
        self.submit_count = row[10]
        c.close()

    def set_all(self, args):
        conn = sqlite3.connect(db_location)
        conn.text_factory = str
        c = conn.cursor()
        c.execute('''UPDATE problem SET
        name = ?, title = ?, info_main = ?, info_hint = ?, info_input = ?, info_output = ?, example_input = ?, example_output = ?, difficulty = ? WHERE id = ?''',
        [args['name'], args['title'], args['info_main'], args['info_hint'], args['info_input'], args['info_output'], args['example_input'], args['example_output'], args['difficulty'], args['id']])
        conn.commit()
        c.close()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_title(self):
        return self.title

    def get_info_main(self):
        return self.info_main

    def get_info_hint(self):
        return self.info_hint

    def get_info_input(self):
        return self.info_input

    def get_info_output(self):
        return self.info_output

    def get_example_input(self):
        return self.example_input

    def get_example_output(self):
        return self.example_output

    def get_difficulty(self):
        return self.difficulty

    def get_accept_count(self):
        return self.accept_count

    def get_submit_count(self):
        return self.submit_count

    def get_accept_rate(self):
        if self.submit_count == 0:
            return 0
        return int(float(self.accept_count) / float(self.submit_count) * 100)
