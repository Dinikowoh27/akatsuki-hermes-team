#!/usr/bin/env python3
"""
create-topics.py

Auto-create Telegram forum topics untuk Akatsuki Team.
Pakai bot orchestrator untuk membuat semua topic di grup.
Setelah sukses, update tokens.json dengan topic_id.

Usage:
  python3 scripts/create-topics.py tokens.json
"""
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

VALID_ICON_COLORS = [7322096, 16478047, 16749490, 16777215]


def api_call(token, method, params=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = None
    if params:
        data = urllib.parse.urlencode(params).encode()
    try:
        with urllib.request.urlopen(url, data=data, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return json.loads(body)
        except Exception:
            return {"ok": False, "error": body}


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/create-topics.py tokens.json")
        sys.exit(1)

    tokens_path = sys.argv[1]
    with open(tokens_path, "r") as f:
        cfg = json.load(f)

    tg = cfg["telegram"]
    group_id = tg["group_id"]
    orch = tg["orchestrator"]
    workers = tg["workers"]

    token = orch["bot_token"]
    if not token or token.startswith("123456789:"):
        print("[ERROR] Bot token orchestrator belum diisi di tokens.json")
        sys.exit(1)

    # Verifikasi bot bisa akses grup
    me = api_call(token, "getMe")
    if not me.get("ok"):
        print(f"[ERROR] getMe gagal: {me}")
        sys.exit(1)
    print(f"[OK] Bot orchestrator: @{me['result'].get('username')}")

    # Buat mapping nama -> topic config
    topics_to_create = {
        orch["profile_name"]: orch,
    }
    topics_to_create.update(workers)

    color_idx = 0
    for name, topic_cfg in topics_to_create.items():
        topic_name = topic_cfg.get("topic_name", name)
        if topic_cfg.get("topic_id"):
            print(f"[SKIP] {name}: sudah punya topic_id {topic_cfg['topic_id']}")
            continue

        params = {
            "chat_id": group_id,
            "name": topic_name,
            "icon_color": VALID_ICON_COLORS[color_idx % len(VALID_ICON_COLORS)],
        }
        print(f"[CREATE] {name}: {topic_name} ...")
        resp = api_call(token, "createForumTopic", params)
        if resp.get("ok"):
            topic_id = resp["result"]["message_thread_id"]
            topic_cfg["topic_id"] = topic_id
            print(f"[OK] {name}: topic_id = {topic_id}")
        else:
            # Kalau topic sudah ada, Telegram biasanya error "TOPIC_NOT_MODIFIED" atau sejenis
            # User harus isi manual topic_id dari Telegram URL
            print(f"[FAIL] {name}: {resp.get('description', resp)}")
            print(f"       Kalau topic sudah ada, isi topic_id di tokens.json secara manual.")
        color_idx += 1

    # Simpan kembali
    with open(tokens_path, "w") as f:
        json.dump(cfg, f, indent=2)

    print("\n[SAVED] tokens.json sudah diperbarui.")
    print("[NEXT] Jalankan ./setup.sh untuk inject topic_id & token ke tiap profil.")


if __name__ == "__main__":
    main()
