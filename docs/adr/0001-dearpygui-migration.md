# 从 wxPython 迁移 UI 框架到 dearpygui

将 UI 层从 wxPython（retained mode, wxFormBuilder 代码生成）迁移到 dearpygui（immediate mode, 纯函数手写 UI），保留 pydantic 模型层和 ffmpeg 执行层不变。

## 决策依据

**wxPython 三个实质性痛点：**
1. wxFormBuilder 代码生成流程（`SimpleCutPy.fbp` → `SimpleCutPy.py`）引入间接层，改 UI 需跨工具操作
2. OOP 继承链使 UI 代码臃肿（`MainFrame` → `SimpleCutPyMainFrame` 子类化），每个控件的事件绑定需要"胶水代码"
3. 原生 win32 控件风格缺乏现代感，外观无法定制

**dearpygui 直接命中以上三点：** 无代码生成器、无继承树、GPU 渲染的现代视觉风格。团队成员有 Unity IMGUI 经验，能适应 immediate mode 范式。

## 考虑过的替代方案

| 方案 | 拒绝原因 |
|---|---|
| **保持 wxPython** | 痛点持续，未来 UI 改动阻力递增 |
| **PyQt/PySide** | 同样 retained mode + OOP 继承链；GPL 许可复杂；打包体积相似 |
| **Web UI（Electron/Flask+CEF）** | 过度工程——视频剪辑工具不需要 HTTP 层；打包体积剧增 |
| **tkinter** | 外观更差，拖放支持有限 |
| **重写全栈** | 模型层和 ffmpeg 执行层已验证稳定，无需改动 |

## 迁移范围

- **重写：** `SimpleCutMainFrame.py`（UI 胶水代码）、`SimpleCutPy.py`（wxFormBuilder 生成代码，删除）、`main.py`（入口）、`controller/core.py`（降级为纯数据管理器）
- **不动：** `export/`（模型 + ffmpeg 执行）、`tools/`、`message.py`、`meta.py`
- **新增：** `src/ui/` 包（纯函数式 tab 渲染模块）

## 关键设计决策

- Tab 结构保留（Notebook → 手搓树节点模拟）
- 列表控件用 `dpg.add_table`
- 文件拖放简化为视口全局接收
- 导出完成通知用 Windows toast（`winotify`）
- 检查更新网络请求异步化（避免阻塞渲染循环）
- 导出路径新增"浏览"按钮（`dpg.add_file_dialog`）
- 导出失败用持久红色状态条 + toast 双通道反馈

## 已知风险

- dearpygui 2.x 的 PyInstaller 兼容性需验证（底层 C++ renderer 可能缺失 DLL）
- immediate mode 下输入框选中行切换时的值与缓存同步逻辑较 retained mode 复杂
