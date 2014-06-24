from Src.gui.DirectoryView import DirectoryCtrlView

__author__ = 'Mario'

import wx
import wx.xrc
import wx.aui

from CanvasView import Canvas
from CanvasLogic import CanvasLogic
from DirectoryView import DirectoryCtrlView


# ##########################################################################
# # Class MainFrame
# ##########################################################################

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                          size=wx.Size(1500, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.initAUIManager()
        self.initSystem()
        self.initMenu()


    def initSystem(self):
        self.canvasLogic = CanvasLogic(Canvas=self.canvas)

    def initAUIManager(self):
        self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(605, 458),
                                   style=wx.TAB_TRAVERSAL)

        self.m_mgr = wx.aui.AuiManager()
        self.m_mgr.SetManagedWindow(self.pnlDocking)
        self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)

        self.m_directoryCtrl = DirectoryCtrlView(self.pnlDocking)
        self.m_mgr.AddPane(self.m_directoryCtrl,
                           wx.aui.AuiPaneInfo().Left().CloseButton(False).MaximizeButton(True).MinimizeButton(
                               True).PinButton(True).Resizable().MinSize(wx.Size(500, 500)).Floatable())

        self.canvas = Canvas(parent=self.pnlDocking, ProjectionFun=None, Debug=0, BackgroundColor="White", )
        self.m_mgr.AddPane(self.canvas,
                           wx.aui.AuiPaneInfo().Center().Name("Canvas").Position(0).CloseButton(False).MaximizeButton(
                               True).MinimizeButton(True).PinButton(True).Resizable().Floatable().Movable().MinSize(
                               wx.Size(1000, 400)))

        self.m_mgr.Update()

    def initMenu(self):
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

        wx.CallAfter(self._postStart)

    def _postStart(self):
        ## Starts stuff after program has initiated
        self.canvas.ZoomToFit(Event=None)

    def __del__(self):
        self.m_mgr.UnInit()


class SimpleFrame(MainFrame):
    def __init__(self, parent):
        MainFrame.__init__(self, parent)


app = wx.App(False)
frame = SimpleFrame(None)
frame.Show(True)

app.MainLoop()
