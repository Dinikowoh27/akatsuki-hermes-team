#!/bin/bash
# Akatsuki Team Profile Creator
# Creates all 10 profiles with base config structure

set -e

PROFILES=(pain itachi sasori obito kisame konan deidara zetsu treasury madara)
BASE_DIR="$HOME/.hermes/profiles"

echo "🌀 Creating Akatsuki Team Profiles..."
echo ""

for profile in "${PROFILES[@]}"; do
    echo "Creating profile: $profile"
    
    # Create directories
    mkdir -p "$BASE_DIR/$profile"/{skills,memories,cron,sessions}
    
    # Create placeholder config (user must fill in API keys)
    cat > "$BASE_DIR/$profile/config.yaml" <<EOF
# $profile profile config
# TODO: Fill in your API keys in ~/.hermes/.env

model:
  default: deepseek-v4-flash  # Change as needed
  provider: custom
  base_url: https://llm.kimchi.dev/openai/v1
  api_key: \${KIMCHI_API_KEY}

agent:
  max_turns: 90

toolsets:
  - hermes-cli
  - terminal
  - file

display:
  personality: technical
  compact: false

telegram:
  reactions: false
  extra:
    rich_messages: true
EOF

    echo "  ✓ Created $profile"
done

echo ""
echo "✅ All profiles created!"
echo ""
echo "Next steps:"
echo "1. Edit each profile config in $BASE_DIR/<profile>/config.yaml"
echo "2. Set model, provider, and toolsets per profile"
echo "3. Add API keys to ~/.hermes/.env"
echo "4. Start gateways: hermes gateway --profile <profile>"
echo ""
echo "See AKATSUKI_TEAM_GUIDE.md for full setup instructions."
