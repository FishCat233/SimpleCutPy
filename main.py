from PureClipMainFrame import *

if __name__ == '__main__':
    App = wx.App()
    mainFrame = PureClipMainFrame(debug_log_level=3)
    mainFrame.Show(True)
    App.MainLoop()
