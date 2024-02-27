import wx
from PureClipMainFrame import *
from DataUtils import *

if __name__ == '__main__':
    App = wx.App()
    mainFrame = PureClipMainFrame(None)
    mainFrame.Show(True)
    App.MainLoop()