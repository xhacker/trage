# NDSOJ core judge #

import os
import subprocess
import time
import filecmp
import ConfigParser

core_config = ConfigParser.RawConfigParser()
core_config.read("core.conf")
tmp_dir = core_config.get("dir", "tmp_dir")

class Judge:
    def __init__(self, name, lang, source_dir, ans_dir, tpoint_count,\
    tpoint_in, tpoint_ans, tpoint_timelmt, tpoint_memolmt):
        self.name = name
        self.lang = lang
        self.source_dir = source_dir
        self.ans_dir = ans_dir
        self.tpoint_count = tpoint_count
        self.tpoint_in = tpoint_in
        self.tpoint_ans = tpoint_ans
        self.tpoint_timelmt = tpoint_timelmt
        self.tpoint_memolmt = tpoint_memolmt

    def compile(self):
        if self.lang == "c":
            compile_command = 'gcc -o "%s" "%s.%s"' % (tmp_dir + self.name,\
                self.source_dir + self.name, self.lang) 
        # elif self.lang == "cpp":
        #     compile_command = ''
        # elif self.lang == "pas":
        #     compile_command = ''
        else:
            # not available now
            pass
        
        compile_proc = subprocess.Popen(compile_command,\
            stdout = subprocess.PIPE, shell = True)
        # time.sleep(2)
        compile_err = compile_proc.stdout.read()
        if len(compile_err) > 0:
            return compile_err
        else:
            return 0

    def judge(self):
        # now only single file. UNFINISHED!!!
        result = {'AC': True, 'tpoint_status': [], 'tpoint_ans': [], 'tpoint_out': [], 'tpoint_time': [], 'tpoint_correct': 0, }
        for i in range(0, self.tpoint_count):
            self.clean(exe = False)
            os.symlink(self.ans_dir + self.tpoint_in[i],\
                tmp_dir + self.name + ".in")
            subprocess.Popen("cd " + tmp_dir + "; ./" + self.name, shell = True)
            time.sleep(0.1) # NOT GOOD!!!
            # IF NO OUTPUT FILE?
            # NEED SMARTER DIFF
            if filecmp.cmp(self.ans_dir + self.tpoint_ans[i],\
            tmp_dir + self.name + ".out"):
                # right answer
                result['tpoint_correct'] = result['tpoint_correct'] + 1
                result['tpoint_status'].append("AC")
                ans_file = open(self.ans_dir + self.tpoint_ans[i], "r")
                result['tpoint_ans'].append(ans_file.read())
                ans_file.close()
                pass
            else:
                result['tpoint_status'].append("WA")
                ans_file = open(self.ans_dir + self.tpoint_ans[i], "r")
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
