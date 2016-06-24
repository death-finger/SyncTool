# 同步功能实现

import os
import hashlib
from tkinter.messagebox import askyesno
from tkinter import *


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


def compare(pth_src, pth_des):
    file_new = []
    dir_new = []
    file_exist = []

    if not (pth_src and os.path.exists(pth_src)):
        print('Source Path Not exist!')
        return
    elif not (pth_des and os.path.exists(pth_des)):
        print('Destination Path Not Exist!')
        if askyesno('Create Destination Path [%s]?' % pth_des):
            os.mkdir(pth_des)
        else:
            return

    src_pth = pth_src if pth_src[-1] == '/' else pth_src + '/'
    des_pth = pth_des if pth_des[-1] == '/' else pth_des + '/'
    src_pth_list = [x.replace(src_pth, '') for x in listdir(src_pth)]
    des_pth_list = [x.replace(des_pth, '') for x in listdir(des_pth)]

    for item in src_pth_list:
        if item not in des_pth_list:
            if os.path.isdir(os.path.join(src_pth, item)):
                dir_new.append(item)
            else:
                file_new.append(item)
        else:
            file_exist.append(item)

    changed_list = []
    for item in file_exist:
        pth_from = os.path.join(pth_src, item)
        pth_to = os.path.join(pth_des, item)
        if os.path.isdir(pth_from): continue
        src_file = open(pth_from, 'rb')
        des_file = open(pth_to, 'rb')
        src_hash = hashlib.sha1()
        des_hash = hashlib.sha1()
        while True:
            src_data = src_file.read(20000000)
            des_data = des_file.read(20000000)
            if not (src_data and des_data): break
            src_hash.update(src_data)
            des_hash.update(des_data)
            if src_hash.hexdigest() != des_hash.hexdigest():
                changed_list.append(item)
                break
    sync_list = (dir_new, file_new, changed_list)
    return sync_list


def sync(txt, sync_list, pth_src, pth_des):
    if txt: txt.delete(0.0, END)

    for item in sync_list[0]:
        pth_to = os.path.join(pth_des, item)
        os.mkdir(pth_to)
        if txt: txt.insert(END, 'Create Path => %s\n' % pth_to)

    for item in sync_list[1]:
        pth_to = os.path.join(pth_des, item)
        pth_from = os.path.join(pth_src, item)
        file_in = open(pth_from, 'rb')
        file_out = open(pth_to, 'wb')
        while True:
            data = file_in.read(2048000)
            if not data: break
            file_out.write(data)
        if txt: txt.insert(END, 'Creath File ==> %s\n' % pth_to)

    for item in sync_list[2]:
        pth_from = os.path.join(pth_src, item)
        pth_to = os.path.join(pth_des, item)
        src_file = open(pth_from, 'rb')
        des_file = open(pth_to, 'wb')
        while True:
            data = src_file.read(10000000)
            if not data: break
            des_file.write(data)
        if txt: txt.insert(END, 'Changed >>> %s\n' % pth_from)
"""
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


def compare(src_pth, des_pth):
    if not os.path.exists(src_pth):
        print('Source Path Not exist!')
        return
    elif not os.path.exists(des_pth):
        print('Destination Path Not Exist!')
        if input('Create Destination Path [%s]?' % des_pth)[0] in ['Y', 'y']:
            os.mkdir(des_pth)
        else:
            return
    src_pth = src_pth if src_pth[-1] == '/' else src_pth + '/'
    des_pth = des_pth if des_pth[-1] == '/' else des_pth + '/'
    src_pth_list = [x.replace(src_pth, '') for x in listdir(src_pth)]
    des_pth_list = [x.replace(des_pth, '') for x in listdir(des_pth)]
    file_new = []
    dir_new = []
    file_exist = []
    for item in src_pth_list:
        if item not in des_pth_list:
            if os.path.isdir(os.path.join(src_pth, item)):
                dir_new.append(item)
            else:
                file_new.append(item)
        else:
            file_exist.append(item)
    return src_pth, dir_new, file_new, file_exist


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
        src_hash = hashlib.sha1()
        des_hash = hashlib.sha1()
        while True:
            src_data = src_file.read(20000000)
            des_data = des_file.read(20000000)
            if not (src_data and des_data): break
            src_hash.update(src_data)
            des_hash.update(des_data)
            if src_hash.hexdigest() != des_hash.hexdigest():
                changed_list.append(item)
                break

    for item in changed_list:
        pth_from = os.path.join(src_pth, item)
        pth_to = os.path.join(des_pth, item)
        src_file = open(pth_from, 'rb')
        des_file = open(pth_to, 'wb')
        while True:
            data = src_file.read(10000000)
            if not data: break
            des_file.write(data)
        print('Changed >>> ', pth_from)
"""

if __name__ == '__main__':
    test_pth = '/Users/joshuapu/Documents/Scripts'
    des_pth = '/Users/joshuapu/Documents/Backup'
    import time
    start = time.time()
    dir_list, file_list, file_exist = compare(test_pth, des_pth)
    sync_new_files(dir_list, file_list, test_pth, des_pth)
    sync_exist_files(file_exist, test_pth, des_pth)
    print(time.time() - start)
