import json
import subprocess
import sys
from pathlib import Path

from judge_card.generator import generate, load_card
from judge_card.render import html, markdown
from judge_card.schema import validate

ROOT = Path(__file__).resolve().parents[1]

def test_generate_valid():
    card=generate({"model":"local","synthetic":True,"results":[{"probe":"position_bias","flip_rate":0.2}]})
    assert not validate(card)
    assert len(card["prompt_hash"]) == 64


def test_loads_json_example():
    card = load_card(ROOT / "examples/tutorial_judge_card.json")
    assert card["synthetic"] is True
    assert not validate(card)


def test_validate_rejects_bad_card():
    assert "known_biases/0/probe must be a non-empty string" in validate(
        {
            "model_id": "local",
            "prompt_hash": "8b43803b5242924e5260b9fb7393b5e61cad1ed6278c0c854c85bd4943d4a96e",
            "calibration_summary": {},
            "known_biases": [{"value": 1}],
            "recommended_use": "diagnostic only",
            "generated_at": "2026-05-12T00:00:00+00:00",
        }
    )


def test_markdown_and_html_render():
    card = generate({"model": "local", "synthetic": True, "results": [{"probe": "position_bias", "flip_rate": 0.2}]})
    rendered = markdown(card)
    assert "not a model benchmark" in rendered
    assert "position_bias" in rendered
    assert html(card).startswith("<html>")


def test_cli_generate_and_validate(tmp_path):
    bench = tmp_path / "bench.json"
    bench.write_text(json.dumps({"model": "local", "synthetic": True, "results": [{"probe": "verbosity_bias", "flip_rate": 0.1}]}))
    card = tmp_path / "card.md"
    env = {"PYTHONPATH": str(ROOT / "src")}
    generated = subprocess.run(
        [sys.executable, "-m", "judge_card.generator", "generate", "--from", str(bench), "--out", str(card)],
        text=True,
        capture_output=True,
        env=env,
    )
    assert generated.returncode == 0, generated.stderr + generated.stdout
    assert "verbosity_bias" in card.read_text(encoding="utf-8")
    valid = subprocess.run(
        [sys.executable, "-m", "judge_card.generator", "validate", str(ROOT / "examples/tutorial_judge_card.json")],
        text=True,
        capture_output=True,
        env=env,
    )
    assert valid.returncode == 0, valid.stderr + valid.stdout
