#!/usr/bin/env python3
"""
patch-env.py

Inject TELEGRAM_BOT_TOKEN, HOME_CHANNEL, dan ALLOWED_USERS ke .env tiap profil.
Membaca data dari tokens.json.

Usage:
  python3 scripts/patch-env.py tokens.json
"""
import json
import os
import sys
from pathlib import Path


def update_env_file(env_path: Path, kv: dict):
    lines = []
    if env_path.exists():
        lines = env_path.read_text().splitlines()

    existing = {}
    for i, line in enumerate(lines):
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            existing[k.strip()] = i

    for key, value in kv.items():
        new_line = f"{key}={value}"
        if key in existing:
            lines[existing[key]] = new_line
        else:
            lines.append(new_line)

    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text("\n".join(lines) + "\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/patch-env.py tokens.json")
        sys.exit(1)

    tokens_path = sys.argv[1]
    with open(tokens_path, "r") as f:
        cfg = json.load(f)

    tg = cfg["telegram"]
    group_id = tg["group_id"]
    allowed_users = ",".join(str(u) for u in tg.get("allowed_users", []))
    lounge_topic = None

    # Cari topic lounge kalau ada
    for name, tc in tg["workers"].items():
        if "lounge" in tc.get("topic_name", "").lower():
            lounge_topic = tc.get("topic_id")

    base_dir = Path.home() / ".hermes"

    def patch_profile(profile_name, topic_cfg):
        if profile_name == "default":
            profile_dir = base_dir  # default profile di ~/.hermes
        else:
            profile_dir = base_dir / "profiles" / profile_name

        env_path = profile_dir / ".env"
        topic_id = topic_cfg.get("topic_id")
        if not topic_id:
            print(f"[WARN] {profile_name}: topic_id kosong, lewati TELEGRAM_HOME_CHANNEL")
            home_channel = ""
            cron_thread = ""
        else:
            home_channel = f"{group_id}:{topic_id}"
            cron_thread = str(topic_id)

        home_name = topic_cfg.get("topic_name", profile_name)

        # allowed_topics env fallback (comma-separated)
        allowed_topics = [str(topic_id)] if topic_id else []
        if lounge_topic:
            allowed_topics.append(str(lounge_topic))

        kv = {
            "TELEGRAM_BOT_TOKEN": topic_cfg["bot_token"],
            "TELEGRAM_ALLOWED_USERS": allowed_users,
            "TELEGRAM_HOME_CHANNEL": home_channel,
            "TELEGRAM_HOME_CHANNEL_NAME": home_name,
            "TELEGRAM_CRON_THREAD_ID": cron_thread,
            "TELEGRAM_ALLOWED_TOPICS": ",".join(allowed_topics),
        }

        # Kalau file .env masih default dari Hermes, pastikan tidak duplikat komentar
        update_env_file(env_path, kv)
        print(f"[OK] {profile_name}: {env_path}")

    # Orchestrator
    orch = tg["orchestrator"]
    orch_name = orch.get("profile_name", "slevensyai")
    patch_profile(orch_name, orch)

    # Workers
    for worker_name, worker_cfg in tg["workers"].items():
        patch_profile(worker_name, worker_cfg)

    print("\n[DONE] Semua .env sudah di-patch.")


if __name__ == "__main__":
    main()
