# Detecting Model Extraction Attacks

## API Reference

## Libraries

| Library | Install | Purpose |
|---------|---------|---------|
| adversarial-robustness-toolbox | `pip install adversarial-robustness-toolbox` | Extraction, inversion, and membership-inference attacks + defenses |
| scikit-learn | `pip install scikit-learn` | Surrogate / attack model training |
| numpy | `pip install numpy` | Confidence-vector math, perturbation |

## ART Extraction Attacks (`art.attacks.extraction`)

| Class | Key params | Purpose |
|-------|-----------|---------|
| `KnockoffNets` | `nb_stolen`, `batch_size_query`, `nb_epochs`, `sampling_strategy` | Train surrogate from black-box queries (Knockoff Nets) |
| `CopycatCNN` | `nb_stolen`, `batch_size_fit`, `batch_size_query` | Copycat surrogate extraction for neural nets |
| `attack.extract(x, thief_classifier=...)` | — | Run extraction; returns trained surrogate classifier |

## ART Inference Attacks (`art.attacks.inference.membership_inference`)

| Class | Key methods | Purpose |
|-------|-------------|---------|
| `MembershipInferenceBlackBox` | `.fit(...)`, `.infer(x, y)` | Black-box membership inference (AML.T0024.000) |
| `MembershipInferenceBlackBoxRuleBased` | `.infer(x, y)` | Rule-based MIA baseline (no shadow training) |

## ART Defenses (postprocessors)

| Class | Purpose |
|-------|---------|
| `art.defences.postprocessor.ReverseSigmoid` | Perturb output probabilities to hinder extraction |
| `art.defences.postprocessor.Rounded` | Round confidence values to reduce leaked precision |
| `art.defences.postprocessor.HighConfidence` | Suppress low-confidence outputs |

## Estimator Wrappers

| Class | Purpose |
|-------|---------|
| `art.estimators.classification.SklearnClassifier` | Wrap a scikit-learn model as an ART victim |
| `art.estimators.classification.KerasClassifier` / `PyTorchClassifier` | Wrap DL models |

## Detection Signals (custom)

| Signal | Heuristic |
|--------|-----------|
| Query volume | Queries/principal/window above baseline |
| Unique-input ratio | `unique(input_hash)/queries` → ~1.0 |
| Confidence-request ratio | Fraction of calls demanding full probability vectors |

## External References

- ART docs: https://adversarial-robustness-toolbox.readthedocs.io/
- MITRE ATLAS AML.T0024: https://atlas.mitre.org/techniques/AML.T0024

---

## Standards and Controls

## MITRE ATLAS Techniques

| ID | Name | Tactic | Rationale |
|----|------|--------|-----------|
| AML.T0024 | Exfiltration via AI Inference API | Exfiltration | Parent technique: abusing the inference API to steal model value or training data. |
| AML.T0024.000 | Infer Training Data Membership | Exfiltration | Membership inference — determine if a record was in the training set (privacy leak). |
| AML.T0024.001 | Invert AI Model | Exfiltration | Model inversion — reconstruct training inputs from confidence scores. |
| AML.T0024.002 | Extract ML Model | Exfiltration | Model stealing — train a surrogate from query/response pairs to clone the model. |

## NIST AI RMF

| ID | Function | Rationale |
|----|----------|-----------|
| MEASURE-2.6 | AI system security and resilience are evaluated and documented | Extraction/inference testing measures and documents the model's resilience to inference-API abuse. |

## Official Resources

- MITRE ATLAS AML.T0024: https://atlas.mitre.org/techniques/AML.T0024
- MITRE ATLAS Matrix: https://atlas.mitre.org/matrices/ATLAS
- Adversarial Robustness Toolbox (Trusted-AI): https://github.com/Trusted-AI/adversarial-robustness-toolbox
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework

## Key Research

- Tramèr et al., "Stealing Machine Learning Models via Prediction APIs" (USENIX Security 2016)
- Shokri et al., "Membership Inference Attacks Against Machine Learning Models" (IEEE S&P 2017)
- Orekondy et al., "Knockoff Nets: Stealing Functionality of Black-Box Models" (CVPR 2019)
