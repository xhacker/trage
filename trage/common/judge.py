#!/usr/bin/python
# -*- coding: utf-8 -*-

import gettext
from gettext import gettext as _
gettext.textdomain('trage')

import os
import time
import shutil
import subprocess
from trage.common.general import *

def unlock():
    if os.path.lexists(os.path.join(trage_dir, "JudgeLock")):
        os.remove(os.path.join(trage_dir, "JudgeLock"))

class Judge:
    def __init__(self, id, source_file):
        self.id = id
        self.source_file = source_file
        self.lang = os.path.splitext(source_file)[1].lstrip('.').lower()
        self.prob_dir = os.path.join(prob_root_dir, self.id)
        while os.path.lexists(os.path.join(trage_dir, "JudgeLock")):
            print 'Another judger is running...wait...'
            time.sleep(2)
        open(os.path.join(trage_dir, "JudgeLock"), 'w')

    def load(self):
        '''Load problem config file'''
        config_file = os.path.join(self.prob_dir, 'problem.conf')

        import ConfigParser
        config = ConfigParser.RawConfigParser()
        if os.path.lexists(config_file) == False:
            return 1 # Wrong problem id
        try:
            config.read(config_file)
            self.name = config.get("main", "name")
            self.tpoint_count = config.getint("test_point", "test_point_count")
            self.tpoint_timelmt = []
            self.tpoint_memlmt = []
            self.tpoint_correct = 0
            self.tpoint_current = 0
            timelmt_all = None
            memlmt_all = None
            if config.has_option("test_point", "time_limit_all"):
                timelmt_all = float( config.get("test_point", "time_limit_all") )
            if config.has_option("test_point", "mem_limit_all"):
                memlmt_all = float( config.get("test_point", "mem_limit_all") )
            for i in range(0, self.tpoint_count):
                if timelmt_all:
                    self.tpoint_timelmt.append(timelmt_all)
                else:
                    self.tpoint_timelmt.append( float( config.get("test_point", "time_limit_" + str(i)) ) )
                if memlmt_all:
                    self.tpoint_memlmt.append(memlmt_all)
                else:
                    self.tpoint_memlmt.append( int( config.get("test_point", "mem_limit_" + str(i)) ) )
        except:
            return 2 # Error

    def compile(self):
        '''Compile'''
        # Make a link for the source file
        abs_source_file = os.path.abspath(self.source_file)
        if os.path.lexists(self.source_file) == False:
            return _('Source file does not exist.')
        if os.path.lexists( os.path.join(tmp_dir, self.name + "." + self.lang) ):
            os.remove( os.path.join(tmp_dir, self.name + "." + self.lang) )
        try:
            os.symlink(abs_source_file, os.path.join(tmp_dir, self.name + "." + self.lang))
        except:
            return _('An error has occured, please report the bug to the developers.')

        # Compile command
        self.tmp_name = str(time.time())
        if self.lang == "c":
            compile_command = 'gcc -lm -o "%s" "%s"' % (os.path.join(tmp_dir, self.tmp_name), os.path.join(tmp_dir, self.name + "." + self.lang))
        elif self.lang == "cpp":
            compile_command = 'g++ -lm -o "%s" "%s"' % (os.path.join(tmp_dir, self.tmp_name), os.path.join(tmp_dir, self.name + "." + self.lang))
        elif self.lang == "pas":
            compile_command = 'fpc -o"%s" "%s"' % (os.path.join(tmp_dir, self.tmp_name), os.path.join(tmp_dir, self.name + "." + self.lang))
        else:
            return _('Sorry, we don\'t support your programming language currently.')

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
        '''Judge a test point'''
        if self.tpoint_current >= self.tpoint_count:
            self.clean(lock = True)
            return None

        tpoint = self.tpoint_current
        self.tpoint_current += 1
        self.clean(exe = False)

        in_file = os.path.join(self.prob_dir, str(tpoint) + ".in")
        out_file = os.path.join(tmp_dir, self.name + ".out")
        ans_file = os.path.join(self.prob_dir, str(tpoint) + ".ans")

        if (os.path.lexists(in_file) == False
            or os.path.lexists(ans_file) == False):
            return {'error': 1}
        try:
            shutil.copyfile(in_file, os.path.join(tmp_dir, self.name + ".in"))
        except:
            return {'error': 1}

        org_dir = os.getcwd()
        os.chdir(tmp_dir)
        exec_proc = subprocess.Popen("/usr/bin/time -f '%%e\\n%%M' sh -c './%s>/dev/null 2>&1'" % (self.tmp_name), stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        os.chdir(org_dir)

        time_multiple = 1.3
        max_time = self.tpoint_timelmt[tpoint] * time_multiple;
        cur_time = 0.0
        return_code = 0
        TLE = False
        while cur_time <= max_time:
            if exec_proc.poll() != None:
                return_code = exec_proc.poll()
                break
            time.sleep(0.1)
            cur_time += 0.1

        if cur_time > max_time:
            exec_proc.terminate()
            subprocess.Popen("killall " + self.tmp_name, shell = True)
            TLE = True

        result = { 'error': 0, 'tpoint': tpoint + 1,
                   'timelmt': self.tpoint_timelmt[tpoint],
                   'memlmt': self.tpoint_memlmt[tpoint] }

        # RTE
        if return_code:
            result['status'] = 'RTE'
            return result

        if TLE:
            exec_time = cur_time
        else:
            exec_time = float(exec_proc.stdout.readline())
            result['time'] = exec_time
            exec_mem = float(exec_proc.stdout.readline()) / 4 / 1000
            result['mem']  = exec_mem

        # TLE
        if exec_time > self.tpoint_timelmt[tpoint]:
            result['status'] = 'TLE'
            return result

        from diff import diff_file
        no_out_file = False
        if not os.path.lexists(out_file):
            no_out_file = True
        if no_out_file or diff_file(ans_file, out_file):
            result['status'] = 'WA'
            ans_f = open(ans_file)
            result['ans'] = ans_f.read()
            ans_f.close()
            if no_out_file:
                result['out'] = 'No output file. Please check your program.'
            else:
                out_f = open(out_file)
                result['out'] = out_f.read()
                out_f.close()
        else:
            # Right answer
            self.tpoint_correct += 1
            result['status'] = 'AC'

        return result

    def get_result(self):
        if self.tpoint_correct == self.tpoint_count:
            AC = True
        else:
            AC = False
        return { 'tpoint_count': self.tpoint_count,
                 'tpoint_correct': self.tpoint_correct,
                 'AC': AC }


    def clean(self, io = True, exe = True, lock = False):
        if io:
            if os.path.lexists(os.path.join(tmp_dir, self.name + ".in")):
                os.remove(os.path.join(tmp_dir, self.name + ".in"))
            if os.path.lexists(os.path.join(tmp_dir, self.name + ".out")):
                os.remove(os.path.join(tmp_dir, self.name + ".out"))
        if exe:
            if os.path.lexists(os.path.join(tmp_dir, self.name + ".o")):
                os.remove(os.path.join(tmp_dir, self.name + ".o"))
            if os.path.lexists(os.path.join(tmp_dir, self.tmp_name)):
                os.remove(os.path.join(tmp_dir, self.tmp_name))
        if lock:
            if os.path.lexists(os.path.join(trage_dir, "JudgeLock")):
                os.remove(os.path.join(trage_dir, "JudgeLock"))

    def __del__(self):
        self.clean(lock = True)
