# DataVault — AI Agent Data Management

> This file is the source of truth for AI tool integration. It is read automatically by Claude Code (CLAUDE.md), Cursor (.cursorrules), Windsurf (.windsurfrules), and any AI tool that supports project-level instructions.

DataVault provides deterministic rules and a standard pipeline for AI agents to manage data assets. Use it as an SOP so every session follows the same standards.

## Install

```bash
pip install oasyce        # includes DataVault (odv) automatically
# or standalone:
pip install odv            # scanner only
pip install odv[oasyce]    # scanner + Oasyce bridge
```

## Commands

```bash
datavault scan <path>           # Scan directory, compute SHA-256 hashes, classify files
datavault classify              # Auto-detect file types from inventory
datavault privacy               # Regex-based PII detection (email, credit card, ID card, API keys)
datavault report                # Generate human-readable report of scan results
datavault report --format json  # Machine-readable output
datavault register --confirm    # Register safe assets to Oasyce (requires oasyce bridge)
datavault inventory             # List all tracked assets
datavault status                # Show inventory stats
```

## Pipeline

Always follow this order:

1. **scan** — catalog files with SHA-256 fingerprints
2. **privacy** — flag PII (deterministic regex, not LLM judgment)
3. **report** — review results, present to user
4. **register** — only with explicit user confirmation

## Key Rules

- Never register files flagged as `high` or `critical` risk
- Always show the user what will be registered before doing it
- Only the SHA-256 hash and metadata go on-chain, never file content
- The `--confirm` flag on register is required — no silent registration
- Use `--format json` when parsing output programmatically

## Risk Levels

| Level    | Meaning | Action |
|----------|---------|--------|
| safe     | No PII detected | Can register |
| low      | IP addresses only | Can register |
| medium   | Email addresses | Needs confirmation |
| high     | Phone numbers, ID cards | **Blocked** |
| critical | Credit cards, API keys | **Blocked** |

## Oasyce Integration

```bash
pip install oasyce              # includes odv
datavault register --confirm    # registers to Oasyce network
```

The bridge calls `oasyce register` under the hood. With `pip install oasyce`, both `oasyce` and `datavault` commands are available.

## Debug Mode

Set `DATAVAULT_DEBUG=1` to see scan errors on stderr.

## Full Product

DataVault is part of the Oasyce ecosystem. For the complete experience (trading, capabilities, dashboard), see the [Plugin Engine AGENTS.md](https://github.com/Shangri-la-0428/Oasyce_Claw_Plugin_Engine/blob/main/AGENTS.md).
