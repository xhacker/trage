# NDSOJ local judge #

import core
import ConfigParser

# read judge config file
config = ConfigParser.RawConfigParser()
config.read("test/test.conf") # replace with argv
name = config.get("main", "name")
lang = config.get("main", "lang")
source_dir = config.get("dir", "source_dir")
ans_dir = config.get("dir", "ans_dir")
tpoint_count = config.getint("test_point", "test_point_count")
tpoint_in = []
tpoint_ans = []
tpoint_timelmt = []
tpoint_memolmt = []
for i in range(0, tpoint_count):
    tpoint_in.append( config.get("test_point", "in_file_" + str(i)) )
    tpoint_ans.append( config.get("test_point", "ans_file_" + str(i)) )
    tpoint_timelmt.append( config.get("test_point", "time_limit_" + str(i)) )
    tpoint_memolmt.append( config.get("test_point", "memo_limit_" + str(i)) )

# judge
judge = core.Judge(name, lang, source_dir, ans_dir, tpoint_count,\
    tpoint_in, tpoint_ans, tpoint_timelmt, tpoint_memolmt)
print "Problem: " + name
compile_err = judge.compile()
if compile_err != 0:
    print "Compile failed:"
    print compile_err
else:
    result = judge.judge()
del judge

# display result
if result['AC']:
    print "Accept. (%d/%d)" % (result['tpoint_correct'], tpoint_count)
else:
    print "Not accept. ($d/%d)" % (result['tpoint_correct'], tpoint_count)
for i in range(0, tpoint_count):
    print "Test point %d: %s" % (i, result['tpoint_status'][i])
    if(result['tpoint_status'][i] == "WA"):
        print "Right answer:"
        print result['tpoint_ans'][i]
        print "Your answer:"
        print result['tpoint_out'][i]
