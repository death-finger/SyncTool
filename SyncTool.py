# 主程序

import _thread
import SyncFunc
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.filedialog import askdirectory


class SyncTool(Tk):

    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.start()
        self.lbl_pth_src, self.lbl_pth_des = self.makeLabel()
        self.lbl_files, self.lbl_folders, self.lbl_diff, \
            self.lbl_total, self.lbl_prog = self.makeStatus()
        self.txt = self.makeText()
        self.makeMenu()

###################################
# UI界面
###################################

    def makeLabel(self):
        frm_lbl = Frame(self)
        frm_lbl.pack(side=TOP, fill=X)
        btn_src = Button(frm_lbl, text='Source:', height=1, width=7, relief=FLAT,
                         command=self.selectSrc)
        btn_src.grid(row=0, column=0, sticky=W)
        btn_dest = Button(frm_lbl, text='Destin:', height=1, width=7, relief=FLAT,
                          command=self.selectDest)
        btn_dest.grid(row=1, column=0, sticky=W)
        lbl_pth_src = Label(frm_lbl, height=1, relief=FLAT)
        lbl_pth_des = Label(frm_lbl, height=1, relief=FLAT)
        lbl_pth_src.grid(row=0, column=1, sticky=EW)
        lbl_pth_des.grid(row=1, column=1, sticky=EW)
        return lbl_pth_src, lbl_pth_des

    def makeStatus(self):
        frm_stat = Frame(self)
        frm_stat.pack(side=TOP, anchor=NW, fill=BOTH)
        for name, row, col in self.stat_names:
            lbl = Label(frm_stat, text=name, height=1, relief=FLAT)
            lbl.grid(row=row, column=col, sticky=N)

        def makeblank(row, col):
            lbl = Label(frm_stat, text='N/A', relief=GROOVE)
            lbl.grid(row=row, column=col, sticky=EW)
            return lbl

        lbl_files = makeblank(0, 1)
        lbl_folders = makeblank(0, 3)
        lbl_diff = makeblank(0, 5)
        lbl_total = makeblank(1, 1)
        lbl_prog = makeblank(1, 3)
        return lbl_files, lbl_folders, lbl_diff, lbl_total, lbl_prog

    def makeText(self):
        frm_txt = Frame(self)
        frm_txt.pack(side=TOP, fill=BOTH, expand=YES)
        txt = Text(frm_txt)
        txt.pack(side=TOP, fill=BOTH, expand=YES)
        return txt

    def makeMenu(self):
        frm_menu = Frame(self)
        frm_menu.pack(side=BOTTOM, anchor=NW, fill=X)
        for item in self.menu_list:
            btn = Button(frm_menu, text=item['text'], height=1, width=8,
                         command=item['command'])
            btn.pack(side=item['side'])


###################################
# UI功能
###################################

    def selectSrc(self):
        self.pth_src = askdirectory(initialdir='~', title='Select Source Folder')
        if self.pth_src:
            self.lbl_pth_src.config(text=self.pth_src)

    def selectDest(self):
        self.pth_des = askdirectory(initialdir='~', title='Select Destination Folder')
        if self.pth_des:
            self.lbl_pth_des.config(text=self.pth_des)

    def exit(self):
        if askyesno('Quit', 'Really to quit?'):
            self.quit()

    def start(self):
        self.stat_names = [('NewFiles:', 0, 0), ('NewFolders:', 0, 2),
                           ('DiffFiles:', 0, 4),
                           ('Total:', 1, 0), ('Progress:', 1, 2)]
        self.menu_list = [{'text':'AutoSync', 'command':self.AutoSync, 'side':'left'},
                          {'text':'Compare', 'command':self.compare, 'side':'left'},
                          {'text':'Sync', 'command':self.sync, 'side':'left'},
                          {'text':'Quit', 'command':self.exit, 'side':'right'}]

#    def compare(self):
#        self.lbl_prog.config(text='N/A')
#        self.sync_list = SyncFunc.compare(self.pth_src, self.pth_des,
#                                          lbl_list={'NewFiles':self.lbl_files, 'NewFolders':self.lbl_folders,
#                                                    'Diff':self.lbl_diff, 'Total':self.lbl_total})

    def compare(self):
        self.lbl_prog.config(text='N/A')
        self.sync_list, file_exist = \
            SyncFunc.compare_new(self.pth_src, self.pth_des,
                                 lbl_list={'NewFiles':self.lbl_files, 'NewFolders':self.lbl_folders,
                                           'Total':self.lbl_total})

        self.sync_list.append([])
        _thread.start_new_thread(SyncFunc.compare_exist,
                                 (file_exist, self.pth_src, self.pth_des, self.sync_list[2], self.lbl_diff))

    def sync(self):
        _thread.start_new_thread(SyncFunc.sync,
                                 (self.txt, self.sync_list, self.pth_src, self.pth_des, self.lbl_prog))

    def AutoSync(self):
        pass


"""
###################################
# 同步功能
###################################

    def listdir(self, pth):
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

    def compare(self, pth_src, pth_des):
        file_new = []
        dir_new = []
        file_exist = []

        if not (self.pth_src and os.path.exists(self.pth_src)):
            print('Source Path Not exist!')
            return
        elif not (self.pth_des and os.path.exists(self.pth_des)):
            print('Destination Path Not Exist!')
            if askyesno('Create Destination Path [%s]?' % self.des_pth):
                os.mkdir(self.des_pth)
            else:
                return

        src_pth = self.pth_src if self.pth_src[-1] == '/' else self.pth_src + '/'
        des_pth = self.pth_des if self.pth_des[-1] == '/' else self.pth_des + '/'
        src_pth_list = [x.replace(src_pth, '') for x in self.listdir(src_pth)]
        des_pth_list = [x.replace(des_pth, '') for x in self.listdir(des_pth)]

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
            pth_from = os.path.join(self.pth_src, item)
            pth_to = os.path.join(self.pth_des, item)
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

        self.sync_list = (dir_new, file_new, changed_list)

    def sync(self):
        self.txt.delete(0.0, END)

        for item in self.sync_list[0]:
            pth_to = os.path.join(self.pth_des, item)
            os.mkdir(pth_to)
            self.txt.insert(END, 'Create Path => %s\n' % pth_to)

        for item in self.sync_list[1]:
            pth_to = os.path.join(self.pth_des, item)
            pth_from = os.path.join(self.pth_src, item)
            file_in = open(pth_from, 'rb')
            file_out = open(pth_to, 'wb')
            while True:
                data = file_in.read(2048000)
                if not data: break
                file_out.write(data)
            self.txt.insert(END, 'Creath File ==> %s\n' % pth_to)

        for item in self.sync_list[2]:
            pth_from = os.path.join(self.pth_src, item)
            pth_to = os.path.join(self.pth_des, item)
            src_file = open(pth_from, 'rb')
            des_file = open(pth_to, 'wb')
            while True:
                data = src_file.read(10000000)
                if not data: break
                des_file.write(data)
            self.txt.insert(END, 'Changed >>> %s\n' % pth_from)
"""

if __name__ == '__main__':
    import sys
    class Test(SyncTool):
        def selectSrc(self):
            self.pth_src = r'G:\BackupTest' if sys.platform == 'win32' else r'/Users/joshuapu/Documents/Scripts'
            self.lbl_pth_src.config(text=self.pth_src)

        def selectDest(self):
            self.pth_des = r'Y:\Backup' if sys.platform == 'win32' else r'/Users/joshuapu/Documents/Backup'
            self.lbl_pth_des.config(text=self.pth_des)
    Test()
    mainloop()