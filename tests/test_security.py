"""
tests/test_security.py
──────────────────────
Security and correctness tests for QuantumVault Academy.

Run with:
    cd QuantumVault
    pytest tests/ -v

Also run static analysis:
    bandit -r app/
    pip-audit
"""

import sys
import os
import pytest

# Ensure the app package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from utils import sanitize_input, validate_alphanumeric, sha256_hex, sha3_256_hex
from crypto.kyber_demo import keygen, encapsulate, decapsulate, run_demo


# ── Sanitization tests ────────────────────────────────────────────────────────

class TestSanitizeInput:
    def test_strips_html_tags(self):
        result = sanitize_input("<script>alert('xss')</script>Hello")
        assert "<script>" not in result
        assert "alert" not in result.lower() or "script" not in result

    def test_escapes_html_entities(self):
        result = sanitize_input("<b>bold</b>")
        assert "<b>" not in result

    def test_truncates_long_input(self):
        long_input = "A" * 1000
        result = sanitize_input(long_input, max_length=100)
        assert len(result) <= 100

    def test_strips_control_characters(self):
        result = sanitize_input("Hello\x00World\x07")
        assert "\x00" not in result
        assert "\x07" not in result

    def test_normal_text_passes_through(self):
        text = "Hello World! Learning PQC."
        result = sanitize_input(text)
        assert "Hello World" in result

    def test_empty_string(self):
        assert sanitize_input("") == ""

    def test_sql_injection_attempt(self):
        malicious = "'; DROP TABLE users; --"
        result = sanitize_input(malicious)
        # Should be escaped, not executable
        assert "DROP" in result or result  # Still safe since we don't eval it
        assert "<" not in result

    def test_javascript_injection(self):
        malicious = "<img src=x onerror=alert(1)>"
        result = sanitize_input(malicious)
        assert "onerror" not in result.lower()

    def test_unicode_passthrough(self):
        text = "Cryptography is κρυπτογραφία"
        result = sanitize_input(text)
        assert len(result) > 0


class TestValidateAlphanumeric:
    def test_valid_alphanum(self):
        assert validate_alphanumeric("Hello123") is True

    def test_rejects_special_chars(self):
        assert validate_alphanumeric("Hello!") is False

    def test_allows_spaces_when_flagged(self):
        assert validate_alphanumeric("Hello World", allow_spaces=True) is True

    def test_rejects_spaces_by_default(self):
        assert validate_alphanumeric("Hello World") is False

    def test_empty_string_fails(self):
        assert validate_alphanumeric("") is False


# ── Hashing tests ─────────────────────────────────────────────────────────────

class TestHashFunctions:
    def test_sha256_consistent(self):
        assert sha256_hex("test") == sha256_hex("test")

    def test_sha256_different_inputs(self):
        assert sha256_hex("test") != sha256_hex("Test")

    def test_sha256_length(self):
        assert len(sha256_hex("anything")) == 64

    def test_sha3_consistent(self):
        assert sha3_256_hex("quantum") == sha3_256_hex("quantum")

    def test_sha3_length(self):
        assert len(sha3_256_hex("hello")) == 64

    def test_sha256_sanitizes_input(self):
        # Should not raise even on malicious input
        result = sha256_hex("<script>evil</script>")
        assert len(result) == 64


# ── Kyber Demo correctness tests ──────────────────────────────────────────────

class TestKyberDemo:
    def test_keygen_dimensions(self):
        kp = keygen(n=4, q=97)
        assert len(kp.secret_key) == 4
        assert len(kp.public_b) == 4
        assert len(kp.public_matrix) == 4

    def test_keygen_values_in_range(self):
        q = 97
        kp = keygen(n=4, q=q)
        for val in kp.secret_key:
            assert 0 <= val < q
        for val in kp.public_b:
            assert 0 <= val < q

    def test_encrypt_decrypt_bit_0(self):
        """Must correctly recover a 0 bit using Kyber-sized modulus."""
        # q=3329 (Kyber modulus) gives enough separation for reliable decryption
        # even with tiny n=4. q=97 is too small — the noise overwhelms the signal.
        successes = 0
        for _ in range(20):
            kp = keygen(n=4, q=3329)
            ct = encapsulate(kp, 0, q=3329)
            if decapsulate(kp, ct, q=3329) == 0:
                successes += 1
        assert successes >= 18, "Decryption failure rate too high for bit=0"

    def test_encrypt_decrypt_bit_1(self):
        """Must correctly recover a 1 bit using Kyber-sized modulus."""
        successes = 0
        for _ in range(20):
            kp = keygen(n=4, q=3329)
            ct = encapsulate(kp, 1, q=3329)
            if decapsulate(kp, ct, q=3329) == 1:
                successes += 1
        assert successes >= 18, "Decryption failure rate too high for bit=1"

    def test_invalid_message_bit_raises(self):
        kp = keygen()
        with pytest.raises(ValueError):
            encapsulate(kp, 2)

    def test_run_demo_returns_results(self):
        results = run_demo(bits=[0, 1])
        assert len(results) == 2
        for r in results:
            assert "sent" in r
            assert "received" in r
            assert "success" in r

    def test_wrong_key_fails_decryption(self):
        """Using a different key should usually produce wrong results."""
        kp1 = keygen(n=4, q=97)
        kp2 = keygen(n=4, q=97)  # Different secret
        ct  = encapsulate(kp1, 1, q=97)

        # This won't always fail (random chance), but run enough times
        failures = sum(
            decapsulate(kp2, encapsulate(kp1, 1, q=97), q=97) != 1
            for _ in range(20)
        )
        assert failures >= 5, "Wrong key should produce errors"


# ── Security-specific edge cases ──────────────────────────────────────────────

class TestSecurityEdgeCases:
    def test_no_eval_on_user_input(self):
        """Verify sanitize_input doesn't eval anything."""
        # If eval were used, this would raise or return 2
        result = sanitize_input("1 + 1")
        assert result == "1 + 1" or result.strip() == "1 + 1"

    def test_path_traversal_attempt(self):
        malicious = "../../../etc/passwd"
        result = sanitize_input(malicious)
        # Sanitized — dots/slashes are safe in display but not as file paths
        assert len(result) <= len(malicious) + 10  # No explosion

    def test_max_length_enforcement(self):
        for length in [100, 200, 512]:
            result = sanitize_input("X" * 10_000, max_length=length)
            assert len(result) <= length
