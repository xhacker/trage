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
        self.prob_dir    = os.path.join(os.getenv("HOME"), ".trage/problem", self.source, self.id)

    def load(self):
        '''读取题目配置文件'''
        config_file = os.path.join(self.prob_dir, 'problem.conf')

        import ConfigParser
        config    = ConfigParser.RawConfigParser()
        if os.path.lexists(config_file) == False:
            return 1 # Wrong problem id
        try:
            config.read(config_file)
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
        except:
            return 2 # Error

    def compile(self):
        '''编译'''
        # Make a link for the source file
        abs_source_file = os.path.abspath(self.source_file)
        if os.path.lexists(self.source_file) == False:
            return "Source file does not exist."
        if os.path.lexists( os.path.join(tmp_dir, self.name + "." + self.lang) ):
            os.remove( os.path.join(tmp_dir, self.name + "." + self.lang) )
        try:
            os.symlink(abs_source_file, os.path.join(tmp_dir, self.name + "." + self.lang))
        except:
            return "An error has occured, please report the bug to the developers."

        # Compile command
        if self.lang == "c":
            compile_command = 'gcc -o "%s" "%s"' % (os.path.join(tmp_dir, self.name), os.path.join(tmp_dir, self.name + "." + self.lang))
        elif self.lang == "cpp":
            # 实验性支持 C++
            compile_command = 'g++ -o "%s" "%s"' % (os.path.join(tmp_dir, self.name), os.path.join(tmp_dir, self.name + "." + self.lang))
        elif self.lang == "pas":
            # 实验性支持 Pascal
            compile_command = 'fpc -o"%s" "%s"' % (os.path.join(tmp_dir, self.name), os.path.join(tmp_dir, self.name + "." + self.lang))
        else:
            return "Sorry, we don't support your programming language currently."

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
        if self.tpoint_current >= self.tpoint_count:
            self.clean()
            return None

        tpoint = self.tpoint_current
        self.tpoint_current += 1
        self.clean(exe = False)

        in_file  = os.path.join(self.prob_dir, str(tpoint) + ".in")
        out_file = os.path.join(tmp_dir, self.name + ".out")
        ans_file = os.path.join(self.prob_dir, str(tpoint) + ".ans")

        if os.path.lexists(in_file) == False \
                or os.path.lexists(ans_file) == False:
            return {'error': 1}
        try:
            os.symlink(in_file, os.path.join(tmp_dir, self.name + ".in"))
        except:
            return {'error': 1}

        import subprocess
        exec_proc = subprocess.Popen("cd " + tmp_dir + "; /usr/bin/time -f \"%e\\n%M\" ./" + self.name + " > /dev/null", stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        #exec_proc = subprocess.Popen("cd " + tmp_dir + "; /usr/bin/time -f \"%e\\n%M\" ./" + self.name + " > /dev/null", stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = True)
        # TOO UGLY!!!
        # waitpid, wait4 ?
        # for j in range(0, 10000):
        # if j > self.tpoint_timelmt[i] * 2 * 10:
        # try:
        # exec_proc.kill()
        # except:
        # pass
        # return_code = 0
        # TLE_flag = True
        # break
        # time.sleep(0.1)
        # if exec_proc.poll() == 0:
        # return_code = exec_proc.returncode()
        # break
        return_code = exec_proc.wait()

        result = {'error': 0, 'tpoint': tpoint + 1,       \
                  'timelmt': self.tpoint_timelmt[tpoint], \
                  'memlmt': self.tpoint_memlmt[tpoint] }

        # RTE
        if return_code:
            result['status'] = 'RTE'
            return result

        exec_time      = float(exec_proc.stdout.readline())
        result['time'] = exec_time
        exec_mem       = float(exec_proc.stdout.readline()) / 4 / 1000
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


    def clean(self, io = True, exe = True):
        if io:
            if os.path.lexists(os.path.join(tmp_dir, self.name + ".in")):
                os.remove(os.path.join(tmp_dir, self.name + ".in"))
            if os.path.lexists(os.path.join(tmp_dir, self.name + ".out")):
                os.remove(os.path.join(tmp_dir, self.name + ".out"))
        if exe:
            if os.path.lexists(os.path.join(tmp_dir, self.name)):
                os.remove(os.path.join(tmp_dir, self.name))

    def __del__(self):
        self.clean()
