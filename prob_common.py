#!/usr/bin/python
# -*- coding: utf-8 -*-

class Problem:
    def __init__(self, source, id):
        self.source = source
        self.id     = id

    def load(self):
        '''读取题目配置文件及数据库'''
        # Get directory path
        import os
        prob_dir = os.path.join(os.getenv("HOME"), ".trage/problem", self.source, self.id)
        
        # Read problem config file
        import ConfigParser
        config        = ConfigParser.RawConfigParser()
        try:
            config.read(os.path.join(prob_dir, "problem.conf"))
            self.name = config.get("main", "name")
        except:
            return 1 # Error

        # Read database
        # TODO
        self.info = None
    
    def getName(self):
        return self.name
    
    def getInfo(self):
        return self.info
        pass

    def getProbList(self):
        # TODO
        pass
