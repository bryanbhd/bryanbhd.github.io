# Bryan Debnam

**Systems Architect → AI Platform Architect / MLOps**
Lewisville, TX · bdebnam@gmail.com · [linkedin.com/in/bryanhd](https://www.linkedin.com/in/bryanhd)

**Resume —** [request a copy](mailto:bdebnam@gmail.com?subject=Resume%20request) · PDF or DOCX,
AI Platform / MLOps or Systems Architect.

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

Each project is tagged **[Work]** (current employer) or **[Independent R&D]** (personal), and
scoped: **Pilot** (in limited use on real workloads, ahead of formal rollout),
**Reference build** (complete and running, single-environment / not scale-tested), **POC**
(proves the pattern).

### 1. AI Governance & MLOps Lifecycle — **[Independent R&D]** · *Reference build, flagship*

An end-to-end model-governance pipeline for a 7-agent LLM system, applying SOX/ITGC evidentiary
rigor to AI oversight.

**Detail —** [Case study: a real gate-fail → fix → re-validate cycle](case-studies/mlops-governance/)

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
- **Model-version cost/quality comparison** — compare cost and quality across registered
  model versions to inform promotion decisions.
- **Stack:** MLflow 3.x (Postgres backend, decoupled artifact volume, Vault-sourced secrets,
  AppRole), Marquez, Ollama, Grafana, Python.

### 2. Provider-Agnostic Agentic AI Platform ("Script Portal" / Agent Bridge) — **[Work]** · *Pilot — daily driver*

An internal accelerator — teams get interchangeable agentic-AI backends that can act against
real enterprise systems under one allowlist and masking model, instead of a per-tool approval
for every new agent.

- **Interchangeable agent backends** — Claude Code CLI, Copilot GPT CLI, and a **custom VS Code
  "Agent Bridge" extension** (LLM-broker) — behind a shared allowlist and output-masking layer.
- **Provider-independent agent contract** — spans tool use, memory, reasoning workflows, and
  decision frameworks, so the underlying model or vendor can be swapped without changing how
  agents are invoked or governed.
- **Secret-aware execution framework** with output masking applied to agent transcripts, so
  agents can act against authenticated internal systems under one safety model rather than
  per-tool exceptions.
- **Piloted on identity-lifecycle workflows** — account-hygiene checks, expiring-credential
  monitoring, and tickets whose summary and detail are **model-generated** rather than
  templated, with credential renewal handled inside the same governed boundary.
- **Closed loop, not just detection** — privileged actions run *inside* the allowlist and
  masking boundary rather than as scripted exceptions around it, so the framework extends to
  new use cases under the same governance model.

*Scope: single-operator pilot. Broader rollout is designed around a dedicated service identity
with least-privilege delegation.*

### 3. Agentic-OS Sandbox — **[Independent R&D]** · *Reference build (self-hosted AI platform)*

A ~60-instance self-hosted platform on a single dual-GPU host — the environment projects 1 and 4 run in.

**Detail —** [Architecture & infrastructure deck](architecture/) ·
[AI service cards](model-cards/) for the on-prem model fleet

- **Incus** (LXD-successor) fleet — ~60 containers/VMs across projects; a 3-master/3-worker
  k3s cluster; ZFS/Btrfs pools with snapshot rollback; four segmented bridge networks with
  reverse-proxy-only external exposure (Caddy).
- **Dual RTX 3090** GPU passthrough at the container level — PCI-addressed device assignment,
  runtime NVIDIA library injection (survives host driver upgrades), consumed by an Ollama fleet
  (~20 models, role-based routing) and an image-gen stack.
- **Observability:** Prometheus, Grafana, Loki, Pyroscope, Checkmk, OpenTelemetry collector;
  a custom token-metrics proxy tapping Ollama traffic for per-model Prometheus metrics;
  Langfuse traces costed against a per-model pricing model for per-model spend reporting.
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

### 5. SOX/ITGC Automation & Copilot Enterprise Governance — **[Work]** · *Pilot*

- **Two cooperating Playwright RPA agents** run the audit-evidence cycle end to end — the first
  interprets incoming evidence requests and resolves what each control activity requires; the
  second collects the required records from enterprise systems and assembles timestamped,
  masked **evidence packages** filed under the correct control.
- **Auditor-ready output** — evidence arrives already scoped to the control activity rather than
  as raw exports someone has to reconcile by hand.
- Built and led the **SOX/ITGC compliance program** — 60+ control activities, PowerShell-
  automated evidence generation; primary liaison between Infrastructure, Security, and Audit.
- Manage the org's **GitHub Enterprise Copilot** deployment; built an n8n workflow monitoring
  seat utilization — reclaimed 25 inactive seats (~$475–725/month).
- Led **M&A technology integration for four acquisitions** — M365 tenant consolidation, AD/Entra
  ID identity integration for ~1,800 users, 400+ mailbox/OneDrive migrations, multi-forest AD
  trust across 6 forests.

### 6. Multi-Account AWS Landing Zone — **[Independent R&D]** · *Reference build (control plane)*

A personally-owned **9-account AWS Organization** built as a governance reference
architecture — the multi-account control plane, not a workload environment.

- **Account topology** separated by blast radius rather than by team: Security (CloudTrail
  administration, Config aggregation), Shared Services (Central Backup, Backup Administrator,
  Network), and Workloads.
- **OU hierarchy** — Security, Shared Services (nested Network OU), and a Workloads OU
  subdivided into Dev, Test, QA, Prod, Prod-Sim, ML, and IoT, so **service control policies**
  scope per environment tier.
- **Federated identity** — IAM Identity Center fronting all member accounts, federated to an
  external **Entra ID** tenant; SSO device-code flow with per-account permission sets, so no
  account carries long-lived IAM access keys.
- **Centralized security telemetry** — dedicated CloudTrail administration and Config
  aggregator accounts, keeping audit evidence where workload OUs cannot write to it.
- **Backup separation of duties** — distinct Central Backup and Backup Administrator accounts,
  isolating backup data from the identities that administer it.

*Scope: control-plane and governance build. The workload OUs are provisioned but intentionally
unpopulated — the artifact is the account structure, delegation model, and identity federation,
not running services.*

### 7. SaaS Procurement & Spend Optimization Platform — **[Work]** · *Pilot*

An Azure-hosted internal portal that turns scattered vendor licensing data into a single
view of software spend and seat waste.

- **Multi-source aggregation** — pulls licensing and usage data from vendor REST APIs and
  normalizes seat models that differ from vendor to vendor into one comparable schema.
- **Waste detection** — surfaces duplicate license assignments, unused seats, and per-vendor
  spend, producing an actionable reclaim list rather than a static dashboard.
- **Shared component library** — reuses helpers from the agent framework (project 2): Active
  Directory and Graph email helpers, plus the duplicate-account detection logic generalized into
  duplicate **license** assignment detection — the same instinct applied to identity and to spend.
- **Delivery** — built through agentic AI-assisted development (Claude Code, GitHub Copilot)
  and shipped via **Azure DevOps build and release pipelines** with Azure service connections.

---

### 8. DevSecOps Pipeline, Secrets Hygiene & Backup Automation — **[Independent R&D]** · *Reference build*

The CI/CD, security-scanning and recovery layer behind project 3: every change to the platform
repo goes through a multi-scanner security gate, and every finding lands in one tracked place.

- **Security gate (Azure DevOps, self-hosted agent)** — five scanners, hard-gating on the
  serious tiers: **gitleaks** (secrets, full history), **checkov + trivy config** (IaC),
  **semgrep** (SAST), **trivy** (container-image CVEs), plus a custom **"no secrets on command
  lines"** check (below). **SonarQube** runs on every main build for code quality and tech-debt
  tracking — informational, not a gate; semgrep is the SAST gate.
- **One findings dashboard** — all scanners feed **DefectDojo** as one product: SARIF reimports
  into long-lived tests with automatic closure of fixed findings, a stale-run guard so an older
  build can't reopen what a newer one fixed, and SonarQube pulled in through its API import.
- **Case study — credentials in process arguments.** Found Vault AppRole secrets, tokens and
  database passwords being passed to `curl` as command-line arguments (readable by any process
  via `/proc/<pid>/cmdline`) across 28 scripts and pipelines. Fixed all of them (stdin and
  process substitution instead of argv; CI secret variables mapped through `env:` instead of
  inlined), verified against live Vault, and turned the rule into a **CI gate** so it can't
  regress.
- **Pipeline credential model** — HashiCorp Vault AppRole per pipeline with single-path,
  read-only policies; secret IDs bound to the agent's address; deploy access through
  **forced-command SSH keys** (one key can run exactly one allow-listed installer script).
- **App deploy pipelines** — deploy/teardown for an EHR demo stack, FHIR/DICOM services, a ledger
  API service and sports-analytics apps, each logging in to Vault with its own narrow role.
- **Backup & recovery** — nightly fleet backups via ZFS snapshot + incremental send with a
  bounded window and a carryover queue; daily logical dumps of every PostgreSQL and MariaDB
  database (read-only dump accounts); everything **age-encrypted to a hardware-key recipient**,
  shipped off-box to a NAS and checksum-verified; a status dashboard over the job history.

## Skills — evidenced vs. actively building

| Area | Evidenced (projects above) | Actively building |
|---|---|---|
| **MLOps** | MLflow registry, champion/challenger, staged promotion + rollback, drift detection, Marquez lineage, LLM-as-judge eval, GenAI datasets | production-scale operation; Prefect/Dagster pipelines |
| **Agentic AI** | provider-agnostic orchestration, VS Code broker extension, MCP/A2A services, RAG (Qdrant), guardrails (llm-guard), garak red-teaming | LangGraph multi-agent; agentic RAG |
| **AI security / governance** | garak triage app, remediation library, guardrail-aware scans, SOX/ITGC rigor applied to AI | NIST AI RMF / EU AI Act mapping; eval-gated release in CI |
| **Infra / platform** | Incus fleet, k3s, Slurm, GlusterFS, GPU passthrough, ZFS, segmented networking, Caddy, Vault | Terraform; GitOps (ArgoCD/Flux) |
| **Observability** | Prometheus, Grafana, Loki, Pyroscope, OTel collector, custom metrics proxy, Langfuse | — |
| **Cloud** | AWS SA-Associate + AI Practitioner; Azure Solutions Architect Expert; multi-account AWS Organization (project 6), Landing Zones, Well-Architected | deeper hands-on breadth on both |
| **Data** | Spark 3.5, MinIO/S3A, Qdrant, Postgres; MLflow on Postgres | Iceberg/Delta lakehouse + catalog |
| **Languages** | Python, Bash, PowerShell | — |
| **Enterprise delivery** | M&A integration ×4, identity modernization (~1,800 users), SOX program lead, Copilot rollout, lead-by-influence | — |

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

- **Independent R&D** is personal work, not a production system with a user base — it
  demonstrates architecture judgment, integration breadth, and knowledge of failure modes. The
  sandbox is a **single-host reference platform** (projects 1, 3, 4); the AWS landing zone is a
  control-plane build with intentionally unpopulated workload OUs (project 6).
- **"At scale / in production" evidence** comes from the **work** at my current employer: four
  M&A integrations, identity modernization for ~1,800 users, a 60+-control SOX program, and an
  org-wide Copilot rollout. The agent-platform projects built on top of that experience —
  Script Portal, the SOX evidence agents, and the spend portal — are **pilots** ahead of formal
  rollout. Projects 2, 5, 7.

---

## Verification

Issuer-hosted records, verifiable without an account:

- **Microsoft Certified: Azure Solutions Architect Expert** — [verify on Microsoft
  Learn](https://learn.microsoft.com/api/credentials/share/en-us/DebnamBryan-0771/9CE5F1B1F5EE4BF?sharingId=3CD650BEC1A4B731)
  · earned Nov 18, 2019, expires Nov 19, 2027 · certification number ABA961-E2X9C0
- **Microsoft Certified: Azure Administrator Associate** — [verify on Microsoft
  Learn](https://learn.microsoft.com/api/credentials/share/en-us/DebnamBryan-0771/2A541EB9D2212380?sharingId=3CD650BEC1A4B731)
  · earned Apr 24, 2019, expires Oct 25, 2027 · certification number 628584-CT21D1
- **AWS certifications** — [Credly badge
  wall](https://www.credly.com/users/bryan-debnam.158b6f96) · Solutions Architect – Associate
  (earned Jan 4, 2026, expires Jan 4, 2029), AI Practitioner (earned Nov 2, 2025, expires Nov 2,
  2028), Cloud Practitioner (earned Aug 15, 2024, expires Jan 4, 2029)
- **Post Graduate Program in AI & Machine Learning: Business Applications**, McCombs School of
  Business, UT Austin — [verify](https://vrfy.digital/index.php?key=onsxllql) · conferred July
  2025, 9.5 CEUs
