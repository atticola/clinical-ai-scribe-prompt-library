from pathlib import Path

def test_prompt_exists():
    assert Path('prompts/001_demo.yaml').exists()
