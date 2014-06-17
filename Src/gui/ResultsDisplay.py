__author__ = 'Mario'

import wx
import pygame
#from Frame import MyFrame1

class PygameDisplay(wx.Window):
    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.parent = parent
        self.hwnd = self.GetHandle()

        self.size = self.GetSizeTuple()
        self.size_dirty = True

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.fps = 30.0
        self.timespacing = 1000.0 / self.fps
        self.timer.Start(self.timespacing, False)

        self.linespacing = 5

    def Update(self, event):
        # Any update tasks would go here (moving sprites, advancing animation frames etc.)
        self.Redraw()

    def Redraw(self):
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False

        self.screen.fill((0,0,0))

        cur = 0

        w, h = self.screen.get_size()
        while cur <= h:
            pygame.draw.aaline(self.screen, (255, 255, 255), (0, h - cur), (cur, 0))

            cur += self.linespacing

        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.ImageFromData(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
        dc = wx.ClientDC(self)  # Device context for drawing the bitmap
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        del dc

    def OnPaint(self, event):
        self.Redraw()
        event.Skip()  # Make sure the parent frame gets told to redraw as well

    def OnSize(self, event):
        self.size = self.GetSizeTuple()
        self.size_dirty = True

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        # This may or may not be necessary now that Pygame is just drawing to surfaces
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)


class ModelDisplay(PygameDisplay):
    def __init__(self, parent, id):
        PygameDisplay.__init__(self, parent, id)
        pygame.font.init()
        self.mainfont = pygame.font.Font(None, 40)
        self.text = self.mainfont.render("Showing Simulation Results", True, (255, 0, 0))
        self.borw = True  # True = draw a black background, False = draw a white background
        self.points = []  # A list of points to draw

        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

    def Update(self, event):
        PygameDisplay.Update(self, event)
        #self.borw = not self.borw  # Alternate the background colour
        #self.redraw()

        for i, point in enumerate(self.points):  # Slide all the points down and slightly to the right
            self.points[i] = (point[0] + 0.1, point[1] + 1)

    def Redraw(self):
        # If the size has changed, create a new surface to match it
        if self.size_dirty:
            self.screen = pygame.Surface(self.size, 0, 32)
            self.size_dirty = False

        # Draw the background
        if self.borw:
            self.screen.fill((0, 0, 0))
        else:
            self.screen.fill((255, 255, 255))

        self.screen.blit(self.text, (0, 0))

        # Draw circles at all the stored points
        for point in self.points:
            pygame.draw.circle(self.screen, (0, 255, 0), (int(point[0]), int(point[1])), 5)

        s = pygame.image.tostring(self.screen, 'RGB')  # Convert the surface to an RGB string
        img = wx.ImageFromData(self.size[0], self.size[1], s)  # Load this string into a wx image
        bmp = wx.BitmapFromImage(img)  # Get the image in bitmap form
        dc = wx.ClientDC(self)  # Device context for drawing the bitmap
        dc.DrawBitmap(bmp, 0, 0, False)  # Blit the bitmap image to the display
        del dc

    def OnClick(self, event):
        self.points.append(event.GetPositionTuple())  # Add a new point at the mouse position


class ModelFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, size = (600, 300), style = wx.CAPTION | wx.SYSTEM_MENU | wx.CLOSE_BOX)

        self.display = ModelDisplay(self, -1)

        self.SetTitle("ModelFrame")

