# 同步功能实现

import os, sys

test_pth = '/Users/joshuapu/Documents/Scripts'
des_pth = '/Users/joshuapu/Documents/Backup'
sep = '\n' + '=' * 32 + '\n'

def compare(pth1, pth2):
    if not os.path.exists(pth1):
        print('pth1 not exist!')
        return
    elif not os.path.exists(pth2):
        print('pth2 not exist!')
        if input('Create pth2?')[0] in ['Y', 'y']:
            os.mkdir(pth2)
        else:
            return
    pth1 = pth1 if pth1[-1] == '/' else pth1 + '/'
    pth2 = pth2 if pth2[-1] == '/' else pth2 + '/'
    pth_list_1 = [x.replace(pth1, '') for x in listdir(pth1)]
    pth_list_2 = [x.replace(pth2, '') for x in listdir(pth2)]
    file_new = []
    dir_new = []
    file_exist = []
    for item in pth_list_1:
        if item not in pth_list_2:
            if os.path.isdir(os.path.join(pth1, item)):
                dir_new.append(item)
            else:
                file_new.append(item)
        else:
            file_exist.append(item)

    return dir_new, file_new, file_exist


def listdir(pth):
    result = []
    def sub_list(pth, result):
        for item in os.listdir(pth):
            real_pth = os.path.join(pth, item)
            if os.path.isdir(real_pth):
                result.append(real_pth)
                sub_list(real_pth, result)
            elif os.path.isfile(real_pth):
                result.append(real_pth)
    sub_list(pth, result)
    return result

def sync_new_files(dir_list, file_list, src_pth, des_pth):
    for item in dir_list:
        pth_to = os.path.join(des_pth, item)
        os.mkdir(pth_to)
        print('Create Path => ', pth_to)
    for item in file_list:
        pth_to = os.path.join(des_pth, item)
        pth_from = os.path.join(src_pth, item)
        file_in = open(pth_from, 'rb')
        file_out = open(pth_to, 'wb')
        while True:
            data = file_in.read(2048000)
            if not data: break
            file_out.write(data)
        print('Creath File ==> ', pth_to)

def sync_exist_files(file_list, src_pth, des_pth):
    changed_list = []
    for item in file_list:
        pth_from = os.path.join(src_pth, item)
        pth_to = os.path.join(des_pth, item)
        if os.path.isdir(pth_from): continue
        src_file = open(pth_from, 'rb')
        des_file = open(pth_to, 'rb')
        while True:
            src_data = src_file.read(2048000)
            des_data = des_file.read(2048000)
            if not (src_data and des_data): break
            if src_data != des_data:
                changed_list.append(item)
                break

    for item in changed_list:
        pth_from = os.path.join(src_pth, item)
        pth_to = os.path.join(des_pth, item)
        src_file = open(pth_from, 'rb')
        des_file = open(pth_to, 'wb')
        while True:
            data = src_file.read(2048000)
            if not data: break
            des_file.write(data)
        print('Changed >>> ', pth_from)


dir_list, file_list, file_exist = compare(test_pth, des_pth)
#print(file_list)
sync_new_files(dir_list, file_list, test_pth, des_pth)
sync_exist_files(file_exist, test_pth, des_pth)