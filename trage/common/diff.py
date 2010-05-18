def diff_file(filename1, filename2):
    file1 = open(filename1)
    file2 = open(filename2)
    str1 = file1.read()
    str2 = file2.read()

    str1 = str1.replace('\r\n', '\n')
    str1 = str1.replace('\r', '\n')
    str1 = str1.rstrip('\n')
    str2 = str2.replace('\r\n', '\n')
    str2 = str2.replace('\r', '\n')
    str2 = str2.rstrip('\n')

    if str1 == str2:
        return False
    return True
