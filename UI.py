# UI配置
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.filedialog import askdirectory


class SyncUI(Tk):
    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.start()
        self.lbl_pth_src, self.lbl_pth_des = self.makeLabel()
        self.lbl_files, self.lbl_folders, self.lbl_diff, \
        self.lbl_total, self.lbl_prog = self.makeStatus()
        self.txt = self.makeText()
        self.makeMenu()

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
        return lbl_files, lbl_folders, lbl_diff, lbl_total,lbl_prog

    def makeText(self):
        frm_txt = Frame(self)
        frm_txt.pack(side=TOP, fill=BOTH, expand=YES)
        txt = Text(frm_txt)
        txt.pack(side=TOP, fill=BOTH, expand=YES)
        return txt

    def makeMenu(self):
        frm_menu = Frame(self)
        frm_menu.pack(side=BOTTOM, anchor=NW, fill=X)
        btn_sync = Button(frm_menu, text='Sync', height=1, width=7,
                          command=self.sync)
        btn_sync.pack(side=LEFT, anchor=W)
        btn_quit = Button(frm_menu, text='Quit', height=1, width=7,
                          command=self.quit)
        btn_quit.pack(side=RIGHT, anchor=E)


###################################
# 功能
###################################

    def selectSrc(self):
        self.pth_src = askdirectory(initialdir='/', title='Select Source Folder')
        if self.pth_src:
            self.lbl_pth_src.config(text=self.pth_src)

    def selectDest(self):
        self.pth_des = askdirectory(initialdir='/', title='Select Destination Folder')
        if self.pth_des:
            self.lbl_pth_des.config(text=self.pth_des)

    def sync(self):
        raise NotImplementedError

    def quit(self):
        if askyesno('Quit', 'Really to quit?'):
            sys.exit()

    def start(self):
        self.stat_names = [('NewFiles:', 0, 0), ('NewFolders:', 0, 2),
                           ('DiffFiles:', 0, 4),
                           ('Total:', 1, 0), ('Progress:', 1, 2)]



if __name__ == '__main__':
    class Test(SyncUI):
        def __init__(self):
            SyncUI.__init__(self)
            self.lbl_pth_src.config(text='/This/Is/Test/Path/For/Source')
            self.lbl_pth_des.config(text='/That/Is/Test/Path/For/D/D/D/Des-tination/!/!!!!!!!!')
        def quit(self):
            sys.exit()
    Test()
    mainloop()