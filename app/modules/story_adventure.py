import streamlit as st
import random

HEROES = [
    {"name": "Captain Kyber",     "emoji": "🔐", "power": "magic key exchange",     "fips": "FIPS 203"},
    {"name": "Sir Dilithium",     "emoji": "✍️",  "power": "unbreakable signatures", "fips": "FIPS 204"},
    {"name": "Falcon",            "emoji": "🦅", "power": "tiny magic shields",      "fips": "FIPS 206"},
    {"name": "Rainbow Shield",    "emoji": "🌲", "power": "hash tree protection",    "fips": "FIPS 205"},
    {"name": "Crystal Guardian",  "emoji": "💎", "power": "lattice crystal armor",   "fips": "FIPS 203"},
    {"name": "Lady Sphincs",      "emoji": "🌈", "power": "rainbow hash magic",      "fips": "FIPS 205"},
]

MONSTERS = [
    {"name": "The Password Gobbler",    "emoji": "👾", "fear": "strong encryption"},
    {"name": "The Sneaky Hacker Bot",   "emoji": "🤖", "fear": "digital signatures"},
    {"name": "The Quantum Blob",        "emoji": "🌀", "fear": "post-quantum math"},
    {"name": "The Cookie Monster Virus","emoji": "🍪", "fear": "secure connections"},
    {"name": "The Data Thief Dragon",   "emoji": "🐉", "fear": "lattice shields"},
    {"name": "The Shor Monster",        "emoji": "💀", "fear": "Kyber key exchange"},
]

BADGES = {
    1:  {"name": "First Story!",   "emoji": "⭐"},
    3:  {"name": "Story Explorer", "emoji": "🌟"},
    5:  {"name": "Crypto Reader",  "emoji": "📚"},
    10: {"name": "PQC Hero",       "emoji": "🏆"},
}

PUZZLES = [
    {
        "q": "What does a magic KEY do in cryptography?",
        "opts": ["Opens treasure chests (locks/unlocks data)", "Makes cookies", "Flies in the sky", "Plays music"],
        "ans": 0,
        "fact": "Encryption keys lock and unlock data — just like Captain Kyber uses magic keys to protect treasure chests!"
    },
    {
        "q": "What is a DIGITAL SIGNATURE used for?",
        "opts": ["Drawing pictures", "Proving a message is really from YOU", "Sending emails faster", "Making passwords"],
        "ans": 1,
        "fact": "Sir Dilithium's unbreakable signature proves a message really came from you and nobody changed it!"
    },
    {
        "q": "Why do we need POST-QUANTUM cryptography?",
        "opts": ["Because it sounds cool", "Because quantum computers could break old codes", "Because monsters are real", "Because keys are pretty"],
        "ans": 1,
        "fact": "Quantum computers are coming! They could break old encryption. That is why we need Kyber, Dilithium, Falcon and SPHINCS+!"
    },
    {
        "q": "What does KYBER protect?",
        "opts": ["Pizza recipes", "Secret keys shared between computers", "Dragon eggs", "Cookie jars"],
        "ans": 1,
        "fact": "Kyber (FIPS 203) protects the secret keys that computers share when you visit a website!"
    },
    {
        "q": "Which hero makes the SMALLEST shields?",
        "opts": ["Captain Kyber", "Sir Dilithium", "Falcon", "Rainbow Shield"],
        "ans": 2,
        "fact": "Falcon (FIPS 206) makes the smallest signatures of all 4 NIST heroes — perfect for tiny smart devices!"
    },
]

FALLBACK_STORIES = [
    {
        "hero": "Captain Kyber",
        "monster": "The Password Gobbler",
        "story": """# Captain Kyber and the Password Gobbler! 🔐

Once upon a time in the magical land of Cryptopia, a hungry monster called **The Password Gobbler** 👾 was eating everyone's secret passwords!

CHOMP! There goes Bobby's password!
GULP! There goes Sally's password!

Everyone was scared. But then... WHOOSH! ✨

**Captain Kyber** 🔐 flew in wearing shiny blue armor!

"Don't worry!" said Captain Kyber. "I have a special magic called **Key Exchange**! Instead of passwords, I'll give everyone a magic key that even the Gobbler can't eat!"

Captain Kyber waved a magic wand and created two keys — one public, one secret. The Gobbler tried to grab them... but the math was TOO HARD! 🧮

"I can't eat this!" cried the Gobbler. "The numbers are impossible!"

The Gobbler decided to go back to school and learn about protecting secrets instead.

And everyone's passwords were safe forever after! 🎉

*The End* 🌟

**What we learned:** Captain Kyber (FIPS 203) uses special math called Module-LWE to keep secrets safe!"""
    },
    {
        "hero": "Sir Dilithium",
        "monster": "The Sneaky Hacker Bot",
        "story": """# Sir Dilithium Saves the Secret Treehouse! ✍️

Deep in the Quantum Forest, **The Sneaky Hacker Bot** 🤖 was sending fake messages to trick everyone!

"I am the Queen! Give me all the treasure!" said a fake message.
But the Queen never wrote that! 😱

Then **Sir Dilithium** ✍️ arrived with a magical quill!

"I will sign every message with my UNBREAKABLE signature!" said Sir Dilithium.

He signed the real messages with special lattice magic. Now everyone could check — is this really from the Queen?

The Hacker Bot tried to copy the signature... BZZT! ERROR! The math was impossible! 🚫

"I cannot fake this!" cried the Bot. "The signature is unbreakable!"

The Hacker Bot decided to use its powers for good instead.

Now all messages in the forest are signed and safe! ✅

*The End* 🌟

**What we learned:** Sir Dilithium (FIPS 204) creates digital signatures that nobody can fake!"""
    },
]

def get_fallback_story(hero_name, monster_name):
    for s in FALLBACK_STORIES:
        if s["hero"] == hero_name:
            return s["story"]
    h = next((h for h in HEROES if h["name"] == hero_name), HEROES[0])
    m = next((mo for mo in MONSTERS if mo["name"] == monster_name), MONSTERS[0])
    return (
        "# " + h["name"] + " Saves the Day! " + h["emoji"] + "\n\n"
        "Once upon a time, " + h["emoji"] + " **" + h["name"] + "** heard that "
        + m["emoji"] + " **" + m["name"] + "** was trying to steal everyone's secret treasure!\n\n"
        "**" + h["name"] + "** used their magical power of " + h["power"] + " to protect everyone.\n\n"
        "The monster tried and tried but could not break through the post-quantum shield!\n\n"
        "**" + m["name"] + "** said: 'I give up! I will learn to protect secrets too!'\n\n"
        "Everyone celebrated and learned about **" + h["fips"] + "** — "
        "the real magic that keeps our data safe!\n\n"
        "*The End* 🌟\n\n"
        "**What we learned:** " + h["name"] + " (" + h["fips"] + ") uses " + h["power"] + " to protect us!"
    )


def render_storybook(story_text, hero_emoji, monster_emoji):
    """Interactive fairy tale storybook with SVG illustrations, page turning, animations."""
    import streamlit.components.v1 as components

    clean = (story_text
             .replace('\\', '\\\\')
             .replace('\r', '')
             .replace('"', "'")
             .replace('`', "'")
             .replace('\n', '<br>')
    )

    html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:transparent;font-family:Georgia,'Times New Roman',serif;
     overflow:hidden;user-select:none;}

#wrap{display:flex;flex-direction:column;align-items:center;padding:10px 6px;}

/* ── BOOK ── */
#book{
    display:flex;width:100%;max-width:700px;
    filter:drop-shadow(0 10px 24px rgba(0,0,0,0.4));
}

/* ── PAGES ── */
.page{
    flex:1;position:relative;overflow:hidden;
    min-height:400px;
}
#page-1{
    background:linear-gradient(108deg,#f0ddb0,#fdf3e3 40%,#fdf8f0);
    border-radius:8px 0 0 8px;
    border:1.5px solid #c4a35a;border-right:none;
    display:flex;flex-direction:column;
}
#page-2{
    background:linear-gradient(252deg,#f0ddb0,#fdf3e3 40%,#fdf8f0);
    border-radius:0 8px 8px 0;
    border:1.5px solid #c4a35a;border-left:none;
    display:flex;flex-direction:column;
}
.page::before{
    content:'';position:absolute;inset:7px;
    border:1.5px solid #c4a35a40;border-radius:4px;pointer-events:none;z-index:2;
}

/* ── SPINE ── */
#spine{
    width:20px;flex-shrink:0;
    background:linear-gradient(to bottom,#7a5c10,#c4a35a 25%,#f5d278 50%,#c4a35a 75%,#7a5c10);
    box-shadow:inset -2px 0 6px rgba(0,0,0,0.3),inset 2px 0 6px rgba(0,0,0,0.3);
}

/* ── ILLUSTRATION PANEL ── */
.illus-wrap{
    width:100%;height:160px;overflow:hidden;
    border-bottom:1.5px solid #c4a35a50;
    position:relative;flex-shrink:0;
}
.illus-wrap svg{width:100%;height:100%;}

/* ── PAGE CONTENT ── */
.page-content{
    padding:10px 16px 36px 16px;flex:1;overflow:hidden;
}
.pg-num{
    text-align:center;font-size:10px;color:#8b6914;
    font-style:italic;letter-spacing:1px;margin-bottom:3px;
}
.stars-row{
    text-align:center;font-size:11px;margin-bottom:4px;letter-spacing:4px;
}
.star{cursor:pointer;display:inline-block;color:#c4a35a;
    transition:transform 0.2s,filter 0.2s;}
.star:hover,.star.lit{color:#fbbf24;
    filter:drop-shadow(0 0 5px #fbbf24);transform:scale(1.4) rotate(15deg);}
.ch-title{
    text-align:center;font-size:13px;font-weight:bold;
    color:#5c3d0e;line-height:1.4;margin-bottom:4px;
}
.ornament{text-align:center;color:#8b6914;font-size:12px;
    letter-spacing:3px;margin:3px 0;}
.story-body{
    font-size:12.5px;line-height:1.8;color:#2c1810;text-align:justify;
}
.drop-cap{
    float:left;font-size:40px;line-height:0.75;
    padding-right:4px;padding-top:5px;color:#8b6914;font-weight:bold;
}
.end-orn{
    text-align:center;color:#8b6914;font-size:11px;
    letter-spacing:3px;margin-top:8px;display:none;
}

/* ── CONTROLS ── */
#controls{
    display:flex;justify-content:space-between;align-items:center;
    width:100%;max-width:700px;margin-top:8px;gap:6px;
}
.nav-btn{
    padding:7px 16px;border-radius:20px;border:2px solid #c4a35a;
    background:linear-gradient(135deg,#8b6914,#c4a35a);
    color:#fdf3e3;font-size:12px;font-weight:bold;cursor:pointer;
    font-family:Georgia,serif;box-shadow:0 3px 8px rgba(0,0,0,0.2);
    transition:all 0.15s;
}
.nav-btn:hover{transform:translateY(-2px);filter:brightness(1.15);}
.nav-btn:disabled{opacity:0.3;cursor:not-allowed;transform:none;}
#read-btn{
    padding:7px 14px;border-radius:20px;border:2px solid #3b82f6;
    background:linear-gradient(135deg,#1d4ed8,#3b82f6);
    color:white;font-size:11px;cursor:pointer;font-family:Georgia,serif;
    transition:all 0.15s;
}
#read-btn:hover{transform:translateY(-2px);filter:brightness(1.15);}
#page-indicator{font-size:10px;color:#8b6914;font-style:italic;text-align:center;}

/* ── ANIMATIONS ── */
.page.flip-out{animation:flipOut 0.25s ease forwards;}
.page.flip-in{animation:flipIn 0.25s ease forwards;}
@keyframes flipOut{0%{opacity:1;}100%{opacity:0;transform:perspective(600px) rotateY(-12deg);}}
@keyframes flipIn{0%{opacity:0;transform:perspective(600px) rotateY(12deg);}100%{opacity:1;}}

.sparkle{position:fixed;pointer-events:none;z-index:9999;font-size:13px;
    animation:spkl 0.75s ease forwards;}
@keyframes spkl{
    0%{opacity:1;transform:scale(1) translate(0,0);}
    100%{opacity:0;transform:scale(0) translate(var(--tx),var(--ty));}}

.trail{position:fixed;pointer-events:none;z-index:9998;
    width:5px;height:5px;border-radius:50%;animation:trailF 0.55s ease forwards;}
@keyframes trailF{0%{opacity:0.85;}100%{opacity:0;transform:scale(0);}}

/* ── CLOUD ANIMATION ── */
@keyframes driftCloud{0%{transform:translateX(-80px);}100%{transform:translateX(120%);}}
@keyframes floatHero{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
@keyframes twinkle{0%,100%{opacity:1;}50%{opacity:0.2;}}
@keyframes monsterShake{0%,100%{transform:translateX(0);}25%{transform:translateX(-4px);}75%{transform:translateX(4px);}}
</style>
</head>
<body>
<div id="wrap">

  <div id="book">
    <!-- LEFT PAGE -->
    <div class="page" id="page-1">
      <div class="illus-wrap" id="illus-1"></div>
      <div class="page-content">
        <div class="pg-num" id="pg-num-1">~ Page 1 ~</div>
        <div class="stars-row">
          <span class="star" onclick="litStar(this)">✦</span>
          <span class="star" onclick="litStar(this)">✦</span>
          <span class="star" onclick="litStar(this)">✦</span>
        </div>
        <div class="ch-title" id="ch-title">📖 Loading...</div>
        <div class="ornament">~ ❧ ~</div>
        <div class="story-body" id="body-1"></div>
        <div class="end-orn" id="end-1"></div>
      </div>
    </div>

    <div id="spine"></div>

    <!-- RIGHT PAGE -->
    <div class="page" id="page-2">
      <div class="illus-wrap" id="illus-2"></div>
      <div class="page-content">
        <div class="pg-num" id="pg-num-2">~ Page 2 ~</div>
        <div class="stars-row">
          <span class="star" onclick="litStar(this)">✦</span>
          <span class="star" onclick="litStar(this)">✦</span>
          <span class="star" onclick="litStar(this)">✦</span>
        </div>
        <div class="story-body" id="body-2"></div>
        <div class="end-orn" id="end-2"></div>
      </div>
    </div>
  </div>

  <div id="controls">
    <button class="nav-btn" id="prev-btn" onclick="prevPage()" disabled>◀ Prev</button>
    <div style="display:flex;flex-direction:column;align-items:center;gap:3px;">
      <div id="page-indicator">Page 1 of 1</div>
      <button id="read-btn" onclick="readPage()">🔊 Read Aloud</button>
    </div>
    <button class="nav-btn" id="next-btn" onclick="nextPage()">Next ▶</button>
  </div>
</div>

<script>
var HERO = '""" + hero_emoji + """';
var MONSTER = '""" + monster_emoji + """';
var RAW = \"""" + clean + """\";

// ── SVG SCENES ───────────────────────────────────────────────────────────────
// Each scene is a full SVG illustration for a page spread
// Scene 0: Opening — hero and monster meet in magical forest
// Scene 1: Battle — hero uses power against monster
// Scene 2: Resolution — everyone celebrates together

function makeScene(type){
    if(type===0) return sceneForest();
    if(type===1) return sceneBattle();
    return sceneCelebrate();
}

function sceneForest(){
    return `<svg viewBox="0 0 340 160" xmlns="http://www.w3.org/2000/svg">
    <!-- Sky gradient -->
    <defs>
        <linearGradient id="sky0" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#1e3a5f"/>
            <stop offset="100%" stop-color="#3b82f6"/>
        </linearGradient>
        <linearGradient id="ground0" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#166534"/>
            <stop offset="100%" stop-color="#14532d"/>
        </linearGradient>
    </defs>
    <!-- Sky -->
    <rect width="340" height="160" fill="url(#sky0)"/>
    <!-- Stars -->
    <circle cx="30" cy="15" r="1.5" fill="white" opacity="0.9" style="animation:twinkle 1.5s infinite"/>
    <circle cx="80" cy="10" r="1" fill="white" opacity="0.8" style="animation:twinkle 2s infinite 0.3s"/>
    <circle cx="140" cy="20" r="1.5" fill="white" opacity="0.9" style="animation:twinkle 1.8s infinite 0.6s"/>
    <circle cx="200" cy="8" r="1" fill="white" opacity="0.7" style="animation:twinkle 2.2s infinite 0.1s"/>
    <circle cx="260" cy="18" r="1.5" fill="white" opacity="0.9" style="animation:twinkle 1.6s infinite 0.4s"/>
    <circle cx="310" cy="12" r="1" fill="white" opacity="0.8" style="animation:twinkle 1.9s infinite 0.7s"/>
    <!-- Moon -->
    <circle cx="290" cy="30" r="18" fill="#fef3c7" opacity="0.95"/>
    <circle cx="298" cy="24" r="13" fill="#3b82f6" opacity="0.9"/>
    <!-- Clouds -->
    <g style="animation:driftCloud 18s linear infinite">
        <ellipse cx="60" cy="40" rx="30" ry="12" fill="white" opacity="0.2"/>
        <ellipse cx="80" cy="34" rx="20" ry="10" fill="white" opacity="0.25"/>
    </g>
    <g style="animation:driftCloud 24s linear infinite 8s">
        <ellipse cx="180" cy="30" rx="25" ry="10" fill="white" opacity="0.18"/>
        <ellipse cx="200" cy="25" rx="18" ry="8" fill="white" opacity="0.22"/>
    </g>
    <!-- Ground -->
    <rect y="120" width="340" height="40" fill="url(#ground0)"/>
    <!-- Grass tufts -->
    <path d="M0,120 Q10,110 20,120 Q30,110 40,120 Q50,110 60,120 Q70,110 80,120 Q90,110 100,120 Q110,110 120,120 Q130,110 140,120 Q150,110 160,120 Q170,110 180,120 Q190,110 200,120 Q210,110 220,120 Q230,110 240,120 Q250,110 260,120 Q270,110 280,120 Q290,110 300,120 Q310,110 320,120 Q330,110 340,120" fill="#15803d" opacity="0.8"/>
    <!-- Trees left -->
    <rect x="20" y="70" width="8" height="55" fill="#854d0e"/>
    <ellipse cx="24" cy="65" rx="20" ry="28" fill="#166534"/>
    <ellipse cx="24" cy="55" rx="14" ry="20" fill="#15803d"/>
    <!-- Trees right -->
    <rect x="290" y="75" width="8" height="50" fill="#854d0e"/>
    <ellipse cx="294" cy="70" rx="20" ry="26" fill="#166534"/>
    <ellipse cx="294" cy="58" rx="14" ry="18" fill="#15803d"/>
    <!-- Castle in background -->
    <rect x="145" y="55" width="50" height="55" fill="#1e3a5f" opacity="0.7"/>
    <rect x="140" y="45" width="14" height="30" fill="#1e3a5f" opacity="0.7"/>
    <rect x="186" y="45" width="14" height="30" fill="#1e3a5f" opacity="0.7"/>
    <rect x="155" y="40" width="30" height="15" fill="#1d4ed8" opacity="0.5"/>
    <!-- Battlements -->
    <rect x="140" y="38" width="5" height="7" fill="#1e3a5f" opacity="0.7"/>
    <rect x="148" y="38" width="5" height="7" fill="#1e3a5f" opacity="0.7"/>
    <rect x="186" y="38" width="5" height="7" fill="#1e3a5f" opacity="0.7"/>
    <rect x="194" y="38" width="5" height="7" fill="#1e3a5f" opacity="0.7"/>
    <!-- Castle window glow -->
    <rect x="160" y="65" width="12" height="16" rx="6" fill="#fbbf24" opacity="0.6"/>
    <!-- Path -->
    <ellipse cx="170" cy="138" rx="60" ry="8" fill="#854d0e" opacity="0.4"/>
    <!-- Hero character -->
    <text x="105" y="118" font-size="28" text-anchor="middle"
        style="animation:floatHero 2.5s ease-in-out infinite">` + HERO + `</text>
    <!-- Monster character -->
    <text x="240" y="118" font-size="28" text-anchor="middle"
        style="animation:monsterShake 3s ease-in-out infinite">` + MONSTER + `</text>
    <!-- Magic sparkles between them -->
    <circle cx="170" cy="105" r="3" fill="#fbbf24" opacity="0.8" style="animation:twinkle 0.8s infinite"/>
    <circle cx="175" cy="95" r="2" fill="#60a5fa" opacity="0.9" style="animation:twinkle 1.2s infinite 0.2s"/>
    <circle cx="165" cy="100" r="2" fill="#10b981" opacity="0.8" style="animation:twinkle 1s infinite 0.4s"/>
    </svg>`;
}

function sceneBattle(){
    return `<svg viewBox="0 0 340 160" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <radialGradient id="glow1" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.8"/>
            <stop offset="100%" stop-color="#1d4ed8" stop-opacity="0"/>
        </radialGradient>
        <linearGradient id="bgBattle" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#0f172a"/>
            <stop offset="100%" stop-color="#1e3a5f"/>
        </linearGradient>
    </defs>
    <!-- Dark dramatic sky -->
    <rect width="340" height="160" fill="url(#bgBattle)"/>
    <!-- Magic glow center -->
    <ellipse cx="170" cy="90" rx="90" ry="60" fill="url(#glow1)" opacity="0.5"/>
    <!-- Lightning bolts -->
    <path d="M130,20 L120,55 L135,55 L125,90" stroke="#fbbf24" stroke-width="3" fill="none" opacity="0.8"/>
    <path d="M210,15 L200,50 L215,50 L205,85" stroke="#60a5fa" stroke-width="3" fill="none" opacity="0.8"/>
    <!-- Stars -->
    <circle cx="40" cy="20" r="1.5" fill="white" opacity="0.7" style="animation:twinkle 1.2s infinite"/>
    <circle cx="290" cy="15" r="1.5" fill="white" opacity="0.7" style="animation:twinkle 1.8s infinite 0.5s"/>
    <circle cx="60" cy="45" r="1" fill="white" opacity="0.5" style="animation:twinkle 2s infinite 0.3s"/>
    <circle cx="300" cy="40" r="1" fill="white" opacity="0.5" style="animation:twinkle 1.6s infinite 0.7s"/>
    <!-- Ground -->
    <rect y="125" width="340" height="35" fill="#0f2040"/>
    <path d="M0,125 Q20,118 40,125 Q60,118 80,125 Q100,118 120,125 Q140,118 160,125 Q180,118 200,125 Q220,118 240,125 Q260,118 280,125 Q300,118 320,125 Q330,118 340,125" fill="#1e3a5f"/>
    <!-- Magic shield bubble from hero -->
    <ellipse cx="135" cy="105" rx="38" ry="32" fill="none" stroke="#10b981" stroke-width="2"
        opacity="0.6" style="animation:twinkle 1s infinite"/>
    <ellipse cx="135" cy="105" rx="32" ry="26" fill="#10b98115" stroke="#10b981" stroke-width="1"
        opacity="0.4"/>
    <!-- Lattice grid inside shield -->
    <line x1="105" y1="90" x2="165" y2="90" stroke="#10b981" stroke-width="0.5" opacity="0.4"/>
    <line x1="105" y1="100" x2="165" y2="100" stroke="#10b981" stroke-width="0.5" opacity="0.4"/>
    <line x1="105" y1="110" x2="165" y2="110" stroke="#10b981" stroke-width="0.5" opacity="0.4"/>
    <line x1="120" y1="78" x2="120" y2="128" stroke="#10b981" stroke-width="0.5" opacity="0.4"/>
    <line x1="135" y1="75" x2="135" y2="133" stroke="#10b981" stroke-width="0.5" opacity="0.4"/>
    <line x1="150" y1="78" x2="150" y2="128" stroke="#10b981" stroke-width="0.5" opacity="0.4"/>
    <!-- Hero with glow -->
    <circle cx="115" cy="108" r="26" fill="#10b98120"/>
    <text x="115" y="120" font-size="30" text-anchor="middle"
        style="animation:floatHero 1.8s ease-in-out infinite">` + HERO + `</text>
    <!-- Monster recoiling -->
    <text x="230" y="122" font-size="30" text-anchor="middle"
        style="animation:monsterShake 0.5s ease-in-out infinite">` + MONSTER + `</text>
    <!-- Monster sweat drops -->
    <circle cx="215" cy="98" r="3" fill="#60a5fa" opacity="0.7"/>
    <circle cx="208" cy="107" r="2" fill="#60a5fa" opacity="0.6"/>
    <!-- Magic particles between them -->
    <circle cx="175" cy="95" r="4" fill="#fbbf24" opacity="0.9" style="animation:twinkle 0.6s infinite"/>
    <circle cx="185" cy="105" r="3" fill="#10b981" opacity="0.8" style="animation:twinkle 0.8s infinite 0.2s"/>
    <circle cx="178" cy="115" r="3" fill="#f97316" opacity="0.8" style="animation:twinkle 0.7s infinite 0.4s"/>
    <circle cx="190" cy="95" r="2" fill="#a78bfa" opacity="0.9" style="animation:twinkle 0.9s infinite 0.1s"/>
    <!-- FIPS label -->
    <rect x="10" y="10" width="80" height="16" rx="4" fill="#10b981" opacity="0.8"/>
    <text x="50" y="22" font-size="9" fill="white" text-anchor="middle" font-family="monospace">FIPS 203/204/205/206</text>
    </svg>`;
}

function sceneCelebrate(){
    return `<svg viewBox="0 0 340 160" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="sunriseBg" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.3"/>
            <stop offset="40%" stop-color="#f97316" stop-opacity="0.2"/>
            <stop offset="100%" stop-color="#166534"/>
        </linearGradient>
        <radialGradient id="sunGlow" cx="50%" cy="0%" r="60%">
            <stop offset="0%" stop-color="#fde68a" stop-opacity="0.9"/>
            <stop offset="100%" stop-color="#fbbf24" stop-opacity="0"/>
        </radialGradient>
    </defs>
    <!-- Happy sunrise sky -->
    <rect width="340" height="160" fill="#1e3a5f"/>
    <rect width="340" height="160" fill="url(#sunriseBg)"/>
    <!-- Sun rays -->
    <circle cx="170" cy="0" r="60" fill="url(#sunGlow)"/>
    <circle cx="170" cy="0" r="28" fill="#fde68a" opacity="0.9"/>
    <!-- Rainbow arc -->
    <path d="M20,100 Q170,-20 320,100" fill="none" stroke="#ef4444" stroke-width="4" opacity="0.6"/>
    <path d="M28,104 Q170,-10 312,104" fill="none" stroke="#f97316" stroke-width="4" opacity="0.6"/>
    <path d="M36,108 Q170,0 304,108" fill="none" stroke="#fbbf24" stroke-width="4" opacity="0.6"/>
    <path d="M44,112 Q170,10 296,112" fill="none" stroke="#10b981" stroke-width="4" opacity="0.6"/>
    <path d="M52,116 Q170,20 288,116" fill="none" stroke="#3b82f6" stroke-width="4" opacity="0.6"/>
    <path d="M60,120 Q170,30 280,120" fill="none" stroke="#8b5cf6" stroke-width="4" opacity="0.6"/>
    <!-- Happy clouds -->
    <ellipse cx="60" cy="50" rx="30" ry="14" fill="white" opacity="0.7"/>
    <ellipse cx="75" cy="42" rx="22" ry="12" fill="white" opacity="0.8"/>
    <ellipse cx="280" cy="45" rx="28" ry="12" fill="white" opacity="0.7"/>
    <ellipse cx="295" cy="37" rx="20" ry="11" fill="white" opacity="0.8"/>
    <!-- Ground -->
    <rect y="125" width="340" height="35" fill="#166534"/>
    <path d="M0,125 Q10,115 20,125 Q30,115 40,125 Q50,115 60,125 Q70,115 80,125 Q90,115 100,125 Q110,115 120,125 Q130,115 140,125 Q150,115 160,125 Q170,115 180,125 Q190,115 200,125 Q210,115 220,125 Q230,115 240,125 Q250,115 260,125 Q270,115 280,125 Q290,115 300,125 Q310,115 320,125 Q330,115 340,125" fill="#15803d"/>
    <!-- Flowers -->
    <circle cx="50" cy="124" r="4" fill="#f97316"/>
    <circle cx="100" cy="122" r="3" fill="#ef4444"/>
    <circle cx="240" cy="124" r="4" fill="#fbbf24"/>
    <circle cx="290" cy="122" r="3" fill="#f97316"/>
    <!-- Confetti falling -->
    <rect x="80" y="30" width="6" height="4" rx="1" fill="#ef4444" opacity="0.8" style="animation:floatHero 1.5s infinite"/>
    <rect x="150" y="20" width="5" height="4" rx="1" fill="#3b82f6" opacity="0.8" style="animation:floatHero 2s infinite 0.3s"/>
    <rect x="220" y="35" width="6" height="4" rx="1" fill="#10b981" opacity="0.8" style="animation:floatHero 1.8s infinite 0.6s"/>
    <rect x="260" y="25" width="5" height="3" rx="1" fill="#fbbf24" opacity="0.8" style="animation:floatHero 1.6s infinite 0.2s"/>
    <rect x="120" y="40" width="4" height="4" rx="1" fill="#a78bfa" opacity="0.8" style="animation:floatHero 2.2s infinite 0.8s"/>
    <!-- Hero and Monster together happily -->
    <text x="130" y="122" font-size="32" text-anchor="middle"
        style="animation:floatHero 2s ease-in-out infinite">` + HERO + `</text>
    <text x="210" y="122" font-size="32" text-anchor="middle"
        style="animation:floatHero 2s ease-in-out infinite 0.5s">` + MONSTER + `</text>
    <!-- Stars and sparkles -->
    <text x="165" y="108" font-size="14" text-anchor="middle" style="animation:twinkle 1s infinite">⭐</text>
    <text x="85" y="95" font-size="12" style="animation:twinkle 1.4s infinite 0.3s">✨</text>
    <text x="258" y="90" font-size="12" style="animation:twinkle 1.2s infinite 0.6s">✨</text>
    <!-- NIST badges -->
    <rect x="8" y="8" width="55" height="14" rx="3" fill="#10b981" opacity="0.85"/>
    <text x="35" y="19" font-size="8" fill="white" text-anchor="middle" font-family="monospace">FIPS 203-206</text>
    <rect x="277" y="8" width="55" height="14" rx="3" fill="#3b82f6" opacity="0.85"/>
    <text x="304" y="19" font-size="8" fill="white" text-anchor="middle" font-family="monospace">Quantum Safe!</text>
    </svg>`;
}

// ── STORY PARSING ────────────────────────────────────────────────────────────
function parseStory(text){
    var lines = text.split('<br>').map(function(l){return l.trim();}).filter(Boolean);
    var title='', paras=[];
    lines.forEach(function(l){
        if(l.match(/^#+/)) title=l.replace(/^#+/,'').replace(/[*_]/g,'').trim();
        else paras.push(l);
    });
    return {title:title||'A Quantum Adventure', paras:paras};
}

var parsed=parseStory(RAW);
var TITLE=parsed.title;
var PARAS=parsed.paras;
var CHUNK=3;
var SPREADS=[];
for(var i=0;i<PARAS.length;i+=CHUNK) SPREADS.push(PARAS.slice(i,i+CHUNK));
if(!SPREADS.length) SPREADS.push(['Once upon a time...']);
var cur=0;

// ── RENDER SPREAD ────────────────────────────────────────────────────────────
function renderSpread(){
    var spread=SPREADS[cur];
    var mid=Math.ceil(spread.length/2);
    var left=spread.slice(0,mid);
    var right=spread.slice(mid);

    // Pick scene based on spread position
    var total=SPREADS.length;
    var sceneIdx = cur===0?0:(cur>=total-1?2:1);

    // Left illustration
    document.getElementById('illus-1').innerHTML=makeScene(sceneIdx);
    // Right illustration — next scene or same
    var sceneIdx2=cur>=total-1?2:(sceneIdx===0?1:sceneIdx);
    document.getElementById('illus-2').innerHTML=makeScene(sceneIdx2);

    // Title on first spread
    document.getElementById('ch-title').textContent=TITLE;

    // Build HTML
    var lHTML='';
    left.forEach(function(p,i){
        if(i===0&&cur===0&&p.length>0)
            lHTML+='<span class="drop-cap">'+p[0]+'</span>'+p.slice(1)+'<br><br>';
        else lHTML+=p+'<br><br>';
    });
    var rHTML='';
    right.forEach(function(p){ rHTML+=p+'<br><br>'; });

    // Animate
    var p1=document.getElementById('page-1');
    var p2=document.getElementById('page-2');
    p1.classList.add('flip-out');p2.classList.add('flip-out');
    setTimeout(function(){
        document.getElementById('body-1').innerHTML=lHTML;
        document.getElementById('body-2').innerHTML=rHTML;
        document.getElementById('pg-num-1').textContent='~ Page '+(cur*2+1)+' ~';
        document.getElementById('pg-num-2').textContent='~ Page '+(cur*2+2)+' ~';
        document.getElementById('page-indicator').textContent='Page '+(cur+1)+' of '+SPREADS.length;
        var last=cur===SPREADS.length-1;
        document.getElementById('end-1').style.display='none';
        document.getElementById('end-2').style.display=last?'block':'none';
        document.getElementById('end-2').textContent=last?'~ The End ✦ ~':'';
        p1.classList.remove('flip-out');p2.classList.remove('flip-out');
        p1.classList.add('flip-in');p2.classList.add('flip-in');
        setTimeout(function(){p1.classList.remove('flip-in');p2.classList.remove('flip-in');},280);
    },240);

    document.getElementById('prev-btn').disabled=(cur===0);
    document.getElementById('next-btn').disabled=(cur===SPREADS.length-1);
}

// ── NAVIGATION ───────────────────────────────────────────────────────────────
function nextPage(){
    if(cur<SPREADS.length-1){cur++;renderSpread();spawnSparkles(window.innerWidth/2,200,8);}
}
function prevPage(){
    if(cur>0){cur--;renderSpread();spawnSparkles(window.innerWidth/2,200,8);}
}

// ── READ ALOUD — Natural Human Storyteller Voice ────────────────────────────
var isReading = false;

function getBestVoice(){
    // What this does:
    // Gets all available voices from the browser
    // Tries each preferred voice name in order
    // Returns the first match found
    // Different devices have different voices available
    var voices = window.speechSynthesis.getVoices();
    var preferred = [
        'Samantha',
        'Moira',
        'Karen',
        'Fiona',
        'Victoria',
        'Allison',
        'Ava',
        'Serena',
        'Tessa',
        'Veena',
        'Zira',
        'Hazel',
        'Susan',
        'Google UK English Female',
        'Google US English',
        'Microsoft Zira',
        'Microsoft Hazel',
    ];
    for(var i=0;i<preferred.length;i++){
        for(var j=0;j<voices.length;j++){
            if(voices[j].name===preferred[i]) return voices[j];
        }
    }
    // Try partial match
    for(var j=0;j<voices.length;j++){
        var n=voices[j].name.toLowerCase();
        if(n.indexOf('female')!==-1||n.indexOf('woman')!==-1||
           n.indexOf('girl')!==-1||n.indexOf('samantha')!==-1||
           n.indexOf('karen')!==-1||n.indexOf('moira')!==-1)
            return voices[j];
    }
    // Last resort - any non-default voice
    for(var j=0;j<voices.length;j++){
        if(!voices[j].default) return voices[j];
    }
    return voices.length>0?voices[0]:null;
}

function preprocessText(text){
    // What this does:
    // Cleans up the text and adds natural pauses
    // by inserting commas and periods where humans
    // would naturally pause when telling a story
    return text
        .replace(/<br>/g,' ')
        .replace(/[*_#]/g,'')
        .replace(/\s+/g,' ')
        // Add breathing room after these words
        .replace(/(and then|but then|suddenly|meanwhile|finally|however|therefore)/gi,
            function(m){return m+', ';})
        // Make ellipsis into a real pause
        .replace(/\.\.\./g,'. ')
        // Clean up double spaces
        .replace(/\s+/g,' ')
        .trim();
}

function readPage(){
    // What this does:
    // Stops any current speech first
    // Preprocesses the text for natural delivery
    // Speaks sentence by sentence with pauses between
    // Updates button to show reading state
    window.speechSynthesis.cancel();
    isReading = true;

    var raw = preprocessText(SPREADS[cur].join(' '));

    // Split into sentences
    // What this does: regex matches text up to and including
    // a sentence-ending punctuation mark
    var sentences = raw.match(/[^.!?]+[.!?]*/g) || [raw];
    sentences = sentences.filter(function(s){return s.trim().length>2;});

    var btnEl = document.getElementById('read-btn');
    btnEl.textContent = '⏹ Stop';
    btnEl.onclick = stopReading;
    btnEl.style.background = 'linear-gradient(135deg,#dc2626,#ef4444)';

    var idx = 0;

    function speakNext(){
        if(!isReading || idx>=sentences.length){
            finishReading();
            return;
        }

        var sentence = sentences[idx].trim();
        idx++;
        if(!sentence){speakNext();return;}

        var utt = new SpeechSynthesisUtterance(sentence);

        // What this does:
        // Sets voice properties based on sentence type
        // Exciting sentences get faster rate and higher pitch
        // Slow sentences get lower rate for suspense
        var voice = getBestVoice();
        if(voice) utt.voice = voice;
        utt.volume = 1.0;
        utt.lang = 'en-US';

        var isExciting = /[!]/.test(sentence);
        var isQuestion = /[?]/.test(sentence);
        var isOpening = /once upon|long ago|far away/i.test(sentence);
        var isEnding = /the end|lived happily|ever after/i.test(sentence);
        var isSuspense = /suddenly|darkness|danger|beware|careful/i.test(sentence);

        if(isOpening){
            // Slow warm opening
            utt.rate = 0.72;
            utt.pitch = 0.95;
        } else if(isEnding){
            // Slow gentle ending
            utt.rate = 0.68;
            utt.pitch = 0.90;
        } else if(isExciting){
            // Fast exciting delivery
            utt.rate = 1.05;
            utt.pitch = 1.25;
        } else if(isQuestion){
            // Slightly slower with rising feel
            utt.rate = 0.82;
            utt.pitch = 1.15;
        } else if(isSuspense){
            // Slow dramatic suspense
            utt.rate = 0.70;
            utt.pitch = 0.88;
        } else {
            // Natural storytelling pace
            utt.rate = 0.82;
            utt.pitch = 1.05;
        }

        // What this does:
        // When each sentence finishes, waits a natural pause
        // then reads the next sentence
        // Pause length varies by punctuation type
        utt.onend = function(){
            if(!isReading) return;
            var pause = 180;
            if(isExciting) pause = 420;
            if(isQuestion) pause = 350;
            if(isEnding) pause = 600;
            if(isSuspense) pause = 500;
            setTimeout(speakNext, pause);
        };

        utt.onerror = function(){ setTimeout(speakNext, 100); };
        window.speechSynthesis.speak(utt);
    }

    // What this does:
    // Waits 150ms for browser voices to fully load
    // before starting to speak
    setTimeout(function(){
        window.speechSynthesis.getVoices();
        speakNext();
    }, 150);
}

function stopReading(){
    // What this does:
    // Cancels all pending speech
    // Resets button back to read aloud state
    isReading = false;
    window.speechSynthesis.cancel();
    finishReading();
}

function finishReading(){
    isReading = false;
    var btnEl = document.getElementById('read-btn');
    btnEl.textContent = '🔊 Read Aloud';
    btnEl.onclick = readPage;
    btnEl.style.background = 'linear-gradient(135deg,#1d4ed8,#3b82f6)';
}

// What this does:
// Pre-loads voices when page opens
// Some browsers need this call to populate the voice list
window.speechSynthesis.onvoiceschanged = function(){
    window.speechSynthesis.getVoices();
};


// ── STAR TAP ─────────────────────────────────────────────────────────────────
function litStar(el){
    el.classList.toggle('lit');
    var r=el.getBoundingClientRect();
    spawnSparkles(r.left+8,r.top+8,5);
}

// ── SPARKLES ─────────────────────────────────────────────────────────────────
var SPKL=['✨','⭐','🌟','💫','✦','★'];
function spawnSparkles(x,y,n){
    for(var i=0;i<n;i++){
        (function(){
            var el=document.createElement('div');
            el.className='sparkle';
            el.textContent=SPKL[Math.floor(Math.random()*SPKL.length)];
            var a=Math.random()*Math.PI*2;
            var d=30+Math.random()*55;
            el.style.left=x+'px';el.style.top=y+'px';
            el.style.setProperty('--tx',Math.cos(a)*d+'px');
            el.style.setProperty('--ty',Math.sin(a)*d+'px');
            el.style.animationDelay=(Math.random()*0.15)+'s';
            document.body.appendChild(el);
            setTimeout(function(){el.remove();},900);
        })();
    }
}

// ── CURSOR TRAIL ─────────────────────────────────────────────────────────────
var TCOLS=['#fbbf24','#60a5fa','#10b981','#f97316','#a78bfa'];
var tc=0;
document.addEventListener('mousemove',function(e){
    if(tc++%3!==0)return;
    var el=document.createElement('div');el.className='trail';
    el.style.left=e.clientX+'px';el.style.top=e.clientY+'px';
    el.style.background=TCOLS[Math.floor(Math.random()*TCOLS.length)];
    document.body.appendChild(el);
    setTimeout(function(){el.remove();},600);
});

// ── INIT ─────────────────────────────────────────────────────────────────────
renderSpread();
</script>
</body>
</html>
"""
    st.iframe(html_code, height=560, scrolling=False)



def render_story_adventure():
    """AI-powered interactive storybook for K-6 students."""

    if "story_badges" not in st.session_state:
        st.session_state.story_badges = []
    if "stories_read" not in st.session_state:
        st.session_state.stories_read = 0
    if "current_story" not in st.session_state:
        st.session_state.current_story = None
    if "story_puzzle_done" not in st.session_state:
        st.session_state.story_puzzle_done = False
    if "current_puzzle" not in st.session_state:
        st.session_state.current_puzzle = None

    # Header
    st.markdown(
        "<div style='text-align:center;padding:10px 0'>"
        "<div style='font-size:3.5rem'>🦸</div>"
        "<h2 style='color:#60a5fa;margin:4px 0'>Quantum Monster Adventures</h2>"
        "<p style='color:#94a3b8;font-size:13px'>AI-powered stories that teach real cryptography!</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # Badge display
    if st.session_state.story_badges:
        badges = " ".join([b["emoji"] + " " + b["name"] for b in st.session_state.story_badges])
        st.markdown(
            "<div style='background:#071520;border:1px solid #fbbf2440;"
            "border-radius:10px;padding:8px;text-align:center;"
            "font-size:12px;color:#fbbf24'>🏅 Your Badges: " + badges + "</div>",
            unsafe_allow_html=True
        )

    if st.session_state.stories_read > 0:
        st.caption("📚 Stories read: " + str(st.session_state.stories_read))

    st.markdown("---")

    # Grade selector
    grade = st.radio(
        "📚 Select your grade level:",
        ["K-2 (Ages 5-7)", "Grades 3-6 (Ages 8-11)"],
        horizontal=True,
        key="story_grade"
    )

    col1, col2 = st.columns(2)
    with col1:
        hero_opts = [h["name"] for h in HEROES] + ["🎲 Surprise me!"]
        hero_choice = st.selectbox("🦸 Choose your hero:", hero_opts, key="hero_sel")
    with col2:
        monster_opts = [m["name"] for m in MONSTERS] + ["🎲 Surprise me!"]
        monster_choice = st.selectbox("👾 Choose a monster:", monster_opts, key="monster_sel")

    if hero_choice == "🎲 Surprise me!":
        hero_choice = random.choice([h["name"] for h in HEROES])
    if monster_choice == "🎲 Surprise me!":
        monster_choice = random.choice([m["name"] for m in MONSTERS])

    hero = next((h for h in HEROES if h["name"] == hero_choice), HEROES[0])
    monster = next((m for m in MONSTERS if m["name"] == monster_choice), MONSTERS[0])

    # Preview card
    st.markdown(
        "<div style='background:#071520;border:1px solid #1a3a5a;"
        "border-radius:10px;padding:12px;text-align:center;margin:8px 0'>"
        "<span style='font-size:2.5rem'>" + hero["emoji"] + " ⚔️ " + monster["emoji"] + "</span><br>"
        "<span style='color:#60a5fa;font-size:13px;font-weight:bold'>"
        + hero["name"] + " vs " + monster["name"] + "</span>"
        "</div>",
        unsafe_allow_html=True
    )

    if st.button("✨ Create My Story!", type="primary", use_container_width=True, key="gen_story"):
        st.session_state.story_puzzle_done = False
        st.session_state.current_puzzle = random.choice(PUZZLES)

        is_young = "K-2" in grade
        word_count = "120-150" if is_young else "200-250"
        style = (
            "Use very simple words, short sentences, fun sounds like WHOOSH and BOOM. "
            "No technical terms. Feel like a picture book with emojis."
            if is_young else
            "Gradually introduce real concepts through fantasy metaphors: "
            "magic keys=encryption keys, treasure chests=encrypted data, "
            "magic locks=cryptographic algorithms. Include the FIPS number naturally."
        )

        prompt = (
            "Write a fun " + word_count + " word children's story for grade level "
            + ("K-2" if is_young else "3-6") + ". "
            "Hero: " + hero["name"] + " " + hero["emoji"] + " whose power is " + hero["power"]
            + " (" + hero["fips"] + "). "
            "Monster: " + monster["name"] + " " + monster["emoji"]
            + " who is afraid of " + monster["fear"] + ". "
            "Teach about post-quantum cryptography in a fun way. "
            "End positively. Start with a title. Use short paragraphs and emojis. "
            + style
        )

        with st.spinner("✨ Writing your magical story..."):
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY", ""))
                response = client.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=600,
                    messages=[{"role": "user", "content": prompt}]
                )
                story_text = response.content[0].text
            except Exception:
                story_text = get_fallback_story(hero["name"], monster["name"])

        st.session_state.current_story = story_text
        st.session_state.stories_read += 1

        count = st.session_state.stories_read
        if count in BADGES:
            badge = BADGES[count]
            if badge not in st.session_state.story_badges:
                st.session_state.story_badges.append(badge)
                st.balloons()
                st.success("🎉 New badge: " + badge["emoji"] + " " + badge["name"])

        st.rerun()

    # Display story
    if st.session_state.current_story:
        st.markdown("---")
        render_storybook(
            st.session_state.current_story,
            hero["emoji"],
            monster["emoji"]
        )

        st.markdown("")

        # Puzzle section
        if not st.session_state.story_puzzle_done and st.session_state.current_puzzle:
            st.markdown("---")
            st.markdown("### 🧩 Quick Puzzle!")
            st.caption("Answer correctly to earn your story certificate!")

            pz = st.session_state.current_puzzle
            answer = st.radio(pz["q"], pz["opts"], key="puzzle_ans")

            if st.button("✅ Submit Answer", key="puzzle_sub", type="primary"):
                if answer == pz["opts"][pz["ans"]]:
                    st.success("🎉 CORRECT! " + pz["fact"])
                    st.session_state.story_puzzle_done = True
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Not quite! Hint: " + pz["fact"])

        # Certificate
        if st.session_state.story_puzzle_done:
            st.markdown("---")
            st.markdown(
                "<div style='background:linear-gradient(135deg,#0a1f35,#071520);"
                "border:3px solid #fbbf24;border-radius:16px;"
                "padding:24px;text-align:center'>"
                "<div style='font-size:3rem'>🏅</div>"
                "<h3 style='color:#fbbf24;margin:6px 0'>Cyber Hero Certificate</h3>"
                "<p style='color:#94a3b8'>This certifies that</p>"
                "<h2 style='color:#60a5fa'>Future Quantum Guardian</h2>"
                "<p style='color:#94a3b8'>completed a Quantum Monster Adventure<br>"
                "and learned about Post-Quantum Cryptography!</p>"
                "<p style='color:#fbbf24;font-size:11px;margin-top:8px'>"
                "QuantumVault Academy · quantumvaultacademy.com</p>"
                "</div>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📖 Read Another Story!", use_container_width=True, key="another"):
                    st.session_state.current_story = None
                    st.session_state.story_puzzle_done = False
                    st.session_state.current_puzzle = None
                    st.rerun()
            with col2:
                if st.button("🎮 Play a Game!", use_container_width=True, key="play_game"):
                    st.session_state.level = "🔤 Secret Message Maker"
                    st.rerun()

    st.markdown("---")
    st.info(
        "🔐 Post-Quantum Cryptography uses math so hard that even the most powerful "
        "quantum computers cannot break it! NIST finalized 4 standards in 2024: "
        "Kyber (FIPS 203), Dilithium (FIPS 204), SPHINCS+ (FIPS 205), Falcon (FIPS 206)."
    )
