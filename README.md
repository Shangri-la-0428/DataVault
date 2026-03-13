# DataVault

Local-first data asset manager — scan, classify, organize, report.

Know what you have before you decide what to share.

## Install

```bash
pip install datavault
```

## Usage

```bash
# Scan current directory
datavault scan

# Scan a specific path
datavault scan ~/Documents

# Classify a single file
datavault classify report.pdf

# Generate a report
datavault report ~/Documents
datavault report ~/Documents --format json
```

## With Oasyce

DataVault works standalone. When paired with [Oasyce](https://github.com/Shangri-la-0428/Oasyce_Claw_Plugin_Engine), your cataloged assets can be registered, priced, and traded on the decentralized settlement network.

```bash
pip install datavault[oasyce]
```

## License

MIT
