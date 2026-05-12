from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from .render import markdown, html
from .schema import validate


def generate(bench: dict) -> dict:
    prompt_hash = hashlib.sha256(json.dumps(bench.get("results", []), sort_keys=True).encode()).hexdigest()
    return {"model_id": bench.get("model", "unknown"), "prompt_hash": prompt_hash, "calibration_summary": {r.get("probe", "probe"): r.get("flip_rate", r.get("first_position_rate")) for r in bench.get("results", [])}, "known_biases": [{"probe": r.get("probe"), "value": r.get("flip_rate", 0)} for r in bench.get("results", [])], "recommended_use": "Use for diagnostic review only; this is not a benchmark.", "generated_at": datetime.now(timezone.utc).isoformat(), "synthetic": bool(bench.get("synthetic", True))}


def load_card(path: str | Path) -> dict:
    raw = Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def main(argv=None):
    p=argparse.ArgumentParser(prog="judge-card"); sub=p.add_subparsers(dest="cmd", required=True)
    g=sub.add_parser("generate"); g.add_argument("--from", dest="source", required=True); g.add_argument("--out", required=True)
    v=sub.add_parser("validate"); v.add_argument("path")
    args=p.parse_args(argv)
    if args.cmd == "generate":
        card=generate(json.loads(Path(args.source).read_text())); out=Path(args.out)
        out.write_text(markdown(card) if out.suffix=='.md' else html(card) if out.suffix=='.html' else json.dumps(card, indent=2))
        print(json.dumps(card, indent=2)); return 0
    card=load_card(args.path); errors=validate(card); print(json.dumps({"ok": not errors, "errors": errors}, indent=2)); return 0 if not errors else 1
if __name__ == "__main__": raise SystemExit(main())
