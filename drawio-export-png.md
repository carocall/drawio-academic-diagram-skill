# 用 draw.io Desktop 导出 PNG 说明

> 前提：`D:\Software\draw.io` 已加入系统/用户 `Path` 环境变量，且改完**重开终端**生效（已打开的终端不会自动刷新）。  
> 若未配置环境变量，把下面命令里的 `draw.io` 换成完整路径如（ `"D:\Software\draw.io\draw.io.exe"` ）即可。
> 如果本机也没有安装drawio，那么告诉用户，本机没有drawio，无法导出png。

## 单页文件导出

```bat
draw.io --disable-gpu --no-sandbox --enable-unsafe-swiftshader -x -f png --scale 2 --border 20 -o 输出.png 输入.drawio
```

## 多页文件导出（逐页）

> ⚠️ draw.io Desktop **v27 之后 `-p` 页码是 1-based（从 1 开始）**，不再从 0 开始。



```bat
draw.io --disable-gpu --no-sandbox --enable-unsafe-swiftshader -x -f png --scale 2 --border 20 -p 1 -o 第1页.png 输入.drawio
draw.io --disable-gpu --no-sandbox --enable-unsafe-swiftshader -x -f png --scale 2 --border 20 -p 2 -o 第2页.png 输入.drawio
REM ... 依次 -p 3、-p 4 ... 直到最后一页
```

页数是 `.drawio` 里 `<diagram>` 节点的个数，可打开文件数一下，或用脚本批量：

```bat
@echo off
set EXE=draw.io
set IN=输入.drawio
for /L %%i in (1,1,13) do (
  %EXE% --disable-gpu --no-sandbox --enable-unsafe-swiftshader -x -f png --scale 2 --border 20 -p %%i -o page_%%i.png %IN%
)
```

## 参数含义

| 参数                                                       | 作用                                                          |
| -------------------------------------------------------- | ----------------------------------------------------------- |
| `--disable-gpu --no-sandbox --enable-unsafe-swiftshader` | 无 GPU / 无显示环境下用软件渲染（SwiftShader）出图，**必加**，否则 GPU 进程崩溃导致导出失败 |
| `-x`                                                     | 导出模式（export）                                                |
| `-f png`                                                 | 输出格式 PNG（也支持 `svg`/`pdf`/`vsdx` 等）                          |
| `--scale 2`                                              | 2 倍分辨率（高清），可按需改成 1~3                                        |
| `--border 20`                                            | 图片四周留白 20px                                                 |
| `-p N`                                                   | 导出第 N 页（**N 从 1 开始**）                                       |
| `-o 输出.png`                                              | 输出文件名（建议用英文/数字，避免中文路径编码问题）                                  |
| 末尾 `输入.drawio`                                           | 源文件                                                         |

## 一句话模板（复制即用）

```
draw.io --disable-gpu --no-sandbox --enable-unsafe-swiftshader -x -f png --scale 2 --border 20 -p <页码> -o 输出.png 输入.drawio
```
