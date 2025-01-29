import sys

from SimpleCutMainFrame import *

if __name__ == '__main__':
    App = wx.App()
    mainFrame = PureClipMainFrame()
    mainFrame.Show(True)
    App.MainLoop()

    # TODO: 解决程序没有彻底退出的问题
    # 猜测是 App.MainLoop 主循环没有彻底结束
    sys.exit(0)
