__author__ = 'Mario'

import wx
import wx.xrc
import wx.aui

from Simulation import SimulationCtrl
from os.path import isfile
from CanvasView import Canvas
from wx.lib.floatcanvas import NavCanvas
from wx.lib.floatcanvas import FloatCanvas as FC

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

    def __init__( self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 900,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(605, 458),
                                   style=wx.TAB_TRAVERSAL)

        self.m_mgr = wx.aui.AuiManager()
        self.m_mgr.SetManagedWindow( self.pnlDocking )
        self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)

        #self.m_mgr.AddPane( self.pnlDocking, wx.aui.AuiPaneInfo() .Right() .CloseButton( False) .PinButton( True ).Dock().Resizable().FloatingSize( wx.Size( 344,248 ) ).DockFixed( False ).Layer( 2 ) )
        #self.m_treeCtrl1 = wx.TreeCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        #self.m_mgr.AddPane( self.m_treeCtrl1, wx.aui.AuiPaneInfo() .Left() .CloseButton( False ).MaximizeButton( True ).MinimizeButton( True ).PinButton( True ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( False ) )

        self.pnlSimulation = SimulationCtrl(self.pnlDocking)

        self.m_mgr.AddPane(self.pnlSimulation, wx.aui.AuiPaneInfo().Left().CloseButton( False )
                           .MaximizeButton( True ).MinimizeButton( True ).PinButton( True ).Resizable()
                           .MinSize(wx.Size(300,300)).Floatable() )

        #self.pnlPy = PyPanel(self.pnlDocking)
        #self.pnlPy = DrawFrame(self.pnlDocking)

        canvas = Canvas(parent=self.pnlDocking,
                                  ProjectionFun = None,
                                  Debug = 0,
                                  BackgroundColor = "White",
                                  )


        self.m_mgr.AddPane(canvas, wx.aui.AuiPaneInfo().Center().Name("Canvas").Position(0)
                           .CloseButton( False ).MaximizeButton( True ).MinimizeButton( True )
                           .PinButton( True ).Resizable().Floatable().Movable().MinSize(wx.Size(1000,400)) )

        #self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSel)
        '''
        self.m_genericDirCtrl1 = wx.GenericDirCtrl( self, id=wx.ID_ANY, dir=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(450, 300), style=wx.DIRCTRL_3D_INTERNAL|wx.SUNKEN_BORDER, filter=wx.EmptyString, defaultFilter=0)
        self.m_genericDirCtrl1.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSel)
        self.m_genericDirCtrl1.ShowHidden( False )

        #
        self.m_mgr.AddPane( self.m_genericDirCtrl1, wx.aui.AuiPaneInfo() .Left() .CloseButton( False ).MaximizeButton( True ).MinimizeButton( True ).PinButton( True ).Dock().Resizable().FloatingSize( wx.DefaultSize ).DockFixed( False ) )

        self.m_button1 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button1.SetLabel("Run Simulation")
        self.Bind(wx.EVT_BUTTON, self.Buttonclick, self.m_button1)

        #
        self.m_mgr.AddPane( self.m_button1, wx.aui.AuiPaneInfo() .Left() .CloseButton( False ).PinButton( True ).Dock().Resizable().FloatingSize( wx.Size( 104,60 ) ).DockFixed( False ).Layer( 0 ) )

        self.m_button2 = wx.Button( self, wx.ID_ANY, u"MyButton2", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button2.SetLabel("InteractiveGUI")
        self.Bind(wx.EVT_BUTTON, self.Buttonclick2, self.m_button2)

        #
        self.m_mgr.AddPane( self.m_button2, wx.aui.AuiPaneInfo() .Left() .CloseButton( False ).PinButton( True ).Dock().Resizable().FloatingSize( wx.Size( 104,60 ) ).DockFixed( False ).Layer( 0 ) )
        '''
        self.m_mgr.Update()
        self.Centre( wx.BOTH )

        ## Menu stuff
        self.m_statusBar2 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        self.m_menubar2 = wx.MenuBar( 0 )
        self.m_menu3 = wx.Menu()
        self.m_menubar2.Append( self.m_menu3, u"File" )

        self.m_menu4 = wx.Menu()
        self.m_menubar2.Append( self.m_menu4, u"Tools" )
        self.SetMenuBar( self.m_menubar2 )

        self.m_menu5 = wx.Menu()
        self.m_menubar2.Append(self.m_menu5, u"View")
        self.SetMenuBar( self.m_menubar2)

        #print dir(item)
        #print "Type: ", type(item)
    #def BindEvents(self):


    def __del__( self ):
        self.m_mgr.UnInit()

class SimpleFrame(MyFrame1):
    def __init__(self,parent):
        MyFrame1.__init__(self, parent)

    def clearFunc(self, event):
        self.edit.SetValue("")

app = wx.App(False)
frame = SimpleFrame(None)
frame.Show(True)

app.MainLoop()
