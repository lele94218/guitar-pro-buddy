# Guitar Pro Buddy

[English](README.md) | **简体中文**

面向 Codex 的 Guitar Pro 打谱技能：将用户提供的 PDF、谱面图片或已授权查看的 Guitar Pro 窗口转录为可编辑乐谱，并按需制作练习课件。

## 能做什么

- 整理音轨、弦品、节奏、击勾弦、推弦、滑音、反复和歌词。
- 通过 GP5 与 Guitar Pro 原生文件工作流完成打谱、核对和导出。
- 按用户指定语言制作带讲解、音名、级数、紧凑指板图的 PDF 课件。
- 避免高分辨率图片撑大会话；处理 GPIF 共享对象和歌词覆盖问题。

这是工作流程技能，**不是一键识谱软件**。它不包含商业曲谱、歌词、教材扫描件或账户凭据，也不用于音频扒谱。

## 安装与使用

将仓库内容放到个人技能目录的 `guitar-pro-buddy` 文件夹，例如：

```sh
git clone https://github.com/lele94218/guitar-pro-buddy.git ~/.codex/skills/guitar-pro-buddy
```

如果该目录已有自己的版本，先比较差异并保留本地偏好，不要直接覆盖。

使用示例：

> 使用 $guitar-pro-buddy，把这份 PDF 的指定页转成 Guitar Pro，吉他与人声各一轨。

> 使用 $guitar-pro-buddy，给现有练习谱制作带音名和指板图的 PDF 课件。

默认技能入口是英文版 [SKILL.md](SKILL.md)，也可阅读[中文说明](SKILL.zh-CN.md)，详细资料按任务加载。实际操作 Guitar Pro 需要本机应用及必要的辅助功能权限；依赖与临时产物放在工作项目中。

仓库默认展示英文，可通过页面顶部的链接切换中文；对话和生成课件仍遵循用户指定的语言。

## 随附工具

`prepare_image.py` 需要 Pillow；可在工作项目的虚拟环境中安装 `requirements.txt`。`run_bounded.py` 仅使用 Python 标准库，面向 macOS/Linux。

```sh
# 裁剪、缩小并生成默认不超过 300 KiB 的 JPEG；不会自动显示图片。
python scripts/prepare_image.py source.png review.jpg --crop 100 200 1500 800

# 受监控运行单个 Python 数据转换脚本，默认 192 MiB / 20 秒。
python scripts/run_bounded.py -- transform.py
```

执行器只监控单个 Python 工作进程，超限时终止该进程组；不适用于 GUI、多进程或 GPU 任务。RSS 是采样监控，可能短暂超调，**不是内核内存硬上限**。转换脚本本身仍需限制输入、节点、克隆数量与输出大小。监控随任务结束退出，不安装后台服务。

## 内容结构

- `SKILL.md`：任务选择、工作流与交付要求。
- `references/transcription.zh-CN.md`：转谱、格式与应用操作经验。
- `references/gpif-safety.zh-CN.md`：共享音符、歌词修复与资源限制。
- `references/courseware.zh-CN.md`：课件、音名和指板设计。
- `scripts/`：图片准备与受监控执行工具。

本仓库公开版已移除私人路径和特定用户的归档位置。具体项目要求及用户当前指示优先。
