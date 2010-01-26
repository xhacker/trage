#!/usr/bin/python
# -*- coding: utf-8 -*-

# JudgeShop, functions.

def get_tmp_dir():
    # UNFINISHED
    tmp_dir = "/tmp/"
    return tmp_dir
    
    #~ if not defined(tmp_dir):
        #~ import os
        #~ tmp_dir = os.tempnam(None, "Judge")
        #~ create_dir(tmp_dir)
    #~ 
    #~ return tmp_dir

def judge(pack_source, prob_id, filename):
    
    # Get lang from filename
    lang = "c"
    
    # Get directory path
    tmp_dir = get_tmp_dir()
    import os
    prob_dir = os.path.join(os.getenv("HOME"), ".judgeshop/problem", pack_source, prob_id)

    # Read problem config file
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    try:
        config.read(os.path.join(prob_dir, "problem.conf"))
        name = config.get("main", "name")
    except:
        return "Problem file error, please report the bug to developers."

    # Make a link for the source file
    if os.path.lexists(filename) == False:
        return "Source file not exist."
    if os.path.lexists( os.path.join(tmp_dir, name + "." + lang) ):
        os.remove( os.path.join(tmp_dir, name + "." + lang) )
    try:
        os.symlink(filename, os.path.join(tmp_dir, name + "." + lang))
    except:
        return "An error occured, please report the bug to developers."

    # Judge display text
    text = 'Problem: %s (pack source: "%s", problem id: %d)\n' % (name, pack_source, int(prob_id))

    # Judge
    import core
    judge = core.Judge(prob_dir, name, lang)

    error = judge.load_conf()
    if error:
        text += "Problem file error, please report the bug to developers."
        return text

    text += "\nCompiling...\n"
    error = judge.compile()
    if error:
        if error['error'] == "lang":
            text += "Language not available."
        if error['error'] == 'compile':
            text += "Compile failed.\n" + error['compile_err']
        return text
    text += "Done.\n"

    text += "\nRunning...\n"
    result = judge.execute()

    if result['error']:
        text += "An error occured, please report the bug to developers."
        return text

    if result['AC']:
        text += "Accepted. (%d/%d)\n" % (result['tpoint_correct'], result['tpoint_count'])
    else:
        text += "Not accepted. (%d/%d)\n" % (result['tpoint_correct'], result['tpoint_count'])
    
    for i in range(0, result['tpoint_count']):
        text += "\n* Test point %d: %s" % (i, result['tpoint_status'][i])
        if(result['tpoint_status'][i] != "RTE"):
            text += " (Time: %.2fs/%.1fs, Mem: %.2fM/%dM)\n"\
                % (result['tpoint_time'][i], float(result['tpoint_timelmt'][i]), result['tpoint_mem'][i], result['tpoint_memlmt'][i])
        else:
            text += "\n"
        if result['tpoint_status'][i] == "WA":
            text += "Right answer:\n"
            text += result['tpoint_ans'][i]
            text += "Your answer:\n"
            text += result['tpoint_out'][i]
    # UNFINISHED!!!
    # Update db
    
    return text
