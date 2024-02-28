import wx
import wx.lib.mixins.listctrl

class SortedListCtrl(wx.ListCtrl, wx.lib.mixins.listctrl.ColumnSorterMixin):

    def __init__(self, parent):

        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SORT_ASCENDING)
        wx.lib.mixins.listctrl.ColumnSorterMixin.__init__(self, 0)

        self.itemDataMap = self.iteamMap

    def GetListCtrl(self):
        return self