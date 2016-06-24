# UI配置
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.filedialog import askdirectory


class SyncUI(Tk):
    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.start()
        self.makeMenu()
        self.lbl_pth_src, self.lbl_pth_des = self.makeLabel()
        self.lbl_files, self.lbl_folders, self.lbl_new, \
        self.lbl_diff, self.lbl_prog = self.makeStatus()

    def makeMenu(self):
        frm_menu = Frame(self)
        frm_menu.pack(side=TOP, fill=X)
        for item in self.menu_items:
            btn = Button(frm_menu, text=item['text'], command=item['command'],
                         height=item['height'], width=item['width'], relief=RIDGE)
            btn.pack(side=item['side'])

    def makeLabel(self):
        frm_lbl = Frame(self)
        frm_lbl.pack(side=TOP, fill=X)
        lbl_src = Label(frm_lbl, text='Source:', height=1, relief=FLAT)
        lbl_src.grid(row=0, column=0, sticky=W)
        lbl_dest = Label(frm_lbl, text='Destin:', height=1, relief=FLAT)
        lbl_dest.grid(row=1, column=0, sticky=W)
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
        lbl_new = makeblank(0, 5)
        lbl_diff = makeblank(0, 7)
        lbl_prog = makeblank(2, 1)
        return lbl_files, lbl_folders, lbl_new, lbl_diff, lbl_prog



    def selectSrc(self):
        self.pth_src = askdirectory(initialdir='/', title='Select Source Folder')
        if self.pth_src:
            self.lbl_pth_src.config(text=self.pth_src)

    def selectDest(self):
        self.pth_des = askdirectory(initialdir='/', title='Select Destination Folder')
        if self.pth_des:
            self.lbl_pth_des.config(text=self.pth_des)

    def quit(self):
        if askyesno('Quit', 'Really to quit?'):
            sys.exit()

    def start(self):
        self.menu_items = [{'text':'Source', 'command':self.selectSrc,
                            'height':1, 'width':7, 'side':'left'},
                           {'text':'Destin', 'command':self.selectDest,
                            'height':1, 'width':7, 'side':'left'},
                           {'text':'Quit', 'command':self.quit,
                            'height':1, 'width':7, 'side':'right'}]
        self.stat_names = [('Files:', 0, 0), ('Folders:', 0, 2),
                           ('New:', 0, 4), ('Diff:', 0, 6),
                           ('Progress:', 2, 0)]



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