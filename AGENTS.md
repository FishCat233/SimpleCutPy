# AGENTS.md

## 注意事项

- **不要手动编辑 `src/SimpleCutPy.py`**：该文件由 wxFormBuilder 从 `src/SimpleCutPy.fbp` 自动生成。UI 修改应通过 FormBuilder 完成。
- 项目使用**中文注释/文档 + Conventional Commit + SemVer 语义化版本**。
- `ffmpeg.exe` 内置于 `assets/`，打包后路径通过 `PathHelper.get_ffmpeg_path()` 解析。
- 版本号定义在 `src/meta.py` 的 `VERSION` 变量中。

## 关键文档文件路径

| 文件                  | 用途                               |
| --------------------- | ---------------------------------- |
| `README.md`           | 项目说明                           |
| `CONTEXT.md`          | 领域术语表                         |
| `pyproject.toml`      | 项目依赖与配置                     |
| `src/SimpleCutPy.fbp` | wxFormBuilder UI 源文件            |
| `src/SimpleCutPy.py`  | 自动生成的 UI 代码（不可手动编辑） |
| `TODO.md`             | 当前工作计划                       |

## 工作流

通用的开发工作流程如下：

1. **计划确认**：每次开始工作前，将计划写入 `TODO.md`，待用户确认后再执行。
2. **代码检查**：完成工作后执行 `ruff check .` 和 `ruff format .`

## 附注

**开发运行使用**：`python src/main.py`
**打包构建使用**：`pyinstaller SimpleCutPy.spec`，产物在 `./dist/SimpleCutPy.exe`