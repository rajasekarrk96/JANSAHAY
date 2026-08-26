# 10 — JANSAHAY Document Management & Quarantine Pipeline

## 1. Multi-Stage Document Pipeline

```mermaid
graph TD
    A[Citizen Upload Request] --> B[Quarantine Storage]
    B --> C[Format & MIME Validation]
    C -->|Pass| D[Synthetic Malware Scan]
    C -->|Fail| E[SCAN_FAILED]
    D -->|Pass| F[AVAILABLE / Case Linked]
    D -->|Fail| E
    F --> G[Officer Verification]
    G -->|Accept| H[VERIFIED]
    G -->|Deficient| I[REPLACEMENT_REQUIRED]
    I --> J[Citizen Replaces Document]
    J --> B
```

---

## 2. Storage Strategy
- Files are saved in a sandboxed, non-public directory (`./storage/documents/<case_id>/<doc_id>.<ext>`).
- MIME validation uses magic bytes rather than trusting client HTTP headers.
- Authorized downloads are served through streaming responses validating `can(actor, VIEW_DOCUMENT, document)`.
- No direct static file serving URL is ever enabled.
