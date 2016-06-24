# UI配置
from tkinter import *
from tkinter.messagebox import askyesno
from tkinter.filedialog import askdirectory


class SyncUI(Tk):
    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.start()
        self.makeMenu()

    def makeMenu(self):
        frm_menu = Frame(self)
        frm_menu.pack(side=TOP, fill=X)
        for item in self.menu_items:
            btn = Button(frm_menu, text=item['text'], command=item['command'],
                         height=item['height'], width=item['width'], relief=RIDGE)
            btn.pack(side=item['side'])

    def selectSrc(self):
        self.pth_src = askdirectory(initialdir='/', title='Select Source Folder')

    def selectDest(self):
        self.pth_des = askdirectory(initialdir='/', title='Select Destination Folder')

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



if __name__ == '__main__':
    class Test(SyncUI):
        def quit(self):
            sys.exit()
    Test()
    mainloop()