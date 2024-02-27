# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.1.0-0-g733bf3d)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Pure Clip", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		gSizer1 = wx.GridSizer( 0, 3, 0, 0 )

		self.m_staticText1 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"文件名", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		gSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"开始时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		gSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"结束时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		gSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )


		bSizer4.Add( gSizer1, 1, wx.EXPAND, 5 )

		self.AddFileBtn = wx.Button( self.m_panel2, wx.ID_ANY, u"添加文件", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.AddFileBtn, 0, wx.ALL, 5 )


		self.m_panel2.SetSizer( bSizer4 )
		self.m_panel2.Layout()
		bSizer4.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"素材设置", True )
		self.m_panel3 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"导出文件名（带扩展名）：", wx.DefaultPosition, wx.Size( -1,25 ), 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer6.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_textCtrl2 = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 270,25 ), 0 )
		self.m_textCtrl2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer6.Add( self.m_textCtrl2, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )

		self.m_staticText7 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"帮助：\n1. 在不填写具体路径的情况下，会默认导出到当前路径。\n2. 没了", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )

		bSizer5.Add( self.m_staticText7, 0, wx.ALL, 5 )

		self.ExportBtn = wx.Button( self.m_panel3, wx.ID_ANY, u"导出", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer5.Add( self.ExportBtn, 0, wx.ALL, 5 )


		self.m_panel3.SetSizer( bSizer5 )
		self.m_panel3.Layout()
		bSizer5.Fit( self.m_panel3 )
		self.m_notebook1.AddPage( self.m_panel3, u"导出设置", False )
		self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"关于 Pure Clip：\n一个用于进行简单剪切工作的开源迷你剪辑软件。\n\n项目地址：\n\n--FishCat233\n2024.2.27\n\nPure Clip 版本号\n0.1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer8.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.ProjectWebBtn = wx.Button( self.m_panel4, wx.ID_ANY, u"访问项目", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.ProjectWebBtn, 0, wx.ALL, 5 )


		self.m_panel4.SetSizer( bSizer8 )
		self.m_panel4.Layout()
		bSizer8.Fit( self.m_panel4 )
		self.m_notebook1.AddPage( self.m_panel4, u"关于", False )

		bSizer3.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


		self.SetSizer( bSizer3 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.AddFileBtn.Bind( wx.EVT_BUTTON, self.AddFileBtnOnClick )
		self.ExportBtn.Bind( wx.EVT_BUTTON, self.ExportBtnOnClick )
		self.ProjectWebBtn.Bind( wx.EVT_BUTTON, self.ProjectWebBtnOnClick )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def AddFileBtnOnClick( self, event ):
		event.Skip()

	def ExportBtnOnClick( self, event ):
		event.Skip()

	def ProjectWebBtnOnClick( self, event ):
		event.Skip()


