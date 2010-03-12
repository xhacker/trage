#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
tmp_dir = '/tmp/'

class Judge:
    def __init__(self, source, id, source_file):
        self.source      = source
        self.id          = id
        self.source_file = source_file
        self.lang        = os.path.splitext(source_file)[1].lstrip('.').lower()

    def load(self):
        '''读取题目配置文件'''
        config_file = os.path.join(os.getenv('HOME'), '.trage/problem', self.source, self.id, 'problem.conf')
        
        import ConfigParser
        config    = ConfigParser.RawConfigParser()
        try:
            config.read( os.path.join(config_file) )
        except:
            return 1 # Error
        self.name           = config.get("main", "name")
        self.tpoint_count   = config.getint("test_point", "test_point_count")
        self.tpoint_timelmt = []
        self.tpoint_memlmt  = []
        self.tpoint_correct = 0
        self.tpoint_current = 0
        timelmt_all         = None
        memlmt_all          = None
        if config.has_option("test_point", "time_limit_all"):
            timelmt_all     = float( config.get("test_point", "time_limit_all") )
        if config.has_option("test_point", "mem_limit_all"):
            memlmt_all      = float( config.get("test_point", "mem_limit_all") )
        for i in range(0, self.tpoint_count):
            if timelmt_all:
                self.tpoint_timelmt.append(timelmt_all)
            else:
                self.tpoint_timelmt.append( float( config.get("test_point", "time_limit_" + str(i)) ) )
            if memlmt_all:
                self.tpoint_memlmt.append(memlmt_all)
            else:
                self.tpoint_memlmt.append( int( config.get("test_point", "mem_limit_" + str(i)) ) )
       
    def compile(self):
        '''编译'''
        # Make a link for the source file
        abs_source_file = os.path.abspath(self.source_file)
        if os.path.lexists(self.source_file) == False:
            return "Source file not exist." #TODO Source file does not exist.
        if os.path.lexists( os.path.join(tmp_dir, self.name + "." + self.lang) ):
            os.remove( os.path.join(tmp_dir, self.name + "." + self.lang) )
        try:
            os.symlink(abs_source_file, os.path.join(tmp_dir, self.name + "." + self.lang))
        except:
            return "An error occured, please report the bug to developers."

        # Compile command
        if self.lang == "c":
            compile_command = 'gcc -o "%s" "%s"' % (os.path.join(tmp_dir, self.name), os.path.join(tmp_dir, self.name + "." + self.lang))
        # elif self.lang == "cpp":
        #     compile_command = ''
        # elif self.lang == "pas":
        #     compile_command = ''
        else:
            return 'Sorry, your programming language currently not supported.' #TODO your programming language is not supported currently

        # Compile
        import subprocess
        compile_proc = subprocess.Popen(compile_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        return_code = compile_proc.wait()
        compile_err = compile_proc.stdout.read()
        os.remove( os.path.join(tmp_dir, self.name + "." + self.lang) ) # Clean
        if return_code:
            return compile_err
        else:
            return None

    def judge(self):
        '''评测一个测试点'''
        # TODO
        if self.tpoint_current >= self.tpoint_count:
            return None

        status = 'TLE'
        ans    = None
        out    = None
        time   = 0.23
        mem    = 4.04
        result = {'tpoint': self.tpoint_current + 1, 'status': status, 'ans': ans, 'out': out, 'time': time, 'mem': mem, \
                      'timelmt': self.tpoint_timelmt[self.tpoint_current],\
                      'memlmt': self.tpoint_memlmt[self.tpoint_current] }
        self.tpoint_current += 1
        return result
            
    def getResult(self):
        if self.tpoint_correct == self.tpoint_count:
            AC = True
        else:
            AC = False
        return { 'tpoint_count': self.tpoint_count,
                 'tpoint_correct': self.tpoint_correct,
                 'AC': AC }
