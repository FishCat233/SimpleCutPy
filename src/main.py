import sys

from SimpleCutMainFrame import *

if __name__ == '__main__':
    import logging

    # 配置日志记录
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='SimpleCut.log',
                        filemode='w'
                        )

    App = wx.App()
    mainFrame = SimpleCutPyMainFrame()
    mainFrame.Show(True)
    App.MainLoop()

    sys.exit(0)
