# DataVault — AI Agent Data Management Skill

DataVault provides deterministic rules and a standard pipeline for AI agents to manage data assets. Use it as an SOP so every session follows the same standards.

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

| Level    | Meaning |
|----------|---------|
| safe     | No PII detected |
| low      | IP addresses only |
| medium   | Email addresses |
| high     | Phone numbers, ID cards |
| critical | Credit cards, API keys |

## Oasyce Integration

```bash
pip install odv[oasyce]  # Install with bridge
datavault register --confirm  # Registers to Oasyce network
```

The bridge calls `oasyce register` under the hood. Requires the Oasyce Plugin Engine to be installed.

## Debug Mode

Set `DATAVAULT_DEBUG=1` to see scan errors on stderr.
