# Detecting Indirect Prompt Injection

## API Reference

## LLM Guard

Install: `pip install llm-guard`

| API | Description |
|-----|-------------|
| `from llm_guard.input_scanners import PromptInjection` | Import the injection scanner |
| `PromptInjection(threshold=0.5, match_type=MatchType.FULL)` | Construct scanner (FULL or SENTENCE match) |
| `scanner.scan(text)` | Returns `(sanitized_text, is_valid, risk_score)` |
| `from llm_guard import scan_prompt` | Run multiple scanners over a prompt |

`is_valid == False` indicates an injection was detected.

## Transformers detector models

Install: `pip install transformers torch`

| API | Description |
|-----|-------------|
| `pipeline("text-classification", model=...)` | Load a classifier pipeline |
| `protectai/deberta-v3-base-prompt-injection-v2` | Open prompt-injection classifier (labels: SAFE / INJECTION) |
| `meta-llama/Llama-Prompt-Guard-2-86M` | Meta jailbreak/injection classifier (gated license) |

## Content extraction

| API | Description |
|-----|-------------|
| `BeautifulSoup(html, "html.parser")` | Parse HTML |
| `soup.find_all(string=lambda t: isinstance(t, Comment))` | Extract HTML comments |
| `pypdf.PdfReader(path).pages[i].extract_text()` | Extract PDF text |
| `pytesseract.image_to_string(Image.open(path))` | OCR text from an image |
| `PIL.Image.open(path)._getexif()` | Read EXIF metadata |

## Normalization helpers

| Technique | Method |
|-----------|--------|
| Strip zero-width chars | `str.translate` over U+200B..U+FEFF |
| Strip Unicode tag chars | filter ord in range 0xE0000-0xE007F |
| Canonicalize | `unicodedata.normalize("NFKC", text)` |
| Decode Base64 | `base64.b64decode(token)` |
| Decode ROT13 | `codecs.decode(text, "rot_13")` |

## External References

- LLM Guard PromptInjection docs: https://llm-guard.com/input_scanners/prompt_injection/
- Hugging Face transformers pipelines: https://huggingface.co/docs/transformers/main_classes/pipelines
- pytesseract: https://github.com/madmaze/pytesseract

---

## Standards and Controls

## MITRE ATLAS References

| Technique ID | Name | Tactic | Rationale |
|--------------|------|--------|-----------|
| AML.T0051.001 | LLM Prompt Injection: Indirect | Initial Access | The precise technique detected — injection via ingested artifacts |
| AML.T0051 | LLM Prompt Injection | ML Attack Staging | Parent technique for all prompt-injection variants |
| AML.T0057 | LLM Data Leakage | Exfiltration | Common objective of indirect injection that detection prevents |
| AML.T0053 | LLM Plugin Compromise | Execution | Injected instructions frequently target agent tools/plugins |

## NIST AI RMF References

| ID | Name | Rationale |
|----|------|-----------|
| MEASURE-2.7 | AI system security and resilience are evaluated and documented | Content scanning measures/maintains agent resilience to injection |

## OWASP Top 10 for LLM Applications (2025)

| ID | Name | Rationale |
|----|------|-----------|
| LLM01:2025 | Prompt Injection | The risk this skill detects (indirect variant) |
| LLM02:2025 | Sensitive Information Disclosure | Prevented outcome of a successful indirect injection |

## Official Resources

- MITRE ATLAS: https://atlas.mitre.org/
- OWASP LLM01:2025: https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- LLM Guard: https://llm-guard.com/
- Meta Prompt Guard 2: https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M
- ProtectAI prompt-injection classifier: https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2
- NIST AI RMF: https://www.nist.gov/itl/ai-risk-management-framework
