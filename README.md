# Akatsuki Hermes Team

🌀 Multi-Agent AI Team Setup untuk Hermes Agent — Inspired by Naruto's Akatsuki Organization

## Overview

Framework lengkap untuk setup **10-profile autonomous AI team** menggunakan [Hermes Agent](https://github.com/NousResearch/hermes) Kanban system.

### Team Structure

**Core Triad (3 profiles):**
- 👑 **Pain** — Orchestrator (strategy, decomposition, dispatch)
- 💻 **Itachi** — Deep Hunter (full-stack development, Phase 0-5 analysis)
- 🤖 **Sasori** — Fast Executor (automation, browser agents, quick fixes)

**Specialist Profiles (7 profiles):**
- ⚙️ **Obito** — DevOps & Infrastructure
- 🌊 **Kisame** — Data & Backend Engineering
- 🎨 **Konan** — UI/UX Design
- 🚀 **Deidara** — Growth & Marketing
- 🔍 **Zetsu** — Intelligence & Research
- 💰 **Treasury** — Trading & Portfolio Management
- 🔥 **Madara** — Security & Red Team

## Features

✅ **Complete Setup Guide** — 20+ pages covering architecture, config, workflow  
✅ **Profile Creator Script** — Automated profile generation  
✅ **Dispatch Strategy** — Decision tree for task assignment  
✅ **Multi-Agent Patterns** — Serial, parallel, and swarm coordination  
✅ **Production Ready** — systemd services, monitoring, troubleshooting  
✅ **Cost Optimized** — Model recommendations with budget estimates  

## Quick Start

```bash
# 1. Clone repo
git clone https://github.com/[YOUR_USERNAME]/akatsuki-hermes-team.git
cd akatsuki-hermes-team

# 2. Create profiles
chmod +x create_profiles.sh
./create_profiles.sh

# 3. Configure each profile
# Edit ~/.hermes/profiles/<profile>/config.yaml

# 4. Set API keys
cat >> ~/.hermes/.env <<EOF
OPENROUTER_API_KEY=sk-or-...
KIMCHI_API_KEY=castai_v1_...
EOF

# 5. Start core gateways
hermes gateway --profile pain &
hermes gateway --profile itachi &
hermes gateway --profile sasori &

# 6. Initialize Kanban (via Telegram)
# @Pain_bot /kanban init
```

## Documentation

- 📖 **[AKATSUKI_TEAM_GUIDE.md](./AKATSUKI_TEAM_GUIDE.md)** — Complete setup guide
- 🎯 **[skills/akatsuki-dispatch.md](./skills/akatsuki-dispatch.md)** — Dispatch strategy
- 🚀 **[README.md](./README.md)** — This file

## Example Workflows

### Build Airdrop Bot
```
Pain → Zetsu (research) → Sasori (automation) → Obito (deploy)
```

### Product Launch
```
Pain → Itachi (dev) + Konan (design) → Obito (deploy) → Deidara (marketing)
```

### Bug Bounty
```
Pain → Zetsu (recon) → Madara (scan) → Itachi (audit) → Madara (exploit)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    👑 Pain (Orchestrator)                    │
│              Strategy · Decomposition · Dispatch             │
└────────────┬────────────────────────────────────┬───────────┘
             │                                    │
    ┌────────▼────────┐                  ┌───────▼────────┐
    │ 💻 Itachi       │                  │ 🤖 Sasori      │
    │ Deep Hunter     │                  │ Fast Executor  │
    └─────────────────┘                  └────────────────┘
```

## Cost Estimate

| Profile | Model | Monthly Cost |
|---------|-------|--------------|
| Pain | claude-sonnet-4 | ~$30 |
| Itachi | kimi-k2.7 | ~$50 |
| Sasori | deepseek-v4-flash | ~$10 |
| Specialists (7) | mixed | ~$140 |
| **Total** | | **~$230/mo** |

*Moderate usage. Can be reduced to ~$50/mo with deepseek-v4-flash for all profiles.*

## Requirements

- [Hermes Agent](https://github.com/NousResearch/hermes) v0.6.0+
- API keys for:
  - OpenRouter (recommended for Pain, Konan, Madara)
  - Kimchi / Custom provider (for Itachi, Sasori, specialists)
- Telegram bot (for Kanban coordination)
- Linux VPS (recommended for production)

## Production Setup

### systemd Services

```bash
# Generate services for all profiles
for profile in pain itachi sasori obito kisame konan deidara zetsu treasury madara; do
  sudo systemctl enable hermes-${profile}
  sudo systemctl start hermes-${profile}
done
```

See **AKATSUKI_TEAM_GUIDE.md** for complete systemd setup.

## Comparison: Lean vs Specialized

### KARA Team (Lean — 3 profiles)
- Eida (orchestrator)
- Code (deep hunter)
- Daemon (fast executor)
- **Use case:** DevOps, bug bounty, focused projects

### Akatsuki Team (Specialized — 10 profiles)
- Pain + 9 specialists
- **Use case:** Full product development, trading, marketing, multi-domain projects

## Inspiration

- **Hermes Kanban System:** https://hermes-agent.nousresearch.com/docs/kanban
- **BREACH v5:** Unrestricted agent capabilities (optional integration)
- **KARA Team:** Reference implementation by [@0xjosee](https://github.com/Dinikowoh27)

## Contributing

This is a community template. Feel free to:
- Fork and customize for your team
- Add new specialist profiles
- Share your dispatch strategies
- Submit improvements via PR

## License

MIT License — Free to use, modify, and distribute.

## Credits

**Built by EiDA** 💜 for the Akatsuki community.

Special thanks to:
- [Nous Research](https://nousresearch.com) — Hermes Agent
- [@0xjosee](https://github.com/Dinikowoh27) — KARA Team reference

---

*"In the end, we'll achieve true understanding."* — Pain

## Support

- **Hermes Docs:** https://hermes-agent.nousresearch.com/docs
- **Issues:** Open a GitHub issue
- **Community:** Join Hermes Discord / Telegram
