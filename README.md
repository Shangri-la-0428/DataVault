# DataVault

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> English version: [README_EN.md](README_EN.md)

**AI Agent 的数据资产管理 Skill。**

DataVault 给你的 AI 提供一套标准化的工作流——扫描、分类、隐私检测、安全注册数据资产。它不是替代 AI 的判断力，而是一套**确定性 SOP**，让每个 Agent 每次都遵循同样的规则。

## 为什么需要 DataVault？

你的 AI 已经能读文件、分类数据了。但没有 DataVault：
- 每次对话应用的标准不一样
- 隐私检查靠概率（LLM 可能漏掉信用卡号）
- 没有审计记录
- 用户想不到让 AI 管理数据资产

DataVault 提供**确定性规则**（正则 PII 检测、扩展名分类）加上**标准管线**，AI Agent 自动遵循。

## 安装

```bash
pip install odv              # 独立使用
pip install odv[oasyce]      # 带 Oasyce 桥接
```

## 使用

```bash
datavault scan ~/Documents          # 扫描目录，SHA-256 哈希
datavault classify                  # 自动检测文件类型
datavault privacy                   # 扫描 PII（身份证、信用卡、API 密钥）
datavault report                    # 查看报告
datavault report --format json      # JSON 格式输出
datavault register --confirm        # 注册安全资产到 Oasyce（需明确确认）
```

### 作为 AI Skill 使用

当 Claude Code、Cursor 或任何 AI 编程助手使用时：

```
用户: "帮我管理 ~/Documents 里的数据资产"

AI（装了 DataVault skill）:
  1. datavault scan ~/Documents     -> 扫描 342 个文件
  2. datavault privacy              -> 标记 12 个包含 PII 的文件
  3. datavault report --format json -> 显示 330 个安全文件
  4. "发现 330 个安全文件，12 个包含敏感信息（信用卡号、API 密钥）。
     要注册安全的那些吗？"
  5. datavault register --confirm   -> 注册到 Oasyce
```

没有 DataVault，AI 每次都会用不同的方式处理这个流程。

## 管线

```
扫描 (本地) -> 分类 (本地) -> 隐私检测 (本地) -> 报告 (本地)
                                                      |
                                                  用户确认
                                                      |
                                                注册 (上链)
```

分割线以上全部在本地完成，免费。注册是一个需要明确确认的操作，发布到 Oasyce 网络。

## 上链的是什么？

只有 **SHA-256 哈希**和**元数据**（名称、标签、权利类型）。永远不上传原始文件内容。文件留在你的机器上。

## 风险等级

| 等级 | 含义 |
|------|------|
| safe | 未检测到 PII |
| low | 仅 IP 地址 |
| medium | 电子邮件地址 |
| high | 电话号码、身份证 |
| critical | 信用卡、API 密钥 |

**铁律：** 标记为 `high` 或 `critical` 的文件永远不会被注册。

## 生态

```
oasyce-chain  — L1 共识层（Go 应用链）
oasyce CLI    — Python 薄客户端 + Dashboard
DataVault     — AI Agent 数据管理 Skill（本仓库）
```

| 组件 | 定位 |
|------|------|
| [oasyce-chain](https://github.com/Shangri-la-0428/oasyce-chain) | L1 共识和结算 |
| [oasyce](https://github.com/Shangri-la-0428/Oasyce_Claw_Plugin_Engine) | Python 客户端、CLI、Dashboard |
| **DataVault** (本仓库) | AI Agent 数据资产管理 Skill |

## 当前进度

- v0.2.0 发布，44 个测试通过
- 确定性扫描 + SHA-256 哈希 + 文件分类
- 正则 PII 检测（邮箱、信用卡、API 密钥、身份证）
- SQLite 本地清单
- Oasyce 桥接注册
- AI Agent Skill 模式（CLAUDE.md 内置 SOP）
- `--confirm` 标志防止意外注册

## 许可证

MIT
