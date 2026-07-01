# 🌀 Akatsuki Hermes Team — Panduan Setup yang Benar

> **Multi-Agent AI Team** pakai Hermes Agent Kanban System.  
> **Perbaikan utama repo ini:** bot utama **@SLEVENSYAIBOT** = orchestrator, **Pain & 10 Akatsuki lainnya** = workers.

---

## 📋 Daftar Isi

1. [Konsep yang Benar](#konsep-yang-benar)
2. [Arsitektur](#arsitektur)
3. [Persiapan](#persiapan)
4. [Step-by-Step Setup](#step-by-step-setup)
5. [Konfigurasi Manual (kalau mau tau detail)](#konfigurasi-manual)
6. [Telegram Topics & allowed_topics](#telegram-topics--allowed_topics)
7. [systemd Services](#systemd-services)
8. [Testing](#testing)
9. [Dispatch Rules](#dispatch-rules)
10. [Troubleshooting](#troubleshooting)
11. [FAQ](#faq)
12. [Estimasi Biaya](#estimasi-biaya)

---

## Konsep yang Benar

Jangan sampai kebalik seperti setup sebelumnya:

| Role | Bot | Profile | Dispatcher? | Analogi KARA |
|---|---|---|---|---|
| **Orchestrator** | @SLEVENSYAIBOT | `slevensyai` / `default` | ✅ ON | Eida |
| **Deep Hunter** | @Pain02_bot | `pain` | ❌ OFF | Code |
| **Fast Executor** | @Itachi_bot | `itachi` | ❌ OFF | — |
| **Automation** | @Sasori_bot | `sasori` | ❌ OFF | Daemon |
| **Specialists** | masing-masing | `obito`, `kisame`, `konan`, `deidara`, `zetsu`, `kakuzu`, `madara` | ❌ OFF | — |

**Poin kunci:**
- Hanya **1 profil** yang punya `dispatch_in_gateway: true`.
- Semua worker harus set `orchestrator_profile: <nama_orchestrator>`.
- Pain adalah **salah satu worker**, bukan orchestrator.

---

## Arsitektur

```
User (DM / Group topic)
        │
        ▼
┌─────────────────────────────┐
│  Orchestrator               │
│  @SLEVENSYAIBOT             │
│  gateway + kanban dispatcher│
└──────────────┬──────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌───────┐ ┌────────┐ ┌─────────┐
│ Pain  │ │ Itachi │ │ Sasori  │
└───┬───┘ └───┬────┘ └────┬────┘
    │         │           │
    ▼         ▼           ▼
 Obito · Kisame · Konan · Deidara · Zetsu · Treasury · Madara
```

Alur kerja:
1. User kirim tugas ke **@SLEVENSYAIBOT**.
2. Orchestrator decompose → buat Kanban card → assign ke worker.
3. Worker mengerjakan, report balik ke orchestrator.
4. Orchestrator rangkum hasil ke user.

---

## Persiapan

Sebelum jalankan script:

1. **Hermes Agent sudah terinstall** di VPS.
2. **API keys** tersedia (OpenRouter, Kimchi, dll) → simpan di `~/.hermes/.env`.
3. **11 bot Telegram** sudah dibuat via @BotFather:
   - Satu bot untuk orchestrator (@SLEVENSYAIBOT).
   - Sepuluh bot untuk workers.
4. **Semua bot sudah dimasukkan ke grup Telegram** sebagai admin.
5. **Group Privacy OFF** untuk semua bot via @BotFather.
6. **Topic/Forum sudah di-enable** di grup Telegram.

---

## Step-by-Step Setup

### 1. Clone Repo

```bash
git clone https://github.com/Dinikowoh27/akatsuki-hermes-team.git
cd akatsuki-hermes-team
```

### 2. Siapkan `tokens.json`

```bash
cp tokens.json.example tokens.json
nano tokens.json
```

Isi dengan data asli:
- `group_id`: ID grup Telegram (contoh: `-1001234567890`).
- `allowed_users`: Telegram user ID owner (contoh: `[123456789]`).
- `orchestrator.profile_name`: nama profil bot utama (contoh: `slevensyai`).
- `orchestrator.bot_token`: token @SLEVENSYAIBOT.
- `orchestrator.topic_name`: nama topic orchestrator (contoh: `👑 Slevensyai HQ`).
- `workers.<name>.bot_token`: token tiap worker.
- `workers.<name>.topic_name`: nama topic tiap worker.
- Model & provider di bagian `models`.

### 3. Jalankan Setup

```bash
chmod +x setup.sh
./setup.sh tokens.json
```

Script ini akan:
- Membuat profil orchestrator & 10 worker.
- Generate `config.yaml` dari template.
- Patch `.env` tiap profil.
- Copy skill `akatsuki-dispatch.md` ke `~/.hermes/skills/custom/akatsuki-dispatch/`.

### 4. Buat Forum Topics

```bash
python3 scripts/create-topics.py tokens.json
```

Script pakai bot orchestrator untuk membuat topic di grup. Setelah sukses, `tokens.json` akan terisi `topic_id`.

**Kalau ada topic yang sudah dibuat manual:** isi `topic_id` di `tokens.json` secara manual.

### 5. Update Config & .env dengan topic_id

```bash
./setup.sh tokens.json
```

Jalankan lagi supaya `topic_id` masuk ke `config.yaml` dan `.env`.

### 6. Install systemd Services

```bash
chmod +x scripts/install-systemd.sh
./scripts/install-systemd.sh tokens.json
```

### 7. Start Services

Start orchestrator + core workers dulu:

```bash
systemctl --user enable --now hermes-slevensyai hermes-pain hermes-itachi hermes-sasori
```

Start semua worker:

```bash
for p in slevensyai pain itachi sasori obito kisame konan deidara zetsu kakuzu madara; do
  systemctl --user enable --now hermes-$p
done
```

**Catatan:** Di dalam running gateway, `systemctl restart` bisa diblokir oleh gateway guard. Kalau perlu restart dari luar, gunakan:

```bash
dbus-send --session --dest=org.freedesktop.systemd1 \
  --type=method_call --print-reply \
  /org/freedesktop/systemd1 \
  org.freedesktop.systemd1.Manager.RestartUnit \
  string:"hermes-slevensyai.service" string:"replace"
```

---

## Konfigurasi Manual

Kalau mau setup manual tanpa script, ini config yang paling penting.

### Orchestrator (`~/.hermes/profiles/slevensyai/config.yaml`)

```yaml
model:
  default: claude-sonnet-4
  provider: openrouter
  api_key: ${OPENROUTER_API_KEY}

agent:
  max_turns: 90

toolsets:
  - hermes-cli
  - terminal
  - file
  - kanban
  - delegation

notification_sources: '*'

kanban:
  orchestrator_profile: slevensyai   # MUST sama dengan nama profil ini
  dispatch_in_gateway: true
  dispatch_interval_seconds: 60
  auto_decompose: true
  auto_decompose_per_tick: 3

telegram:
  reactions: false
  allowed_users:
    - 123456789
  extra:
    rich_messages: true
    allowed_topics:
      - 12   # Orchestrator HQ
      - 22   # Lounge
```

### Worker (`~/.hermes/profiles/pain/config.yaml`)

```yaml
model:
  default: deepseek-v4-flash
  provider: custom
  base_url: https://llm.kimchi.dev/openai/v1
  api_key: ${KIMCHI_API_KEY}

agent:
  max_turns: 80

toolsets:
  - hermes-cli
  - terminal
  - file
  - web
  - coding

notification_sources: '*'

kanban:
  orchestrator_profile: slevensyai   # MUST ke orchestrator
  # dispatch_in_gateway: false       # default false, jangan diaktifkan

telegram:
  reactions: false
  allowed_users:
    - 123456789
  extra:
    rich_messages: true
    allowed_topics:
      - 13   # Pain topic
      - 22   # Lounge
```

### `.env` Worker

```bash
TELEGRAM_BOT_TOKEN=123456789:ABC...
TELEGRAM_ALLOWED_USERS=123456789
TELEGRAM_HOME_CHANNEL=-1001234567890:13
TELEGRAM_HOME_CHANNEL_NAME=Pain
TELEGRAM_CRON_THREAD_ID=13
TELEGRAM_ALLOWED_TOPICS=13,22
```

### `.env` Orchestrator

```bash
TELEGRAM_BOT_TOKEN=987654321:XYZ...
TELEGRAM_ALLOWED_USERS=123456789
TELEGRAM_HOME_CHANNEL=-1001234567890:12
TELEGRAM_HOME_CHANNEL_NAME=Slevensyai HQ
TELEGRAM_CRON_THREAD_ID=12
TELEGRAM_ALLOWED_TOPICS=12,22
```

---

## Telegram Topics & allowed_topics

### Membuat Topics

Bisa otomatis pakai script `create-topics.py`, atau manual:

1. Buka grup → buat topic dengan nama sesuai daftar.
2. Untuk dapat `topic_id`, buka topic di Telegram Web/Desktop, lihat URL:
   ```
   https://web.telegram.org/a/#-1001234567890_13
   ```
   Angka `13` setelah underscore adalah `topic_id`.

### Daftar Topic Rekomendasi

| Topic ID | Nama | Bot |
|:---:|:---|:---|
| 12 | 👑 Slevensyai HQ | @SLEVENSYAIBOT |
| 13 | 👑 Pain | @Pain02_bot |
| 14 | 💻 Itachi Lab | @Itachi_bot |
| 15 | 🤖 Sasori Workshop | @Sasori_bot |
| 16 | ⚙️ Obito Ops | @Obito_bot |
| 17 | 🌊 Kisame Data | @Kisame_bot |
| 18 | 🎨 Konan Studio | @Konan_bot |
| 19 | 🚀 Deidara Arena | @Deidara_bot |
| 20 | 🔍 Zetsu Intel | @Zetsu_bot |
| 21 | 💰 Kakuzu Treasury | @Kakuzu_bot |
| 22 | 🔥 Madara Dojo | @Madara_bot |
| 23 | 🌀 Lounge | all bots |

### Kenapa `allowed_topics` Penting?

Tanpa `allowed_topics`, **semua bot akan merespon di setiap topic**. Jadi wajib set di setiap profile:

```yaml
telegram:
  extra:
    allowed_topics:
      - <topic_id_worker_ini>
      - <topic_id_lounge>
```

---

## systemd Services

Template service yang di-generate:

```ini
[Unit]
Description=Hermes Gateway — slevensyai
After=network.target

[Service]
Type=simple
WorkingDirectory=%h
Environment="HOME=%h"
ExecStart=%h/.local/bin/slevensyai gateway run --replace
Restart=always
RestartSec=10
CPUQuota=40%
MemoryMax=768M

[Install]
WantedBy=default.target
```

**Wrapper script** (`~/.local/bin/slevensyai`) dibuat otomatis oleh `hermes profile create`.

**Cek status:**
```bash
systemctl --user status hermes-slevensyai
systemctl --user status hermes-pain
```

**Restart:**
```bash
systemctl --user restart hermes-slevensyai
```

**Catatan:** Kalau command dijalankan dari dalam gateway dan diblokir, gunakan `dbus-send` (lihat Step 7).

---

## Testing

### 1. Cek Gateway Running

```bash
hermes profile list
systemctl --user is-active hermes-slevensyai
systemctl --user is-active hermes-pain
```

### 2. Cek Bot Bisa Baca Grup

Untuk tiap bot:

```bash
TOKEN=$(cat ~/.hermes/profiles/pain/.env | grep TELEGRAM_BOT_TOKEN | cut -d= -f2)
curl -s "https://api.telegram.org/bot${TOKEN}/getMe" | python3 -m json.tool
```

Pastikan `can_read_all_group_messages: true`. Kalau `false`, matikan Group Privacy di @BotFather.

### 3. Test Dispatch

Di topic Orchestrator HQ, kirim:

```
Buatin script Python untuk scrape harga token dari CoinGecko, lalu simpan ke CSV.
```

**Harapan:** Orchestrator membuat Kanban card, assign ke Sasori atau Itachi. Worker tersebut mulai mengerjakan dan report di topic-nya.

### 4. Cek Kanban Board

```bash
hermes -p slevensyai kanban list
hermes -p slevensyai kanban tail
```

---

## Dispatch Rules

Orchestrator memakai skill `akatsuki-dispatch.md` untuk memutuskan assign ke siapa.

| Task Type | Assign ke |
|---|---|
| Planning / architecture / deep dev | Itachi |
| Quick script / automation / browser | Sasori |
| Deploy / VPS / CI/CD / infra | Obito |
| Database / ETL / backend data | Kisame |
| Design / UI/UX / mockup | Konan |
| Marketing / growth / content | Deidara |
| Research / OSINT / intel | Zetsu |
| Trading / portfolio / wallet | Kakuzu |
| Security / bug bounty / red team | Madara |
| General / unclear | Pain |

**Multi-agent patterns:**
- **Serial:** Zetsu → Itachi → Obito
- **Parallel:** Itachi + Konan + Kisame → Obito
- **Swarm:** Madara + Itachi + Zetsu untuk security audit

---

## Troubleshooting

### Semua bot merespon di semua topic

**Penyebab:** `allowed_topics` belum di-set atau Group Privacy masih ON.

**Solusi:**
1. Set `telegram.extra.allowed_topics` di config tiap profile.
2. Matikan Group Privacy semua bot via @BotFather.
3. Restart semua gateway.

### Worker tidak mengerjakan tugas

**Cek:**
```bash
hermes -p slevensyai kanban list
systemctl --user status hermes-pain
journalctl --user -u hermes-pain --no-pager -n 30
```

**Penyebab umum:**
- `orchestrator_profile` di worker beda dengan nama orchestrator.
- Worker gateway tidak running.
- `notification_sources` tidak di-set ke `'*'`.

### Orchestrator tidak mendispatch

**Cek:**
```bash
grep dispatch_in_gateway ~/.hermes/profiles/slevensyai/config.yaml
grep orchestrator_profile ~/.hermes/profiles/slevensyai/config.yaml
```

Pastikan:
```yaml
kanban:
  orchestrator_profile: slevensyai
  dispatch_in_gateway: true
```

### Bot tidak bisa buat topic

**Penyebab:** bot tidak punya permission **Manage topics**.

**Solusi:** di Telegram group → Administrators → pilih bot → enable **Manage Topics**.

### Gateway restart diblokir

Gunakan D-Bus:
```bash
dbus-send --session --dest=org.freedesktop.systemd1 \
  --type=method_call --print-reply \
  /org/freedesktop/systemd1 \
  org.freedesktop.systemd1.Manager.RestartUnit \
  string:"hermes-slevensyai.service" string:"replace"
```

---

## FAQ

### Q: Kenapa Pain bukan orchestrator?
**A:** Karena bot utamanya adalah @SLEVENSYAIBOT. Kalau Pain jadi orchestrator, @SLEVENSYAIBOT jadi bot personal yang nggak bisa dispatch. Pola KARA: Eida = orchestrator, Code/Daemon = workers. Di sini: @SLEVENSYAIBOT = Eida, Pain/Itachi/Sasori = Code/Daemon.

### Q: Apakah 10 worker harus online 24/7?
**A:** Tidak wajib. Bisa start on-demand. Tapi kalau mau dispatch langsung jalan, worker yang sering dipakai (Pain, Itachi, Sasori) sebaiknya online.

### Q: Bisa nggak pakai nama profil lain?
**A:** Bisa. Ganti `profile_name` di `tokens.json`. Pastikan konsisten di semua config.

### Q: Satu bot bisa dipakai untuk beberapa profile?
**A:** Tidak boleh. Setiap profile harus punya bot token sendiri supaya topic routing tidak bentrok.

### Q: `tokens.json` boleh di-commit ke GitHub?
**A:** Jangan! File itu sudah masuk `.gitignore`, tapi tetap hati-hati.

---

## Estimasi Biaya

| Profile | Model | Estimasi/bulan |
|---|---|---|
| Orchestrator (`slevensyai`) | claude-sonnet-4 | ~$30 |
| Pain / Sasori / Obito / Kakuzu | deepseek-v4-flash | ~$10 each |
| Itachi / Kisame / Zetsu | kimi-k2.7 | ~$30–50 each |
| Konan | gpt-4o | ~$25 |
| Deidara | gpt-4o-mini | ~$10 |
| Madara | claude-opus-4 | ~$35 |
| **Total** | | **~$200–300/bulan** |

**Tips hemat:** pakai `deepseek-v4-flash` untuk semua worker → turun ke **~$60–80/bulan**.

---

## Referensi

- Hermes Docs: https://hermes-agent.nousresearch.com/docs
- Hermes Kanban: https://hermes-agent.nousresearch.com/docs/kanban
- KARA Team Reference: setup Eida-Code-Daemon
- Repo ini: https://github.com/Dinikowoh27/akatsuki-hermes-team

---

*Built with 💜 by EiDA for Akatsuki Team.*
