---
name: scientific-research
description: Scientific and ML research workflows — literature search and review (arXiv, PubMed, PMC, bioRxiv, Semantic Scholar, OpenAlex, Crossref with line-pinned citations), publication-quality scientific figures (matplotlib/seaborn), and curated package workflows (scikit-learn, PyTorch Lightning) plus deterministic access to 78 scientific databases (PubChem, ChEMBL, UniProt, PDB, KEGG, Reactome, STRING, ClinicalTrials.gov, FDA, FRED, USPTO, …). Adopted from K-Dense-AI/scientific-agent-skills (MIT, v2.68.0) as a curated subset of its 166 skills. Use for "literature review on X", "find papers about X", "publication figure", "scientific database lookup", ML model-building with sklearn/PyTorch Lightning in a research context. Do not use for business/sales/lead research (see research-and-insight-analysis or account-research), for production agent building (see building-pydantic-ai-agents), or for Hugging Face Jobs training/evals (see huggingface-llm-trainer / huggingface-community-evals).
---

# scientific-research

A curated subset of [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills)
(MIT, 166 skills total, v2.68.0) — the "AI Scientist" skill library with an
arXiv paper (2609.00065). Each reference below is an upstream skill adopted
verbatim (its `SKILL.md` renamed to `<name>.md` so skill loaders don't pick
it up as a nested global skill).

## References

| File | What it does |
|---|---|
| `references/paper-lookup/paper-lookup.md` (+scripts, refs) | Search papers across PubMed, PMC, bioRxiv, medRxiv, arXiv, OpenAlex, Crossref, Semantic Scholar, CORE, Unpaywall; full-text retrieval with line-pinned citations |
| `references/literature-review/literature-review.md` (+scripts, refs) | Structured literature review workflows: scoping, evidence extraction, synthesis |
| `references/scientific-visualization/scientific-visualization.md` (+scripts, refs) | Publication-quality figures: matplotlib/seaborn conventions, journal requirements, colorblind-safe palettes |
| `references/scikit-learn/scikit-learn.md` (+scripts, refs) | Version-aware scikit-learn workflows (models, pipelines, evaluation) |
| `references/pytorch-lightning/pytorch-lightning.md` (+scripts, refs) | PyTorch Lightning training workflows |
| `references/database-lookup/database-lookup.md` (+78 DB references) | Deterministic REST access to 78 public scientific databases with retrieval contracts and endpoint provenance; `references/database_selection_guide.md` picks the right DB |

Scripts referenced inside each skill are relative to that skill's directory
(`references/<name>/scripts/…`) — run them from there or with the full path.
They install dependencies via `uv` on first use.

## Working method

1. **Scope** — frame the question, list the databases/sources that could
   answer it (`database-lookup`'s selection guide for DB work).
2. **Retrieve** — `paper-lookup` for literature (always line-pinned
   citations); `database-lookup` for structured records. Provenance is
   part of the contract: every retrieved record carries its source.
3. **Analyze** — scikit-learn / PyTorch Lightning references for modeling;
   run scripts from the skill directory.
4. **Present** — `scientific-visualization` for figures; evidence-traceable
   writeups (claim → citation), no uncited assertions.

## Extending beyond this subset

The upstream repo has 166 skills (bioinformatics, cheminformatics, proteomics,
clinical, materials, geospatial, lab automation, …). Install any of them for
a specific job:

```bash
gh skill install K-Dense-AI/scientific-agent-skills <skill-name>
# or: npx skills add K-Dense-AI/scientific-agent-skills
```

Their README warns against installing all 166 (standing context cost) — take
the topical subset you need, and review each `SKILL.md` before first use
(third-party skills can execute code).

## Boundaries

- **research-and-insight-analysis / account-research** — business, sales,
  and people research. This skill is for scientific/technical literature and
  databases.
- **huggingface-llm-trainer / huggingface-community-evals** — training and
  evaluating models on Hugging Face infrastructure. This skill is for the
  research workflows around them.
- **building-pydantic-ai-agents** — production agent construction.

Upstream: https://github.com/K-Dense-AI/scientific-agent-skills (MIT).
