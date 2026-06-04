"""
crypto/kyber_demo.py
────────────────────
Simplified CRYSTALS-Kyber–style demonstration.
NOT production cryptography. For education only.

For real PQC, use:
    pip install liboqs-python
    import oqs
    kem = oqs.KeyEncapsulation("Kyber768")

Security notes:
  - random.randint used deliberately for educational clarity.  # nosec B311
  - Real Kyber uses NTT (Number Theoretic Transform) over Z_q[X]/(X^n + 1).
  - Real Kyber uses CRYSTALS-specific noise distributions (centered binomial).
  - DO NOT use this code to protect real data.
"""

from __future__ import annotations
import hashlib
import random
from dataclasses import dataclass, field
from typing import List, Tuple


# ── Constants (toy parameters) ────────────────────────────────────────────────
Q   = 3329    # Real Kyber-512 modulus
N   = 4       # Dimension (real: 256 polynomials)
ETA = 1       # Noise bound — kept at 1 for toy params so decryption is reliable
              # Real Kyber-512: η1=3, η2=2 (works because n=256, q=3329)


# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class KeyPair:
    secret_key: List[int]
    public_matrix: List[List[int]]
    public_b: List[int]

    def public_key_summary(self) -> str:
        return f"A={self.public_matrix!r}, b={self.public_b!r}"


@dataclass
class Ciphertext:
    u: List[int]
    v: int


# ── Core functions ────────────────────────────────────────────────────────────

def _centered_binomial(eta: int) -> int:
    """Sample from centered binomial distribution — approximates Gaussian noise."""
    return sum(random.getrandbits(1) - random.getrandbits(1) for _ in range(eta))  # nosec B311


def keygen(n: int = N, q: int = Q, eta: int = ETA) -> KeyPair:
    """
    Toy key generation (Kyber-inspired).

    Returns (secret_key, public_matrix A, public_vector b)
    where b = A·s + e  (mod q)

    Note: Real Kyber also uses small secret key values (centered binomial).
    We use small s here so that noise in decryption stays bounded:
    the decryption error ≈ e·r - s·e1 + e2, and with small s this stays < q/4.
    """
    # Small secret — real Kyber samples s from the same distribution as noise
    s = [_centered_binomial(eta) for _ in range(n)]
    A = [[random.randint(0, q - 1) for _ in range(n)] for _ in range(n)]  # nosec B311
    e = [_centered_binomial(eta) for _ in range(n)]                    # small noise
    b = [(sum(A[i][j] * s[j] for j in range(n)) + e[i]) % q for i in range(n)]
    return KeyPair(secret_key=s, public_matrix=A, public_b=b)


def encapsulate(kp: KeyPair, message_bit: int, q: int = Q) -> Ciphertext:
    """
    Toy encapsulation (encrypt a 0 or 1 bit).

    Returns ciphertext (u, v).
    """
    if message_bit not in (0, 1):
        raise ValueError("message_bit must be 0 or 1")

    n = len(kp.secret_key)
    r  = [random.randint(0, 1) for _ in range(n)]  # nosec B311
    e1 = [_centered_binomial(2) for _ in range(n)]
    e2 = _centered_binomial(2)

    u = [(sum(kp.public_matrix[j][i] * r[j] for j in range(n)) + e1[i]) % q for i in range(n)]
    v = (sum(kp.public_b[i] * r[i] for i in range(n)) + e2 + (q // 2) * message_bit) % q
    return Ciphertext(u=u, v=v)


def decapsulate(kp: KeyPair, ct: Ciphertext, q: int = Q) -> int:
    """
    Toy decapsulation — recover the message bit.
    The secret key cancels the noise to reveal ≈0 or ≈q/2.
    """
    noisy = (ct.v - sum(kp.secret_key[i] * ct.u[i] for i in range(len(ct.u)))) % q
    return 1 if abs(noisy - q // 2) < q // 4 else 0


# ── Hash helpers (used inside real PQC schemes) ───────────────────────────────

def shake256(data: bytes, output_len: int = 32) -> bytes:
    """
    SHAKE-256 — the XOF (extendable output function) used in CRYSTALS-Kyber
    for pseudo-random byte generation.
    """
    h = hashlib.shake_256()
    h.update(data)
    return h.digest(output_len)


def sha3_256(data: bytes) -> bytes:
    return hashlib.sha3_256(data).digest()


# ── Demo runner ───────────────────────────────────────────────────────────────

def run_demo(bits: List[int] | None = None) -> List[dict]:
    """
    Run a full keygen → encapsulate → decapsulate cycle for each bit in `bits`.
    Returns a list of result dicts (useful for Streamlit display).
    """
    if bits is None:
        bits = [0, 1]

    kp = keygen()
    results = []
    for bit in bits:
        ct  = encapsulate(kp, bit)
        rec = decapsulate(kp, ct)
        results.append({
            "sent": bit,
            "received": rec,
            "success": rec == bit,
            "ciphertext_u": ct.u,
            "ciphertext_v": ct.v,
        })
    return results
