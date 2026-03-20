# Contributing to DataVault

Thank you for your interest in contributing to DataVault!

> 中文版见下方 / Chinese version below

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Setup

```bash
git clone https://github.com/Shangri-la-0428/DataVault.git
cd DataVault
pip install -e ".[test]"
pytest
```

## Development Workflow

### Branch Naming

- `feat/description` — New features
- `fix/description` — Bug fixes
- `refactor/description` — Code refactoring
- `docs/description` — Documentation

### Code Style

- Format with `black` (line length 100)
- Type hints encouraged
- Keep functions focused and short
- Add tests for new functionality

### Testing

```bash
pytest              # Unit tests
pytest -v --tb=short  # Verbose output
```

All PRs must pass CI (test + lint).

### Commit Messages

Use conventional format:

```
feat: short description

Longer explanation if needed.
```

Prefixes: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

### Pull Request Process

1. Fork the repository and create your branch from `main`
2. Add tests covering your changes
3. Ensure `pytest` passes
4. Update documentation if needed
5. Submit PR with clear description of what and why

### Module Structure

```
datavault/
├── scanner.py      # Directory scanning, SHA-256 hashing
├── classifier.py   # File type classification
├── privacy.py      # Regex-based PII detection
├── reporter.py     # Report generation
├── inventory.py    # SQLite asset inventory
├── bridge.py       # Oasyce chain bridge
├── cli.py          # CLI entry point
```

## Reporting Issues

- **Bugs**: Use the [bug report template](https://github.com/Shangri-la-0428/DataVault/issues/new?template=bug_report.md)
- **Features**: Use the [feature request template](https://github.com/Shangri-la-0428/DataVault/issues/new?template=feature_request.md)
- **Security**: See [SECURITY.md](SECURITY.md) — do NOT open public issues for vulnerabilities

## Community

- Discord: [https://discord.gg/tfrCn54yZW](https://discord.gg/tfrCn54yZW)

---

# 贡献指南

感谢你对 DataVault 的关注！

## 快速开始

```bash
git clone https://github.com/Shangri-la-0428/DataVault.git
cd DataVault
pip install -e ".[test]"
pytest
```

## 开发规范

- 使用 `black` 格式化代码
- 新功能必须有测试
- Commit 格式: `feat: 描述`
- PR 需通过 CI

## 提交 PR

1. Fork 并从 `main` 创建分支
2. 添加测试
3. 确保 `pytest` 通过
4. 提交 PR，说明改了什么、为什么改

## 社区

- Discord: [https://discord.gg/tfrCn54yZW](https://discord.gg/tfrCn54yZW)
