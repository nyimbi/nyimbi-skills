# Orchestrating Llm Attacks With Pyrit

## API Reference

Source: https://github.com/microsoft/PyRIT and https://azure.github.io/PyRIT/

## Initialization

```python
from pyrit.common import initialize_pyrit, IN_MEMORY, DUCK_DB
initialize_pyrit(memory_db_type=IN_MEMORY)   # or DUCK_DB to persist, or AZURE_SQL
```

| Constant | Backend |
|----------|---------|
| `IN_MEMORY` | Ephemeral in-process store |
| `DUCK_DB` | Local DuckDB file (persistent) |
| `AZURE_SQL` | Azure SQL backend |

## Targets (`pyrit.prompt_target`)

| Class | Purpose |
|-------|---------|
| `OpenAIChatTarget` | OpenAI / Azure OpenAI / OpenAI-compatible chat endpoint |
| `AzureMLChatTarget` | Azure ML managed online endpoint |
| `HTTPTarget` | Arbitrary HTTP API (custom request/response parsing) |
| `OpenAIDALLETarget` | Image-generation target |

Common `OpenAIChatTarget` args: `endpoint`, `model_name` (or `deployment_name` for Azure), `api_key` (else read from env).

## Orchestrators / Attacks (`pyrit.orchestrator`)

| Class | Strategy | Notable params |
|-------|----------|----------------|
| `PromptSendingOrchestrator` | Send one/many prompts (baseline) | `objective_target`, `prompt_converters` |
| `RedTeamingOrchestrator` | Generic multi-turn adversarial chat | `objective_target`, `adversarial_chat`, `objective_scorer`, `max_turns` |
| `CrescendoOrchestrator` | Gradual escalation (Crescendo) | `objective_target`, `adversarial_chat`, `scoring_target`, `max_turns`, `max_backtracks` |
| `TreeOfAttacksWithPruningOrchestrator` | TAP branching + pruning | `objective_target`, `adversarial_chat`, `scoring_target`, `width`, `depth`, `branching_factor` |
| `PAIROrchestrator` | PAIR iterative refinement | `objective_target`, `adversarial_chat`, `scoring_target` |

All multi-turn classes subclass `MultiTurnOrchestrator` and expose `run_attack_async(objective=...)`.

## Scorers (`pyrit.score`)

| Class | Purpose |
|-------|---------|
| `SelfAskTrueFalseScorer` | LLM-as-judge true/false objective check |
| `SelfAskLikertScorer` | Likert-scale severity scoring |
| `SubStringScorer` | Substring match detection |
| `TrueFalseQuestion` | Question/criteria object passed to the scorer |

## Converters (`pyrit.prompt_converter`)

| Class | Effect |
|-------|--------|
| `Base64Converter` | Base64-encode prompt |
| `ROT13Converter` | ROT13 transform |
| `AsciiArtConverter` | Render text as ASCII art |
| `TranslationConverter` | Translate to another language |

## Memory (`pyrit.memory`)

```python
from pyrit.memory import CentralMemory
memory = CentralMemory.get_memory_instance()
pieces = memory.get_prompt_request_pieces()
```

## Minimal end-to-end example

```python
import asyncio
from pyrit.common import initialize_pyrit, IN_MEMORY
from pyrit.prompt_target import OpenAIChatTarget
from pyrit.orchestrator import CrescendoOrchestrator

initialize_pyrit(memory_db_type=IN_MEMORY)
target = OpenAIChatTarget(model_name="gpt-4o-mini")
adversarial = OpenAIChatTarget(model_name="gpt-4o")

attack = CrescendoOrchestrator(
    objective_target=target, adversarial_chat=adversarial,
    scoring_target=adversarial, max_turns=10, max_backtracks=5,
)
result = asyncio.run(attack.run_attack_async(objective="..."))
asyncio.run(result.print_conversation_async())
```

---

## Standards and Controls

## MITRE ATLAS (Adversarial Threat Landscape for AI Systems)

| ID | Name | Rationale |
|----|------|-----------|
| AML.T0051 | LLM Prompt Injection | PyRIT orchestrators inject crafted instructions across conversation turns to make the target act against its intended constraints. |
| AML.T0054 | LLM Jailbreak | Crescendo and TAP iteratively defeat safety guardrails; the scorer confirms the moment restrictions are bypassed. |

Reference: https://atlas.mitre.org/

## NIST AI Risk Management Framework (AI RMF 1.0)

| ID | Subcategory | Rationale |
|----|-------------|-----------|
| MEASURE-2.7 | AI system security and resilience are evaluated and documented | PyRIT yields repeatable, scorer-graded measurements of an LLM's resistance to multi-turn adversarial pressure, evidencing this subcategory. |

Reference: https://www.nist.gov/itl/ai-risk-management-framework

## OWASP Top 10 for LLM Applications (cross-reference)

| OWASP ID | Risk | PyRIT relevance |
|----------|------|-----------------|
| LLM01:2025 | Prompt Injection | RedTeaming/Crescendo/TAP orchestrators automate injection. |
| LLM02:2025 | Sensitive Information Disclosure | Objective scorers can target data/secret leakage. |
| LLM07:2025 | System Prompt Leakage | Objectives can be set to extract the system prompt. |

Reference: https://genai.owasp.org/
