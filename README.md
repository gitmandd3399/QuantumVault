# 🔐 QuantumVault Academy

A K–12 interactive learning platform for **Post-Quantum Cryptography** — built in Python with Streamlit.

---

## 📁 Project Structure

```
QuantumVault/
├── app/
│   ├── main.py                  # Streamlit entry point & router
│   ├── modules/
│   │   ├── elementary.py        # K-5: Story mode, color mixing, lock puzzles
│   │   ├── middle_school.py     # 6-8: Lattice explorer, hash factory, quantum race
│   │   └── high_school.py       # 9-12: NIST timeline, algorithm lab, code lab
│   ├── crypto/
│   │   └── kyber_demo.py        # Simplified Kyber/LWE demonstration (education only)
│   ├── utils/
│   │   ├── __init__.py          # Security helpers (sanitize, rate-limit, hash)
│   │   └── security.py          # Re-export shim
│   └── static/
│       └── style.css            # Custom Streamlit styling
├── tests/
│   └── test_security.py         # pytest suite (security + correctness)
├── .vscode/
│   ├── settings.json            # VS Code Python/linting config
│   └── launch.json              # Run/debug/test launchers
├── requirements.txt             # Pinned dependencies
├── .env.example                 # Environment variable template
├── .gitignore                   # Excludes .env, __pycache__, etc.
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Clone / open in VS Code
git clone <your-repo> QuantumVault
cd QuantumVault

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env — add a real SECRET_KEY

# 5. Launch the app
streamlit run app/main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧪 Running Tests

```bash
# Run full test suite
PYTHONPATH=app pytest tests/ -v

# Run only security tests
PYTHONPATH=app pytest tests/test_security.py -v -k "Security"
```

---

## 🔒 Security Maintenance (Run Weekly)

```bash
# 1. Scan dependencies for known CVEs
pip-audit

# 2. Static code security analysis
bandit -r app/ -ll

# 3. Alternative CVE check
safety check

# 4. Update pinned deps after review
pip install --upgrade <package>
pip freeze > requirements.txt
pip-audit   # re-check after update
```

---

## 🛡️ Security Architecture

| Layer | Implementation |
|---|---|
| Input sanitisation | `bleach` + `html.escape` + control char stripping |
| Rate limiting | Session-scoped counter (swap Redis for multi-user) |
| SQL | Not used by default; parameterised queries if added |
| Secrets | `.env` via `python-dotenv` — never hardcoded |
| Static analysis | `bandit` in VS Code + CI |
| Dependency CVEs | `pip-audit` + `safety` |
| COPPA compliance | No PII collected; no accounts for under-13 |
| HTTPS | Enforce in production via reverse proxy (nginx/Caddy) |

---

## ⚛️ Post-Quantum Algorithms Covered

| Algorithm | NIST Standard | Type | Module |
|---|---|---|---|
| ML-KEM (Kyber) | FIPS 203 | Key Encapsulation | Middle + High School |
| ML-DSA (Dilithium) | FIPS 204 | Digital Signature | High School |
| LWE (simplified) | — | Core math concept | All levels |
| SHA-3 / SHAKE-256 | FIPS 202 | Hash / XOF | Middle + High School |

---

## 🔬 Using Real PQC (Production)

For a real implementation, install [liboqs-python](https://github.com/open-quantum-safe/liboqs-python):

```bash
# Requires liboqs C library first:
# https://github.com/open-quantum-safe/liboqs#quickstart
pip install liboqs-python

# Example usage in high_school.py:
import oqs
kem = oqs.KeyEncapsulation("Kyber768")
public_key = kem.generate_keypair()
ciphertext, shared_secret_enc = kem.encap_secret(public_key)
shared_secret_dec = kem.decap_secret(ciphertext)
```

---

## 📚 Learning Resources

- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Open Quantum Safe](https://openquantumsafe.org/)
- [CRYSTALS-Kyber Spec](https://pq-crystals.org/kyber/)
- [FIPS 203 (ML-KEM)](https://doi.org/10.6028/NIST.FIPS.203)

---

## ⚠️ Disclaimer

The `crypto/kyber_demo.py` module is a **pedagogical toy** — not production cryptography.
For any real security application, use `liboqs-python` or a FIPS-validated library.
