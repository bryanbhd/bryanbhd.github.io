# Bryan Debnam

**Systems Architect → AI Platform / MLOps Engineer**
Lewisville, TX · bdebnam@gmail.com · [linkedin.com/in/bryanhd](https://www.linkedin.com/in/bryanhd)

**Resume —** AI Platform / MLOps:
[PDF](resume/Bryan_Debnam_Resume_AI_Platform.pdf) ·
[DOCX](resume/Bryan_Debnam_Resume_AI_Platform.docx)
 | Systems Architect:
[PDF](resume/Bryan_Debnam_Resume_Systems_Architect.pdf) ·
[DOCX](resume/Bryan_Debnam_Resume_Systems_Architect.docx)

---

## Positioning

20+ years in enterprise IT, 3+ at the architecture level — cloud migrations, M&A technology
integration, and identity modernization across four acquisitions, plus building and leading a
60+-control SOX/ITGC compliance program.

**At work**, more recently: "Script Portal," an internal platform for interchangeable
agentic-AI backends under one allowlist + output-masking safety model; Playwright RPA agents
for SOX audit evidence; the org's GitHub Enterprise Copilot rollout.

**Independently** (personal R&D; foundation: Texas McCombs AI/ML post-grad, 2024–2025): a full
MLOps governance lifecycle (model registry, champion/challenger promotion with rollback,
automated drift detection, data lineage), an LLM security triage tool, and LLM cost analytics —
all on a self-hosted, dual-GPU Incus/k3s fleet.

**What's distinctive:** the intersection of SOX/ITGC audit discipline and hands-on AI-platform
engineering — few people have both.

---

## Selected projects

Each project is tagged **[Work]** (Inform Diagnostics) or **[Independent R&D]** (personal), and
scoped: **Production** (in real organizational use), **Reference build** (complete and running,
single-environment / not scale-tested), **POC** (proves the pattern).

### 1. AI Governance & MLOps Lifecycle — **[Independent R&D]** · *Reference build, flagship*

An end-to-end model-governance pipeline for a 7-agent LLM system, applying SOX/ITGC evidentiary
rigor to AI oversight.

- **Model registry & staged promotion** (MLflow) — preflight validation gates, automated
  rollback, and a silent-no-op safety guard that blocks unvetted model changes from reaching
  production.
- **Champion/challenger A/B gate** — a staged candidate model is evaluated head-to-head against
  the live champion before any cutover.
- **Automated drift detection** — weekly scheduled scanning, parameter-order-insensitive.
  Caught a live defect in production: an arithmetic self-contradiction in a prompt-scoring agent
  that was inflating its own output score.
- **Data lineage** (Marquez / OpenLineage) across the MLflow ↔ Ollama pipeline — every model
  version, eval run, and promotion decision is auditable.
- **LLM-as-judge evaluation harness** — scores agents on substance (accuracy, completeness, no
  fabrication) rather than surface grammar; registered judge model; testsets logged as MLflow
  GenAI datasets. Brought all 7 agents to a validated quality gate.
- **AI Gateway** (FastAPI/uvicorn) — unified model-access boundary with a local detect-quality
  model; GenAI UI wired (Prompts registry for 7 agent system prompts, review queues, label
  schemas).
- **Stack:** MLflow 3.x (Postgres backend, decoupled artifact volume, Vault-sourced secrets,
  AppRole), Marquez, Ollama, Grafana, Python.

### 2. Provider-Agnostic Agentic AI Platform ("Script Portal" / Agent Bridge) — **[Work]** · *Production*

An internal platform for deploying interchangeable agentic-AI backends under one safety model.

- Interchangeable agent CLIs — Claude Code CLI, Copilot GPT CLI, and a **custom VS Code
  "Agent Bridge" extension** (LLM-broker) — behind a shared allowlist and output-masking layer.
- Secret-aware execution framework; provider-agnostic orchestration so the underlying model/
  vendor can be swapped without changing the agent contract.
- In real use inside the organization.

### 3. Agentic-OS Sandbox — **[Independent R&D]** · *Reference build (self-hosted AI platform)*

A ~60-instance self-hosted platform on a single dual-GPU host — the environment projects 1, 4,
and 5 run in.

**Detail —** [Architecture & infrastructure deck](architecture/) ·
[AI service cards](model-cards/) for the on-prem model fleet

- **Incus** (LXD-successor) fleet — ~60 containers/VMs across projects; a 3-master/3-worker
  k3s cluster; ZFS/Btrfs pools with snapshot rollback; four segmented bridge networks with
  reverse-proxy-only external exposure (Caddy).
- **Dual RTX 3090** GPU passthrough at the container level — PCI-addressed device assignment,
  runtime NVIDIA library injection (survives host driver upgrades), consumed by an Ollama fleet
  (~20 models, role-based routing) and an image-gen stack.
- **Observability:** Prometheus, Grafana, Loki, Pyroscope, Checkmk, OpenTelemetry collector;
  a custom token-metrics proxy tapping Ollama traffic for per-model Prometheus metrics.
- **Secrets:** HashiCorp Vault — every generated credential, per-service AppRole delivery,
  Shamir unseal with auto-unseal automation.
- **Data:** Postgres, MariaDB, MongoDB, Qdrant (vectors), Redis, Elasticsearch/OpenSearch;
  Spark 3.5 + MinIO (S3A) + JupyterLab.
- **Agent orchestration R&D:** MCP/A2A interoperability services (router, HR-policy, time-off
  agents); a local Ollama fleet (~20 models) with role-based routing behind a metrics-tapping
  proxy.

### 4. AI Security Triage (garak-triage) — **[Independent R&D]** · *Reference build*

A red-team scanning and triage pipeline for LLM endpoints.

- Runs **garak** probes against model endpoints; guardrail-aware scans (with/without the
  llm-guard layer in path).
- Triage web UI — finding cards, severity, richer reports, `inspect_report` deep-dive.
- **Remediation library** — maps findings to concrete mitigations.
- Deployable as a service (systemd unit, deploy script, auth'd login).
- Paired with an **llm-guard guardrail** (LiteLLM integration) that returns a graceful
  200-refusal instead of a hard 400 on block.

### 5. LLM Cost Analytics — **[Independent R&D]** · *Reference build*

Cost and usage visibility for a self-hosted / mixed LLM fleet.

- Pulls traces from **Langfuse**, applies a per-model **pricing model**, emits **Prometheus**
  metrics + Grafana; logs to OpenSearch.
- Per-model cost reporting and inventory discovery.
- **MLflow model-version comparison** — compare cost/quality across registered versions.

### 6. SOX/ITGC Automation & Copilot Enterprise Governance — **[Work]** · *Production*

- **Playwright-driven RPA agents** for SOX evidence gathering — agents authenticate to
  enterprise portals, make record-selection decisions, and capture timestamped, masked evidence
  into the correct control package.
- Built and led the **SOX/ITGC compliance program** — 60+ control activities, PowerShell-
  automated evidence generation; primary liaison between Infrastructure, Security, and Audit.
- Manage the org's **GitHub Enterprise Copilot** deployment; built an n8n workflow monitoring
  seat utilization — reclaimed 25 inactive seats (~$475–725/month).
- Led **M&A technology integration for four acquisitions** — M365 tenant consolidation, AD/Entra
  ID identity integration for ~1,800 users, 400+ mailbox/OneDrive migrations, multi-forest AD
  trust across 6 forests.

---

## Skills — evidenced vs. currently deepening

| Area | Evidenced (projects above; W = work, R = independent R&D) | Currently deepening |
|---|---|---|
| **MLOps** | MLflow registry, champion/challenger, staged promotion + rollback, drift detection, Marquez lineage, LLM-as-judge eval, GenAI datasets | production scale; Prefect/Dagster pipelines; feature store |
| **Agentic AI** | provider-agnostic orchestration, VS Code broker extension, MCP/A2A services, RAG (Qdrant), guardrails (llm-guard), garak red-teaming | LangGraph/CrewAI multi-agent; Agentic RAG; long-term memory |
| **AI security / governance** | garak triage app, remediation library, guardrail-aware scans, SOX/ITGC rigor applied to AI | NIST AI RMF / EU AI Act mapping; eval-gated release in CI |
| **Infra / platform** | Incus fleet, k3s, GPU passthrough, ZFS, segmented networking, Caddy, Vault | Terraform / IaC at scale; GitOps (ArgoCD/Flux) |
| **Observability** | Prometheus, Grafana, Loki, Pyroscope, OTel collector, custom metrics proxy, Langfuse | business-AI metrics + DORA in one pipeline |
| **Cloud** | AWS SA-Associate + AI Practitioner + Cloud Practitioner; Azure Solutions Architect Expert + Admin Associate; Landing Zones, Well-Architected, multi-account governance (architecture level) | deep hands-on AWS **and** Azure; SageMaker; cost governance at scale |
| **Data** | Spark 3.5, MinIO/S3A, Qdrant, Postgres; MLflow on Postgres | Iceberg/Delta lakehouse + catalog; Ray; large-scale platforms |
| **Languages** | Python, Bash, PowerShell | Java / Scala (JVM depth) |
| **Enterprise delivery** | M&A integration ×4, identity modernization (~1,800 users), SOX program lead, Copilot rollout, lead-by-influence | people leadership of a team / sub-leaders |

---

## Certifications & education

- **AWS** *(all current)***:** Solutions Architect – Associate (2026, exp. 2029) · AI
  Practitioner (2025, exp. 2028) · Cloud Practitioner (2024, exp. 2029)
- **Microsoft** *(active through 2027)***:** Azure Solutions Architect Expert · Azure
  Administrator Associate · Azure Fundamentals (2019) · **AI-102 Azure AI Engineer
  Associate — in progress**
- **Post Graduate Program in AI & Machine Learning: Business Applications** — McCombs School
  of Business, The University of Texas at Austin (conferred July 2025)
- **A.A.S., Information Technology — CIT: Network Administration & Support** — Dallas County
  Community College District (now Dallas College)
- U.S. patent (2014 Microsoft hackathon project, placed 25th worldwide)

---

## Honest scope statement

Two separate evidence bases, never blurred:

- **Independent R&D (the sandbox)** is a **single-host reference platform**, not a production
  system with a user base — it demonstrates architecture judgment, integration breadth, and
  knowledge of failure modes. Projects 1, 3, 4, 5.
- **"At scale / in production" evidence** comes from the **work** at Inform Diagnostics: four
  M&A integrations, identity modernization for ~1,800 users, a 60+-control SOX program, an
  org-wide Copilot rollout, and the Script Portal agent platform in real internal use.
  Projects 2, 6.

---

## Verification

Issuer-hosted records, verifiable without an account:

- **Microsoft Certified: Azure Solutions Architect Expert** — [verify on Microsoft
  Learn](https://learn.microsoft.com/api/credentials/share/en-us/DebnamBryan-0771/9CE5F1B1F5EE4BF?sharingId=3CD650BEC1A4B731)
  · earned Nov 2019, active through Nov 2027
- **Post Graduate Program in AI & Machine Learning: Business Applications**, McCombs School of
  Business, UT Austin — [verify](https://vrfy.digital/index.php?key=onsxllql) · conferred July
  2025, 9.5 CEUs
