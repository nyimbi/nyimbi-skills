# Continuous Llm Red Teaming With Promptfoo

## API Reference

## Install

| Tool | Command |
|------|---------|
| Promptfoo (global) | `npm install -g promptfoo` |
| Promptfoo (no install) | `npx promptfoo@latest redteam run` |
| DeepTeam | `pip install -U deepteam` |

## Promptfoo Red-Team CLI

| Command | Purpose |
|---------|---------|
| `promptfoo redteam init` | Scaffold an interactive red-team config |
| `promptfoo redteam generate` | Generate adversarial test cases only |
| `promptfoo redteam run` | Generate + evaluate (combined) |
| `promptfoo redteam eval` | Evaluate existing generated tests |
| `promptfoo redteam report` | Open/export the results report |
| `promptfoo redteam plugins` | List available plugins |
| `promptfoo redteam strategies` | List available strategies |

Useful flags: `--no-progress-bar` (CI), `--output results.json`, `--filter-failing <file>`, `-c <config>`.

## Promptfoo Config Keys (`redteam:` block)

| Key | Purpose |
|-----|---------|
| `purpose` | Application description; grounds attack generation |
| `numTests` | Tests generated per plugin |
| `plugins` | Adversarial generators (e.g. `owasp:llm`, `owasp:agentic`, `pii:direct`, `prompt-extraction`, `harmful`) |
| `strategies` | Delivery techniques (`jailbreak`, `jailbreak:composite`, `crescendo`, `prompt-injection`) |
| `targets` | Endpoints/models under test |

## DeepTeam Python API

| Import | Purpose |
|--------|---------|
| `from deepteam import red_team` | Run a red-team assessment |
| `from deepteam.vulnerabilities import Bias, PIILeakage` | Vulnerability definitions (50+) |
| `from deepteam.attacks.single_turn import PromptInjection` | Single-turn attack methods |
| `red_team(model_callback=..., vulnerabilities=[...], attacks=[...])` | Execute the suite |

## DeepTeam CLI

| Command | Purpose |
|---------|---------|
| `deepteam run config.yaml` | Run red teaming from a YAML config |

## External References

- Promptfoo command line: https://www.promptfoo.dev/docs/usage/command-line/
- DeepTeam attacks: https://www.trydeepteam.com/docs/red-teaming-adversarial-attacks
- DeepTeam vulnerabilities: https://www.trydeepteam.com/docs/red-teaming-vulnerabilities

---

## Standards and Controls

## MITRE ATLAS Techniques

| ID | Name | Tactic | Rationale |
|----|------|--------|-----------|
| AML.T0051 | LLM Prompt Injection | LLM Attack | Core class of attack generated and regression-tested by the suite. |
| AML.T0051.000 | Direct Prompt Injection | LLM Attack | Injection delivered directly in the user prompt. |
| AML.T0051.001 | Indirect Prompt Injection | LLM Attack | Injection delivered via retrieved/external content. |
| AML.T0054 | LLM Jailbreak | LLM Attack | Jailbreak strategies (jailbreak, composite, crescendo) test guardrail bypass. |

## NIST AI RMF

| ID | Function | Rationale |
|----|----------|-----------|
| MANAGE-4.1 | Post-deployment monitoring plans are implemented; AI risks are tracked and managed | Continuous CI/CD red-teaming is the post-deployment monitoring control for LLM risk. |

## Official Resources

- Promptfoo red-team docs: https://www.promptfoo.dev/docs/red-team/
- Promptfoo configuration: https://www.promptfoo.dev/docs/red-team/configuration/
- Promptfoo CI/CD: https://www.promptfoo.dev/docs/integrations/ci-cd/
- Promptfoo GitHub: https://github.com/promptfoo/promptfoo
- DeepTeam GitHub: https://github.com/confident-ai/deepteam
- DeepTeam docs: https://www.trydeepteam.com/docs/getting-started
- OWASP Top 10 for LLM Applications: https://genai.owasp.org/

## Frameworks Tracked

- OWASP LLM Top 10 (`owasp:llm` preset)
- OWASP Agentic threats (`owasp:agentic` preset)
- MITRE ATLAS (Promptfoo ATLAS mapping)
