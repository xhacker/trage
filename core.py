#!/usr/bin/python
# -*- coding: utf-8 -*-

# Core judge
# Request argu: type("system", "user"), prob_id, lang

import os
import time
import ConfigParser
import subprocess

def compare_file(filename1, filename2):
    file1 = open(filename1)
    file2 = open(filename2)
    str1 = file1.read()
    str2 = file2.read()
    
    str1 = str1.rstrip("\n")
    str2 = str2.rstrip("\n")
    
    if str1 == str2:
        # Same file
        return False
    return True

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
        self.tpoint_memlmt = []
        for i in range(0, self.tpoint_count):
            self.tpoint_timelmt.append( float( config.get("test_point", "time_limit_" + str(i)) ) )
            self.tpoint_memlmt.append( int( config.get("test_point", "mem_limit_" + str(i)) ) )
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
            'tpoint_time': [], 'tpoint_mem': [], 'tpoint_correct': 0, 'tpoint_count': self.tpoint_count, 'tpoint_timelmt': self.tpoint_timelmt, 'tpoint_memlmt': self.tpoint_memlmt}
        
        for i in range(0, self.tpoint_count):
            self.clean(exe = False)
            
            # Problem file error
            in_filename = self.prob_dir + str(i) + ".in"
            ans_filename = self.prob_dir + str(i) + ".ans"
            out_filename = tmp_dir + self.name + ".out"
            if os.path.lexists(in_filename) == False\
                or os.path.lexists(ans_filename) == False:
                return {'error': 1}
            try:
                os.symlink(in_filename, tmp_dir + self.name + ".in")
            except:
                return {'error': 1}

            exec_proc = subprocess.Popen("cd " + tmp_dir + "; ./" + self.name, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
            # UNFINISHED (time, memory)
            return_code = exec_proc.wait()
            
            # Runtime error
            if return_code:
                result['tpoint_status'].append("RTE")
                result['tpoint_ans'].append(None)
                result['tpoint_out'].append(None)
                result['tpoint_time'].append(None)
                result['tpoint_mem'].append(None)
                result['AC'] = False
                continue
            
            no_output_file = False
            if not os.path.lexists(out_filename):
                no_output_file = True
            if no_output_file or compare_file(ans_filename, out_filename):
                result['tpoint_status'].append("WA")
                ans_file = open(ans_filename)
                result['tpoint_ans'].append(ans_file.read())
                ans_file.close()
                if no_output_file:
                    result['tpoint_out'].append("")
                else:
                    out_file = open(out_filename)
                    result['tpoint_out'].append(out_file.read())
                    out_file.close()
                result['AC'] = False
            else:
                # Right answer
                result['tpoint_correct'] = result['tpoint_correct'] + 1
                result['tpoint_status'].append("AC")
                result['tpoint_ans'].append(None)
                result['tpoint_out'].append(None)
            
            # UNFINISHED
            result['tpoint_time'].append(0.334)
            result['tpoint_mem'].append(46.42)
            
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
