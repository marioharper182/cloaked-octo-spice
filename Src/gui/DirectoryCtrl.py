__author__ = 'Mario'
# -*- coding: utf-8 -*-

# ##########################################################################
# # Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

from os.path import isfile

import wx
import wx.xrc

#from ResultsDisplay import ModelFrame
from directoryCtrlPanel import directoryCtrlPanel



###########################################################################
## Class MyPanel2
###########################################################################

class SimulationCtrl(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)
        self.initSizers()
        self.bindEvents()

    def initSizers(self):
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        #self.m_genericDirCtrl = wx.GenericDirCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.DIRCTRL_3D_INTERNAL|wx.SUNKEN_BORDER, wx.EmptyString, 0 )
        self.m_directoryCtrl = directoryCtrlPanel(self)
        #self.m_genericDirCtrl.ShowHidden( False )
        #self.m_genericDirCtrl.SetMinSize( wx.Size( -1,250 ) )

        bSizer1.Add(self.m_directoryCtrl, 100, wx.EXPAND | wx.ALL, 5)

        #bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        #self.m_button1 = wx.Button(self, wx.ID_ANY, u"Run Simulation", wx.DefaultPosition, wx.DefaultSize, 0)
        #bSizer6.Add(self.m_button1, 0, wx.ALL, 5)

        #self.m_button2 = wx.Button(self, wx.ID_ANY, u"Interactive Gui", wx.DefaultPosition, wx.DefaultSize, 0)
        #bSizer6.Add(self.m_button2, 0, wx.ALL, 5)

        #bSizer1.Add(bSizer6, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

    def bindEvents(self): pass
        #self.m_genericDirCtrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSel)
        #self.Bind(wx.EVT_BUTTON, self.Buttonclick, self.m_button1)
        #self.Bind(wx.EVT_BUTTON, self.Buttonclick2, self.m_button2)

    def __del__(self):
        pass

    def OnSel(self, event):
        #item = event.GetItem()
        #print "Event: ", [ "%s" % (x) for x in dir(event)]
        #item = event.GetItem()
        #f = self.m_genericDirCtrl.GetFilePath()
        if isfile(f):
            print f
            self.selectedFile = f

    def Buttonclick2(self, event):
        #GUIframe = DrawFrame(self)
        #GUIframe.Show()
        self.Layout()

    def Buttonclick(self, event):
        #newframe = ModelFrame(self)
        #newframe.Show()
        self.Layout()

