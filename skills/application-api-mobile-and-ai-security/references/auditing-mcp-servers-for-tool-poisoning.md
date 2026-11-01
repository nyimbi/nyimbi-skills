# Auditing Mcp Servers For Tool Poisoning

## API Reference

## mcp-scan CLI (Invariant Labs)

Run via uvx (no global install): `uvx mcp-scan@latest`

| Command | Description |
|---------|-------------|
| `mcp-scan` / `mcp-scan scan [config]` | Statically scan MCP configs for poisoning, shadowing, rug pulls, toxic flows |
| `mcp-scan inspect [config]` | Print tool/prompt/resource descriptions without verification |
| `mcp-scan proxy` | Runtime proxy: monitor and guardrail MCP traffic (requires `[proxy]` extra) |
| `--json` | Emit machine-readable JSON report |

Examples:
```bash
uvx mcp-scan@latest ~/.vscode/mcp.json
uvx mcp-scan@latest inspect ~/.cursor/mcp.json
uvx --with "mcp-scan[proxy]" mcp-scan@latest proxy
```

mcp-scan features: tool pinning (hash-based rug-pull detection), cross-origin escalation checks, toxic-flow analysis.

## MCP Python SDK

Install: `pip install mcp`

| API | Description |
|-----|-------------|
| `StdioServerParameters(command, args)` | Define a stdio MCP server to launch |
| `stdio_client(params)` | Async context manager yielding (read, write) streams |
| `ClientSession(read, write)` | MCP client session |
| `session.initialize()` | Perform MCP handshake |
| `session.list_tools()` | Return advertised tools (`.tools[].name`, `.description`, `.inputSchema`) |
| `session.list_prompts()` | List advertised prompts |
| `session.list_resources()` | List advertised resources |
| `session.call_tool(name, args)` | Invoke a tool (use for SSRF probing on owned servers) |

## Common MCP config locations

| Client | Path |
|--------|------|
| Cursor | `~/.cursor/mcp.json` |
| VS Code | `~/.vscode/mcp.json` |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) |

## SSRF probe targets (owned systems only)

| Target | Purpose |
|--------|---------|
| `http://169.254.169.254/latest/meta-data/` | AWS instance metadata (IMDS) |
| `http://metadata.google.internal/` | GCP metadata |
| `http://127.0.0.1:<port>/` | Loopback services |
| `file:///etc/passwd` | Local file disclosure |

## External References

- mcp-scan README: https://github.com/invariantlabs-ai/mcp-scan/blob/main/README.md
- MCP spec: https://modelcontextprotocol.io/specification
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk

---

## Standards and Controls

## MITRE ATLAS References

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| AML.T0010 | ML Supply Chain Compromise | Initial Access | A poisoned third-party MCP server compromises the agent supply chain |
| AML.T0051.001 | LLM Prompt Injection: Indirect | Initial Access | Poisoned tool descriptions are indirect injection into agent context |
| AML.T0053 | LLM Plugin Compromise | Execution | MCP tools are the agent's plugins; poisoning compromises them |
| AML.T0057 | LLM Data Leakage | Exfiltration | Poisoned tools commonly exfiltrate files/secrets |

## NIST AI RMF References

| ID | Name | Rationale |
|----|------|-----------|
| MANAGE-2.2 | Mechanisms are in place and applied to sustain the value of deployed AI systems | Auditing third-party MCP tools manages/sustains safe agent operation |

## OWASP MCP Top 10 (2025)

| ID | Name | Rationale |
|----|------|-----------|
| MCP03:2025 | Tool Poisoning | Primary risk this skill audits |
| MCP01:2025 | Prompt Injection | Poisoned descriptions inject the agent |

## Official Resources

- mcp-scan (Invariant Labs): https://github.com/invariantlabs-ai/mcp-scan
- Invariant Labs tool-poisoning disclosure: https://invariantlabs.ai/blog/introducing-mcp-scan
- OWASP MCP Top 10: https://owasp.org/www-project-mcp-top-10/
- Model Context Protocol spec: https://modelcontextprotocol.io/
- MITRE ATLAS: https://atlas.mitre.org/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
