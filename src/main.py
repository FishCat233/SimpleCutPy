import sys

from SimpleCutMainFrame import *

if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    App = wx.App()
    mainFrame = SimpleCutPyMainFrame()
    mainFrame.Show(True)
    App.MainLoop()

    sys.exit(0)
