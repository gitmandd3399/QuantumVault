"""Shared PQC vocabulary bank for QuantumVault word games.

Each entry: (word, emoji, simple_def, full_def, example, tier, category)
  tier 1 = K-2 (short words, simplest ideas)
  tier 2 = 2nd-3rd
  tier 3 = 4th-5th
Used by: Vocab Cards, Word Search, Word Rescue.
"""

VOCAB_BANK = [
# ── TIER 1 ──────────────────────────────────────────────────────────────
("KEY","🔑","The special tool that locks and unlocks a secret message.","A piece of secret data used to encrypt or decrypt information.","No key means no peeking at the message!",1,"Basics"),
("LOCK","🔒","Something that keeps your stuff safe.","In computing, a lock is a math puzzle that protects data.","Your diary has a lock. So does your data!",1,"Basics"),
("CODE","🔤","Secret writing that only your friend can read.","A system for representing information in another form.","A=1, B=2, C=3 is a simple code.",1,"Basics"),
("SAFE","🛡️","Not in any danger.","Protected from harm or unauthorized access.","Your password keeps your account safe.",1,"Basics"),
("BIT","1️⃣","The tiniest piece of computer information.","A single binary digit — either 0 or 1.","Everything on a computer is made of bits!",1,"Computers"),
("BYTE","🍪","Eight bits stuck together.","A group of 8 bits, enough to store one character.","The letter A takes up one byte.",1,"Computers"),
("DATA","📊","Information a computer keeps.","Any information stored or sent by a computer.","Your photos and messages are data.",1,"Computers"),
("HASH","🍳","A scrambled fingerprint for data.","A fixed-size output computed from any input.","Change one letter and the whole hash changes!",1,"Basics"),
("HIDE","🙈","To put something out of sight.","To conceal information from people who should not see it.","Encryption hides your message.",1,"Basics"),
("SPY","🕵️","Someone who sneaks and watches.","Someone who secretly gathers information.","Encryption stops spies from reading your notes.",1,"Threats"),
("SEED","🌱","The start of a random number.","A starting value used to generate random numbers.","If someone knows your seed, they can guess your numbers.",1,"Math"),
("GRID","▦","Rows and rows of dots.","A regular arrangement of points in space.","A lattice is a giant grid of dots!",1,"Math"),
("MATH","➕","Numbers and number puzzles.","The study of numbers, shapes, and patterns.","All secret codes are built from math.",1,"Math"),
("CHIP","🔲","The little brain inside a computer.","A small piece of silicon holding electronic circuits.","Your phone has chips that do encryption.",1,"Computers"),
("FILE","📁","Where a computer saves your stuff.","A named collection of data stored on a device.","You can encrypt a file to keep it private.",1,"Computers"),
("HACK","💻","Sneaking into a computer.","Gaining access to a system, often without permission.","Good hackers help find and fix problems!",1,"Threats"),
("SIGN","✍️","Your own special mark.","To attach proof that a message came from you.","You sign a message so friends know it is really you.",1,"Signatures"),
("WALL","🧱","It blocks things from coming in.","A barrier that filters unwanted network traffic.","A firewall is like a guard at the door.",1,"Defense"),
("MASK","🎭","It covers something up.","Hiding data so it cannot be read directly.","Noise masks the secret in lattice math.",1,"Math"),
("SWAP","🔄","To trade places.","To exchange two pieces of data.","The SWAP gate trades two qubits.",1,"Quantum"),
("PATH","🛤️","The way you go.","A route through a network or a puzzle.","Finding the shortest path in a lattice is very hard!",1,"Math"),
("SCAN","🔍","To look at something closely.","Examining a system for problems or weaknesses.","Security teams scan for vulnerabilities.",1,"Defense"),
("ZERO","0️⃣","The number 0.","One of the two values a bit can hold.","Bits are always 0 or 1.",1,"Computers"),
("TRAP","🪤","Something that catches you.","A one-way function is like a trapdoor.","Easy to fall in, very hard to climb out!",1,"Math"),

# ── TIER 2 ──────────────────────────────────────────────────────────────
("CIPHER","🔐","Another word for a secret code.","A method for encrypting and decrypting messages.","The Caesar cipher shifts every letter.",2,"Basics"),
("SECRET","🤫","Something only you know.","Information kept hidden from others.","Your private key is a secret.",2,"Basics"),
("KYBER","💎","The new super-lock nobody can break.","ML-KEM, FIPS 203 — the NIST post-quantum key exchange standard.","Kyber protects the key that locks your data.",2,"PQC"),
("QUBIT","⚛️","A quantum bit that can be 0 and 1 at once.","The basic unit of quantum information.","A qubit is like a coin spinning in the air.",2,"Quantum"),
("VAULT","🏦","A super-safe room for treasure.","A secure place where valuable data is stored.","Encryption is a vault for your information.",2,"Defense"),
("VIRUS","🦠","A bad computer bug that spreads.","Malicious software that attaches to files and spreads.","Antivirus software hunts for these.",2,"Threats"),
("NONCE","🎲","A number you use only one time.","A value used once to prevent replay attacks.","Reusing a nonce can break your encryption!",2,"Math"),
("NOISE","📻","Fuzzy static that hides a secret.","Small random values added to make problems hard.","Noise is what makes LWE secure.",2,"Math"),
("PRIME","🔢","A number only 1 and itself divide.","A number with exactly two divisors.","2, 3, 5, 7, and 11 are primes.",2,"Math"),
("ROUND","🔁","One turn of mixing things up.","One repetition of a cipher's scrambling steps.","AES uses 10 to 14 rounds.",2,"Basics"),
("TRUST","🤝","Believing something is safe.","Confidence that a system or party is genuine.","Certificates create a chain of trust.",2,"Signatures"),
("BLOCK","🧊","A chunk of data.","A fixed-size group of bits a cipher works on.","AES encrypts 128 bits at a time.",2,"Basics"),
("CLOUD","☁️","Computers far, far away.","Remote servers that store and process your data.","Cloud data still needs encryption!",2,"Computers"),
("CRACK","💥","To break open a secret code.","To defeat encryption without the key.","Quantum computers could crack RSA.",2,"Threats"),
("FALCON","🦅","A tiny signature for tiny gadgets.","FN-DSA — a compact post-quantum signature scheme.","Great for smartwatches with little memory.",2,"PQC"),
("HACKER","👤","Someone who sneaks into computers.","A person who explores or breaks into systems.","White hat hackers help defend systems.",2,"Threats"),
("HIDDEN","🫥","Tucked away where nobody sees.","Concealed from view or detection.","The secret is hidden in the noise.",2,"Basics"),
("PUZZLE","🧩","A brain teaser to solve.","A problem requiring cleverness to solve.","Crypto is built on puzzles that are hard to solve.",2,"Math"),
("RANDOM","🎰","Mixed up with no pattern.","Unpredictable and without any pattern.","Good keys must be truly random.",2,"Math"),
("SECURE","🔏","Locked up nice and safe.","Protected against unauthorized access.","HTTPS makes a website connection secure.",2,"Defense"),
("SERVER","🖥️","A big computer that saves things.","A computer that provides services to other computers.","Game scores live on a server.",2,"Computers"),
("SIGNAL","📡","A message sent through the air.","Information transmitted from one place to another.","WiFi signals carry your encrypted data.",2,"Computers"),
("SYSTEM","⚙️","All the parts working together.","A set of connected components that work as a whole.","A security system has many layers.",2,"Defense"),
("VECTOR","➡️","An arrow that points somewhere.","A list of numbers describing a point or direction.","Lattice math uses vectors in many dimensions.",2,"Math"),
("BINARY","🔟","Counting with just 0 and 1.","The base-2 number system computers use.","In binary, 5 is written 101.",2,"Computers"),
("DECODE","🔓","To turn a secret back into words.","To convert encoded data back to its original form.","Only the right key can decode it.",2,"Basics"),
("ENCODE","🔒","To turn words into a secret.","To convert data into another format.","Encode your message before sending.",2,"Basics"),
("MODULE","📦","One piece of a bigger thing.","A self-contained component of a system.","The ML in ML-KEM stands for Module-Lattice.",2,"PQC"),
("SHIELD","🛡️","It blocks attacks.","A protective barrier against threats.","Post-quantum crypto is a shield against quantum attacks.",2,"Defense"),
("ATTACK","⚔️","When a bad guy tries to break in.","An attempt to breach or damage a system.","Shor's algorithm is a quantum attack on RSA.",2,"Threats"),
("PUBLIC","📢","Everybody can see it.","Information that can safely be shared with anyone.","Your public key is meant to be shared!",2,"Signatures"),
("GROVER","🔎","A quantum search trick.","A quantum algorithm that speeds up searching.","Grover only gives a square-root speedup.",2,"Threats"),
("PHOTON","💡","A tiny particle of light.","The elementary particle of light.","Photons can carry qubits over fiber.",2,"Quantum"),

# ── TIER 3 ──────────────────────────────────────────────────────────────
("QUANTUM","⚛️","A super-fast new kind of computer.","Relating to the physics of very small particles.","Quantum computers use qubits instead of bits.",3,"Quantum"),
("ENCRYPT","🔐","To lock up a message.","To convert data into an unreadable form using a key.","Always encrypt sensitive data before sending it.",3,"Basics"),
("DECRYPT","🔓","To unlock a message and read it.","To convert encrypted data back to readable form.","Only the private key can decrypt it.",3,"Basics"),
("LATTICE","🏗️","A giant grid of dots with a secret inside.","A regular grid of points in high-dimensional space.","Lattice problems resist quantum attacks.",3,"PQC"),
("NETWORK","🌐","Computers all connected together.","A group of connected computers that share data.","The internet is a network of networks.",3,"Computers"),
("PRIVACY","🤐","Keeping your own stuff to yourself.","The right to control who sees your information.","Encryption protects your privacy.",3,"Defense"),
("PROTECT","🛡️","To keep something safe from harm.","To defend against threats or damage.","Firewalls and encryption protect your data.",3,"Defense"),
("SECURITY","🔒","Everything that keeps you safe.","The practice of defending systems and data.","Cybersecurity is a whole career field!",3,"Defense"),
("PASSWORD","🔑","The secret word that lets you in.","A secret string used to prove your identity.","Long, unique passwords are the strongest.",3,"Defense"),
("FIREWALL","🧱","A computer guard at the door.","A system that filters network traffic by rules.","Firewalls block suspicious connections.",3,"Defense"),
("DILITHIUM","🛡️","A strong lock that signs your name.","ML-DSA, FIPS 204 — the NIST post-quantum signature standard.","Dilithium proves a message really came from you.",3,"PQC"),
("SPHINCS","🌲","A safe lock built from math trees.","SLH-DSA, FIPS 205 — hash-based signatures.","SPHINCS+ uses only hash functions for security.",3,"PQC"),
("ALGORITHM","📋","A recipe of steps for a computer.","A step-by-step procedure for solving a problem.","Shor's algorithm factors numbers quickly.",3,"Basics"),
("COMPUTER","💻","A machine that does math super fast.","A device that processes data using instructions.","Your phone is a powerful computer.",3,"Computers"),
("INTERNET","🌍","How all the computers talk.","The global network connecting billions of devices.","Every internet connection needs encryption.",3,"Computers"),
("MESSAGE","💬","Something you send to a friend.","Information transmitted from sender to receiver.","Encrypt your message so only your friend reads it.",3,"Basics"),
("SIGNATURE","✒️","Your special mark that proves it is you.","Cryptographic proof of authorship and integrity.","A digital signature cannot be forged without the private key.",3,"Signatures"),
("KEYPAIR","🗝️","Two keys that work together.","A matched public and private key.","Share the public key, guard the private one!",3,"Signatures"),
("SCRAMBLE","🌀","To mix it all up.","To rearrange data so it appears meaningless.","Encryption scrambles your message.",3,"Basics"),
("DIGITAL","💾","Made of 0s and 1s.","Represented as discrete numeric values.","Digital signatures work on digital files.",3,"Computers"),
("PATTERN","🔷","Something that repeats.","A regular, detectable arrangement.","Good encryption leaves no patterns to find.",3,"Math"),
("PROTOCOL","📜","The rules for talking safely.","An agreed set of rules for communication.","TLS is the protocol securing web traffic.",3,"Computers"),
("SOLUTION","💡","The answer to a puzzle.","The result that solves a problem.","Finding the solution to a lattice problem is very hard.",3,"Math"),
("STANDARD","🏛️","The rule everyone agrees to use.","An official specification adopted widely.","NIST publishes cryptographic standards.",3,"PQC"),
("TRAPDOOR","🚪","Easy one way, super hard the other.","A function easy to compute but hard to reverse.","Trapdoor functions are the heart of public-key crypto.",3,"Math"),
("SCIENTIST","🔬","A person who studies and discovers.","Someone who investigates the natural world.","Scientists at NIST tested dozens of algorithms.",3,"PQC"),
("CHALLENGE","🎯","A hard task to try.","A problem posed to test a system or person.","NIST ran a public challenge to find PQC algorithms.",3,"PQC"),
("ENCRYPTED","🔐","All locked up and safe.","Converted into an unreadable protected form.","Your encrypted messages look like gibberish to spies.",3,"Basics"),
("PLAINTEXT","📄","A message before it gets locked.","The original readable form of a message.","Plaintext goes in, ciphertext comes out.",3,"Basics"),
("CIPHERTEXT","🔣","A message after it gets locked.","The scrambled output of encryption.","Ciphertext is useless without the key.",3,"Basics"),
("CRYPTOGRAPHY","🔐","The science of secret codes.","The study of secure communication techniques.","Cryptography protects the entire internet.",3,"Basics"),
("HARDWARE","🖲️","The parts you can touch.","The physical components of a computer.","Some encryption runs in dedicated hardware.",3,"Computers"),
("SOFTWARE","💿","The programs inside a computer.","Instructions that tell hardware what to do.","Keep your software updated for security!",3,"Computers"),
("PARTICLE","✨","A teeny tiny bit of stuff.","A very small unit of matter or energy.","Quantum physics describes particle behavior.",3,"Quantum"),
("SUPERPOSITION","🌗","Being two things at once.","A quantum state that is a blend of 0 and 1.","Superposition ends the moment you measure.",3,"Quantum"),
("ENTANGLEMENT","🔗","Two particles linked together.","A quantum link where measuring one reveals the other.","Einstein called it spooky action at a distance.",3,"Quantum"),
("HADAMARD","🎰","The coin-flip gate.","A quantum gate that creates superposition.","Apply H twice and you get back where you started!",3,"Quantum"),
("MEASUREMENT","📏","Looking at a qubit makes it choose.","Observing a quantum state, collapsing it to 0 or 1.","Measurement destroys superposition.",3,"Quantum"),
("CERTIFICATE","📜","A digital ID card for websites.","A signed document binding a public key to an identity.","Your browser checks certificates automatically.",3,"Signatures"),
("AUTHENTIC","✅","Real and not a fake.","Verified as genuine.","Signatures prove a message is authentic.",3,"Signatures"),
("INTEGRITY","🧾","Nothing was changed.","Assurance that data has not been altered.","Hashes protect integrity.",3,"Signatures"),
("MIGRATION","🚚","Moving to something new.","Transitioning systems to new algorithms.","PQC migration will take many years.",3,"PQC"),
("QUANTUMSAFE","🦸","Safe even from a quantum computer.","Resistant to attacks by quantum computers.","ML-KEM and ML-DSA are quantum-safe.",3,"PQC"),
("CODEBREAKER","🕵️","Someone who cracks secret codes.","A person who analyzes and defeats ciphers.","Alan Turing was a famous codebreaker.",3,"Threats"),
("FACTORING","✖️","Splitting a number into its parts.","Finding which primes multiply to make a number.","RSA breaks if factoring becomes easy.",3,"Math"),
("SIMULATION","🧪","Pretending on a computer.","Modeling a real system with software.","Quantum computers are great at simulating molecules.",3,"Quantum"),
]


def get_words(tier=None, category=None, max_len=None, min_len=None):
    """Filter the bank. Returns a list of tuples."""
    out = []
    for w in VOCAB_BANK:
        word, emoji, simple, full, ex, t, cat = w
        if tier is not None and t != tier:
            continue
        if category is not None and cat != category:
            continue
        if max_len is not None and len(word) > max_len:
            continue
        if min_len is not None and len(word) < min_len:
            continue
        out.append(w)
    return out


def word_list(tier=None, category=None, max_len=None, min_len=None):
    """Just the words, for word search / rescue."""
    return [w[0] for w in get_words(tier, category, max_len, min_len)]


def cards(tier=None, category=None):
    """Dicts shaped for the Vocab Cards game."""
    colors = {"Basics": "#10b981", "Quantum": "#8b5cf6", "PQC": "#3b82f6",
              "Math": "#f59e0b", "Computers": "#06b6d4", "Threats": "#ef4444",
              "Defense": "#22c55e", "Signatures": "#a855f7"}
    out = []
    for word, emoji, simple, full, ex, t, cat in get_words(tier, category):
        out.append({"word": word.title() if len(word) > 4 else word,
                    "emoji": emoji, "simple": simple, "full": full,
                    "example": ex, "tier": t, "category": cat,
                    "color": colors.get(cat, "#6366f1")})
    return out


def hints(tier=None):
    """(word, hint) pairs for Word Rescue."""
    return [(w[0], w[2]) for w in get_words(tier)]


if __name__ == "__main__":
    print("total terms:", len(VOCAB_BANK))
    for t in (1, 2, 3):
        print(f"  tier {t}: {len(get_words(tier=t))}")
    cats = {}
    for w in VOCAB_BANK:
        cats[w[6]] = cats.get(w[6], 0) + 1
    print("categories:", cats)
    seen = set()
    for word, emoji, simple, full, ex, t, cat in VOCAB_BANK:
        assert word.isalpha() and word.isupper(), f"bad word: {word}"
        assert word not in seen, f"duplicate: {word}"
        assert len(simple) < 90, f"simple def too long: {word}"
        seen.add(word)
    print("all checks passed")
