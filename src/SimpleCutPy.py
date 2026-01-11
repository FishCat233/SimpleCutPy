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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Simple Cut", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( 500,300 ), wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.list_ctrl = wx.ListCtrl( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_SORT_ASCENDING )
		self.list_ctrl.SetMinSize( wx.Size( 470,130 ) )

		bSizer4.Add( self.list_ctrl, 0, wx.ALL, 5 )

		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText71 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"开始时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )

		bSizer9.Add( self.m_staticText71, 0, wx.ALL, 5 )

		self.StartTimeCtrl = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.StartTimeCtrl, 0, wx.ALL, 5 )


		bSizer81.Add( bSizer9, 1, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText8 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"结束时间", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer10.Add( self.m_staticText8, 0, wx.ALL, 5 )

		self.EndTimeCtrl = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.EndTimeCtrl, 0, wx.ALL, 5 )


		bSizer81.Add( bSizer10, 1, wx.EXPAND, 5 )


		bSizer4.Add( bSizer81, 1, wx.EXPAND, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.AddFileBtn = wx.Button( self.m_panel2, wx.ID_ANY, u"添加文件", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.AddFileBtn, 0, wx.ALL, 5 )

		self.RemoveBtn = wx.Button( self.m_panel2, wx.ID_ANY, u"移除文件", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.RemoveBtn, 0, wx.ALL, 5 )

		self.MovUpBtn = wx.Button( self.m_panel2, wx.ID_ANY, u"向上移动", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.MovUpBtn, 0, wx.ALL, 5 )

		self.MovDownBtn = wx.Button( self.m_panel2, wx.ID_ANY, u"向下移动", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.MovDownBtn, 0, wx.ALL, 5 )

		self.ClearAllBtn = wx.Button( self.m_panel2, wx.ID_ANY, u"清除全部", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.ClearAllBtn, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )


		self.m_panel2.SetSizer( bSizer4 )
		self.m_panel2.Layout()
		bSizer4.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"素材设置", False )
		self.m_panel3 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		self.export_ctrl = wx.StaticText( self.m_panel3, wx.ID_ANY, u"导出文件名（带扩展名）：", wx.DefaultPosition, wx.Size( -1,25 ), 0 )
		self.export_ctrl.Wrap( -1 )

		bSizer6.Add( self.export_ctrl, 0, wx.ALL, 5 )

		self.ExportNameCtrl = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 270,25 ), 0 )
		self.ExportNameCtrl.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer6.Add( self.ExportNameCtrl, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )

		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText81 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"文件大小控制：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText81.Wrap( -1 )

		bSizer12.Add( self.m_staticText81, 0, wx.ALL, 5 )

		SizeControlModeChoices = [ u"x264", u"mbps", u"不控制" ]
		self.SizeControlMode = wx.Choice( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, SizeControlModeChoices, 0 )
		self.SizeControlMode.SetSelection( 0 )
		self.SizeControlMode.SetMinSize( wx.Size( 200,-1 ) )

		bSizer12.Add( self.SizeControlMode, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer12, 1, wx.EXPAND, 5 )

		bSizer121 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText811 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"导出码率（Mbps）：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText811.Wrap( -1 )

		bSizer121.Add( self.m_staticText811, 0, wx.ALL, 5 )

		self.MbpsCtrl = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 295,-1 ), 0 )
		bSizer121.Add( self.MbpsCtrl, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer121, 1, wx.EXPAND, 5 )

		bSizer101 = wx.BoxSizer( wx.HORIZONTAL )

		self.export_ctrl1 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"导出路径：", wx.DefaultPosition, wx.Size( -1,25 ), 0 )
		self.export_ctrl1.Wrap( -1 )

		bSizer101.Add( self.export_ctrl1, 0, wx.ALL, 5 )

		self.ExportPathCtrl = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 350,25 ), 0 )
		self.ExportPathCtrl.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer101.Add( self.ExportPathCtrl, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer101, 1, wx.EXPAND, 5 )

		bSizer122 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText812 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"多音轨处理：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText812.Wrap( -1 )

		bSizer122.Add( self.m_staticText812, 0, wx.ALL, 5 )

		MultiTrackModeChoices = [ u"只选择第一个音轨", u"全部合并为单音轨", u"上面两个都要（两次输出）" ]
		self.MultiTrackMode = wx.Choice( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, MultiTrackModeChoices, 0 )
		self.MultiTrackMode.SetSelection( 0 )
		self.MultiTrackMode.SetMinSize( wx.Size( 200,-1 ) )

		bSizer122.Add( self.MultiTrackMode, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer122, 1, wx.EXPAND, 5 )

		bSizer16 = wx.BoxSizer( wx.HORIZONTAL )

		self.ExportBtn = wx.Button( self.m_panel3, wx.ID_ANY, u"导出", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer16.Add( self.ExportBtn, 0, wx.ALL, 5 )


		bSizer5.Add( bSizer16, 1, wx.EXPAND, 5 )


		self.m_panel3.SetSizer( bSizer5 )
		self.m_panel3.Layout()
		bSizer5.Fit( self.m_panel3 )
		self.m_notebook1.AddPage( self.m_panel3, u"导出设置", True )
		self.m_panel41 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		self.IntroductionText = wx.StaticText( self.m_panel41, wx.ID_ANY, u"第一步，添加文件\n第二步，设置时间\n第三步，填写导出设置\n第四步，点击导出按钮\n\n如果不知道有些参数有什么用可以不填，应用会使用默认的设置\n\n小技巧：\n- 起止时间里的空格会被替换为“:”，例如“01 20\"会被替换为\"01:20\"\n- 起止时间如果是\"开头\"或者\"结尾\"，则不会对开始时间和结尾时间进行选择", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.IntroductionText.Wrap( -1 )

		self.IntroductionText.SetMinSize( wx.Size( 460,290 ) )

		bSizer13.Add( self.IntroductionText, 0, wx.ALL, 5 )


		self.m_panel41.SetSizer( bSizer13 )
		self.m_panel41.Layout()
		bSizer13.Fit( self.m_panel41 )
		self.m_notebook1.AddPage( self.m_panel41, u"使用说明", False )
		self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"关于 Simple Cut Py：\n一个用于进行简单剪切工作的开源迷你剪辑软件。\n\n项目地址：\n\n--FishCat233\n2024.2.27", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer8.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.VersionText = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Simple Cut Py 版本号\n{VERSION}", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.VersionText.Wrap( -1 )

		bSizer8.Add( self.VersionText, 0, wx.ALL, 5 )

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
		self.list_ctrl.Bind( wx.EVT_DROP_FILES, self.list_ctrl_on_drop_files )
		self.list_ctrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.on_list_item_selected )
		self.StartTimeCtrl.Bind( wx.EVT_TEXT, self.on_start_time_ctrl_text )
		self.EndTimeCtrl.Bind( wx.EVT_TEXT, self.on_end_time_ctrl_text )
		self.AddFileBtn.Bind( wx.EVT_BUTTON, self.on_add_file_button_click )
		self.RemoveBtn.Bind( wx.EVT_BUTTON, self.on_remove_file_button_click )
		self.MovUpBtn.Bind( wx.EVT_BUTTON, self.on_move_up_file_button_click )
		self.MovDownBtn.Bind( wx.EVT_BUTTON, self.on_move_down_file_button_click )
		self.ClearAllBtn.Bind( wx.EVT_BUTTON, self.on_clear_all_button_click )
		self.MbpsCtrl.Bind( wx.EVT_TEXT, self.on_size_control_mode_change )
		self.ExportBtn.Bind( wx.EVT_BUTTON, self.on_export_button_click )
		self.ProjectWebBtn.Bind( wx.EVT_BUTTON, self.on_open_project_website_button_click )

	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def list_ctrl_on_drop_files( self, event ):
		event.Skip()

	def on_list_item_selected( self, event ):
		event.Skip()

	def on_start_time_ctrl_text( self, event ):
		event.Skip()

	def on_end_time_ctrl_text( self, event ):
		event.Skip()

	def on_add_file_button_click( self, event ):
		event.Skip()

	def on_remove_file_button_click( self, event ):
		event.Skip()

	def on_move_up_file_button_click( self, event ):
		event.Skip()

	def on_move_down_file_button_click( self, event ):
		event.Skip()

	def on_clear_all_button_click( self, event ):
		event.Skip()

	def on_size_control_mode_change( self, event ):
		event.Skip()

	def on_export_button_click( self, event ):
		event.Skip()

	def on_open_project_website_button_click( self, event ):
		event.Skip()


