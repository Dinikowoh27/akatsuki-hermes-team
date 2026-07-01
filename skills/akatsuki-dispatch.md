---
name: akatsuki-dispatch
description: >
  Decomposition and dispatch playbook untuk Akatsuki Team.
  Orchestrator = profil bot utama (@SLEVENSYAIBOT). Workers = 10 profil Akatsuki.
  Worker names: pain, itachi, sasori, obito, kisame, konan, deidara, zetsu, kakuzu, madara.
tags: [orchestrator, dispatch, kanban, akatsuki]
---

# Akatsuki Dispatch Strategy

> **Orchestrator = profil bot utama (@SLEVENSYAIBOT).**  
> **Pain, Itachi, Sasori, dll = workers.**  
> Orchestrator menerima tugas dari user, lalu decompose dan assign ke worker yang tepat.

Pain's decision tree untuk decompose dan assign tasks ke specialist profiles.

## 🎯 Profile Mapping

### Orchestrator (satu-satunya dispatcher)

| Profile | Bot | Role |
|---------|-----|------|
| **`<ORCHESTRATOR_NAME>`** | @SLEVENSYAIBOT | Decomposition, dispatch, final approval, strategy |

### Core Workers (Default)

| Profile | Archetype | Primary Domains | When to Assign |
|---------|-----------|----------------|---------------|
| **Itachi** | Deep Hunter | Full-stack dev, architecture, security review | Complex features, technical design, Phase 0-5 analysis |
| **Sasori** | Fast Executor | Automation, browser agent, quick fixes | Scripts, bots, rapid iteration, airdrop automation |

### Specialists (On-Demand)

| Profile | Trigger Keywords | Avoid |
|---------|-----------------|-------|
| **Obito** | deploy, VPS, Docker, CI/CD, nginx, monitoring, infrastructure | frontend code, design |
| **Kisame** | database, ETL, API backend, PostgreSQL, Redis, data pipeline | UI, marketing |
| **Konan** | design, wireframe, Figma, UI/UX, prototype, mockup | backend code, deployment |
| **Deidara** | marketing, Twitter, viral, SEO, growth, content, community | security, infrastructure |
| **Zetsu** | research, OSINT, recon, alpha, airdrop intel, competitor | implementation |
| **Treasury** | trading, meme coin, portfolio, PnL, wallet, sniper | design, DevOps |
| **Madara** | security, bug bounty, penetration test, exploit, red team | growth, marketing |

---

## 🔍 Task Classification

### By Complexity

```yaml
Simple (1-2h):
  - Assign: Sasori (fast executor)
  - Examples: script automation, config changes, quick fixes

Medium (1-2 days):
  - Assign: Itachi or specialist
  - Examples: feature implementation, API integration, design system

Complex (3+ days):
  - Strategy:
    1. Decompose into phases
    2. Itachi for architecture/Phase 0
    3. Distribute implementation to specialists
    4. Itachi for final integration/Phase 5
  - Examples: full product launch, multi-agent system, platform migration
```

### By Domain

```yaml
Full-Stack Feature:
  - Phase 0-1 (design): Itachi + Konan
  - Phase 2-3 (backend): Kisame
  - Phase 3 (frontend): Itachi
  - Phase 4 (deploy): Obito
  - Phase 5 (review): Itachi

Airdrop Campaign:
  - Research: Zetsu (find opportunities)
  - Bot dev: Sasori (automation)
  - Wallet mgmt: Treasury (multi-wallet setup)
  - Deploy: Obito (VPS + monitoring)

Marketing Launch:
  - Content: Deidara (tweets, blog posts)
  - Design: Konan (social cards, landing page)
  - Dev: Itachi (landing page code)
  - Deploy: Obito
  - Growth: Deidara (execution)

Bug Bounty:
  - Recon: Zetsu (target info)
  - Scan: Madara (automated tools)
  - Manual audit: Itachi (code review)
  - Exploit: Madara (PoC development)
  - Report: Pain (compile findings)

Infrastructure:
  - Setup: Obito (provision, config)
  - Security: Madara (hardening)
  - Monitoring: Obito (alerts, logs)
```

---

## 🚦 Dispatch Decision Tree

```
Task received
    │
    ├─ Is it research/intel? → Zetsu
    ├─ Is it urgent/simple script? → Sasori
    ├─ Is it security/red team? → Madara
    ├─ Is it design/UI? → Konan
    ├─ Is it marketing/growth? → Deidara
    ├─ Is it trading/portfolio? → Treasury
    ├─ Is it infra/deploy? → Obito
    ├─ Is it data/backend only? → Kisame
    │
    └─ Default (dev/complex):
        ├─ Needs deep analysis? → Itachi
        └─ Fast iteration? → Sasori
```

---

## 📋 Multi-Agent Coordination Patterns

### Pattern 1: Serial (Waterfall)
Zetsu → Itachi → Obito → Deidara

**Use when:** Dependencies clear, sequential phases.

**Example:** Product launch
1. Zetsu: market research
2. Itachi: build product
3. Obito: deploy
4. Deidara: marketing

### Pattern 2: Parallel (Concurrent)
(Itachi + Konan + Kisame) → Obito

**Use when:** Independent work streams, merge at end.

**Example:** Full-stack feature
- Itachi: frontend
- Konan: design system
- Kisame: API backend
- → Obito: deploy all

### Pattern 3: Swarm (Collaborative)
Madara + Itachi + Zetsu (同時進行, shared context)

**Use when:** Complex problem, need multiple perspectives.

**Example:** Security audit
- Madara: automated scans
- Itachi: code review
- Zetsu: threat intelligence
- → All contribute to final report

---

## ⚠️ Anti-Patterns (Don't Do This)

```yaml
❌ Konan for backend code:
  - Konan = design specialist
  - Assign backend to Kisame or Itachi

❌ Sasori for deep architecture:
  - Sasori = fast executor, not strategic planner
  - Assign to Itachi

❌ Deidara for security audit:
  - Deidara = growth, not security
  - Assign to Madara

❌ Treasury for UI design:
  - Treasury = trading logic
  - Assign to Konan

❌ Overloading Itachi:
  - Don't assign everything to Itachi
  - Distribute simple tasks to Sasori/specialists
```

---

## 🔄 Escalation Rules

### When to Escalate Back to Pain

```yaml
Worker stuck (>2 failed attempts):
  - Pain reviews task
  - Reassign or decompose further

Scope creep detected:
  - Worker flags: "This is bigger than expected"
  - Pain re-scopes and redistributes

Conflict between workers:
  - Example: Itachi and Obito disagree on architecture
  - Pain makes final call

Security issue found:
  - Always loop Madara
  - Pain decides: patch now vs. defer
```

---

## 📊 Load Balancing

Track each worker's queue:

```yaml
Max concurrent tasks per profile:
  Pain: 5 (orchestration only)
  Itachi: 3 (deep work needs focus)
  Sasori: 5 (fast iterations)
  Specialists: 2 each

Priority when multiple workers available:
  1. Least loaded
  2. Most relevant skill match
  3. Fastest recent completion time
```

---

## 🧪 Testing Assignment

Always route back through Itachi for Phase 5 review:

```yaml
Flow:
  Worker completes task
    → Itachi reviews (Phase 5)
    → Itachi tests
    → Itachi approves or requests changes
    → Done
```

---

## 🎓 Learning from Failures

Pain tracks:
- Which assignments failed
- Why they failed
- Adjust dispatch rules

Example:
```yaml
Failure: Assigned UI work to Sasori
Root cause: Sasori optimized for automation, not design
Fix: Route all UI to Konan
Update: Add "UI" keyword → Konan in dispatch tree
```

---

## 🔧 Dispatch Template (Pain's Internal Prompt)

```markdown
Task: [User request]

**Analysis:**
- Domain: [dev / infra / design / marketing / research / trading / security]
- Complexity: [simple / medium / complex]
- Urgency: [high / normal / low]
- Dependencies: [list blockers]

**Decomposition:**
1. Subtask 1 → [Profile] [estimated time]
2. Subtask 2 → [Profile] [blocked by #1]
3. ...

**Dispatch:**
- [ ] #1 → @Profile (Topic ID)
- [ ] #2 → @Profile (Topic ID) [blocked by #1]

**Success Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

**Review:** Itachi (Phase 5)
```

---

## 📚 References

- Hermes Kanban: https://hermes-agent.nousresearch.com/docs/kanban
- KARA Team (Eida-Code-Daemon): `/home/ubuntu/eida-workspace/`
- Akatsuki Guide: `./AKATSUKI_TEAM_GUIDE.md`

---

**Pain's Mantra:**
> *"Understand the task. Decompose ruthlessly. Assign precisely. Monitor constantly."*
