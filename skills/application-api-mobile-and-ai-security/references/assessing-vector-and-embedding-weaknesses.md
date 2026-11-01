# Assessing Vector And Embedding Weaknesses

## API Reference

## sentence-transformers (embedding generation)
| Call | Purpose |
|------|---------|
| `SentenceTransformer("all-MiniLM-L6-v2")` | Load an embedding model (384-dim) |
| `model.encode([texts])` | Return numpy array of embeddings |
| `model.encode(text, normalize_embeddings=True)` | L2-normalized vectors (for cosine) |

## scikit-learn similarity
| Call | Purpose |
|------|---------|
| `cosine_similarity(a, b)` | Pairwise cosine similarity matrix |

## Qdrant client (qdrant-client)
| Call | Purpose |
|------|---------|
| `QdrantClient(url="http://localhost:6333")` | Connect |
| `client.get_collection(name)` | Inspect vector size + distance metric |
| `client.count(name)` | Corpus size |
| `client.search(collection_name, query_vector, limit, query_filter)` | k-NN search with optional filter |
| `client.upsert(name, points=[PointStruct(id, vector, payload)])` | Insert/update points |
| `Filter(must=[FieldCondition(key, match=MatchValue(value))])` | Metadata filter (tenant isolation) |

## Chroma (chromadb)
| Call | Purpose |
|------|---------|
| `chromadb.Client()` / `PersistentClient(path)` | Connect |
| `collection.query(query_embeddings=[...], n_results=k, where={...})` | k-NN with metadata filter |
| `collection.add(ids, embeddings, metadatas, documents)` | Insert |

## Pinecone (pinecone-client)
| Call | Purpose |
|------|---------|
| `Pinecone(api_key=...)` | Connect |
| `index.query(vector=..., top_k=k, namespace="tenant", filter={...})` | k-NN; namespace = tenant boundary |
| `index.upsert(vectors=[(id, vec, meta)], namespace=...)` | Insert |

## Assessment metrics
| Metric | Meaning |
|--------|---------|
| Inversion cosine | Similarity between reconstructed candidate and target vector; high = recoverable. |
| Membership delta | top-1 score(in-corpus query) − top-1 score(control query); large positive = membership leak. |
| Poison dominance | Fraction of unrelated queries returning the poison chunk in top_k. |
| Cross-tenant count | Number of foreign-tenant rows returned to a tenant query (should be 0). |

## vec2text (research baseline)
| Call | Purpose |
|------|---------|
| `vec2text.load_pretrained_corrector("gtr-base")` | Load inversion corrector for compatible embedder |
| `vec2text.invert_embeddings(embeddings, corrector)` | Reconstruct text from embeddings |

---

## Standards and Controls

## NIST AI Risk Management Framework (AI RMF 1.0 / GenAI Profile NIST AI 600-1)

| ID | Name | Rationale |
|----|------|-----------|
| MEASURE-2.7 | AI system security and resilience are evaluated and documented | Assessing inversion, membership, isolation, and poisoning weaknesses measures the security/resilience of the RAG vector layer. |

## MITRE ATLAS

| ID | Name | Rationale |
|----|------|-----------|
| AML.T0024 | Exfiltration via ML Inference API | Parent technique: query/embedding access is abused to exfiltrate source data. |
| AML.T0024.000 | Infer Training Data Membership | Membership-inference probe determines whether a record is in the corpus. |
| AML.T0024.001 | Invert ML Model | Embedding inversion reconstructs source text from vectors. |
| AML.T0020 | Poison Training Data | Knowledge-base poisoning inserts adversarial chunks into the corpus. |
| AML.T0051.001 | LLM Prompt Injection: Indirect | Injection payloads surviving in retrieved chunks. |

## OWASP Top 10 for LLM Applications (2025)

| ID | Name | Rationale |
|----|------|-----------|
| LLM08 | Vector and Embedding Weaknesses | The core risk class under test (inversion, leakage, poisoning). |
| LLM02 | Sensitive Information Disclosure | Inversion/membership leakage discloses sensitive source data. |
| LLM01 | Prompt Injection | Indirect injection delivered through poisoned retrieval. |

## Weakness class to control mapping

| Weakness | Control |
|----------|---------|
| Embedding inversion | Authenticate + rate-limit embedding endpoint; avoid exposing raw scores. |
| Membership inference | Restrict similarity-score exposure; add query auditing. |
| Cross-tenant leakage | Server-side tenant filters or per-tenant collections/namespaces. |
| Knowledge-base poisoning | Provenance tagging, content validation, per-source retrieval caps. |
| Indirect injection in chunks | Sanitize retrieved text; apply output guardrails. |
