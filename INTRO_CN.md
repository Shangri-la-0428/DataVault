# DataVault — 先搞清楚你有什么，再决定分享什么

## 它能帮你做什么

你的电脑里散落着大量文件——文档、表格、图片、代码、数据集。你大概知道它们在哪，但你不知道：

- 哪些文件里有**敏感信息**（身份证号、银行卡、API 密钥）？
- 哪些文件有**商业价值**，可以变现？
- 哪些文件该**加密保护**，哪些可以放心分享？

**DataVault 帮你搞清楚这些。** 它是一个本地扫描工具：

- 🔍 **扫描** — 告诉它一个文件夹，它自动扫描所有文件
- 🏷️ **分类** — 自动识别文件类型、内容特征、敏感程度
- ⚠️ **预警** — 发现敏感信息立刻提醒你
- 📋 **报告** — 生成清晰的资产清单，告诉你"你有什么"

**一句话**：在你决定把数据分享给任何人之前，先用 DataVault 看看你到底有什么。

---

## 为什么需要它

**场景 1：你想用 Oasyce 把数据变现**
→ 先用 DataVault 扫描，确保不会把包含身份证号的文件注册上去。

**场景 2：你要给合作伙伴共享文件夹**
→ 先扫一遍，确认里面没有 API 密钥、密码、私钥。

**场景 3：你想整理数字资产**
→ DataVault 生成的报告告诉你：多少个文件、多大、什么类型、哪些有风险。

---

## 3 步搞定

### 安装

```bash
pip install odv
```

### 扫描

```bash
datavault scan ~/Documents
```

输出类似：

```
Scanning ~/Documents ...
  Found 847 files (2.3 GB)
  Classified: 312 documents, 201 images, 94 spreadsheets, 240 other

⚠️  Sensitive content detected:
  ~/Documents/taxes/2024.xlsx — contains possible ID numbers
  ~/Documents/dev/config.env — contains API keys

📊 Report saved: ~/Documents/.datavault/report.json
```

### 查看报告

```bash
datavault report ~/Documents
```

看到完整的文件分类、敏感预警、统计摘要。

---

## 和 Oasyce 一起用

DataVault 独立可用，不需要 Oasyce。但如果你想把数据变现：

```bash
pip install odv[oasyce]
```

扫描后可以一键把安全的文件注册到 Oasyce 网络：

```
DataVault 扫描 → 过滤敏感文件 → 注册到 Oasyce → AI Agent 付费使用 → 你收钱
```

DataVault 是漏斗的第一步——**先保护，再变现**。

---

## 完整命令

```bash
datavault scan <path>           # 扫描文件夹
datavault classify <file>       # 分类单个文件
datavault report <path>         # 生成报告
datavault report <path> --json  # JSON 格式报告
```

---

## 它是怎么工作的

DataVault 完全在本地运行，**不联网、不上传**：

1. 遍历文件夹中的所有文件
2. 读取文件头和内容特征
3. 用正则表达式检测敏感信息（身份证、银行卡、密钥等）
4. 将结果存入本地 SQLite 数据库（`.datavault/` 目录）
5. 生成人类可读的报告

你的文件不会离开你的电脑。

---

*DataVault v0.2.0 · MIT License*
