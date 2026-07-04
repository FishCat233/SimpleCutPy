# dearpygui 迁移工作计划

## 文件变更清单

| 操作 | 文件 | 状态 |
|------|------|------|
| 删除 | `src/SimpleCutPy.py` | ✅ 已删除 |
| 删除 | `src/SimpleCutPy.fbp` | ✅ 已删除 |
| 重写 | `src/SimpleCutMainFrame.py` | ✅ 已删除，拆分为 `src/ui/tabs/*.py` |
| 重写 | `src/main.py` | ✅ 完成 |
| 降级 | `src/controller/core.py` | ✅ 完成 |
| 新增 | `src/ui/__init__.py` | ✅ 完成 |
| 新增 | `src/ui/app.py` | ✅ 完成 |
| 新增 | `src/ui/tabs/source_tab.py` | ✅ 完成 |
| 新增 | `src/ui/tabs/export_tab.py` | ✅ 完成 |
| 新增 | `src/ui/tabs/help_tab.py` | ✅ 完成 |
| 新增 | `src/ui/tabs/about_tab.py` | ✅ 完成 |
| 新增 | `src/ui/tabs/status_bar.py` | ✅ 完成 |
| 新增 | `src/ui/components/file_drop.py` | ✅ 完成 |
| 修改 | `pyproject.toml` | ✅ 完成（wxPython→dearpguy+winotify） |
| 不动 | `src/export/*` | ✅ |
| 不动 | `src/tools/*` | ✅ |
| 不动 | `src/message.py` | ✅ |
| 不动 | `src/meta.py` | ✅ |

## 待验证 / 待完善

- [ ] **运行验证**：添加文件、时间编辑、排序、删除、导出完整流程
- [ ] **表格行选中高亮**：目前 selectable 高亮方式待确认视觉表现
- [ ] **导出完成 toast**：winotify 通知（当前仅状态条反馈）
- [ ] **检查更新弹窗**：deapygui 原生弹窗（popup/modal）替代 wx.MessageBox
- [ ] **PyInstaller 打包测试**：`pyinstaller SimpleCutPy.spec`，需更新 spec 文件
- [ ] **ruff check + format 全项目**（已有旧文件 lint 警告未在此次解决）
