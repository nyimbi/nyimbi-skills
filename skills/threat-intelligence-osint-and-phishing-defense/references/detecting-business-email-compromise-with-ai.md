# Detecting Business Email Compromise With Ai

## API Reference

## NLP Feature Extraction

| Feature | Description | BEC Signal |
|---------|-------------|------------|
| urgency_score | Ratio of urgency words to total | High = suspicious |
| pressure_score | Ratio of secrecy/pressure words | High = suspicious |
| financial_score | Ratio of financial terms | High = suspicious |
| authority_score | Ratio of executive title mentions | High = suspicious |
| caps_ratio | Uppercase character ratio | High = aggressive tone |
| unique_word_ratio | Vocabulary diversity metric | Low = template-like |

## scikit-learn Classification Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
    ("clf", RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)
predictions = pipeline.predict(X_test)
```

## Writing Style Analysis (Stylometry)

```python
# Sentence length distribution for author verification
import re, math
sentences = re.split(r'[.!?]+', text)
lengths = [len(s.split()) for s in sentences if s.strip()]
mean_len = sum(lengths) / len(lengths)
variance = sum((l - mean_len)**2 for l in lengths) / len(lengths)
std_dev = math.sqrt(variance)
```

## Microsoft Graph API - Suspicious Mail Rules

```http
GET https://graph.microsoft.com/v1.0/users/{id}/mailFolders/inbox/messageRules
Authorization: Bearer {token}

# Detect forwarding rules (T1114.003)
GET https://graph.microsoft.com/v1.0/users/{id}/mailFolders/inbox/messageRules?$filter=actions/forwardTo ne null
```

## Impersonation Signal Patterns

```python
# Mobile signature (creates urgency excuse)
r"sent from my (iphone|ipad|android|mobile)"
# Discourages verification
r"(please|kindly).*(do not|don't).*(reply|respond|call)"
# Unavailability excuse
r"(i am|i'm).*(in a meeting|traveling|on a flight)"
# Time pressure
r"(handle|process|complete).*(today|immediately|by end of day)"
```

## CLI Usage

```bash
python agent.py --file email_body.txt
python agent.py --file email_body.txt --baseline-file sender_style.json
```

---

## Standards and Controls

## MITRE ATT&CK References
- **T1566.001/002**: Phishing (Spearphishing Attachment/Link)
- **T1534**: Internal Spearphishing
- **T1656**: Impersonation
- **T1586.002**: Compromise Accounts: Email Accounts
- **T1114.003**: Email Collection: Email Forwarding Rule

## AI/ML Techniques for BEC Detection
| Technique | Application | Accuracy |
|---|---|---|
| BERT embeddings + SVC | Email classification | 98.65% |
| Transformer NLP | Writing style analysis | 96%+ |
| Anomaly detection | Behavioral baseline deviation | 94%+ |
| Graph neural networks | Communication pattern analysis | 93%+ |
| Sentiment analysis | Urgency/manipulation detection | 91%+ |

## FBI IC3 BEC Statistics
- $2.9 billion losses reported in 2023
- BEC accounts for 27% of all cybercrime financial losses
- Average loss per BEC incident: $125,000
- 21,832 BEC complaints filed in 2023

## Detection Categories
- **Impostor Detection**: AI identifies display name/domain impersonation
- **Account Takeover Detection**: Behavioral anomalies from compromised accounts
- **Writing Style Analysis**: NLP compares email to sender's historical style
- **Intent Classification**: ML classifies email as payment/credential/data request
- **Relationship Analysis**: Graph analysis of sender-recipient communication patterns

---

## Workflows

## Workflow 1: AI-Powered BEC Detection Pipeline

```
Inbound email arrives
  |
  v
[Feature extraction]
  +-- Sender metadata (domain, IP, authentication)
  +-- Email content (subject, body, NLP features)
  +-- Behavioral context (communication history, timing)
  +-- Relationship graph (sender-recipient pattern)
  |
  v
[Multi-model analysis (parallel)]
  +-- Impostor classifier: Display name/domain impersonation
  +-- NLP model: Writing style vs. sender baseline
  +-- Behavioral model: Request anomaly detection
  +-- Intent classifier: Payment/credential/data request
  |
  v
[Confidence scoring]
  +-- Aggregate model outputs
  +-- Weight by model confidence and context
  +-- Generate overall BEC probability score
  |
  v
[Action]
  +-- Score >= 90%: Auto-quarantine + SOC alert
  +-- Score 70-89%: Warning banner + analyst queue
  +-- Score 50-69%: Warning banner only
  +-- Score < 50%: Deliver normally
```

## Workflow 2: Model Feedback Loop

```
BEC verdict generated
  |
  v
[User/analyst feedback]
  +-- User reports false positive (legitimate email flagged)
  +-- Analyst confirms true positive (BEC caught)
  +-- User reports missed BEC (false negative)
  |
  v
[Feedback integration]
  +-- Update sender trust score
  +-- Retrain model with corrected labels
  +-- Adjust confidence thresholds
  +-- Update behavioral baselines
```

---

## Working Template

## AI Platform Configuration
| Setting | Value | Status |
|---|---|---|
| Platform | | |
| Integration | API-based (Microsoft Graph) | |
| Baseline training period | 30+ days | |
| Scanning scope | Inbound + Internal + Outbound | |

## Detection Thresholds
| Score Range | Classification | Action |
|---|---|---|
| 90-100% | High-confidence BEC | Auto-quarantine + SOC alert |
| 70-89% | Moderate BEC | Warning banner + analyst queue |
| 50-69% | Low-confidence BEC | Warning banner only |
| < 50% | Likely legitimate | Deliver normally |

## VIP Protection List
| Name | Title | Email | Writing Style Profiled |
|---|---|---|---|
| | CEO | | |
| | CFO | | |
| | CTO | | |

## Model Performance Metrics
| Metric | Target | Current |
|---|---|---|
| Detection accuracy | > 98% | |
| False positive rate | < 0.05% | |
| Mean detection time | < 5 sec | |
| BEC catch rate vs. rules | +25% | |
