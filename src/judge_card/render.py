def markdown(card: dict) -> str:
    lines=["# Judge Card", "", f"- Model: {card.get('model_id')}", f"- Prompt hash: {card.get('prompt_hash')}", f"- Generated: {card.get('generated_at')}", "", "## Calibration Summary"]
    for k,v in card.get('calibration_summary',{}).items(): lines.append(f"- {k}: {v}")
    lines += ["", "## Known Biases"]
    for b in card.get('known_biases',[]): lines.append(f"- {b.get('probe','unknown')}: {b.get('value')}")
    lines += ["", "## Recommended Use", card.get('recommended_use','')]
    return "\n".join(lines)+"\n"
def html(card: dict) -> str:
    return "<html><body><pre>" + markdown(card).replace('&','&amp;').replace('<','&lt;') + "</pre></body></html>"
