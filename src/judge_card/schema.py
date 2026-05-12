REQUIRED = ["model_id", "prompt_hash", "calibration_summary", "known_biases", "recommended_use", "generated_at"]
def validate(card: dict) -> list[str]:
    return [f"missing {field}" for field in REQUIRED if field not in card]
