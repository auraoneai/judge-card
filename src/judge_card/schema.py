from __future__ import annotations

import re
from datetime import datetime

REQUIRED = ["model_id", "prompt_hash", "calibration_summary", "known_biases", "recommended_use", "generated_at"]
SHA256_HEX = re.compile(r"^[a-fA-F0-9]{64}$")


def validate(card: dict) -> list[str]:
    errors = [f"missing {field}" for field in REQUIRED if field not in card]
    if errors:
        return errors

    if not isinstance(card.get("model_id"), str) or not card["model_id"].strip():
        errors.append("model_id must be a non-empty string")
    if not isinstance(card.get("prompt_hash"), str) or not SHA256_HEX.fullmatch(card["prompt_hash"]):
        errors.append("prompt_hash must be a 64-character SHA-256 hex string")
    if not isinstance(card.get("calibration_summary"), dict):
        errors.append("calibration_summary must be an object")
    if not isinstance(card.get("known_biases"), list):
        errors.append("known_biases must be an array")
    else:
        for index, bias in enumerate(card["known_biases"]):
            if not isinstance(bias, dict):
                errors.append(f"known_biases/{index} must be an object")
                continue
            if not isinstance(bias.get("probe"), str) or not bias["probe"].strip():
                errors.append(f"known_biases/{index}/probe must be a non-empty string")
            if "value" not in bias:
                errors.append(f"known_biases/{index}/value is required")
    if not isinstance(card.get("recommended_use"), str) or not card["recommended_use"].strip():
        errors.append("recommended_use must be a non-empty string")
    generated_at = card.get("generated_at")
    if not isinstance(generated_at, str):
        errors.append("generated_at must be an ISO-8601 string")
    else:
        try:
            datetime.fromisoformat(generated_at.replace("Z", "+00:00"))
        except ValueError:
            errors.append("generated_at must be an ISO-8601 string")
    if "synthetic" in card and not isinstance(card["synthetic"], bool):
        errors.append("synthetic must be a boolean")
    return errors
