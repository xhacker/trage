#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

prob_root_dir = os.path.join(os.getenv("HOME"), ".trage/problem/user")

def get_problist():
    files = os.listdir(prob_root_dir)
    files.sort()
    problist = []
    for directory in files:
        if os.path.isdir(os.path.join(prob_root_dir, directory)):
            prob = Problem('user', directory)
            prob.load()
            problist.append({
                'id': prob.get_id(),
                'name': prob.get_name(),
                'title': prob.get_title()
            })
    return problist

class Problem:
    def __init__(self, source, id):
        self.source = source
        self.id = id

    def load(self):
        '''读取题目配置文件及数据库'''
        # Get directory path
        prob_dir = os.path.join(os.getenv("HOME"), ".trage/problem", self.source, self.id)

        # Read problem config file
        import ConfigParser
        config = ConfigParser.RawConfigParser()
        try:
            config.read(os.path.join(prob_dir, "problem.conf"))
            self.name = config.get("main", "name")
            self.title = config.get("main", "title")
        except:
            return 1 # Error

        # Read database
        # TODO
        self.info = None

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_title(self):
        return self.title

    def get_info(self):
        return self.info
