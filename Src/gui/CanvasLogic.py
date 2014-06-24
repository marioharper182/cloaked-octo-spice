__author__ = 'Mario'

import wx

ver = 'local'

import sys
sys.path.append("..")
from wx.lib.floatcanvas import NavCanvas,  Resources
from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas.Utilities import BBox

import numpy as N
class CanvasLogic:
    def __init__(self, Canvas, Model):
        self.Canvas=Canvas
        self.Model=Model
        self.initBindings()


    def initBindings(self):
        self.Canvas.Bind(FC.EVT_MOTION, self.OnMove )
        self.Canvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp )

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        and moves the object it is clicked on

        """
        #self.SetStatusText("%.4f, %.4f"%tuple(event.Coords))

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

class MovingObjectMixin:
    """
    Methods required for a Moving object

    """
    def GetOutlinePoints(self):
        """
        Returns a set of points with which to draw the outline when moving the
        object.

        Points are a NX2 array of (x,y) points in World coordinates.


        """
        BB = self.BoundingBox
        OutlinePoints = N.array( ( (BB[0,0], BB[0,1]),
                                   (BB[0,0], BB[1,1]),
                                   (BB[1,0], BB[1,1]),
                                   (BB[1,0], BB[0,1]),
                                 )
                               )

        return OutlinePoints

class ConnectorObjectMixin:
    """
    Mixin class for DrawObjects that can be connected with lines

    Note that this version only works for Objects that have an "XY" attribute:
      that is, one that is derived from XHObjectMixin.

    """

    def GetConnectPoint(self):
        return self.XY

class MovingBitmap(FC.ScaledBitmap, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  ScaledBitmap, MovingObjectMixin and ConnectorObjectMixin
    pass

class MovingCircle(FC.Circle, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  Circle MovingObjectMixin and ConnectorObjectMixin
    pass


class MovingGroup(FC.Group, MovingObjectMixin, ConnectorObjectMixin):

    def GetConnectPoint(self):
        return self.BoundingBox.Center

class NodeObject(FC.Group, MovingObjectMixin, ConnectorObjectMixin):
    """
    A version of the moving group for nodes -- an ellipse with text on it.
    """
    def __init__(self,
                 Label,
                 XY,
                 WH,
                 BackgroundColor = "BLUE",
                 TextColor = "Black",
                 InForeground  = False,
                 IsVisible = True):
        XY = N.asarray(XY, N.float).reshape(2,)
        WH = N.asarray(WH, N.float).reshape(2,)
        Label = FC.ScaledText(Label,
                        XY,
                        Size = WH[1] / 2.0,
                        Color = TextColor,
                        Position = 'cc',
                        )
        self.Ellipse = FC.Ellipse( (XY - WH/2.0),
                               WH,
                               FillColor = BackgroundColor,
                               LineStyle = None,
                               )
        FC.Group.__init__(self, [self.Ellipse, Label], InForeground, IsVisible)

    def GetConnectPoint(self):
        return self.BoundingBox.Center


class MovingText(FC.ScaledText, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  ScaledBitmap, MovingObjectMixin and ConnectorObjectMixin
    pass

class MovingTextBox(FC.ScaledTextBox, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    ## All we need to do is is inherit from:
    ##  ScaledBitmap, MovingObjectMixin and ConnectorObjectMixin
    pass

class ConnectorLine(FC.LineOnlyMixin, FC.DrawObject,):
    """

    A Line that connects two objects -- it uses the objects to get its coordinates
    The objects must have a GetConnectPoint() method.

    """
    ##fixme: this should be added to the Main FloatCanvas Objects some day.
    def __init__(self,
                 Object1,
                 Object2,
                 LineColor = "Black",
                 LineStyle = "Solid",
                 LineWidth    = 1,
                 InForeground = False):
        FC.DrawObject.__init__(self, InForeground)

        self.Object1 =  Object1
        self.Object2 =  Object2
        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth

        self.CalcBoundingBox()
        self.SetPen(LineColor,LineStyle,LineWidth)

        self.HitLineWidth = max(LineWidth,self.MinHitLineWidth)

    def CalcBoundingBox(self):
        self.BoundingBox = BBox.fromPoints((self.Object1.GetConnectPoint(),
                                            self.Object2.GetConnectPoint()) )
        if self._Canvas:
            self._Canvas.BoundingBoxDirty = True


    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = N.array( (self.Object1.GetConnectPoint(),
                           self.Object2.GetConnectPoint()) )
        Points = WorldToPixel(Points)
        dc.SetPen(self.Pen)
        dc.DrawLines(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawLines(Points)


class TriangleShape1(FC.Polygon, MovingObjectMixin):

    def __init__(self, XY, L):

        """
        An equilateral triangle object
        XY is the middle of the triangle
        L is the length of one side of the Triangle
        """

        XY = N.asarray(XY)
        XY.shape = (2,)

        Points = self.CompPoints(XY, L)

        FC.Polygon.__init__(self, Points,
                                  LineColor = "Black",
                                  LineStyle = "Solid",
                                  LineWidth    = 2,
                                  FillColor    = "Red",
                                  FillStyle    = "Solid")
    ## Override the default OutlinePoints
    def GetOutlinePoints(self):
        return self.Points

    def CompPoints(self, XY, L):
        c = L/ N.sqrt(3)

        Points = N.array(((0, c),
                          ( L/2.0, -c/2.0),
                          (-L/2.0, -c/2.0)),
                          N.float_)

        Points += XY
        return Points

class TreeNode:
    dx = 15
    dy = 4
    def __init__(self, name, Children = []):
        self.Name = name
        #self.parent = None -- Is this needed?
        self.Children = Children
        self.Point = None # The coords of the node.

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