# Detecting Data And Model Poisoning

## API Reference

## Adversarial Robustness Toolbox (ART)

Install: `pip install adversarial-robustness-toolbox`

| API | Description |
|-----|-------------|
| `from art.estimators.classification import KerasClassifier` | Wrap a Keras model for ART (also `PyTorchClassifier`, `TensorFlowV2Classifier`) |
| `from art.defences.detector.poison import ActivationDefence` | Activation-clustering poisoning detector (Chen et al., 2018) |
| `ActivationDefence(classifier, x_train, y_train)` | Construct the defense |
| `defence.detect_poison(nb_clusters=2, nb_dims=10, reduce="PCA")` | Returns `(report, is_clean_lst)`; `is_clean_lst[i]==0` => poisoned |
| `from art.defences.detector.poison import SpectralSignatureDefense` | Spectral-signature poisoning detector |
| `SpectralSignatureDefense(classifier, x, y, expected_pp_poison=0.05, batch_size=128, eps_multiplier=1.5)` | Construct |
| `defence.detect_poison()` | Returns `(report, is_clean_lst)` |

## Cleanlab

Install: `pip install cleanlab`

| API | Description |
|-----|-------------|
| `from cleanlab.filter import find_label_issues` | Find mislabeled samples |
| `find_label_issues(labels, pred_probs, return_indices_ranked_by="self_confidence")` | Ranked indices of label issues |
| `from cleanlab.outlier import OutOfDistribution` | Outlier / OOD detection |
| `from cleanlab import Datalab` | End-to-end data audit (label, outlier, near-duplicate) |

## safetensors (safe serialization)

Install: `pip install safetensors`

| API | Description |
|-----|-------------|
| `from safetensors.numpy import load_file` | Load weights without executing pickle |
| `from safetensors.torch import load_file` | PyTorch variant |

## Integrity commands

| Command | Purpose |
|---------|---------|
| `sha256sum model.safetensors` | Compute weight digest to compare to published value |
| `find ./models -name "*.pt" -o -name "*.bin" -o -name "*.pkl"` | Locate unsafe pickle-based artifacts |

## External References

- ART defenses docs: https://adversarial-robustness-toolbox.readthedocs.io/en/latest/modules/defences/detector_poisoning.html
- Cleanlab docs: https://docs.cleanlab.ai/
- safetensors: https://github.com/huggingface/safetensors

---

## Standards and Controls

## MITRE ATLAS References

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| AML.T0020 | Poison Training Data | ML Attack Staging | Injection of manipulated samples into the training corpus |
| AML.T0018 | Backdoor ML Model | Persistence | Trigger-activated hidden behavior in the trained model |
| AML.T0010 | ML Supply Chain Compromise | Initial Access | Poisoned public datasets / trojaned downloaded weights |
| AML.T0024 | Exfiltration via ML Inference API | Exfiltration | Some poisoning leaks data via model responses |

## NIST AI RMF References

| ID | Name | Rationale |
|----|------|-----------|
| MEASURE-2.7 | AI system security and resilience are evaluated and documented | Poisoning detection measures the integrity/resilience of the ML pipeline |

## OWASP Top 10 for LLM Applications (2025)

| ID | Name | Rationale |
|----|------|-----------|
| LLM04:2025 | Data and Model Poisoning | Primary risk this skill detects |
| LLM03:2025 | Supply Chain | Trojaned weights/datasets entry path |

## Official Resources

- Adversarial Robustness Toolbox: https://github.com/Trusted-AI/adversarial-robustness-toolbox
- ART poisoning defenses docs: https://adversarial-robustness-toolbox.readthedocs.io/en/latest/modules/defences/detector_poisoning.html
- Cleanlab: https://github.com/cleanlab/cleanlab
- safetensors: https://github.com/huggingface/safetensors
- OWASP LLM04:2025: https://genai.owasp.org/llmrisk/llm042025-data-and-model-poisoning/
- MITRE ATLAS: https://atlas.mitre.org/
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
