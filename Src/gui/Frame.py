from Src.gui.DirectoryView import directoryCtrlPanel

__author__ = 'Mario'

from os.path import isfile

import wx
import wx.xrc
import wx.aui
from wx.lib.floatcanvas import NavCanvas
from wx.lib.floatcanvas import FloatCanvas as FC

from CanvasView import Canvas


# ##########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(1500, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(605, 458),
                                   style=wx.TAB_TRAVERSAL)

        self.m_mgr = wx.aui.AuiManager()
        self.m_mgr.SetManagedWindow(self.pnlDocking)
        self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)

        self.m_directoryCtrl = directoryCtrlPanel(self.pnlDocking)
        self.m_mgr.AddPane(self.m_directoryCtrl,
                           wx.aui.AuiPaneInfo().Left().CloseButton(False).MaximizeButton(True).MinimizeButton(
                               True).PinButton(True).Resizable().MinSize(wx.Size(500, 500)).Floatable())

        canvas = Canvas(parent=self.pnlDocking, ProjectionFun=None, Debug=0, BackgroundColor="White", )
        self.m_mgr.AddPane(canvas,
                           wx.aui.AuiPaneInfo().Center().Name("Canvas").Position(0).CloseButton(False).MaximizeButton(
                               True).MinimizeButton(True).PinButton(True).Resizable().Floatable().Movable().MinSize(
                               wx.Size(1000, 400)))

        self.m_mgr.Update()
        self.Centre(wx.BOTH)

        ## Menu stuff
        self.m_statusBar2 = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)
        self.m_menubar2 = wx.MenuBar(0)
        self.m_menu3 = wx.Menu()
        self.m_menubar2.Append(self.m_menu3, u"File")

        self.m_menu4 = wx.Menu()
        self.m_menubar2.Append(self.m_menu4, u"Tools")
        self.SetMenuBar(self.m_menubar2)

        self.m_menu5 = wx.Menu()
        self.m_menubar2.Append(self.m_menu5, u"View")
        self.SetMenuBar(self.m_menubar2)

    def __del__(self):
        self.m_mgr.UnInit()


class SimpleFrame(MyFrame1):
    def __init__(self, parent):
        MyFrame1.__init__(self, parent)


    def clearFunc(self, event):
        self.edit.SetValue("")


app = wx.App(False)
frame = SimpleFrame(None)
frame.Show(True)

app.MainLoop()
