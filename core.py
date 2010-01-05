#!/usr/bin/python
# -*- coding: utf-8 -*-

# Core judge
# Request argu: type("system", "user"), prob_id, lang

import os
import time
import ConfigParser
import subprocess

def compare_file(file1, file2):
    # UNFINISHED
    return False

from common import get_tmp_dir
tmp_dir = get_tmp_dir()

class Judge:
    def __init__(self, prob_dir, name, lang):
        self.prob_dir = prob_dir
        self.name = name
        self.lang = lang
    
    def load_conf(self):
        config = ConfigParser.RawConfigParser()
        try:
            config.read(self.prob_dir + "problem.conf")
        except:
            return {'error': "config"}
        self.tpoint_count = config.getint("test_point", "test_point_count")
        self.tpoint_timelmt = []
        self.tpoint_memolmt = []
        for i in range(0, self.tpoint_count):
            self.tpoint_timelmt.append( config.get("test_point", "time_limit_" + str(i)) )
            self.tpoint_memolmt.append( config.get("test_point", "memo_limit_" + str(i)) )
        return 0

    def compile(self):
        if self.lang == "c":
            compile_command = 'gcc -o "%s" "%s"' % (tmp_dir + self.name, tmp_dir + self.name + "." + self.lang) 
        # elif self.lang == "cpp":
        #     compile_command = ''
        # elif self.lang == "pas":
        #     compile_command = ''
        else:
            # Not available
            return {'error': "lang"}
        
        compile_proc = subprocess.Popen(compile_command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        return_code = compile_proc.wait()
        compile_err = compile_proc.stdout.read()
        if return_code:
            return {'error': "compile", 'compile_err': compile_err}
        else:
            return 0

    def execute(self):
        result = {'error': 0, 'AC': True, 'tpoint_status': [], 'tpoint_ans': [], 'tpoint_out': [],\
            'tpoint_time': [], 'tpoint_correct': 0, 'tpoint_count': self.tpoint_count}
        for i in range(0, self.tpoint_count):
            self.clean(exe = False)
            
            if os.path.lexists(self.prob_dir + str(i) + ".in") == False:
                return {'error': 1}
            try:
                os.symlink(self.prob_dir + str(i) + ".in", tmp_dir + self.name + ".in")
            except:
                return {'error': 1}

            exec_proc = subprocess.Popen("cd " + tmp_dir + "; ./" + self.name, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
            # UNFINISHED (time, memory)
            return_code = exec_proc.wait()
            
            if return_code:
                result['tpoint_status'].append("RTE")
                result['tpoint_ans'].append(None)
                result['tpoint_out'].append(None)
                result['AC'] = False
                continue
            
            try:
                ans_file = open(self.prob_dir + str(i) + ".ans", "r")
            except:
                return {'error': 1}
            try:
                out_file = open(tmp_dir + self.name + ".out", "r")
            except:
                result['tpoint_status'].append("WA")
                result['tpoint_ans'].append(ans_file.read())
                ans_file.close()
                result['tpoint_out'].append("")
                result['AC'] = False
                continue

            if compare_file(ans_file, out_file) == False:
                # Right answer
                result['tpoint_correct'] = result['tpoint_correct'] + 1
                result['tpoint_status'].append("AC")
                result['tpoint_ans'].append(None)
                result['tpoint_out'].append(None)
            else:
                print "shit!"
                result['tpoint_status'].append("WA")
                ans_file = open(self.prob_dir + str(i) + ".ans", "r")
                out_file = open(tmp_dir + self.name + ".out", "r")
                result['tpoint_ans'].append(ans_file.read())
                result['tpoint_out'].append(out_file.read())
                ans_file.close()
                out_file.close()
                result['AC'] = False
            
            self.clean(exe = False)
        self.clean()
        return result
        
    def clean(self, io = True, exe = True):
        if io:
            if os.path.lexists(tmp_dir + self.name + ".in"):
                os.remove(tmp_dir + self.name + ".in")
            if os.path.lexists(tmp_dir + self.name + ".out"):
                os.remove(tmp_dir + self.name + ".out")
        if exe:
            if os.path.lexists(tmp_dir + self.name):
                os.remove(tmp_dir + self.name)

    def __del__(self):
        self.clean()
