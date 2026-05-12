from judge_card.generator import generate, load_card
from judge_card.schema import validate

def test_generate_valid():
    card=generate({"model":"local","synthetic":True,"results":[{"probe":"position_bias","flip_rate":0.2}]})
    assert not validate(card)


def test_loads_json_example():
    card = load_card("examples/tutorial_judge_card.json")
    assert card["synthetic"] is True
    assert not validate(card)
