#!/usr/bin/python

import os
import time

import wx


ID_BUTTON = 100
ID_EXIT = 200
ID_SPLITTER = 300


class MyListCtrl(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        files = os.listdir('.')
        self.home = os.path.abspath("C:\\")
        print "HOME!", self.home

        images = ['images/folder-documents.png', 'images/folder.png']
        # # , 'images/source_py.png', 'images/image.png', 'images/pdf.png', 'images/up16.png'

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Ext')
        self.InsertColumn(2, 'Size', wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(3, 'Modified')

        self.SetColumnWidth(0, 220)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 100)
        self.SetColumnWidth(3, 420)

        self.il = wx.ImageList(16, 16)
        for i in images:
            self.il.Add(wx.Bitmap(i))
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.refreshList(files)

    def refreshList(self, files):
        j = 1
        self.InsertStringItem(0, '..')
        self.SetItemImage(0, 5)

        for i in files:
            (name, ext) = os.path.splitext(i)
            ex = ext[1:]
            size = os.path.getsize(i)
            sec = os.path.getmtime(i)
            self.InsertStringItem(j, name)
            self.SetStringItem(j, 1, ex)
            self.SetStringItem(j, 2, str(size) + ' B')
            self.SetStringItem(j, 3, time.strftime('%Y-%m-%d %H:%M', time.localtime(sec)))

            if os.path.isdir(i):
                self.SetItemImage(j, 1)
            else:
                self.SetItemImage(j, 0)
            '''
            elif ex == 'py':
                self.SetItemImage(j, 2)
            elif ex == 'jpg':
                self.SetItemImage(j, 3)
            elif ex == 'pdf':
                self.SetItemImage(j, 4)
            '''

            if (j % 2) == 0:
                self.SetItemBackgroundColour(j, '#e6f1f5')
            j = j + 1

    def clearItems(self):
        self.DeleteAllItems()
        self.refreshList(os.listdir('.'))


class poplistcontrol(wx.ListCtrl):
    def __init__(self, parent, id):
        wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.InsertColumn(0, 'Name')
        # self.InsertColumn(1, 'Ext')
        #self.InsertColumn(2, 'Size', wx.LIST_FORMAT_RIGHT)
        #self.InsertColumn(3, 'Modified')

        self.SetColumnWidth(0, 220)
        #self.SetColumnWidth(1, 70)
        #self.SetColumnWidth(2, 100)
        #self.SetColumnWidth(3, 420)


class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        for name in filenames:
            file = open(name, 'r')


class FileHunter(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)

        self.splitter = wx.SplitterWindow(self, ID_SPLITTER, style=wx.SP_BORDER)
        self.splitter.SetMinimumPaneSize(50)

        self.p1 = MyListCtrl(self.splitter, -1)
        #self.p2 = poplistcontrol(self.splitter, -1)
        #self.splitter.SplitVertically(self.p1, self.p2)

        ## Other
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SPLITTER_DCLICK, self.OnDoubleClick, id=ID_SPLITTER)

        ## List control events
        self.p1.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick)
        self.p1.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDClick)

        ## Toolbar events
        self.Bind(wx.EVT_TOOL, self.OnHomeClick, id=30)
        self.Bind(wx.EVT_TOOL, self.OnBackClick, id=10)
        self.directoryStack = []

        ##Create OnDrag Listener
        self.p1.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)


        ## Drop Target
        #dt = FileDrop(self.p2)
        #self.p2.SetDropTarget(dt)
        #self.p2.InsertItem()
        '''
        DropTarget = FileDrop(self.p2)
        self.p2.SetDropTarget(DropTarget)
        self.p2.InsertColumn(0, 'Filename')
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self)
        '''
        filemenu = wx.Menu()
        filemenu.Append(ID_EXIT, "&Exit", " Terminate the program")
        editmenu = wx.Menu()
        netmenu = wx.Menu()
        showmenu = wx.Menu()
        configmenu = wx.Menu()
        helpmenu = wx.Menu()

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(netmenu, "&Net")
        menuBar.Append(showmenu, "&Show")
        menuBar.Append(configmenu, "&Config")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)

        tb = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        tb.AddSimpleTool(10, wx.Bitmap('images/go-previous.png'), 'Previous')
        tb.AddSimpleTool(20, wx.Bitmap('images/go-up.png'), 'Up one directory')
        tb.AddSimpleTool(30, wx.Bitmap('images/go-home.png'), 'Home')
        tb.AddSimpleTool(40, wx.Bitmap('images/view-refresh.png'), 'Refresh')
        tb.AddSeparator()
        tb.AddSimpleTool(50, wx.Bitmap('images/document-save.png'), 'Editor')
        tb.AddSimpleTool(60, wx.Bitmap('images/draw-star.png'), 'Terminal')
        tb.AddSeparator()
        tb.AddSimpleTool(70, wx.Bitmap('images/help-info.png'), 'Help')
        tb.AddSeparator()

        tb.Realize()

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        '''
        button1 = wx.Button(self, ID_BUTTON + 1, "F3 View")
        button2 = wx.Button(self, ID_BUTTON + 2, "F4 Edit")
        button3 = wx.Button(self, ID_BUTTON + 3, "F5 Copy")
        button4 = wx.Button(self, ID_BUTTON + 4, "F6 Move")
        button5 = wx.Button(self, ID_BUTTON + 5, "F7 Mkdir")
        button6 = wx.Button(self, ID_BUTTON + 6, "F8 Delete")
        button7 = wx.Button(self, ID_BUTTON + 7, "F9 Rename")
        button8 = wx.Button(self, ID_EXIT, "F10 Quit")

        self.sizer2.Add(button1, 1, wx.EXPAND)
        self.sizer2.Add(button2, 1, wx.EXPAND)
        self.sizer2.Add(button3, 1, wx.EXPAND)
        self.sizer2.Add(button4, 1, wx.EXPAND)
        self.sizer2.Add(button5, 1, wx.EXPAND)
        self.sizer2.Add(button6, 1, wx.EXPAND)
        self.sizer2.Add(button7, 1, wx.EXPAND)
        self.sizer2.Add(button8, 1, wx.EXPAND)

        self.Bind(wx.EVT_BUTTON, self.OnExit, id=ID_EXIT)
        '''

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.splitter, 1, wx.EXPAND)
        #self.sizer.Add(self.sizer2,0,wx.EXPAND)
        self.SetSizer(self.sizer)

        size = wx.DisplaySize()
        self.SetSize(size)

        self.sb = self.CreateStatusBar()
        self.sb.SetStatusText(os.getcwd())
        self.Center()
        self.Show(True)

    def OnExit(self, e):
        self.Close(True)

    def OnSize(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)
        self.sb.SetStatusText(os.getcwd())
        event.Skip()

    def OnDoubleClick(self, event):
        size = self.GetSize()
        self.splitter.SetSashPosition(size.x / 2)

    ## List control events
    def OnClick(self, event):
        path = os.path.join(os.getcwd(), event.GetText())
        print path
        self.sb.SetStatusText(path)

    def OnDClick(self, event):
        ## Check if clicked Item is a directory
        dirpath = os.path.join(os.getcwd(), event.GetText())
        if os.path.isdir(dirpath):
            print "Changing path to: ", dirpath
            try:
                self.directoryStack.append(os.getcwd())
                os.chdir(dirpath)
            except WindowsError as e:
                self.directoryStack.append(os.getcwd())
                os.chdir('..')
                print "WindowsError! ", e
        self.p1.clearItems()

    ## Tool bar events
    def OnHomeClick(self, event):
        dirpath = self.p1.home
        try:
            os.chdir(dirpath)
            print "You have returned home: ", dirpath
            self.directoryStack.append(dirpath)
            self.p1.clearItems()
        except:
            print 'Crap happened on the way home'

    def OnBackClick(self, event):
        if len(self.directoryStack) > 0:
            os.chdir(self.directoryStack.pop())
            self.p1.clearItems()

    def onDrag(self, event):
        data = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetIndex()
        filename = obj.GetItem(id).GetText()
        dirname = os.path.dirname(os.path.abspath(os.listdir(".")[0]))
        fullpath = str(os.path.join(dirname, filename))

        data.AddFile(fullpath)

        dropSource = wx.DropSource(obj)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop()
        print fullpath


app = wx.App(0)
FileHunter(None, -1, 'File Hunter')
app.MainLoop()
