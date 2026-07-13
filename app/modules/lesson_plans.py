def render_lesson_plans():
    """Pre-game lesson plans for Elementary, Middle, and High School PQC modules."""
    import streamlit as st

    st.title("📚 QuantumVault Academy — Lesson Plans")
    st.markdown(
        "**Before you play, read your lesson!** "
        "Each lesson prepares you for the games and activities in your grade level. "
        "Every big word is explained simply — no prior knowledge needed!"
    )

    grade = st.selectbox(
        "Choose your grade level:",
        ["🟢 Elementary (K-5)", "🟡 Middle School (6-8)", "🔴 High School (9-12)"]
    )

    if "Elementary" in grade:
        render_elementary_lessons()
    elif "Middle" in grade:
        render_middle_lessons()
    else:
        render_high_lessons()


def render_elementary_lessons():
    import streamlit as st

    st.markdown("---")
    st.markdown("## 🟢 Elementary School Lesson Plans (K–5)")
    st.markdown("*Estimated total time: 45–60 minutes across all activities*")

    lessons = [
        {
            "title": "📖 Lesson 1: What is a Secret Code?",
            "game": "🔤 Secret Message Maker",
            "time": "10 minutes",
            "objective": "Students will understand that secret codes hide messages so only the right person can read them.",
            "vocab": [
                ("Secret Code", "A special way of writing a message that only certain people can understand. Like a secret language between you and your best friend!"),
                ("Encrypt", "To LOCK a message so it looks like gibberish to strangers. Like putting your diary in a locked box."),
                ("Decrypt", "To UNLOCK a message and read it. Only the person with the right key can do this."),
                ("Key", "The special trick or tool that lets you lock AND unlock a secret message. Without the key, the message is impossible to read!"),
            ],
            "lesson": """
**🎯 Big Idea:** Information needs to be protected, just like your house needs a lock.

**Story Time:** 
Imagine you and your best friend want to pass notes in class without anyone else reading them. You could make up a secret code — maybe A=1, B=2, C=3. So "HI" becomes "8 9". Anyone else who reads it just sees numbers and gets confused!

That's EXACTLY what computers do with your information every time you use the internet. When you log into a game or your parents buy something online, the computer ENCRYPTS (locks) the information first so hackers can't read it.

**Think About It:** 
- 🤔 What would happen if there were NO secret codes on the internet?
- 🤔 Who needs to protect information? (Banks? Doctors? Schools? YOU?)

**Real Life Example:**
When your parent types their password on a website, it gets ENCRYPTED before it travels through the internet. Without encryption, anyone sitting nearby could steal it!

**Get Ready to Play:**
In Secret Message Maker, you'll create and decode your own secret messages — just like real cryptographers (people who make and break codes)!
            """,
            "check": "Ask students: Can you explain what 'encrypt' means using your own words and an example from daily life?"
        },
        {
            "title": "🔑 Lesson 2: Keys, Locks, and Quantum Locks",
            "game": "🧱 Quantum Lock Drop & Tower Defense",
            "time": "10 minutes",
            "objective": "Students will understand the difference between old locks (RSA) and new quantum-safe locks (ML-KEM).",
            "vocab": [
                ("Lock", "In computers, a lock is a math puzzle so hard that it would take MILLIONS of years for a regular computer to solve it."),
                ("RSA", "The OLD type of computer lock used for 40+ years. Like a padlock — strong against normal thieves but could be broken by a quantum computer. RSA stands for Rivest–Shamir–Adleman — the last names of the three scientists who invented it in 1977!"),
                ("Quantum Computer", "A super-powerful NEW type of computer that uses special physics to solve certain math puzzles MUCH faster than regular computers. It could break RSA locks!"),
                ("ML-KEM", "The NEW quantum-safe lock! ML stands for Module Lattice, KEM stands for Key Encapsulation Mechanism. It uses math that even quantum computers CANNOT solve. Think of it as an upgraded, unbreakable lock!"),
                ("NIST", "The National Institute of Standards and Technology — a US government organization of scientists who decide which locks are safe enough to protect America's secrets. In 2024 they said: Use ML-KEM!"),
            ],
            "lesson": """
**🎯 Big Idea:** Old computer locks are in danger. We need NEW quantum-safe locks!

**Story Time:**
Imagine a regular padlock on a locker. A strong person could cut it with bolt cutters — that's like a regular computer attacking RSA.

Now imagine a QUANTUM computer. It's like having a magic key that can try EVERY possible combination at the same time. It could open that padlock in seconds!

But what if you had a MAGICAL LOCK that even the magic key couldn't open? That's ML-KEM — the new quantum-safe lock!

**The Timeline (Super Simple):**
- 1977: Scientists made RSA locks 🔒 (great for 40+ years!)
- 2019: Scientists realized quantum computers could break RSA 😱
- 2024: NIST said "everyone must switch to ML-KEM!" ✅
- TODAY: Google, Apple, and banks are switching right now!

**Classroom Activity:**
Hold up your hand. Your 5 fingers represent 5 years. How many hands until 2030? (About 1 hand = 5 years from now). Quantum computers that can break RSA might be ready in 1-2 hands!

**Get Ready to Play:**
In Quantum Lock Drop, you'll protect servers using new quantum-safe locks. Every lock you place = one piece of data protected from quantum hackers!
            """,
            "check": "Ask students: Why do we need NEW locks if the old RSA locks worked for 40 years?"
        },
        {
            "title": "⛏️ Lesson 3: Mining for Quantum Crystals",
            "game": "⛏️ QuantumCraft (Elementary)",
            "time": "8 minutes",
            "objective": "Students will understand that different algorithms have different strengths, just like different tools for different jobs.",
            "vocab": [
                ("Algorithm", "A set of step-by-step instructions a computer follows to solve a problem. Like a recipe — if you follow the steps exactly, you get the right result!"),
                ("PQC", "Post-Quantum Cryptography. 'Post' means AFTER. So PQC means cryptography (secret codes) designed for the world AFTER quantum computers exist. It's the future of keeping secrets safe!"),
                ("Kyber Crystal", "In the game, Kyber crystals represent ML-KEM — the strongest quantum-safe key exchange algorithm. In real life, ML-KEM protects the keys that lock your data!"),
                ("Dilithium", "Another PQC algorithm — ML-DSA. It creates DIGITAL SIGNATURES, like a super-secure electronic signature that proves YOU sent a message and nobody changed it."),
            ],
            "lesson": """
**🎯 Big Idea:** Different crypto tools protect different things — like how different keys open different locks.

**The Toolbox Analogy:**
A plumber has different tools — a wrench for pipes, a plunger for clogs. Cryptographers have different algorithms:
- 🔑 **ML-KEM (Kyber)** → Protects the KEY that locks your data
- ✍️ **ML-DSA (Dilithium)** → Proves a message is REALLY from you
- 🌲 **SLH-DSA (SPHINCS+)** → Extra secure signatures using math trees
- 🦅 **FN-DSA (Falcon)** → Super small signatures for tiny devices

**Why does size matter?**
Imagine sending a letter. A tiny envelope costs less postage. In computing, smaller = faster and cheaper to send! Falcon makes the TINIEST quantum-safe signatures — perfect for smart devices like your smartwatch or IoT sensors!

**Get Ready to Play:**
In QuantumCraft, you'll mine different crystals that represent these algorithms. Each crystal has different properties — just like the real algorithms!
            """,
            "check": "Ask students: Name one PQC algorithm and what it protects."
        },
        {
            "title": "🧟 Lesson 4: Defending Against Cyber Attacks",
            "game": "🧟 Quantum Zombie Blast",
            "time": "8 minutes",
            "objective": "Students will understand what hackers try to steal and how encryption protects us.",
            "vocab": [
                ("Hacker", "Someone who tries to break into computer systems WITHOUT permission to steal information. Not all hackers are bad — some are 'white hat' hackers who find problems to FIX them!"),
                ("Data Breach", "When a hacker successfully steals information from a computer system. Like a burglar getting into a house and taking valuables."),
                ("Shor Algorithm", "A special program that only runs on quantum computers. It can break RSA encryption MUCH faster than any regular computer. Named after mathematician Peter Shor who discovered it in 1994."),
                ("Server", "A powerful computer that stores information and provides services to other computers. When you play an online game, a server keeps track of your score and other players!"),
                ("Firewall", "A digital security guard that blocks suspicious activity from entering a computer network — like a bouncer at a party who only lets in invited guests."),
            ],
            "lesson": """
**🎯 Big Idea:** Hackers use tools like Shor Algorithm to break old encryption. We defend with PQC!

**The Zombie Analogy:**
In Quantum Zombie Blast, zombies represent SHOR ALGORITHM — the quantum computing attack that can break RSA. Your weapons are PQC algorithms (ML-KEM, ML-DSA) that the zombies CANNOT break through!

**What Hackers Actually Steal:**
- 🏥 Medical records (your health history)
- 🏦 Bank account information
- 🎮 Game account passwords
- 📧 Private messages and emails
- 🏫 School records and grades

**The Good News:**
With PQC (Post-Quantum Cryptography), even if a hacker has a quantum computer, they CANNOT break the new locks! It's like the zombies hitting an unbreakable shield!

**Real Fact:** In 2023, hackers stole data from over 3,000 companies. Most of that data was protected with OLD encryption. With PQC, that data would have been safe!

**Get Ready to Play:**
Use ML-KEM, ML-DSA, SPHINCS+, and Falcon weapons to destroy Shor Zombies before they reach your server. Each weapon represents a real PQC algorithm approved by NIST in 2024!
            """,
            "check": "Ask students: What is Shor Algorithm and why is it dangerous?"
        },
    ]

    for i, lesson in enumerate(lessons):
        with st.expander(f"**{lesson['title']}** — Before playing: {lesson['game']} | ⏱️ {lesson['time']}", expanded=(i==0)):
            st.markdown(f"**🎮 Prepares you for:** {lesson['game']}")
            st.markdown(f"**⏱️ Time:** {lesson['time']}")
            st.markdown(f"**🎯 Learning Goal:** {lesson['objective']}")

            st.markdown("### 📖 Vocabulary — Learn These Words First!")
            for term, definition in lesson['vocab']:
                st.markdown(f"""
<div style='background:#071520;border-left:3px solid #3b82f6;border-radius:6px;
padding:8px 12px;margin-bottom:6px;'>
<b style='color:#60a5fa'>{term}</b><br>
<span style='color:#94a3b8;font-size:14px'>{definition}</span>
</div>""", unsafe_allow_html=True)

            st.markdown("### 📝 Lesson")
            st.markdown(lesson['lesson'])

            st.markdown(f"""
<div style='background:#052e16;border:1px solid #10b981;border-radius:8px;padding:10px;margin-top:10px;'>
<b style='color:#10b981'>✅ Check for Understanding</b><br>
<span style='color:#94a3b8'>{lesson['check']}</span>
</div>""", unsafe_allow_html=True)


def render_middle_lessons():
    import streamlit as st

    st.markdown("---")
    st.markdown("## 🟡 Middle School Lesson Plans (6–8)")
    st.markdown("*Estimated total time: 60–90 minutes across all activities*")

    lessons = [
        {
            "title": "🏗️ Lesson 1: The Math Behind Secret Codes — Lattice Cryptography",
            "game": "🏗️ Lattice Explorer",
            "time": "15 minutes",
            "objective": "Students will understand what a lattice is and why it makes quantum-safe cryptography possible.",
            "vocab": [
                ("Lattice", "A grid of points arranged in a regular pattern — like graph paper but in many dimensions (not just 2D!). Imagine a giant invisible 3D jungle gym filling all of space."),
                ("LWE", "Learning With Errors — the math problem at the heart of ML-KEM. You take a point on a lattice and add a tiny random error to it. Finding the ORIGINAL point from the messy version is IMPOSSIBLE — even for quantum computers! LWE was invented by Oded Regev in 2005."),
                ("Dimension", "A direction in space. Our physical world has 3 dimensions (left-right, up-down, forward-back). Lattice cryptography uses HUNDREDS of dimensions — no computer can navigate that maze!"),
                ("Hard Problem", "A math problem that's easy to create but nearly impossible to reverse. Example: It's easy to multiply 17 × 23 = 391. But if I give you 391, finding 17 and 23 is much harder! PQC uses problems MUCH harder than that."),
                ("ML-KEM", "Module Lattice Key Encapsulation Mechanism — the NIST FIPS 203 standard. The 'Module' part means it uses a ring-shaped lattice structure that makes math faster while staying secure. It replaced RSA for key exchange."),
            ],
            "lesson": """
**🎯 Big Idea:** Lattice math creates problems SO hard that even quantum computers with millions of qubits cannot solve them.

**The Shortest Vector Problem — Explained Simply:**
Imagine a huge 3D grid of dots (a lattice). I pick one dot near the center. Your job: find the CLOSEST dot to the center. 

In 2 dimensions (regular graph paper)? Easy — you can see it.
In 500 dimensions? IMPOSSIBLE. No computer in the universe can do it fast enough.

That's the secret behind ML-KEM!

**Why Quantum Computers Can't Break Lattices:**
Quantum computers are great at ONE thing: trying many possibilities at the same time (called superposition). This is how Shor Algorithm breaks RSA — it tries all possible factors simultaneously.

BUT for lattice problems, trying all possibilities doesn't help. The search space is TOO large — even with quantum superposition, you can't navigate a 500-dimensional maze any faster!

**Real World Numbers:**
- RSA-2048 has a search space of about 2^2048 possibilities
- A quantum computer can crack RSA-2048 in hours using Shor Algorithm
- ML-KEM has a lattice so complex that even with quantum superposition, cracking it would take longer than the age of the universe (13.8 billion years!)

**The NIST Decision (August 13, 2024):**
After 8 years and 69 submitted algorithms from researchers worldwide, NIST chose:
- FIPS 203 → ML-KEM (lattice-based key exchange)
- FIPS 204 → ML-DSA (lattice-based signatures)
- FIPS 205 → SLH-DSA (hash-based signatures)

**Get Ready to Play:**
In Lattice Explorer, you'll navigate through lattice grids and see why finding the shortest vector is so difficult. You'll physically experience the problem that keeps quantum computers locked out!
            """,
            "check": "Ask students: Why can't a quantum computer solve the shortest vector problem? What makes lattice math special?"
        },
        {
            "title": "🏭 Lesson 2: Hash Functions — The Digital Fingerprint",
            "game": "🏭 Hash Factory",
            "time": "12 minutes",
            "objective": "Students will understand what a hash function does and why SHA-3 is quantum-resistant.",
            "vocab": [
                ("Hash Function", "A math machine that takes ANY input (a word, a file, a whole book) and outputs a fixed-size jumble of letters and numbers called a hash. Like a shredder that always produces the same size pile of confetti for the same input!"),
                ("SHA-3", "Secure Hash Algorithm 3 — the current gold standard hash function. Developed by a team called Keccak, standardized by NIST in 2015. Used inside SPHINCS+ (FIPS 205) to create quantum-safe signatures!"),
                ("Collision", "When two DIFFERENT inputs produce the SAME hash output. A good hash function makes collisions practically IMPOSSIBLE to find — even if you tried every computer on Earth for a billion years."),
                ("One-Way Function", "A mathematical operation that's easy to do forward but IMPOSSIBLE to reverse. Hashing is one-way: given a hash, you cannot find what input created it. Like scrambled eggs — easy to scramble, impossible to unscramble!"),
                ("SLH-DSA", "Stateless Hash-Based Digital Signature Algorithm — NIST FIPS 205. Uses SHA-3 hash functions chained together to create quantum-safe signatures. 'Stateless' means you don't need to remember previous signatures to create new ones."),
                ("SPHINCS+", "The algorithm that became SLH-DSA. Uses a complex structure of hash trees to create signatures. It's slower and larger than ML-DSA but uses simpler math — good for applications that need maximum security!"),
            ],
            "lesson": """
**🎯 Big Idea:** Hash functions are mathematical fingerprinters — each document gets a unique fingerprint that cannot be faked.

**The Fingerprint Analogy:**
Every person has unique fingerprints. Police find a fingerprint at a crime scene and match it to a suspect. 

Hash functions do the same for files:
- Document A → SHA-3 → "7f83b1657ff1fc53b92..."
- Document B (one letter changed) → SHA-3 → "adf3e7891ab2cd47f1..." (COMPLETELY different!)

If ANYONE changes even ONE character in a document, the hash changes entirely. This is how you know a file hasn't been tampered with!

**How SHA-3 Works (Simple Version):**
SHA-3 uses a process called a "sponge" — it ABSORBS your input data and SQUEEZES out a fixed-size output. The internal state uses XOR logic gates (you'll learn these in the Logic Gate Lab!) to thoroughly mix everything together.

Input → Absorb into 1600 bits of state → XOR mixing → XOR mixing → XOR mixing → Squeeze out 256 bits → Your hash!

**Why Quantum Computers Can't Easily Break SHA-3:**
Grover's Algorithm (a quantum attack on hash functions) CAN speed up finding collisions — but only by a square root. SHA-3-256 acts like SHA-3-128 against a quantum computer. That's why NIST recommends SHA-3-256 or higher for quantum safety!

**Real Applications of Hash Functions:**
- ✅ Verifying software updates (is this REALLY from Apple/Google?)
- ✅ Storing passwords (websites store your hash, not your actual password)
- ✅ Digital signatures (ML-DSA, SLH-DSA all use hash functions internally)
- ✅ Blockchain technology

**Get Ready to Play:**
In Hash Factory, you'll feed different inputs through SHA-3 and watch how the output changes completely with even tiny differences. You'll understand exactly why hash functions are quantum-resistant!
            """,
            "check": "Ask students: What happens to a SHA-3 hash if you change ONE letter in the original document? Why does this matter for security?"
        },
        {
            "title": "🔑 Lesson 3: How Big Should Your Key Be?",
            "game": "🔬 Key Size Lab",
            "time": "10 minutes",
            "objective": "Students will understand why key size matters and how quantum computers change the math.",
            "vocab": [
                ("Key Size", "How many bits (0s and 1s) make up a cryptographic key. Bigger key = more possible combinations = harder to crack. RSA-2048 has 2048 bits."),
                ("Bit", "The smallest unit of computer information — either 0 or 1. Like a light switch that's either OFF or ON. 8 bits = 1 byte, 1024 bytes = 1 kilobyte."),
                ("Security Level", "Measured in bits — how many operations an attacker needs to crack your encryption. 128-bit security means 2^128 operations needed — that's 340 undecillion attempts! Even a quantum computer can't do that in any reasonable time."),
                ("Grover's Algorithm", "A quantum algorithm (by Lov Grover, 1996) that searches through possibilities faster than any classical computer. It halves the security level: a 256-bit classical key gives only 128-bit quantum security. This is why AES-256 is recommended over AES-128!"),
                ("CNSA 2.0", "Commercial National Security Algorithm Suite 2.0 — the NSA's official list of approved algorithms for protecting US government secrets. Released 2022. Mandates ML-KEM-1024 (256-bit quantum security) for classified systems by 2030."),
            ],
            "lesson": """
**🎯 Big Idea:** Key size is like the number of digits in a combination lock. Quantum computers are like lockpickers who work twice as fast — so we need twice as many digits!

**The Combination Lock Analogy:**
A 3-digit combination lock has 1,000 possible combinations.
A 6-digit lock has 1,000,000 combinations.
A 12-digit lock has 1,000,000,000,000 combinations.

Each extra digit makes it 10 times harder to crack. In binary (0s and 1s):
- Each extra BIT makes it 2 times harder to crack
- Going from 128-bit to 256-bit makes it 2^128 = 340 undecillion times harder!

**The Quantum Threat to Key Size:**
- Classical computer cracking AES-128: 2^128 attempts needed ✅ Safe
- Quantum computer cracking AES-128: 2^64 attempts needed (Grover's Algorithm) ⚠️ Dangerous!
- Quantum computer cracking AES-256: 2^128 attempts needed ✅ Still safe!

This is why NIST recommends using LARGER keys:
- AES-128 → AES-256 (doubles security against quantum)
- RSA-2048 → ML-KEM-768 (completely different math — quantum-safe!)

**Comparing Key Sizes (Key Size Lab Preview):**
| Algorithm | Key Size | Quantum Safe? | Used For |
|-----------|----------|---------------|----------|
| RSA-2048 | 256 bytes | ❌ NO | Old websites |
| ECC-256 | 32 bytes | ❌ NO | Old phones |
| ML-KEM-768 | 1,184 bytes | ✅ YES | New websites |
| ML-DSA-44 | 1,312 bytes | ✅ YES | Digital signing |
| Falcon-512 | 897 bytes | ✅ YES | IoT devices |

**Get Ready to Play:**
In Key Size Lab, you'll race different algorithms head-to-head and see how their key sizes affect speed and security. You'll use the decision calculator to pick the right algorithm for different scenarios!
            """,
            "check": "Ask students: Why does Grover's Algorithm mean we need larger keys? Give a specific example with numbers."
        },
        {
            "title": "⚡ Lesson 4: Logic Gates — The Building Blocks of ALL Cryptography",
            "game": "⚡ Logic Gate Lab",
            "time": "12 minutes",
            "objective": "Students will understand how AND, OR, XOR, NOT, NAND, and NOR gates work and why XOR is the most important gate in cryptography.",
            "vocab": [
                ("Logic Gate", "An electronic circuit that takes binary inputs (0 or 1) and produces a binary output based on a rule. Every computer chip has BILLIONS of logic gates working together!"),
                ("AND Gate", "Output is 1 ONLY if BOTH inputs are 1. Like a door that opens only when you have BOTH a key AND a keycard. Symbol: AND. Truth table: 0+0=0, 0+1=0, 1+0=0, 1+1=1"),
                ("OR Gate", "Output is 1 if AT LEAST ONE input is 1. Like a door that opens if you have EITHER a key OR a keycard. Truth table: 0+0=0, 0+1=1, 1+0=1, 1+1=1"),
                ("XOR Gate", "eXclusive OR — output is 1 if inputs are DIFFERENT. If they're the same, output is 0. This is THE most important gate in cryptography! XOR is used in SHA-3, AES, and all stream ciphers. Truth table: 0⊕0=0, 0⊕1=1, 1⊕0=1, 1⊕1=0"),
                ("NOT Gate", "Flips the input. 0 becomes 1, 1 becomes 0. Also called an inverter. Simple but powerful! Truth table: NOT(0)=1, NOT(1)=0"),
                ("NAND Gate", "NOT AND — the OPPOSITE of AND. Output is 0 ONLY when both inputs are 1. NAND is called a UNIVERSAL GATE because you can build ANY other gate using only NAND gates!"),
                ("NOR Gate", "NOT OR — the OPPOSITE of OR. NOR is ALSO a universal gate! The entire original Apple Mac computer was built using NOR gates."),
                ("Half Adder", "A circuit made from XOR + AND that adds two single binary digits. XOR gives the SUM, AND gives the CARRY. This is how computers do math at the hardware level!"),
            ],
            "lesson": """
**🎯 Big Idea:** Every computer operation — including all cryptography — breaks down into billions of simple logic gate operations happening billions of times per second.

**Why XOR is the King of Crypto:**
XOR has a magical property: it's PERFECTLY REVERSIBLE with the same key!

Example:
- Message: 1 0 1 1 0
- Key:      1 1 0 1 0
- XOR:      0 1 1 0 0  ← encrypted!
- XOR again with same key: 1 0 1 1 0 ← back to original!

This makes XOR the perfect encryption operation. You encrypt AND decrypt with the same key. This is why XOR appears in:
- ✅ AES (Advanced Encryption Standard)
- ✅ SHA-3 (the hash function inside SPHINCS+/SLH-DSA)
- ✅ ML-KEM (Kyber uses XOR in key derivation)
- ✅ Stream ciphers (ChaCha20)

**Building Up Complexity:**
One XOR gate encrypts one bit. Chain 256 XOR gates = encrypt 256 bits. Add some AND, OR, and NOT gates = AES. Add SHA-3 mixing = unbreakable hash. Add lattice math = ML-KEM!

**The SHA-3 Connection:**
SHA-3 processes data using a 5x5 grid of 64-bit words (1,600 bits total). Each round applies 5 operations, all built from XOR, AND, NOT, and rotation. After 24 rounds, your input is thoroughly mixed into a hash that can never be reversed!

**NAND is Universal — Prove it:**
- NOT(A) = NAND(A, A) — connect both NAND inputs together!
- AND(A,B) = NAND(NAND(A,B), NAND(A,B)) — double NAND
- OR(A,B) = NAND(NAND(A,A), NAND(B,B)) — three NANDs!

**Get Ready to Play:**
In Logic Gate Lab, you'll drag and drop real gates onto a canvas, wire them together, and watch circuits come alive. Complete 4 challenges from basic AND circuits to SHA-3 XOR chains!
            """,
            "check": "Ask students: Why is XOR so special for cryptography? Demonstrate with numbers why XOR is perfectly reversible."
        },
    ]

    for i, lesson in enumerate(lessons):
        with st.expander(f"**{lesson['title']}** — Before: {lesson['game']} | ⏱️ {lesson['time']}", expanded=(i==0)):
            st.markdown(f"**🎮 Prepares you for:** {lesson['game']}")
            st.markdown(f"**⏱️ Time:** {lesson['time']}")
            st.markdown(f"**🎯 Learning Goal:** {lesson['objective']}")

            st.markdown("### 📖 Vocabulary — Master These Terms First!")
            for term, definition in lesson['vocab']:
                st.markdown(f"""
<div style='background:#071520;border-left:3px solid #fbbf24;border-radius:6px;
padding:8px 12px;margin-bottom:6px;'>
<b style='color:#fbbf24'>{term}</b><br>
<span style='color:#94a3b8;font-size:14px'>{definition}</span>
</div>""", unsafe_allow_html=True)

            st.markdown("### 📝 Lesson")
            st.markdown(lesson['lesson'])

            st.markdown(f"""
<div style='background:#052e16;border:1px solid #10b981;border-radius:8px;padding:10px;margin-top:10px;'>
<b style='color:#10b981'>✅ Check for Understanding</b><br>
<span style='color:#94a3b8'>{lesson['check']}</span>
</div>""", unsafe_allow_html=True)


def render_high_lessons():
    import streamlit as st

    st.markdown("---")
    st.markdown("## 🔴 High School Lesson Plans (9–12)")
    st.markdown("*Estimated total time: 90–120 minutes across all activities*")

    lessons = [
        {
            "title": "📅 Lesson 1: The NIST PQC Timeline — Why 2024 Changed Everything",
            "game": "📅 NIST Timeline",
            "time": "15 minutes",
            "objective": "Students will understand the historical context of the PQC standardization process and what the 2024 FIPS standards mean for the world.",
            "vocab": [
                ("NIST", "National Institute of Standards and Technology. A US federal agency that sets technical standards for industry and government. When NIST mandates an algorithm, it becomes the law for all federal systems and heavily influences private industry worldwide."),
                ("FIPS", "Federal Information Processing Standards. Official US government standards for cryptography. FIPS 140-2 covers hardware security modules. The 2024 PQC standards are FIPS 203, 204, 205, and 206."),
                ("Shor's Algorithm", "A quantum algorithm discovered by MIT mathematician Peter Shor in 1994. It factors large numbers EXPONENTIALLY faster than any classical algorithm. RSA security relies on factoring being hard — Shor's Algorithm makes it easy on a quantum computer. Factoring 2048-bit RSA: classical = 2^86 years, quantum = ~hours."),
                ("CRQC", "Cryptographically Relevant Quantum Computer. A quantum computer powerful enough to run Shor's Algorithm on real-world key sizes (2048+ bit RSA, 256-bit ECC). Current estimates: CRQC requires ~4,000 logical qubits. IBM projects this is possible by 2033."),
                ("Harvest Now Decrypt Later", "HNDL — a nation-state attack strategy where adversaries intercept and STORE encrypted network traffic today, then decrypt it retroactively once a CRQC exists. Chinese, Russian, and US intelligence agencies are believed to be doing this NOW."),
                ("Migration", "The process of switching from vulnerable algorithms (RSA, ECC, DSA) to quantum-safe algorithms (ML-KEM, ML-DSA, SLH-DSA). Migration is complex because cryptography is embedded in every protocol — TLS, SSH, S/MIME, code signing, VPNs, and more."),
            ],
            "lesson": """
**🎯 Big Idea:** The 2024 NIST standards are the most significant cryptographic event since RSA was invented in 1977. Every organization on Earth must migrate before CRQCs arrive.

**The Full Timeline:**
- **1977**: RSA invented by Rivest, Shamir, Adleman at MIT. Revolutionizes public-key cryptography.
- **1994**: Peter Shor publishes algorithm that breaks RSA on quantum hardware. Alarm bells ring in cryptographic community.
- **2001**: NIST standardizes AES — first major algorithm transition in the modern era.
- **2016**: NIST launches PQC competition. 69 algorithm submissions from teams worldwide. 8-year review process begins.
- **2019-2022**: Multiple rounds of cryptanalysis. Some algorithms broken (Rainbow, SIKE). Field narrows to finalists.
- **August 13, 2024**: NIST publishes FIPS 203, 204, 205. Cryptographic history is made.
- **2026-2027**: Google, Apple, Cloudflare, AWS complete migration. NSA compliance deadline approaches.
- **2030-2033**: Estimated CRQC arrival. All non-migrated systems at risk retroactively.

**What FIPS 203, 204, 205, 206 Actually Mandate:**
| Standard | Algorithm | Type | Key/Sig Size | Security Level |
|----------|-----------|------|--------------|----------------|
| FIPS 203 | ML-KEM-768 | Key Encapsulation | 1,184B pub key | 192-bit quantum |
| FIPS 204 | ML-DSA-65 | Digital Signature | 1,952B pub key | 192-bit quantum |
| FIPS 205 | SLH-DSA-128s | Hash Signature | 32B pub key | 128-bit quantum |
| FIPS 206 | FN-DSA-512 (Falcon) | Compact Signature | 897B pub key | 128-bit quantum |

**The Harvest Now Decrypt Later Threat:**
Think about what data gets encrypted today that's STILL sensitive in 10-15 years:
- Medical records (30-year retention laws in many states)
- National security communications
- Financial transaction records
- Intellectual property and trade secrets
- Personal identity documents

If adversaries are collecting this traffic today and a CRQC exists in 2033, data encrypted with RSA in 2024 becomes readable in 2033. This is NOT theoretical — NSA documents (Snowden, 2013) confirmed mass collection programs. China's Volt Typhoon group (2024) confirmed penetration of US infrastructure.

**What "Already Deployed" Looks Like:**
- ✅ Google Chrome 131+: Hybrid X25519+ML-KEM for all TLS 1.3
- ✅ Cloudflare: All new connections use ML-KEM
- ✅ Apple iMessage: PQXDH (Post-Quantum Extended Diffie-Hellman)
- ✅ Signal: PQXDH deployed globally
- ✅ AWS: Post-quantum TLS available
- ⏳ Most banks: Planning phase
- ❌ Most government agencies: Still assessing
            """,
            "check": "Ask students: What is HNDL and why does it mean organizations needed to start migrating BEFORE CRQCs exist? Give a specific example with a type of data."
        },
        {
            "title": "⚛️ Lesson 2: Quantum Circuit Composer — Qubits, Gates, and Why Shor Works",
            "game": "⚛️ Quantum Circuit Composer",
            "time": "18 minutes",
            "objective": "Students will understand quantum computing fundamentals well enough to understand WHY quantum computers break RSA and WHY lattice math resists them.",
            "vocab": [
                ("Qubit", "Quantum Bit — the basic unit of quantum information. Unlike a classical bit (0 OR 1), a qubit can be in a SUPERPOSITION of 0 and 1 simultaneously until measured. Represented as |0⟩ and |1⟩ using Dirac notation."),
                ("Superposition", "A quantum state where a qubit is both |0⟩ and |1⟩ at the same time — represented as α|0⟩ + β|1⟩ where α and β are probability amplitudes. When MEASURED, it collapses to either 0 or 1. This allows quantum computers to explore many possibilities simultaneously."),
                ("Entanglement", "When two qubits are connected so measuring one INSTANTLY determines the other's state, regardless of distance. Einstein called it 'spooky action at a distance.' The Bell State (created by H + CNOT) is the simplest entangled state: (|00⟩ + |11⟩)/√2"),
                ("Hadamard Gate (H)", "A quantum gate that puts a qubit into equal superposition: H|0⟩ = (|0⟩+|1⟩)/√2. This is HOW quantum parallelism begins — one H gate creates superposition, allowing quantum algorithms to explore multiple paths simultaneously."),
                ("CNOT Gate", "Controlled-NOT — flips the target qubit IF the control qubit is |1⟩. Combined with H, creates entanglement. Matrix: [[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]"),
                ("Quantum Fourier Transform", "QFT — A quantum version of the Discrete Fourier Transform that runs EXPONENTIALLY faster than the classical Fast Fourier Transform. QFT is the core of Shor's Algorithm. It extracts the period of a function, which leads directly to factoring RSA keys."),
                ("Decoherence", "When qubits lose their quantum properties due to interaction with the environment. Current quantum computers have decoherence times of microseconds to milliseconds. This is why error correction is crucial and why CRQCs aren't here yet — we need error-corrected logical qubits."),
                ("OpenQASM", "Open Quantum Assembly Language — a low-level programming language for quantum computers, like assembly language for classical machines. IBM Quantum Composer uses OpenQASM. Example: `h q[0]; cx q[0],q[1];` creates a Bell State."),
            ],
            "lesson": """
**🎯 Big Idea:** Quantum computers use superposition and entanglement to explore exponentially many computational paths simultaneously — which is why they break RSA but NOT lattice cryptography.

**Classical vs Quantum Computing:**
Classical: A bit is always 0 OR 1. A 4-bit register holds ONE number at a time (0-15).
Quantum: A qubit is 0 AND 1 in superposition. A 4-qubit register holds ALL 16 numbers simultaneously.
300 qubits in superposition = more states than atoms in the observable universe.

**How Shor's Algorithm Actually Works (Simplified):**
RSA security relies on: Given N = p × q, finding p and q is computationally hard.
(Example: 15 = 3 × 5 is easy. But 2048-bit N? Classical computers need ~2^86 years)

Shor's quantum approach:
1. Choose a random number 'a'
2. Find the period r of f(x) = a^x mod N (this is where QFT runs on quantum hardware)
3. Use r to compute: p = GCD(a^(r/2)+1, N), q = GCD(a^(r/2)-1, N)
4. RSA is broken!

Step 2 (QFT) is what makes this quantum-only. Classical period-finding takes exponential time. QFT does it in polynomial time — an exponential speedup!

**Why Lattices Resist This:**
Shor's Algorithm exploits the PERIODIC STRUCTURE of RSA math (modular exponentiation has periods). Lattice problems have NO such periodic structure. They're random-looking problems with no mathematical shortcut — even with quantum superposition.

The Shortest Vector Problem in 500 dimensions doesn't become easier with QFT. There's no periodicity to exploit. Even with 10 million perfect qubits, the search space remains intractable.

**Bell State Circuit (You'll Build This):**
```
q[0]: ─── H ─── ● ─── M
                 │
q[1]: ───────── X ─── M
```
QASM: `h q[0]; cx q[0],q[1]; measure q[0] -> c[0]; measure q[1] -> c[1];`
Result: Qubits are entangled — measuring always gives 00 or 11, never 01 or 10!

**Quantum Gate Matrices:**
H = (1/√2) × [[1, 1],[1,-1]]
X = [[0,1],[1,0]] (quantum NOT)
Z = [[1,0],[0,-1]] (phase flip)
These are UNITARY matrices — they're always reversible (unlike classical logic)!

**Get Ready to Play:**
In Quantum Composer, you'll build real circuits in a visual interface matching IBM Quantum Composer. Place gates on qubit wires, see the Bloch sphere update live, watch OpenQASM generate automatically, and complete 4 challenges from Bell States to PQC lattice gates!
            """,
            "check": "Ask students: Explain in your own words why Shor's Algorithm breaks RSA but cannot break ML-KEM. What specific property of RSA does Shor exploit that lattices don't have?"
        },
        {
            "title": "💻 Lesson 3: Code It Yourself — Implementing PQC in Python",
            "game": "🐍 PQC Python Lab",
            "time": "15 minutes",
            "objective": "Students will understand how to use NIST-standardized PQC algorithms in real Python code using the liboqs library.",
            "vocab": [
                ("liboqs", "Open Quantum Safe library — an open-source C library with Python bindings that implements all NIST PQC algorithms. Created by the Open Quantum Safe project at the University of Waterloo. Used by real organizations to begin PQC migration."),
                ("KEM", "Key Encapsulation Mechanism — a protocol where one party generates a key pair (public/private), another party encapsulates (encrypts) a random secret using the public key, and the first party decapsulates (decrypts) it using the private key. ML-KEM is the NIST standard KEM."),
                ("Public Key", "A key that can be shared with ANYONE. Used to encrypt messages or encapsulate keys that only the private key holder can decrypt. For ML-KEM-768: 1,184 bytes."),
                ("Private Key", "A key that NEVER leaves your device. Used to decrypt messages or decapsulate keys. MUST be kept secret. For ML-KEM-768: 2,400 bytes."),
                ("Digital Signature", "A mathematical proof that a specific entity created a specific message. Created with a private key, verified with the public key. ML-DSA signs documents; anyone with the public key can verify the signature but only the private key holder can CREATE valid signatures."),
                ("Key Exchange", "A protocol allowing two parties to establish a SHARED SECRET over a public channel without ever sending the secret itself. Diffie-Hellman is the classical version. ML-KEM is the quantum-safe replacement used in TLS 1.3."),
                ("Hybrid Cryptography", "Running BOTH a classical algorithm (like ECDH) AND a quantum-safe algorithm (like ML-KEM) simultaneously, combining both shared secrets. This approach is currently deployed by Google Chrome and Cloudflare — safe against both classical AND quantum attacks during the transition period."),
                ("TLS", "Transport Layer Security — the protocol that encrypts web traffic (the 'S' in HTTPS). TLS 1.3 is the current version. Google's hybrid X25519+ML-KEM is deployed in TLS 1.3 for all Chrome users today."),
            ],
            "lesson": """
**🎯 Big Idea:** PQC is not theoretical — you can install liboqs-python right now and generate ML-KEM keys that are quantum-safe.

**The PQC Stack (What's Running Under the Hood):**
```
Your Browser (Chrome)
    ↓
TLS 1.3 Handshake
    ↓
X25519 + ML-KEM-768 (Hybrid)
    ↓
ML-KEM: generates keys, encapsulates, decapsulates
    ↓
liboqs C library → FIPS 203 implementation
    ↓
CPU hardware operations
```

**ML-KEM Key Exchange in Python (liboqs):**
```python
import oqs  # pip install liboqs-python

# Alice generates her key pair
with oqs.KeyEncapsulation("Kyber768") as alice:
    alice_public_key = alice.generate_keypair()
    
    # Bob encapsulates a secret using Alice's public key
    with oqs.KeyEncapsulation("Kyber768") as bob:
        ciphertext, shared_secret_bob = bob.encap_secret(alice_public_key)
    
    # Alice decapsulates to get the SAME secret
    shared_secret_alice = alice.decap_secret(ciphertext)
    
    # Both have the SAME shared secret — securely established!
    assert shared_secret_alice == shared_secret_bob
    print("Key exchange successful! Shared secret:", shared_secret_alice.hex()[:32], "...")
```

**ML-DSA Digital Signature in Python:**
```python
import oqs

message = b"This contract was signed by Alice on 2024-08-13"

with oqs.Signature("Dilithium3") as signer:
    public_key = signer.generate_keypair()
    signature = signer.sign(message)

with oqs.Signature("Dilithium3") as verifier:
    is_valid = verifier.verify(message, signature, public_key)
    print("Signature valid:", is_valid)  # True
    
    # Try tampering with the message:
    tampered = b"This contract was signed by Bob on 2024-08-13"
    is_valid_tampered = verifier.verify(tampered, signature, public_key)
    print("Tampered signature valid:", is_valid_tampered)  # False!
```

**Understanding the Numbers:**
ML-KEM-768 generates:
- Public key: 1,184 bytes (slightly larger than RSA-2048's 256 bytes)
- Private key: 2,400 bytes
- Ciphertext: 1,088 bytes
- Shared secret: 32 bytes (same as ECDH!)

The shared secret is the same size as classical — only the keys are larger. This means ML-KEM can be a DROP-IN replacement for ECDH in most protocols!

**Security Proof Overview:**
ML-KEM security reduces to the hardness of Module-LWE. Specifically:
- Given (A, b = As + e) where A is a random matrix, s is the secret, e is small error
- Finding s given (A, b) is the MLWE problem
- No quantum algorithm achieves better than 2^128 operations for ML-KEM-768

**Get Ready to Play:**
In PQC Python Lab, you'll run real liboqs code in the browser, generate actual ML-KEM and ML-DSA keys, and complete coding challenges with an AI tutor that guides you through the implementation!
            """,
            "check": "Ask students: Write pseudocode for a complete ML-KEM key exchange between Alice and Bob. Identify what each party keeps private and what they share publicly."
        },
        {
            "title": "🛡️ Lesson 4: Threat Modeling — What Are We Actually Protecting Against?",
            "game": "🛡️ Harvest Now Decrypt Later Timeline",
            "time": "12 minutes",
            "objective": "Students will be able to conduct a basic quantum threat assessment for an organization and recommend appropriate PQC migration strategies.",
            "vocab": [
                ("Threat Model", "A structured analysis of WHO might attack a system, WHAT they want, HOW they might attack, and what the IMPACT would be. Every security decision should start with a threat model."),
                ("Attack Vector", "The method or pathway an attacker uses to gain unauthorized access. For quantum threats: (1) Break key exchange to read traffic, (2) Forge signatures to impersonate, (3) Break encryption on stored data via HNDL."),
                ("Nation-State Actor", "A hacking group funded and operated by a government. APT40 (China), Cozy Bear (Russia), Equation Group (NSA) are known examples. Nation-states have the RESOURCES to build CRQCs and the MOTIVATION to store encrypted traffic now."),
                ("Zero-Day", "A previously unknown vulnerability exploited before a patch exists. Quantum computers will effectively create zero-days for ALL RSA and ECC implementations simultaneously."),
                ("Defense in Depth", "A security strategy using MULTIPLE layers of protection. If one layer fails, others remain. For PQC: use HYBRID cryptography (classical + quantum-safe) during migration so you're safe against both classical AND quantum attacks."),
                ("Cryptographic Agility", "Designing systems so that cryptographic algorithms can be SWAPPED OUT without redesigning the entire system. Critical for PQC migration — if your code is crypto-agile, migrating from RSA to ML-KEM is straightforward."),
                ("Risk Assessment", "Evaluating the likelihood of an attack × the impact if successful. High-sensitivity data (medical, financial, government) with long retention periods has HIGHEST quantum risk."),
            ],
            "lesson": """
**🎯 Big Idea:** Quantum risk is not uniform — some organizations are at critical risk NOW while others have years to migrate. Threat modeling determines urgency.

**The Quantum Risk Framework:**
Risk = Data Sensitivity × Retention Period × Time to CRQC × Migration Complexity

**High Risk (Migrate NOW):**
- Government and military communications
- Healthcare records (HIPAA mandates 6+ year retention)
- Financial transaction records
- Intellectual property and trade secrets

**Medium Risk (Migrate by 2027):**
- Corporate communications
- Employee personal data
- Customer databases
- Code signing infrastructure

**Lower Risk (Migrate by 2030):**
- Short-lived session keys (these are safe — data has no value after the session)
- Public information with no confidentiality requirement
- Ephemeral communications

**The HNDL Calculation:**
Ask: "Will this data still be sensitive in [CRQC arrival year - current year] years?"
- Medical record from 2024 → still sensitive in 2034? ✅ YES → HIGH RISK
- Session token from 2024 → still sensitive in 2034? ❌ NO → LOW RISK
- Military strategy document → sensitive for 50+ years → CRITICAL RISK

**Migration Complexity Factors:**
1. **Protocol depth**: Is crypto embedded deep in hardware? (High complexity)
2. **Key lifetime**: Long-lived keys need migration first
3. **Regulatory requirements**: HIPAA, FISMA, PCI-DSS all have different timelines
4. **Legacy systems**: Old industrial control systems may not support new key sizes
5. **Performance constraints**: IoT devices may need Falcon (smallest signatures) instead of ML-DSA

**Real Migration Playbook (NIST SP 800-208):**
1. INVENTORY: List all cryptographic primitives in your systems
2. PRIORITIZE: Rank by sensitivity × retention × exposure
3. TEST: Deploy hybrid cryptography in non-production first
4. MIGRATE: Roll out quantum-safe algorithms systematically
5. VERIFY: Cryptographic agility testing post-migration
6. MONITOR: Watch for new cryptanalysis of PQC algorithms

**The Human Factor:**
The biggest risk to PQC migration isn't technical — it's organizational. Most breaches happen because:
- Organizations don't know what cryptography they're using (no inventory)
- Budget allocated after a breach rather than before
- Legacy systems 20+ years old that can't be updated

Security professionals who understand PQC migration are among the highest-paid in cybersecurity right now. Starting salaries: $130,000-$180,000.
            """,
            "check": "Ask students: A hospital has patient records dating back to 2010, encrypted with RSA-2048. Write a one-paragraph threat assessment explaining their quantum risk and your recommended migration priority."
        },
    ]

    for i, lesson in enumerate(lessons):
        with st.expander(f"**{lesson['title']}** — Before: {lesson['game']} | ⏱️ {lesson['time']}", expanded=(i==0)):
            st.markdown(f"**🎮 Prepares you for:** {lesson['game']}")
            st.markdown(f"**⏱️ Time:** {lesson['time']}")
            st.markdown(f"**🎯 Learning Goal:** {lesson['objective']}")

            st.markdown("### 📖 Vocabulary — Master These Terms First!")
            for term, definition in lesson['vocab']:
                st.markdown(f"""
<div style='background:#071520;border-left:3px solid #ef4444;border-radius:6px;
padding:8px 12px;margin-bottom:6px;'>
<b style='color:#ef4444'>{term}</b><br>
<span style='color:#94a3b8;font-size:14px'>{definition}</span>
</div>""", unsafe_allow_html=True)

            st.markdown("### 📝 Lesson")
            st.markdown(lesson['lesson'])

            st.markdown(f"""
<div style='background:#052e16;border:1px solid #10b981;border-radius:8px;padding:10px;margin-top:10px;'>
<b style='color:#10b981'>✅ Check for Understanding</b><br>
<span style='color:#94a3b8'>{lesson['check']}</span>
</div>""", unsafe_allow_html=True)
