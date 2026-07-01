# Akatsuki Hermes Team — Setup yang Benar

🌀 Template multi-agent AI team untuk [Hermes Agent](https://hermes-agent.nousresearch.com/docs).  
**Fokus utama repo ini:** bot **@SLEVENSYAIBOT** jadi orchestrator (kayak Eida), dan 10 profil Akatsuki jadi worker (kayak Code/Daemon).

---

## ⚠️ Perbaikan Konsep yang Sering Salah

Banyak yang langsung anggin **Pain = Orchestrator**. Itu salah kalau bot utamanya adalah **@SLEVENSYAIBOT**.

| Role | Bot | Profile | Dispatcher | Analogi KARA |
|---|---|---|---|---|
| **Orchestrator** | @SLEVENSYAIBOT | `slevensyai` (atau `default`) | ✅ ON | Eida |
| **Deep Hunter** | @Pain02_bot (atau bot Pain) | `pain` | ❌ OFF | Code |
| **Fast Executor** | @Itachi_bot | `itachi` | ❌ OFF | — |
| **Automation** | @Sasori_bot | `sasori` | ❌ OFF | Daemon |
| **Specialists** | masing-masing bot | `obito`, `kisame`, `konan`, `deidara`, `zetsu`, `treasury`, `madara` | ❌ OFF | — |

**Ingat:**
- **1 dispatcher** saja, di profil orchestrator.
- **10 worker** tidak perlu dispatcher.
- Pain cuma salah satu worker, bukan orchestrator.

---

## Arsitektur

```
User (DM / Group / Topic) → @SLEVENSYAIBOT
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Orchestrator       │
                    │  kanban dispatcher  │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
   ┌─────────┐          ┌──────────┐          ┌──────────┐
   │  Pain   │          │  Itachi  │          │  Sasori  │
   └─────────┘          └──────────┘          └──────────┘
        │                      │                      │
        ▼                      ▼                      ▼
   Obito · Kisame · Konan · Deidara · Zetsu · Treasury · Madara
```

---

## Isi Repo

```
akatsuki-hermes-team/
├── README.md                          ← ini
├── AKATSUKI_TEAM_GUIDE.md             ← panduan lengkap step-by-step
├── tokens.json.example                ← template token & topic
├── create_profiles.sh                 ← buat 10 profil worker
├── setup.sh                           ← setup orchestrator + worker + systemd
├── configs/
│   ├── config-orchestrator.yaml
│   └── config-worker.yaml
├── scripts/
│   ├── create-topics.py               ← auto-create Telegram forum topics
│   ├── patch-env.py                   ← inject token ke .env tiap profil
│   └── install-systemd.sh             ← install systemd services
├── systemd/
│   ├── hermes-orchestrator.service
│   └── hermes-worker.service
└── skills/
    └── akatsuki-dispatch.md           ← dispatch strategy untuk orchestrator
```

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Dinikowoh27/akatsuki-hermes-team.git
cd akatsuki-hermes-team

# 2. Copy template token
cp tokens.json.example tokens.json
# Edit tokens.json — isi group_id, allowed_users, dan bot_token tiap profile

# 3. Buat profil & inject config + token
chmod +x setup.sh
./setup.sh

# 4. Buat forum topics di Telegram (pakai bot orchestrator)
python3 scripts/create-topics.py tokens.json

# 5. Install systemd
./scripts/install-systemd.sh tokens.json

# 6. Start services
systemctl --user enable --now hermes-slevensyai hermes-pain hermes-itachi hermes-sasori
```

Lihat [AKATSUKI_TEAM_GUIDE.md](./AKATSUKI_TEAM_GUIDE.md) untuk penjelasan detail tiap langkah.

---

## Alur Kerja yang Benar

1. User kirim tugas ke **@SLEVENSYAIBOT** (DM atau topic orchestrator).
2. Orchestrator decompose tugas, buat Kanban card, assign ke worker.
3. Worker (misal Pain/Itachi/Sasori) mengerjakan, report balik ke orchestrator.
4. Orchestrator rangkum hasil ke user.

---

## Biaya Perkiraan

| Profile | Model | Estimasi/bulan |
|---|---|---|
| Orchestrator (`slevensyai`) | `claude-sonnet-4` | ~$30 |
| Pain / Itachi / Zetsu | `kimi-k2.7` | ~$40–60 each |
| Sasori / Obito / Treasury | `deepseek-v4-flash` | ~$10 each |
| Konan / Deidara | `gpt-4o` / `gpt-4o-mini` | ~$20–30 |
| Madara | `claude-opus-4` | ~$35 |
| **Total** | | **~$200–300/bulan** |

Bisa dipangkas pakai `deepseek-v4-flash` untuk semua worker → **~$50–80/bulan**.

---

## Support

- Hermes Docs: https://hermes-agent.nousresearch.com/docs
- Kanban Docs: https://hermes-agent.nousresearch.com/docs/kanban
- Issues: buka GitHub issue di repo ini.

---

*Built by EiDA 💜 for Akatsuki Team.*
