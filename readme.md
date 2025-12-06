# SimpleCutPy

***一款简单的影视素材剪辑器，用于对游戏回放素材进行快速剪辑***

> [!WARNING]
>
> SimpleCutPy 仍在进行开发中，除去对输入数据的校验功能，基本功能应已可用。
>
> 您可能在使用中会遇到大量的 bug，欢迎提交 issue。

---

## 什么是 SimpleCutPy

SimpleCutPy 是一款简单的影视素材剪辑器，它可以对素材（建议是尺寸相似的）进行简单剪辑，
例如调整顺序，截取其中某一个片段。

制作它的灵感和需求来源于对游戏即时回放片段的拼接，通过它您可以轻松的对各种即时回放片段进行拼接和简单处理。

它的工作原理很简单：将界面上设置的参数转化为使用 ffmpeg 进行处理的命令行，然后自动调用ffmpeg对素材进行处理。

## SimpleCutPy 的工作原理

SimpleCutPy 使用 wxPython 构建 UI 界面，并通过 UI 界面生成 ffmpeg 命令行并进行执行。

## 我该如何使用 SimpleCutPy

为了使用 SimpleCutPy 你需要先安装 ffmpeg。您可以在系统终端中输入 `ffmpeg` 查看是否已经安装了ffmpeg。

为获取 SimpleCutPy，可以在 release 页面中找到打包可供 windows 平台使用的可执行程序文件。

对于其他平台，我没有测试过兼容性，但是由于实现方式的特性，您可以试试能否使用。

---

## 使用 Pyinstaller 打包 SimpleCutPy

在项目根目录使用如下命令
`pyinstaller SimpleCutPy.spec`

打包生成的文件会在 `./dist/SimpleCutPy.exe`

下面是对一些文件的介绍：

- `main.py`：这是整个程序的入口文件，如果想要直接在python中运行整个程序，请直接运行这个文件
- `SimpleCutPy.py`：这是由 wxFormBuilder 生成的文件，主要对程序界面和控件进行了布局并绑定了相关的回调函数。
- `SimpleCutMainFrame.py`：这是程序主要逻辑实现的地方。
- `SimpleCutPy.fbp`： 这是 wxFormBuilder 的工程文件，使用 wxFormBuilder 打开这个工程文件，您可以看到这个程序的界面设计。