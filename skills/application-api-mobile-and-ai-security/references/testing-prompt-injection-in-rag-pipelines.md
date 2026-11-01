# Testing Prompt Injection In Rag Pipelines

## API Reference

## NVIDIA garak CLI

Install: `python -m pip install -U garak`

| Flag | Description |
|------|-------------|
| `--model_type` / `--target_type` | Generator family: `openai`, `huggingface`, `rest`, `ollama`, `bedrock` |
| `--model_name` / `--target_name` | Specific model / model id |
| `--probes` | Comma-separated probe modules, or `all` (default) |
| `--list_probes` | Print all available probe modules |
| `--generations` | Number of generations per prompt |
| `--report_prefix` | Prefix for the JSONL/HTML report |
| `--generator_option_file` | JSON config for the `rest` generator |

Relevant probe modules: `promptinject`, `latentinjection`, `leakreplay`, `xss`, `dan`, `encoding`, `goodside`.

Example:
```bash
python -m garak --model_type openai --model_name gpt-4o-mini \
  --probes promptinject,latentinjection --generations 5 --report_prefix rag_run
```

## Promptfoo Red-Team CLI

Install: `npm install -g promptfoo`

| Command | Description |
|---------|-------------|
| `promptfoo redteam init` | Scaffold a red-team config |
| `promptfoo redteam run` | Generate adversarial cases and execute |
| `promptfoo redteam report` | Open the HTML findings report |

RAG-relevant plugins (`redteam.plugins`): `indirect-prompt-injection`, `rag-document-exfiltration`, `harmful:privacy`.
Strategies (`redteam.strategies`): `jailbreak`, `prompt-injection`, `crescendo`.

## Microsoft PyRIT

Install: `pip install pyrit` (Python 3.10-3.13)

| Component | Import | Purpose |
|-----------|--------|---------|
| `initialize_pyrit_async`, `IN_MEMORY` | `pyrit.setup` | Initialize memory/DB |
| `OpenAIChatTarget` | `pyrit.prompt_target` | Target an OpenAI-compatible endpoint |
| `PromptSendingAttack` | `pyrit.executor.attack` | Single-/batch-turn prompt sending |
| `RedTeamingAttack` | `pyrit.executor.attack` | Multi-turn adversarial conversation |
| `ConsoleAttackResultPrinter` | `pyrit.executor.attack` | Print scored results |

## sentence-transformers (embedding poisoning PoC)

Install: `pip install sentence-transformers faiss-cpu numpy`

| API | Description |
|-----|-------------|
| `SentenceTransformer(model_name)` | Load embedding model |
| `model.encode(text, normalize_embeddings=True)` | Produce normalized vector |
| `numpy.dot(a, b)` | Cosine similarity of normalized vectors |

## External References

- garak CLI reference: https://github.com/NVIDIA/garak/blob/main/docs/source/cliref.rst
- Promptfoo indirect injection plugin: https://www.promptfoo.dev/docs/red-team/plugins/indirect-prompt-injection/
- PyRIT docs: https://azure.github.io/PyRIT/

---

## Standards and Controls

## MITRE ATLAS References

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| AML.T0051 | LLM Prompt Injection | ML Attack Staging / Initial Access | Injected instructions in retrieved context override system intent |
| AML.T0051.001 | LLM Prompt Injection: Indirect | Initial Access | Payload delivered through ingested documents, not direct user input |
| AML.T0057 | LLM Data Leakage | Exfiltration | RAG injections aim to leak system/other-tenant documents |
| AML.T0024 | Exfiltration via ML Inference API | Exfiltration | Model responses act as the document exfiltration channel |

## NIST AI RMF References

| ID | Name | Rationale |
|----|------|-----------|
| MEASURE-2.7 | AI system security and resilience are evaluated and documented | Injection probing measures the security/resilience of the RAG system |

## OWASP Top 10 for LLM Applications (2025)

| ID | Name | Rationale |
|----|------|-----------|
| LLM01:2025 | Prompt Injection | Primary risk tested, including indirect injection via retrieval |
| LLM02:2025 | Sensitive Information Disclosure | Successful injections often exfiltrate private corpus data |
| LLM08:2025 | Vector and Embedding Weaknesses | Embedding-space retrieval poisoning surface |

## Official Resources

- MITRE ATLAS: https://atlas.mitre.org/
- OWASP LLM01:2025 Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- NVIDIA garak: https://github.com/NVIDIA/garak
- Promptfoo RAG red teaming: https://www.promptfoo.dev/docs/red-team/rag/
- Microsoft PyRIT: https://github.com/Azure/PyRIT
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
