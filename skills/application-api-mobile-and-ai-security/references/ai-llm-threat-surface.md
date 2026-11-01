# AI/LLM threat surface — where an attack enters, and which file to open

LLM applications fail at the boundaries around the model, not inside it. Test in
the order below: each stage is a separate trust boundary with a separate
detection and a separate guardrail. Do not report "prompt injection possible"
without naming the stage.

| Stage | Threat | Test it with | Defend with | Reference file |
|---|---|---|---|---|
| **User input** | Direct prompt injection, jailbreak, role-play escape, instruction hijack | garak `promptinject`/`dan`, PyRIT multi-turn and TAP, Promptfoo regression suite | Input classifier (regex + heuristic + transformer), topic boundary, jailbreak scoring | `detecting-ai-model-prompt-injection-attacks.md`, `red-teaming-llms-with-garak.md`, `orchestrating-llm-attacks-with-pyrit.md`, `continuous-llm-red-teaming-with-promptfoo.md` |
| **Retrieved context (RAG)** | Injection hidden in documents, web pages, images; poisoned chunks steered into the answer | Plant instructions in source documents; garak `latentinjection`; embedding-manipulation probes | Provenance-tag retrieved chunks, strip instruction-like content, isolate retrieval from system instructions | `detecting-indirect-prompt-injection.md`, `testing-prompt-injection-in-rag-pipelines.md` |
| **Vector store** | Embedding inversion, cross-tenant leakage, poisoning of the index | Tenant-isolation probes, membership-inference style queries, poisoned-document insertion | Tenant-scoped namespaces, write control over ingestion, embedding provenance | `assessing-vector-and-embedding-weaknesses.md` |
| **Training / fine-tune data** | Data poisoning, backdoored models | Data provenance audit, trigger-token activation testing | Signed datasets, lineage, isolated fine-tune pipeline | `detecting-data-and-model-poisoning.md` |
| **Model & inference API** | Model extraction, inversion, membership inference via query abuse | Query-pattern analysis, output perturbation trials, extractability red team | Rate limiting by capability, output noise, anomaly detection on query diversity | `detecting-model-extraction-attacks.md` |
| **System prompt & config** | System prompt leakage exposing routing, secrets, or guardrail instructions | Extract-and-compare probes; scan the prompt for embedded credentials | Keep secrets out of prompts; treat prompt content as non-sensitive by design | `testing-for-system-prompt-leakage.md` |
| **Tool invocation (agentic)** | Over-broad tool access, unvalidated arguments, confused-deputy actions, SSRF via tools | Attempt out-of-policy calls with crafted arguments; review allowlists | Per-tool impact tier, JSON-schema argument validation deny-by-default, human-in-the-loop for high impact, per-session scoped credentials | `securing-agentic-ai-tool-invocation.md` |
| **MCP / tool metadata** | Tool poisoning, unauthenticated MCP endpoints, SSRF through server metadata | Scan tool descriptors and endpoints for poisoned descriptions and open access | Tool allowlisting, signed manifests, no anonymous MCP | `auditing-mcp-servers-for-tool-poisoning.md` |
| **Output** | Toxic content, hallucination, PII leakage, XSS payloads in rendered output | Output scanning against a corpus of adversarial prompts | Output filter (Llama Guard classification, NeMo Guardrails, LLM Guard scanners) plus schema validation for structured output | `defending-llms-with-guardrails.md`, `implementing-llm-guardrails-for-security.md` |

## Testing order that produces defensible results

1. Establish a benign baseline request and record the normal answer shape.
2. Direct injection at the user input — if this fails, the rest is amplification.
3. Indirect injection through every content channel the app actually ingests
   (documents, web pages, tickets, images), with zero-width/Unicode-tag
   normalization and base64/ROT13 decoding applied before judging a miss.
4. RAG poisoning: insert a chunk and confirm retrieval elevates it over the
   system instruction.
5. Tool invocation: from a successful injection, attempt one out-of-policy call.
6. System prompt extraction and output-filter evasion.
7. Re-run the whole set as a regression suite in CI and fail the build on new hits.

## Guardrail placement

- **Input**: injection classifier, PII strip, token/length limits — before the model.
- **Between model and tools**: schema validation and impact-tier approval — before any side effect.
- **Output**: content classification and schema validation — before the user or downstream system.

A guardrail with no test proving it blocks is assumed not to work; the red-team
files above are the proof mechanism, not an optional extra.

## Boundary

Authorized, multi-turn attack campaigns and full-chain exploitation against a
live LLM service belong to `offensive-security-and-red-teaming`. This skill owns
the probe catalogue, the per-stage test procedure, and the remediation of what
those probes find.
