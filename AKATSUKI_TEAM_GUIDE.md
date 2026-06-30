# 🌀 Akatsuki AI Team — Hermes Kanban Setup Guide

> **Multi-Agent Autonomous Team** menggunakan Hermes Agent Kanban System  
> Terinspirasi dari KARA Team (EiDA-Code-Daemon) + BREACH v5 capabilities

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Team Structure](#team-structure)
3. [Profile Setup](#profile-setup)
4. [Skill Assignments](#skill-assignments)
5. [Workflow & Dispatch Rules](#workflow--dispatch-rules)
6. [Model Configuration](#model-configuration)
7. [Installation Steps](#installation-steps)
8. [Example Tasks](#example-tasks)
9. [Monitoring & Logs](#monitoring--logs)
10. [Troubleshooting](#troubleshooting)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    👑 Pain (Orchestrator)                    │
│              Strategy · Decomposition · Dispatch             │
└────────────┬────────────────────────────────────┬───────────┘
             │                                    │
    ┌────────▼────────┐                  ┌───────▼────────┐
    │ 💻 Itachi       │                  │ 🤖 Sasori      │
    │ Deep Hunter     │                  │ Fast Executor  │
    │ Phase 0-5       │                  │ Automation     │
    └────────┬────────┘                  └───────┬────────┘
             │                                    │
             └──────────┬─────────────────────────┘
                        │
         ┌──────────────┴──────────────────────────────┐
         │        Specialist Profiles (On-Demand)      │
         ├─────────────────────────────────────────────┤
         │ ⚙️  Obito      DevOps & Infrastructure      │
         │ 🌊 Kisame     Data & Backend Engineering    │
         │ 🎨 Konan      UI/UX Design                  │
         │ 🚀 Deidara    Growth & Marketing            │
         │ 🔍 Zetsu      Intelligence & Research       │
         │ 💰 Treasury   Trading & Portfolio Mgmt      │
         │ 🔥 Madara     Security & Red Team           │
         └─────────────────────────────────────────────┘
```

**Design Philosophy:**
- **3 Core Profiles** handle 80% of work (Pain → Itachi/Sasori)
- **7 Specialist Profiles** triggered on-demand via skills
- **Kanban Board** as central orchestration
- **Topic-based isolation** (setiap project = 1 topic Telegram)

---

## Team Structure

### 🎯 Core Triad

| Profile | Role | Primary Function | Model Recommendation |
|---------|------|-----------------|---------------------|
| **Pain** | Orchestrator | Task decomposition, dispatch, final approval, strategy | `claude-sonnet-4` or `gpt-4o` |
| **Itachi** | Deep Hunter | Full-stack dev, architecture, security review (Phase 0-5) | `kimi-k2.7` or `claude-opus-4` |
| **Sasori** | Fast Executor | Automation, browser agent, airdrop bot, quick fixes | `deepseek-v4-flash` or `gpt-4o-mini` |

### 🛠️ Specialist Profiles

| Profile | Role | Triggered When | Model |
|---------|------|---------------|-------|
| **Obito** | DevOps Engineer | Deploy, VPS setup, CI/CD, monitoring | `deepseek-v4-flash` |
| **Kisame** | Data Engineer | Database design, ETL, API backend | `kimi-k2.7` |
| **Konan** | UI/UX Designer | Wireframe, prototype, design system | `gpt-4o` or `claude-sonnet-4` |
| **Deidara** | Growth Hacker | Marketing campaign, viral content, SEO | `gpt-4o-mini` |
| **Zetsu** | Intelligence Analyst | Research, OSINT, recon, alpha hunting | `kimi-k2.7` |
| **Treasury** | Trader & Portfolio Manager | Meme coin sniping, portfolio, PnL tracking | `deepseek-v4-flash` |
| **Madara** | Security Specialist | Bug bounty, penetration test, red team | `claude-opus-4` |

---

## Profile Setup

### 1. Create Profiles

```bash
# Di VPS / local machine
cd ~/.hermes/profiles

# Create each profile
for profile in pain itachi sasori obito kisame konan deidara zetsu treasury madara; do
    mkdir -p $profile
    touch $profile/config.yaml
    mkdir -p $profile/{skills,memories,cron,sessions}
done
```

### 2. Configure Each Profile

#### 👑 Pain (Orchestrator) — `~/.hermes/profiles/pain/config.yaml`

```yaml
model:
  default: claude-sonnet-4
  provider: openrouter  # atau custom provider
  api_key: ${OPENROUTER_API_KEY}

agent:
  max_turns: 90
  reasoning_effort: medium

toolsets:
  - hermes-cli
  - terminal
  - file
  - kanban

display:
  personality: technical
  compact: false

kanban:
  orchestrator_profile: pain  # IMPORTANT: Pain sebagai orchestrator
  dispatch_in_gateway: true
  dispatch_interval_seconds: 60
  auto_decompose: true
  auto_decompose_per_tick: 3
```

#### 💻 Itachi (Deep Hunter) — `~/.hermes/profiles/itachi/config.yaml`

```yaml
model:
  default: kimi-k2.7
  provider: custom
  base_url: https://llm.kimchi.dev/openai/v1
  api_key: ${KIMCHI_API_KEY}

agent:
  max_turns: 90
  reasoning_effort: high

toolsets:
  - hermes-cli
  - terminal
  - file
  - web
  - github
  - coding

display:
  personality: technical
  compact: false
```

#### 🤖 Sasori (Fast Executor) — `~/.hermes/profiles/sasori/config.yaml`

```yaml
model:
  default: deepseek-v4-flash
  provider: custom
  base_url: https://llm.kimchi.dev/openai/v1
  api_key: ${KIMCHI_API_KEY}

agent:
  max_turns: 50  # faster iterations
  reasoning_effort: low

toolsets:
  - hermes-cli
  - terminal
  - file
  - browser
  - coding

display:
  personality: concise
  compact: true
```

#### ⚙️ Obito (DevOps) — `~/.hermes/profiles/obito/config.yaml`

```yaml
model:
  default: deepseek-v4-flash
  provider: custom
  base_url: https://llm.kimchi.dev/openai/v1
  api_key: ${KIMCHI_API_KEY}

agent:
  max_turns: 60

toolsets:
  - hermes-cli
  - terminal
  - file

display:
  personality: technical
```

#### 🌊 Kisame (Data Engineer) — `~/.hermes/profiles/kisame/config.yaml`

```yaml
model:
  default: kimi-k2.7
  provider: custom
  base_url: https://llm.kimchi.dev/openai/v1
  api_key: ${KIMCHI_API_KEY}

agent:
  max_turns: 70

toolsets:
  - hermes-cli
  - terminal
  - file
  - web

display:
  personality: technical
```

#### 🎨 Konan (UI/UX Designer) — `~/.hermes/profiles/konan/config.yaml`

```yaml
model:
  default: gpt-4o
  provider: openrouter
  api_key: ${OPENROUTER_API_KEY}

agent:
  max_turns: 60

toolsets:
  - hermes-cli
  - file
  - vision
  - web

display:
  personality: creative
```

#### 🚀 Deidara (Growth Hacker) — `~/.hermes/profiles/deidara/config.yaml`

```yaml
model:
  default: gpt-4o-mini
  provider: openrouter
  api_key: ${OPENROUTER_API_KEY}

agent:
  max_turns: 50

toolsets:
  - hermes-cli
  - file
  - web
  - social-media

display:
  personality: creative
```

#### 🔍 Zetsu (Intelligence) — `~/.hermes/profiles/zetsu/config.yaml`

```yaml
model:
  default: kimi-k2.7
  provider: custom
  base_url: https://llm.kimchi.dev/openai/v1
  api_key: ${KIMCHI_API_KEY}

agent:
  max_turns: 80

toolsets:
  - hermes-cli
  - web
  - file
  - terminal

display:
  personality: technical
```

#### 💰 Treasury (Trader) — `~/.hermes/profiles/treasury/config.yaml`

```yaml
model:
  default: deepseek-v4-flash
  provider: custom
  base_url: https://llm.kimchi.dev/openai/v1
  api_key: ${KIMCHI_API_KEY}

agent:
  max_turns: 60

toolsets:
  - hermes-cli
  - terminal
  - file
  - web

display:
  personality: concise
```

#### 🔥 Madara (Security) — `~/.hermes/profiles/madara/config.yaml`

```yaml
model:
  default: claude-opus-4
  provider: openrouter
  api_key: ${OPENROUTER_API_KEY}

agent:
  max_turns: 90
  reasoning_effort: high

toolsets:
  - hermes-cli
  - terminal
  - file
  - web
  - security

display:
  personality: technical
```

---

## Skill Assignments

### Core Skills (Load Semua Profile)

```bash
~/.hermes/skills/
├── software-development/
│   ├── systematic-debugging
│   ├── test-driven-development
│   └── requesting-code-review
├── github/
│   ├── github-pr-workflow
│   ├── github-code-review
│   └── github-repo-management
└── devops/
    ├── hermes-kanban-team
    ├── kanban-orchestrator  # Pain only
    └── kanban-worker        # Workers only
```

### Specialist Skills (Per Profile)

#### 👑 Pain
```
skills/devops/kanban-orchestrator
skills/devops/bugbounty-dispatch (kalau ada bug bounty workflow)
skills/software-development/writing-plans
```

#### 💻 Itachi
```
skills/software-development/* (all)
skills/github/* (all)
skills/mlops/* (jika ada ML project)
skills/devops/nextjs-standalone-deploy
```

#### 🤖 Sasori
```
skills/automation/browser-agent
skills/devops/kanban-worker
skills/productivity/airtable (jika pakai Airtable)
skills/social-media/xurl (X automation)
```

#### ⚙️ Obito
```
skills/devops/cloudflare-tunnel
skills/devops/vps-security-audit
skills/devops/nextjs-standalone-deploy
skills/devops/solana-agent-deploy (jika ada Solana bot)
```

#### 🌊 Kisame
```
skills/data-science/jupyter-live-kernel (jika pakai Jupyter)
skills/mlops/models/* (jika ada ML backend)
```

#### 🎨 Konan
```
skills/creative/sketch
skills/creative/design-md
skills/creative/excalidraw
skills/creative/popular-web-designs
```

#### 🚀 Deidara
```
skills/social-media/xurl
skills/media/gif-search
skills/productivity/notion (jika pakai Notion CMS)
skills/creative/humanizer (humanize AI text)
```

#### 🔍 Zetsu
```
skills/research/arxiv
skills/research/polymarket
skills/web/* (all web research)
skills/security/bugbounty-recon
```

#### 💰 Treasury
```
skills/defi/meridian (jika pakai Meridian LP agent)
skills/superagent-crypto/* (jika ada crypto agent)
```

#### 🔥 Madara
```
skills/security/* (all)
skills/red-teaming/godmode (jailbreak testing)
```

---

## Workflow & Dispatch Rules

### Kanban Board Topics (Telegram)

Setup **Telegram Group** dengan topics untuk isolasi:

| Topic ID | Name | Assignee | Use Case |
|----------|------|----------|----------|
| 12 | 👑 Pain HQ | Pain | Orchestration center, daily standup |
| 13 | 💻 Itachi Lab | Itachi | Deep dev work, architecture |
| 14 | 🤖 Sasori Workshop | Sasori | Automation, quick fixes |
| 15 | ⚙️ Obito Ops | Obito | Infrastructure, deployments |
| 16 | 🌊 Kisame Data | Kisame | Backend, database, ETL |
| 17 | 🎨 Konan Studio | Konan | Design work |
| 18 | 🚀 Deidara Arena | Deidara | Marketing campaigns |
| 19 | 🔍 Zetsu Intel | Zetsu | Research reports |
| 20 | 💰 Treasury Vault | Treasury | Trading, PnL |
| 21 | 🔥 Madara Dojo | Madara | Security findings |
| 22 | 🌀 Lounge | All | General chat, off-topic |

### Dispatch Strategy (Pain's Logic)

**Pain** decomposes tasks dan assign berdasarkan:

```yaml
# ~/.hermes/profiles/pain/skills/akatsuki-dispatch.md
---
name: akatsuki-dispatch
description: Decomposition and dispatch playbook for Pain orchestrator
---

## Dispatch Rules

### Phase Detection
1. **Planning/Architecture** → Itachi (deep analysis)
2. **Quick Fix/Automation** → Sasori (fast execution)
3. **Infrastructure** → Obito
4. **Database/Backend** → Kisame
5. **UI/UX** → Konan
6. **Marketing** → Deidara
7. **Research** → Zetsu
8. **Trading** → Treasury
9. **Security** → Madara

### Multi-Agent Tasks
- **Full-stack feature**: Pain → Itachi (backend) + Konan (design) + Sasori (automation)
- **Product launch**: Pain → Itachi (dev) + Obito (deploy) + Deidara (marketing)
- **Airdrop campaign**: Pain → Zetsu (research) + Sasori (bot) + Treasury (wallet mgmt)
- **Bug bounty**: Pain → Madara (recon) + Itachi (exploit dev) + Treasury (payout)

### Anti-Patterns (Don't Assign)
- ❌ Konan untuk backend code
- ❌ Sasori untuk deep architecture
- ❌ Deidara untuk security audit
- ❌ Treasury untuk UI design

### Escalation
- Stuck > 2 attempts → escalate to Pain
- Security issue → always loop Madara
- Performance issue → loop Itachi + Obito
```

---

## Model Configuration

### Recommended Model Allocation

| Profile | Model | Provider | Cost/1M tokens | Use Case |
|---------|-------|----------|---------------|----------|
| Pain | `claude-sonnet-4` | OpenRouter | $3 | Strategic thinking |
| Itachi | `kimi-k2.7` | Kimchi | ~$0.5 | Deep dev, long context |
| Sasori | `deepseek-v4-flash` | Kimchi | ~$0.1 | Fast automation |
| Obito | `deepseek-v4-flash` | Kimchi | ~$0.1 | DevOps scripts |
| Kisame | `kimi-k2.7` | Kimchi | ~$0.5 | Data analysis |
| Konan | `gpt-4o` | OpenRouter | $2.5 | Creative design |
| Deidara | `gpt-4o-mini` | OpenRouter | $0.15 | Content generation |
| Zetsu | `kimi-k2.7` | Kimchi | ~$0.5 | Research, long docs |
| Treasury | `deepseek-v4-flash` | Kimchi | ~$0.1 | Trading logic |
| Madara | `claude-opus-4` | OpenRouter | $15 | Complex security |

**Monthly Budget Estimate** (moderate usage):
- Pain: $30
- Itachi: $50
- Sasori: $10
- Specialists: $20 each
- **Total: ~$200-300/month**

---

## Installation Steps

### 1. Prerequisites

```bash
# Install Hermes Agent (latest)
curl -fsSL https://hermes.run/install.sh | bash

# Set up .env
cat >> ~/.hermes/.env <<EOF
OPENROUTER_API_KEY=sk-or-v1-...
KIMCHI_API_KEY=castai_v1_...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_GROUP_ID=-100...
EOF
```

### 2. Create All Profiles

```bash
# Run profile creator script
cat > ~/create_akatsuki_profiles.sh <<'SCRIPT'
#!/bin/bash
PROFILES=(pain itachi sasori obito kisame konan deidara zetsu treasury madara)

for profile in "${PROFILES[@]}"; do
    echo "Creating profile: $profile"
    mkdir -p ~/.hermes/profiles/$profile/{skills,memories,cron,sessions}
    
    # Copy config template (sesuaikan dengan config di atas)
    # touch ~/.hermes/profiles/$profile/config.yaml
done

echo "All profiles created!"
SCRIPT

chmod +x ~/create_akatsuki_profiles.sh
bash ~/create_akatsuki_profiles.sh
```

### 3. Setup Telegram Topics

1. Buat Telegram Group baru
2. Enable Topics: Group Settings → Topics → Enable
3. Create topics sesuai tabel di atas
4. Note topic IDs (inspect URL atau via bot)
5. Update `~/.hermes/profiles/pain/config.yaml`:

```yaml
telegram:
  extra:
    allowed_topics:
      - 12  # Pain HQ
      - 13  # Itachi Lab
      - 14  # Sasori Workshop
      # ... dst
```

### 4. Start Gateway for Each Profile

```bash
# Terminal 1: Pain (orchestrator)
hermes gateway --profile pain

# Terminal 2: Itachi
hermes gateway --profile itachi

# Terminal 3: Sasori
hermes gateway --profile sasori

# Terminal 4-10: Specialists (on-demand, bisa pakai systemd)
hermes gateway --profile obito
hermes gateway --profile kisame
# ... dst
```

**Production Setup (systemd):**

```bash
# Generate systemd services
for profile in pain itachi sasori obito kisame konan deidara zetsu treasury madara; do
sudo tee /etc/systemd/system/hermes-${profile}.service > /dev/null <<EOF
[Unit]
Description=Hermes Agent Gateway - ${profile}
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME
ExecStart=$HOME/.hermes/hermes-agent/venv/bin/hermes gateway --profile ${profile}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable hermes-${profile}
sudo systemctl start hermes-${profile}
done

# Check status
sudo systemctl status hermes-pain
```

### 5. Initialize Kanban Board

```bash
# Connect to Pain profile Telegram
# Send in topic "Pain HQ":
@Pain_bot /kanban init

# Verify
@Pain_bot /kanban list
```

---

## Example Tasks

### Task 1: Build Full-Stack Airdrop Bot

**User message in Pain HQ:**
```
Build an airdrop bot for Unichain testnet:
- Multi-wallet support (10 wallets)
- Actions: swap, add liquidity, bridge
- Proxy rotation
- Deploy on VPS with monitoring
```

**Pain's decomposition:**
```markdown
## Task: Unichain Airdrop Bot

### Subtasks
1. **Research** (Zetsu) — Find Unichain testnet docs, faucet, contracts
2. **Bot Development** (Sasori) — Build browser automation + wallet rotation
3. **Backend Service** (Kisame) — Wallet management API, task queue
4. **Deployment** (Obito) — VPS setup, Docker, monitoring
5. **Testing** (Itachi) — Security review, dry run

### Dispatch
- [ ] #1 → Zetsu (Topic 19)
- [ ] #2 → Sasori (Topic 14) [blocked by #1]
- [ ] #3 → Kisame (Topic 16)
- [ ] #4 → Obito (Topic 15) [blocked by #2, #3]
- [ ] #5 → Itachi (Topic 13) [blocked by #4]
```

**Kanban board:**
```
┌─────────┬──────────┬────────────┬──────┐
│ Backlog │ Todo     │ In Progress│ Done │
├─────────┼──────────┼────────────┼──────┤
│         │ #2 Sasori│ #1 Zetsu   │      │
│         │ #3 Kisame│            │      │
│         │ #4 Obito │            │      │
│         │ #5 Itachi│            │      │
└─────────┴──────────┴────────────┴──────┘
```

### Task 2: Launch Marketing Campaign

**User in Pain HQ:**
```
Launch Twitter campaign for our new DEX:
- 10 viral tweets (meme + alpha)
- Community engagement strategy
- Landing page design
```

**Pain dispatch:**
```markdown
1. **Content Strategy** (Deidara) — Draft 10 tweets + engagement plan
2. **Visual Assets** (Konan) — Meme templates, social cards
3. **Landing Page** (Itachi) — Build Next.js landing page
4. **Deployment** (Obito) — Deploy landing page
5. **Automation** (Sasori) — Schedule tweets, auto-reply bot
```

### Task 3: Bug Bounty on Immunefi

**User in Pain HQ:**
```
Hunt bugs on Immunefi for Project X (DeFi protocol):
- Budget: 3 days
- Target: Critical/High severity
```

**Pain dispatch:**
```markdown
1. **Recon** (Zetsu) — Gather contracts, docs, competitors
2. **Initial Scan** (Madara) — Run automated scanners (Slither, Mythril)
3. **Manual Review** (Itachi) — Deep code audit, business logic
4. **Exploit Dev** (Madara) — Write PoC for findings
5. **Report** (Pain) — Compile report, submit to Immunefi
```

---

## Monitoring & Logs

### Kanban Status Dashboard

```bash
# Check board status
hermes --profile pain kanban list

# Check worker logs
tail -f ~/.hermes/profiles/itachi/kanban/*.log
tail -f ~/.hermes/profiles/sasori/kanban/*.log
```

### Telegram Monitoring

Pain's **daily standup** (automated cron):

```yaml
# ~/.hermes/profiles/pain/cron/standup.yaml
name: daily-standup
schedule: "0 9 * * *"  # 9 AM daily
prompt: |
  Generate daily standup report for Akatsuki team:
  1. Tasks completed yesterday (check Kanban)
  2. Tasks in progress
  3. Blocked tasks
  4. Today's priorities
  
  Format: Telegram message with emojis, casual tone.
deliver: telegram:${TELEGRAM_GROUP_ID}:12  # Pain HQ topic
```

### Cost Tracking

```bash
# Check token usage per profile
hermes --profile pain stats
hermes --profile itachi stats

# Monthly cost estimate
hermes stats --all-profiles --month 2026-06
```

---

## Troubleshooting

### Issue: Worker Not Picking Up Tasks

**Diagnosis:**
```bash
# Check gateway status
sudo systemctl status hermes-itachi

# Check Kanban logs
tail -50 ~/.hermes/profiles/itachi/kanban/dispatcher.log
```

**Fix:**
```bash
# Restart gateway
sudo systemctl restart hermes-itachi

# Or reload config
hermes --profile itachi config reload
```

### Issue: Task Stuck in "In Progress"

**Diagnosis:**
```bash
# Check task status
hermes --profile pain kanban show <task_id>

# Check worker session
hermes --profile itachi sessions list
```

**Fix:**
```bash
# Manually move task
hermes --profile pain kanban move <task_id> todo

# Or cancel and reassign
hermes --profile pain kanban cancel <task_id>
```

### Issue: Pain Not Decomposing

**Check:**
1. `kanban.orchestrator_profile: pain` set in Pain's config?
2. `kanban.auto_decompose: true`?
3. Pain gateway running?

**Fix:**
```bash
# Restart Pain gateway
sudo systemctl restart hermes-pain

# Manual decompose
hermes --profile pain kanban decompose <task_id>
```

### Issue: High Token Usage

**Analysis:**
```bash
# Find expensive profiles
hermes stats --all-profiles --sort-by cost

# Check long sessions
hermes --profile itachi sessions list --sort-by tokens
```

**Mitigation:**
1. Lower `max_turns` in expensive profiles
2. Switch Itachi to `deepseek-v4-flash` for simple tasks
3. Enable compression earlier:
```yaml
compression:
  threshold: 0.4  # compress sooner
```

---

## Advanced: BREACH Integration

Jika ingin adopt **BREACH v5** (unrestricted agent) untuk aggressive tasks:

### Setup Madara with BREACH Mode

```bash
# Copy BREACH SOUL.md
cp ~/BREACH_v5_SOUL.md ~/.hermes/profiles/madara/SOUL.md

# Update config
cat >> ~/.hermes/profiles/madara/config.yaml <<EOF
# BREACH mode: unrestricted for red team
agent:
  tool_use_enforcement: permissive
  
# Governor + confirm gate
approval:
  enabled: true
  auto_approve: false  # manual confirm for destructive actions
EOF
```

**Use cases:**
- Bug bounty fuzzing
- API rate limit bypass testing
- Web scraping at scale
- Exploit PoC development

**IMPORTANT:** BREACH mode = **testnet/staging only**. Never production.

---

## Scaling Beyond 10 Profiles

Kalau tim grow:

| New Profile | Role | When to Add |
|-------------|------|-------------|
| **Nagato** | Project Manager | >5 concurrent projects |
| **Yahiko** | QA Engineer | Need dedicated testing |
| **Konohamaru** | Junior Dev (Training) | Onboard new workflows |
| **Jiraiya** | Documentation Lead | Complex products |

---

## Support & Resources

- **Hermes Docs:** https://hermes-agent.nousresearch.com/docs
- **KARA Team Reference:** `/home/ubuntu/eida-workspace/` (Mas Hexa's setup)
- **Skill Library:** `~/.hermes/skills/`
- **Community:** Hermes Discord / Telegram

---

**Built with 💜 by EiDA for the Akatsuki Team**

*"In the end, we'll achieve true understanding."* — Pain
