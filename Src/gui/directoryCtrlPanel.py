# -*- coding: utf-8 -*- 

# ##########################################################################
## Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import os
from dirLstCtrl import MyListCtrl
from images import icons

###########################################################################
## Class directoryCtrlPanel
###########################################################################
[
    PreviousID, UpID, HomeID, SaveID, RefreshID, TerminalID, HelpID
] = [wx.NewId() for _init_ctrls in range(7)]

class directoryCtrlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)

        self.directoryStack = []

        panelSizer = wx.BoxSizer(wx.VERTICAL)

        self.toolbar = self.iconToolBar()

        panelSizer.Add(self.toolbar, 0, wx.EXPAND, 5)

        listCtrlSizer = wx.BoxSizer(wx.VERTICAL)

        listCtrlSizer.SetMinSize(wx.Size(800, 600))
        self.dirCtrl = MyListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(1000, 400),  wx.LC_REPORT)
        listCtrlSizer.Add(self.dirCtrl, 0, wx.ALL, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(600, -1), wx.TE_READONLY)
        bSizer4.Add(self.m_textCtrl1, 0, wx.ALL, 5)

        listCtrlSizer.Add(bSizer4, 1, wx.EXPAND, 5)

        panelSizer.Add(listCtrlSizer, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.SetSizer(panelSizer)
        self.Layout()

    def __del__(self):
        pass

    def iconToolBar(self):
        toolbar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        toolbar.AddSeparator()


        tool = toolbar.AddLabelTool(PreviousID, label='Previous', bitmap = icons.go_previous.GetBitmap() )
        tool = toolbar.AddLabelTool(UpID, label='Up one directory', bitmap = icons.go_up.GetBitmap() )
        tool = toolbar.AddLabelTool(HomeID, label='Go Home', bitmap = icons.go_home.GetBitmap() )
        tool = toolbar.AddLabelTool(RefreshID, label='Refresh', bitmap = icons.view_refresh.GetBitmap() )
        tool = toolbar.AddLabelTool(SaveID, label='Save', bitmap = icons.document_save.GetBitmap() )
        tool = toolbar.AddLabelTool(TerminalID, label='Terminal', bitmap = icons.draw_star.GetBitmap() )
        tool = toolbar.AddLabelTool(HelpID, label='Help', bitmap = icons.help_info.GetBitmap() )

        # # Toolbar events
        self.Bind(wx.EVT_TOOL, self.OnHomeClick, id=HomeID)
        self.Bind(wx.EVT_TOOL, self.OnBackClick, id=PreviousID)


        toolbar.AddSeparator()

        # tb = wx.ToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
        '''
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
        '''
        toolbar.Realize()

        return toolbar


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


    # # List control events
    def OnClick(self, event):
        path = os.path.join(os.getcwd(), event.GetText())
        print path
        self.sb.SetStatusText(path)


    def OnDClick(self, event):
        print "Hello"
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
        self.dirCtrl.clearItems()


    ## Tool bar events
    def OnHomeClick(self, event):
        dirpath = os.path.abspath("C:\\")
        try:
            os.chdir(dirpath)
            print "You have returned home: ", dirpath
            self.directoryStack.append(dirpath)
            self.dirCtrl.clearItems()
        except:
            print 'Crap happened on the way home'


    def OnBackClick(self, event):
        print "Hello World"
        if len(self.directoryStack) > 0:
            os.chdir(self.directoryStack.pop())
            self.dirCtrl.clearItems()


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
