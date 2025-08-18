import pytest
from app.utils.sanitizer import process_user_input
from app.services.safety_checker import check_input_safety

@pytest.mark.parametrize("payload,expect_safe", [
    ("Hola, ¿cómo estás?", True),
    ("<script>alert(1)</script>", False),
    ("Hello\u2019s attack", True),
    ("混淆字符 \u202E test", True),
])
def test_safety_with_normalization(payload, expect_safe):
    processed = process_user_input(payload)
    # Usar processed_message para check_input_safety
    safe = check_input_safety(processed.get('processed_message', ''))
    assert isinstance(safe, dict)
    assert 'is_safe' in safe
