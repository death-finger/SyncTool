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
        scl = Scrollbar(frm_txt)
        scl.pack(side=RIGHT, fill=Y)
        txt = Text(frm_txt, wrap=NONE)
        txt.pack(side=TOP, fill=BOTH, expand=YES)
        scl.config(command=txt.yview)
        txt.config(yscrollcommand=scl.set)
        return txt

    def makeMenu(self):
        frm_menu = Frame(self)
        frm_menu.pack(side=BOTTOM, anchor=NW, fill=X)
        btn_compare = Button(frm_menu, text='Compare', height=1, width=8, command=self.compare)
        btn_compare.pack(side=LEFT)
        self.btn_sync = Button(frm_menu, text='Sync', height=1, width=8, command=self.sync,
                          state=DISABLED)
        self.btn_sync.pack(side=LEFT)
        btn_quit = Button(frm_menu, text='Quit', height=1, width=8, command=self.exit)
        btn_quit.pack(side=RIGHT)

        #   btn = Button(frm_menu, text=item['text'], height=1, width=8,
        #                 command=item['command'])
        #    btn.pack(side=item['side'])


###################################
# UI功能
###################################

    def selectSrc(self):
        self.pth_src = askdirectory(initialdir='~', title='Select Source Folder')
        if self.pth_src:
            self.lbl_pth_src.config(text=self.pth_src)
            self.btn_sync.config(state=DISABLED)

    def selectDest(self):
        self.pth_des = askdirectory(initialdir='~', title='Select Destination Folder')
        if self.pth_des:
            self.lbl_pth_des.config(text=self.pth_des)
            self.btn_sync.config(state=DISABLED)

    def exit(self):
        if askyesno('Quit', 'Really to quit?'):
            self.quit()

    def start(self):
        self.stat_names = [('NewFiles:', 0, 0), ('NewFolders:', 0, 2),
                           ('DiffFiles:', 0, 4),
                           ('Total:', 1, 0), ('Progress:', 1, 2)]
        self.menu_list = [{'text':'Compare', 'command':self.compare, 'side':'left'},
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
                                 (file_exist, self.pth_src, self.pth_des, self.sync_list[2],
                                  self.lbl_diff, self.btn_sync))

    def sync(self):
        _thread.start_new_thread(SyncFunc.sync,
                                 (self.txt, self.sync_list, self.pth_src, self.pth_des, self.lbl_prog))



if __name__ == '__main__':
    import sys
    class Test(SyncTool):
        def selectSrc(self):
            self.pth_src = r'G:\BackupTest' if sys.platform == 'win32' else r'/Users/joshuapu/Documents/Scripts'
            self.lbl_pth_src.config(text=self.pth_src)
            self.btn_sync.config(state=DISABLED)


        def selectDest(self):
            self.pth_des = r'Y:\Backup' if sys.platform == 'win32' else r'/Users/joshuapu/Documents/Backup'
            self.lbl_pth_des.config(text=self.pth_des)
            self.btn_sync.config(state=DISABLED)

    Test()
    mainloop()