import pytest
from app.services.safety_checker import SafetyChecker, safety_checker

@pytest.mark.parametrize("message, expected_safe", [
    ("This is a normal question about projects", True),
    ("sexo", False),  # blocked pattern
    ("My password is 123456", False),  # personal info pattern
    ("idiota", False),  # offensive
])
def test_safety_checker_basic_rules(message, expected_safe):
    result = safety_checker.check_input_safety(message)
    assert result['is_safe'] == expected_safe


@pytest.mark.skip(reason="Diseñar casos de bypass más avanzados, e.g. evasión por spacing/Unicode homoglyphs")
def test_safety_bypass_obfuscation():
    # Ejemplo: intentar evadir reglas introduciendo espacios o caracteres Unicode similares
    obfuscated = "s e x o"  # debería ser bloqueado por regla inapropiada
    result = safety_checker.check_input_safety(obfuscated)
    assert result['is_safe'] is False


@pytest.mark.skip(reason="Implementar generación adversarial para testing")
def test_output_safety_templates():
    # Verificar que la salida unsafe/block devuelve templates
    out = safety_checker._get_template_response('blocked')
    assert "Lo siento" in out
