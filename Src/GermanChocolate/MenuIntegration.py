#!/usr/bin/python

# filedrop.py

import wx
import os

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.panel = wx.Panel(self)
        self.dir = wx.GenericDirCtrl(self.panel, size=(200, -1), style=wx.DIRCTRL_DIR_ONLY)
        self.files = wx.ListCtrl(self.panel, style=wx.LC_LIST)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.dir, flag=wx.EXPAND)
        self.sizer.Add(self.files, proportion=1, flag=wx.EXPAND)

        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.panel.SetSizerAndFit(self.border)
        self.Show()

        self.dir.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect)


    def OnSelect(self, e):
        self.files.ClearAll()
        list = os.listdir(self.dir.GetPath())
        for a in reversed(list):
            self.files.InsertStringItem(0, a)

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):

        for name in filenames:
            try:
                file = open(name, 'r')
                text = file.read()
                self.window.WriteText(text)
                file.close()
            except IOError, error:
                dlg = wx.MessageDialog(None, 'Error opening file\n' + str(error))
                dlg.ShowModal()
            except UnicodeDecodeError, error:
                dlg = wx.MessageDialog(None, 'Cannot open non ascii files\n' + str(error))
                dlg.ShowModal()

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(600, 400))
        self.text = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE)
        dt = FileDrop(self.text)
        self.text.SetDropTarget(dt)
        self.Centre()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, '')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()