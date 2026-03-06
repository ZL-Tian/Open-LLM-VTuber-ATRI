![](./assets/banner.jpg)

# Open-LLM-VTuber-ATRI

本项目基于 [Open-LLM-VTuber](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber) 进行二次开发，面向 ATRI 角色形象完成了定制化配置，并在原项目能力基础上补充了歌曲播放、唱歌能力与大模型请求并发控制等功能。

## 项目简介

Open-LLM-VTuber-ATRI 旨在提供一个可落地运行的 ATRI 角色方案，覆盖角色形象、语音、交互能力和基础运行配置。当前仓库主要围绕 Windows 环境进行整理，适合作为本地部署和二次开发的基础版本。

## Windows 配置流程

以下流程根据 `开发文档.docx` 中“配置方法：（Windows）”整理，并按常见开源项目的部署方式重写。

### 1. 环境准备

请先安装项目运行所需的基础工具：

```powershell
winget install Git.Git
winget install ffmpeg
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 获取项目代码

使用 Git 克隆仓库，并拉取子模块：

```powershell
git clone https://github.com/ZL-Tian/Open-LLM-VTuber-ATRI.git --recursive
cd Open-LLM-VTuber-ATRI
```

如需使用桌面端启动方式，可另外从上游发布页下载并安装桌面客户端：

- [Open-LLM-VTuber Releases](https://github.com/Open-LLM-VTuber/Open-LLM-VTuber/releases)
- 推荐安装包：`open-llm-vtuber-1.2.1-setup.exe`

### 3. 配置项目文件

克隆完成后，请先检查并修改以下与本地环境相关的路径：

- `mcp_servers.json` 中 `audio-player` 和 `sing-server` 的实际路径
- `mcp_tools/sing-mcp/player.py` 中 `SONG_FILE_PATH` 的歌曲目录路径

### 4. 配置模型与 API

#### 4.1 配置 LLM API

项目默认使用智谱开放平台作为 LLM 服务，可在以下地址申请 API Key：

- [智谱开放平台 API Key 管理](https://open.bigmodel.cn/usercenter/proj-mgmt/apikeys)

将申请到的 Key 填入 `conf.yaml` 对应模型配置下的 `llm_api_key` 字段，例如 `zhipu_llm.llm_api_key`。

如果所使用的大模型服务存在并发限制，请同步设置：

```yaml
max_concurrent_requests: 1
```

`max_concurrent_requests` 用于限制发送到该模型后端的最大并发请求数。若服务端只允许单并发，建议设置为 `1`。

#### 4.2 配置翻译 API

项目中的翻译能力使用腾讯云混元大模型接口：

- [腾讯云控制台](https://console.cloud.tencent.com/)

获取密钥后，请按本地运行环境写入系统环境变量，不要将密钥硬编码到源码中。

### 5. 配置 TTS

项目当前使用 GPT-SoVITS 方案配置 ATRI 的 TTS 能力。

1. 下载 GPT-SoVITS 整合包：

   [GPT-SoVITS 整合包说明](https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e/dkxgpiy9zb96hob4)

2. 下载 ATRI 对应权重：

   [ATRI_GPT-SoVITS](https://huggingface.co/2DIPW/ATRI_GPT-SoVITS)

3. 按如下方式放置权重文件：

```text
atri-e10.ckpt -> GPT_weights_v4
atri_e25_s5250.pth -> SoVITS_weights_v4
```

### 6. 启动服务

先启动 TTS 服务：

```powershell
cd <GPT-SoVITS-v2pro-20250604目录>
runtime\python.exe api_v2.py
```

再启动本项目服务：

```powershell
cd <Open-LLM-VTuber-ATRI目录>
uv run run_server.py
```

如果已经安装桌面客户端，也可以直接点击桌面的 `open-llm-vtuber` 应用图标启动图形界面。

## 当前已完成的工作

- 已配置 ATRI 的 Live2D 形象
- 已接入并配置 ATRI 的 TTS 模型
- 已加入播放歌曲与唱歌功能
- 已加入大模型请求并发数控制，可通过 `max_concurrent_requests` 配置

## 资源声明

- TTS 模型来源：[https://www.bilibili.com/video/BV11u4m1w71A](https://www.bilibili.com/video/BV11u4m1w71A)
- Live2D 模型来源：[https://www.bilibili.com/video/BV1Rs4y187rJ](https://www.bilibili.com/video/BV1Rs4y187rJ)
