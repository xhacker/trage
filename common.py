#!/usr/bin/python
# -*- coding: utf-8 -*-

# JudgeShop, functions.

def get_tmp_dir():
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    try:
        config.read("config.conf")
    except:
        tmp_dir = "/tmp/"
    else:
        tmp_dir = config.get("dir", "tmp_dir")
    return tmp_dir

def judge(pack_source, prob_id, filename):
    
    # Get lang from filename
    lang = "c"
    
    # Get directory path
    tmp_dir = get_tmp_dir()
    # UNFINISHED!!!
    prob_dir = "/home/xhacker/.judgeshop/problem/" + pack_source + "/" + prob_id + "/"

    # Read problem config file
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    try:
        config.read(prob_dir + "problem.conf")
        name = config.get("main", "name")
    except:
        return "Problem file error, please report the bug to developers."

    # Make a link for the source file
    import os
    if os.path.lexists(filename) == False:
        return "Source file not exist."
    if os.path.lexists(tmp_dir + name + "." + lang):
        os.remove(tmp_dir + name + "." + lang)
    try:
        os.symlink(filename, tmp_dir + name + "." + lang)
    except:
        return "An error occured, please report the bug to developers."

    # Judge display text
    text = 'Problem: %s (pack source: "%s", problem id: %d)\n' % (name, pack_source, int(prob_id))

    # Judge
    import core
    judge = core.Judge(prob_dir, name, lang)

    error = judge.load_conf()
    if error:
        text = text + "Problem file error, please report the bug to developers."
        return text

    text = text + "\nCompiling...\n"
    error = judge.compile()
    if error:
        if error['error'] == "lang":
            text = text + "Language not available."
        if error['error'] == 'compile':
            text = text + "Compile failed.\n" + error['compile_err']
        return text
    text = text + "Done.\n"

    text = text + "\nRunning...\n"
    result = judge.execute()

    if result['error']:
        text = text + "An error occured, please report the bug to developers."
        return text

    if result['AC']:
        text = text + "Accepted. (%d/%d)\n" % (result['tpoint_correct'], result['tpoint_count'])
    else:
        text = text + "Not accepted. (%d/%d)\n" % (result['tpoint_correct'], result['tpoint_count'])
    
    for i in range(0, result['tpoint_count']):
        text = text + "\n* Test point %d: %s" % (i, result['tpoint_status'][i])
        if(result['tpoint_status'][i] != "RTE"):
            text = text + " (Time: %.3fs/%.1fs, Mem: %.2fM/%dM)\n"\
                % (result['tpoint_time'][i], float(result['tpoint_timelmt'][i]), result['tpoint_mem'][i], result['tpoint_memlmt'][i])
        else:
            text = text + "\n"
        if result['tpoint_status'][i] == "WA":
            text = text + "Right answer:\n"
            text = text + result['tpoint_ans'][i]
            text = text + "Your answer:\n"
            text = text + result['tpoint_out'][i]
    # UNFINISHED!!!
    # Update db
    
    return text
