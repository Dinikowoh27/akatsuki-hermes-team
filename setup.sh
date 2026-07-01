#!/bin/bash
# setup.sh — Setup lengkap Akatsuki Team
# Usage: ./setup.sh [tokens.json]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOKENS_FILE="${1:-tokens.json}"

if [[ ! -f "$TOKENS_FILE" ]]; then
    echo "[ERROR] File tidak ditemukan: $TOKENS_FILE"
    echo "Copy dari template dulu: cp tokens.json.example tokens.json"
    exit 1
fi

ORCH_NAME=$(python3 -c "import json; print(json.load(open('$TOKENS_FILE'))['telegram']['orchestrator'].get('profile_name','slevensyai'))")
WORKERS=(pain itachi sasori obito kisame konan deidara zetsu madara)

echo "🌀 Akatsuki Team Setup"
echo "   Orchestrator: $ORCH_NAME"
echo "   Workers: ${WORKERS[@]}"
echo ""

# --- Buat profil orchestrator ---
if [[ "$ORCH_NAME" != "default" ]]; then
    if ! hermes profile list 2>/dev/null | grep -q "^$ORCH_NAME "; then
        echo "[CREATE] Profil orchestrator: $ORCH_NAME"
        hermes profile create "$ORCH_NAME" --description "Orchestrator bot utama @SLEVENSYAIBOT"
    else
        echo "[SKIP] Profil $ORCH_NAME sudah ada"
    fi
fi

# --- Buat profil worker ---
for profile in "${WORKERS[@]}"; do
    if ! hermes profile list 2>/dev/null | grep -q "^$profile "; then
        echo "[CREATE] Profil worker: $profile"
        hermes profile create "$profile" --description "Akatsuki worker: $profile"
    else
        echo "[SKIP] Profil $profile sudah ada"
    fi
done

# --- Generate config.yaml dari template ---
echo ""
echo "[CONFIG] Generate config.yaml tiap profil..."
python3 "$SCRIPT_DIR/scripts/apply-config.py" "$TOKENS_FILE"

# --- Patch .env tiap profil ---
echo ""
echo "[ENV] Patch .env tiap profil..."
python3 "$SCRIPT_DIR/scripts/patch-env.py" "$TOKENS_FILE"

echo ""
echo "✅ Setup selesai!"
echo ""
echo "Langkah selanjutnya:"
echo "  1. Pastikan semua bot sudah admin di grup Telegram (dengan 'Manage topics')."
echo "  2. Buat forum topics: python3 scripts/create-topics.py $TOKENS_FILE"
echo "  3. Jalankan lagi ./setup.sh $TOKENS_FILE untuk update topic_id ke config & .env"
echo "  4. Install systemd: ./scripts/install-systemd.sh $TOKENS_FILE"
echo "  5. Start services: systemctl --user enable --now hermes-$ORCH_NAME hermes-pain hermes-itachi hermes-sasori"
echo ""
