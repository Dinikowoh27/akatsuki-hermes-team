#!/usr/bin/env python3
"""
apply-config.py

Generate config.yaml untuk orchestrator & worker profiles dari template + tokens.json.

Usage:
  python3 scripts/apply-config.py tokens.json
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path


def load_yaml(path: Path):
    return path.read_text()


def write_yaml(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)


def model_block(model_cfg: dict) -> str:
    lines = [
        f"  default: {model_cfg['default']}",
        f"  provider: {model_cfg['provider']}",
    ]
    if "base_url" in model_cfg:
        lines.append(f"  base_url: {model_cfg['base_url']}")
    lines.append(f"  api_key: ${{{model_cfg['api_key_env']}}}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/apply-config.py tokens.json")
        sys.exit(1)

    repo_dir = Path(__file__).resolve().parent.parent
    tokens_path = Path(sys.argv[1]).resolve()
    with open(tokens_path, "r") as f:
        cfg = json.load(f)

    tg = cfg["telegram"]
    models = cfg["models"]
    orch = tg["orchestrator"]
    orch_name = orch.get("profile_name", "slevensyai")
    workers = tg["workers"]
    allowed_users = tg.get("allowed_users", [])
    owner_user_id = allowed_users[0] if allowed_users else 0
    group_id = tg["group_id"]

    # Cari lounge topic
    lounge_topic = None
    for name, wc in workers.items():
        if "lounge" in wc.get("topic_name", "").lower():
            lounge_topic = wc.get("topic_id")

    base_dir = Path.home() / ".hermes"

    def profile_dir(name: str) -> Path:
        if name == "default":
            return base_dir
        return base_dir / "profiles" / name

    # --- Orchestrator ---
    orch_template = load_yaml(repo_dir / "configs" / "config-orchestrator.yaml")
    orch_model = models.get("orchestrator", models.get(orch_name, {}))
    orch_topic_id = orch.get("topic_id") or 0

    orch_config = orch_template
    orch_config = re.sub(r"^model:\n.*?(?=\nagent:)", "model:\n" + model_block(orch_model), orch_config, flags=re.DOTALL)
    orch_config = orch_config.replace("<ORCHESTRATOR_NAME>", orch_name)
    orch_config = orch_config.replace("<OWNER_USER_ID>", str(owner_user_id))
    orch_config = orch_config.replace("<ORCHESTRATOR_TOPIC_ID>", str(orch_topic_id))
    orch_config = orch_config.replace("<LOUNGE_TOPIC_ID>", str(lounge_topic or 0))

    orch_cfg_path = profile_dir(orch_name) / "config.yaml"
    write_yaml(orch_cfg_path, orch_config)
    print(f"[OK] {orch_name}: {orch_cfg_path}")

    # --- Workers ---
    worker_template = load_yaml(repo_dir / "configs" / "config-worker.yaml")
    for worker_name, worker_cfg in workers.items():
        worker_model = models.get(worker_name, {})
        if not worker_model:
            print(f"[WARN] {worker_name}: tidak ada model config, pakai default worker template")

        worker_topic_id = worker_cfg.get("topic_id") or 0
        worker_allowed_topics = [str(worker_topic_id)]
        if lounge_topic:
            worker_allowed_topics.append(str(lounge_topic))

        wc = worker_template
        if worker_model:
            wc = re.sub(r"^model:\n.*?(?=\nagent:)", "model:\n" + model_block(worker_model), wc, flags=re.DOTALL)
        wc = wc.replace("<ORCHESTRATOR_NAME>", orch_name)
        wc = wc.replace("<OWNER_USER_ID>", str(owner_user_id))
        wc = wc.replace("<WORKER_NAME>", worker_name)
        wc = wc.replace("<WORKER_TOPIC_ID>", str(worker_topic_id))
        wc = wc.replace("<LOUNGE_TOPIC_ID>", str(lounge_topic or 0))

        worker_cfg_path = profile_dir(worker_name) / "config.yaml"
        write_yaml(worker_cfg_path, wc)
        print(f"[OK] {worker_name}: {worker_cfg_path}")

    # --- Copy dispatch skill ke global skills ---
    skill_src = repo_dir / "skills" / "akatsuki-dispatch.md"
    skill_dst_dir = base_dir / "skills" / "custom" / "akatsuki-dispatch"
    skill_dst_dir.mkdir(parents=True, exist_ok=True)
    skill_dst = skill_dst_dir / "SKILL.md"
    shutil.copy2(skill_src, skill_dst)
    print(f"[OK] Dispatch skill: {skill_dst}")

    print("\n[DONE] Config & skill sudah di-apply.")
    print("[NEXT] Jalankan: python3 scripts/patch-env.py tokens.json")


if __name__ == "__main__":
    main()
