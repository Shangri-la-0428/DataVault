# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.2.x   | Yes       |

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

Please report vulnerabilities privately to: **wutc@oasyce.com**

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

| Step | Timeline |
|------|----------|
| Acknowledgment | 48 hours |
| Initial assessment | 7 days |
| Fix target | 30 days |

We follow coordinated disclosure — we will work with you on timing before any public announcement.

## Scope

### In Scope

- PII detection bypass (privacy.py fails to flag sensitive data)
- Data exfiltration via bridge (file content sent to chain instead of hash)
- SQLite injection in inventory operations
- Path traversal in scanner
- Unauthorized file registration (bypassing `--confirm` requirement)

### Out of Scope

- Issues in dependencies (report upstream)
- Social engineering
- Denial of service via large directory scanning
