def diff_file(filename1, filename2):
    # full compare
    file1 = open(filename1)
    file2 = open(filename2)
    str1 = file1.read()
    str2 = file2.read()
    
    str1 = str1.rstrip("\n")
    str2 = str2.rstrip("\n")
    
    if str1 == str2:
        return False
    return True
