__author__ = 'Mario'

import wx
import sys
sys.path.append("..")
from wx.lib.floatcanvas import NavCanvas
from wx.lib.floatcanvas import FloatCanvas as FC

from CanvasLogic import LayoutTree, NodeObject, MovingTextBox, TraverseTree, ConnectorLine

class TreeNode:
    dx = 15
    dy = 4
    def __init__(self, name, Children = []):
        self.Name = name
        self.Children = Children
        self.Point = None # The coords of the node.

    def __str__(self):
        return "TreeNode: %s"%self.Name
    __repr__ = __str__


## Build Tree:
'''
leaves = [TreeNode(name) for name in ["Result 1","Result 2"] ]
VP1 = TreeNode("Subset1", Children = leaves)
VP2 = TreeNode("IsolatedResult1")

Model1 = TreeNode("Model1", [VP1, VP2])
Model2 = TreeNode("Model2", [TreeNode("Result1"), TreeNode("Result2")])
elements = TreeNode("Root", [Model1, Model2])
'''
Result = TreeNode("Result")
Branch1 = TreeNode("Branch1", [Result])
elements1 = TreeNode("None1", [Branch1])
elements2 = TreeNode("None2", [Branch1])

class Canvas(NavCanvas.NavCanvas):


    def __init__(self, *args, **kwargs):
        NavCanvas.NavCanvas.__init__(self, *args,**kwargs)


        self.elements1 = elements1
        LayoutTree(self.elements1, 0, 0, 3)
        self.AddTree(self.elements1)

        self.elements2 = elements2
        LayoutTree(self.elements2, 0, 0, 1)
        self.AddTree(self.elements2)


        self.Canvas.ZoomToBB()
        self.MoveObject = None
        self.Moving = False

        self.initBindings()


    def initBindings(self):
        self.Canvas.Bind(FC.EVT_MOTION, self.OnMove )
        self.Canvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp )

    def OnMove(self, event):

        if self.Moving:
            dxy = event.GetPosition() - self.StartPoint
            # Draw the Moving Object:
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.MoveObject is not None:
                dc.DrawPolygon(self.MoveObject)
            self.MoveObject = self.StartObject + dxy
            dc.DrawPolygon(self.MoveObject)

    def OnLeftUp(self, event):
        if self.Moving:
            self.Moving = False
            if self.MoveObject is not None:
                dxy = event.GetPosition() - self.StartPoint
                dxy = self.Canvas.ScalePixelToWorld(dxy)
                self.MovingObject.Move(dxy)
            self.Canvas.Draw(True)

    def AddTree(self, root):
        Nodes = []
        Connectors = []
        EllipseW = 15
        EllipseH = 4
        def CreateObject(node):
            if node.Children:
                object = NodeObject(node.Name,
                                    node.Point,
                                    (15, 4),
                                    BackgroundColor = "LIGHT BLUE",
                                    TextColor = "Black",
                                    )
            else:
                object = MovingTextBox(node.Name,
                                    node.Point,
                                    2.0,
                                    BackgroundColor = "YELLOW",
                                    Color = "Black",
                                    Position = "cl",
                                    PadSize = 1
                                    )
            node.DrawObject = object
            Nodes.append(object)
        def AddConnectors(node):
            for child in node.Children:
                Connector = ConnectorLine(node.DrawObject, child.DrawObject, LineWidth=3, LineColor="Red")
                Connectors.append(Connector)
        ## create the Objects
        TraverseTree(root, CreateObject)
        ## create the Connectors
        TraverseTree(root, AddConnectors)
        ## Add the connectors to the Canvas first, so they are underneath the nodes
        self.Canvas.AddObjects(Connectors)
        ## now add the nodes
        self.Canvas.AddObjects(Nodes)
        # Now bind the Nodes -- DrawObjects must be Added to a Canvas before they can be bound.
        for node in Nodes:
            #pass
            node.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)



    def ObjectHit(self, object):
        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoordsPixel
            self.StartObject = self.Canvas.WorldToPixel(object.GetOutlinePoints())
            self.MoveObject = None
            self.MovingObject = object


    def LayoutTree(root, x, y, level):
        NumNodes = len(root.Children)
        root.Point = (x,y)
        x += root.dx
        y += (root.dy * level * (NumNodes-1) / 2.0)
        for node in root.Children:
            LayoutTree(node, x, y, level-1)
            y -= root.dy * level

    def TraverseTree(root, func):
        func(root)
        for child in (root.Children):
            TraverseTree(child, func)

#class DrawFrame(wx.Frame):
class MyFrame2(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                        title = wx.EmptyString, pos = wx.DefaultPosition,
                        size = wx.Size( 900,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        draw = Canvas(self )
        '''
        canvas = NavCanvas.NavCanvas(id=wx.ID_ANY,parent=self,
                          ProjectionFun = None,
                          Debug = 0,
                          BackgroundColor = "White",
                          )
        '''


def SimpleFrame(parent):
    return MyFrame2(parent)
'''
app = wx.App(False)
frame = SimpleFrame(None)
frame.Show(True)

app.MainLoop()
'''

