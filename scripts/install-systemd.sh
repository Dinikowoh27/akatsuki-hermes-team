#!/bin/bash
# install-systemd.sh
# Install systemd user services untuk orchestrator & worker profiles.
# Usage: ./scripts/install-systemd.sh tokens.json

set -e

TOKENS_FILE="${1:-tokens.json}"

ORCH_NAME=$(python3 -c "import json; print(json.load(open('$TOKENS_FILE'))['telegram']['orchestrator'].get('profile_name','slevensyai'))")
WORKERS=(pain itachi sasori obito kisame konan deidara zetsu madara)

SYSTEMD_DIR="$HOME/.config/systemd/user"
mkdir -p "$SYSTEMD_DIR"

SERVICE_TEMPLATE='[Unit]
Description=Hermes Gateway — %PROFILE_NAME%
After=network.target

[Service]
Type=simple
WorkingDirectory=%h
Environment="HOME=%h"
ExecStart=%h/.local/bin/%PROFILE_NAME% gateway run --replace
Restart=always
RestartSec=10
CPUQuota=40%%
MemoryMax=768M

[Install]
WantedBy=default.target
'

write_service() {
    local profile=$1
    local path="$SYSTEMD_DIR/hermes-${profile}.service"
    echo "$SERVICE_TEMPLATE" | sed \
        -e "s|%PROFILE_NAME%|$profile|g" \
        > "$path"
    echo "[OK] $path"
}

# Orchestrator
write_service "$ORCH_NAME"

# Workers
for profile in "${WORKERS[@]}"; do
    write_service "$profile"
done

systemctl --user daemon-reload

echo ""
echo "✅ systemd services terinstall."
echo "Start orchestrator + core workers:"
echo "  systemctl --user enable --now hermes-$ORCH_NAME hermes-pain hermes-itachi hermes-sasori"
echo ""
echo "Start semua worker:"
echo "  for p in $ORCH_NAME ${WORKERS[@]}; do systemctl --user enable --now hermes-\$p; done"
