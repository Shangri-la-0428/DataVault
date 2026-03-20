# DataVault

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 中文版: [README.md](README.md)

**AI agent skill for data asset management.**

DataVault gives your AI a standardized workflow for scanning, classifying, and safely registering data assets. It's not a replacement for AI judgment — it's a consistent SOP that ensures every agent follows the same rules.

## Why?

Your AI can already read files and classify data. But without DataVault:
- Every session applies different standards
- Privacy checks are probabilistic (LLM might miss a credit card number)
- There's no audit trail of what was checked
- Users don't think to ask their AI to manage data assets

DataVault solves this by providing **deterministic rules** (regex-based PII detection, extension-based classification) plus a **standard pipeline** that AI agents follow automatically.

## Install

```bash
pip install odv              # Standalone
pip install odv[oasyce]      # With Oasyce bridge
```

## Usage

```bash
datavault scan ~/Documents          # Scan & catalog files (SHA-256 hash)
datavault classify                  # Auto-detect file types
datavault privacy                   # Scan for PII (ID cards, credit cards, API keys)
datavault report                    # Review results before publishing
datavault report --format json      # Machine-readable output
datavault register --confirm        # Register safe assets to Oasyce (explicit action)
```

### As an AI Skill

When used by Claude Code, Cursor, or any AI coding agent:

```
User: "Help me manage my data assets in ~/Documents"

AI (with DataVault skill):
  1. datavault scan ~/Documents     -> catalogs 342 files
  2. datavault privacy              -> flags 12 files with PII
  3. datavault report --format json -> shows 330 safe files
  4. "I found 330 files safe to register. 12 contain sensitive data
     (credit card numbers, API keys). Want me to register the safe ones?"
  5. datavault register --confirm   -> registers to Oasyce
```

Without DataVault, the AI would freestyle this process differently every time.

## Pipeline

```
scan (local) -> classify (local) -> privacy (local) -> report (local)
                                                           |
                                                     user reviews
                                                           |
                                                    register (chain)
```

Everything above the line is local and free. The register step is an explicit, confirmed action that publishes to the Oasyce network.

## What Goes On-Chain?

Only the **SHA-256 hash** and **metadata** (name, tags, rights type). Never the original file content. The file stays on your machine.

## Risk Levels

| Level | Meaning |
|-------|---------|
| safe | No PII detected |
| low | IP addresses only |
| medium | Email addresses |
| high | Phone numbers, ID cards |
| critical | Credit cards, API keys |

**Rule:** Files flagged as `high` or `critical` are never registered.

## Ecosystem

```
oasyce-chain  — L1 consensus layer (Go appchain)
oasyce CLI    — Python thin client + Dashboard
DataVault     — AI agent data management skill (this repo)
```

| Component | Role |
|-----------|------|
| [oasyce-chain](https://github.com/Shangri-la-0428/oasyce-chain) | L1 consensus & settlement |
| [oasyce](https://github.com/Shangri-la-0428/Oasyce_Claw_Plugin_Engine) | Python client, CLI, Dashboard |
| **DataVault** (this repo) | AI agent data management skill |

## Current Progress

- v0.2.0 released, 44 tests passing
- Deterministic scanning + SHA-256 hashing + file classification
- Regex-based PII detection (emails, credit cards, API keys, ID cards)
- SQLite local inventory
- Oasyce bridge for on-chain registration
- AI agent skill mode (built-in SOP via CLAUDE.md)
- `--confirm` flag prevents accidental registration

## License

MIT
