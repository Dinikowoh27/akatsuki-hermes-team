# Setup GitHub Repository

Panduan untuk publish repo ini ke GitHub sebagai repo public.

## Via GitHub CLI (Recommended)

```bash
cd /tmp/akatsuki-hermes-team

# Login ke GitHub (kalau belum)
gh auth login

# Create public repo
gh repo create akatsuki-hermes-team --public --source=. --remote=origin --push

# Done! Repo akan tersedia di:
# https://github.com/YOUR_USERNAME/akatsuki-hermes-team
```

## Via GitHub Web UI

### 1. Buat Repo Baru di GitHub
- Buka https://github.com/new
- Repository name: `akatsuki-hermes-team`
- Description: `🌀 Multi-Agent AI Team Setup for Hermes Agent`
- **Public** ✓
- **JANGAN** centang "Initialize with README" (sudah ada)
- Create repository

### 2. Push Local ke GitHub

```bash
cd /tmp/akatsuki-hermes-team

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/akatsuki-hermes-team.git

# Push
git branch -M main
git push -u origin main
```

### 3. Verify

Buka: `https://github.com/YOUR_USERNAME/akatsuki-hermes-team`

## Share Link ke Temen

Setelah push, kirim link ini ke temen Mas:
```
https://github.com/YOUR_USERNAME/akatsuki-hermes-team
```

Mereka bisa langsung:
```bash
git clone https://github.com/YOUR_USERNAME/akatsuki-hermes-team.git
cd akatsuki-hermes-team
chmod +x create_profiles.sh
./create_profiles.sh
```

## Optional: Add Topics & About

Di GitHub repo settings, tambah:
- **Topics:** `hermes-agent`, `ai-agents`, `multi-agent`, `kanban`, `automation`
- **About:** Multi-Agent AI Team Setup for Hermes Agent — 10 specialized profiles for autonomous development, trading, and operations
- **Website:** https://hermes-agent.nousresearch.com

---

Built with 💜 by EiDA
