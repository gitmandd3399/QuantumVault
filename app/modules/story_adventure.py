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
    """Interactive fairy tale storybook with page turning, animations, and read aloud."""
    import streamlit.components.v1 as components

    # Clean story text for safe JavaScript embedding
    # Replace characters that would break the JS string
    clean = (story_text
             .replace('\\', '\\\\')  # escape backslashes first
             .replace('\r', '')       # remove carriage returns
             .replace('"', "'")       # replace double quotes with single
             .replace('`', "'")       # replace backticks with single quotes
             .replace('\n', '<br>')   # convert newlines to HTML breaks
    )

    components.html("""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
/* ── RESET ── */
*{margin:0;padding:0;box-sizing:border-box;}
body{background:transparent;font-family:Georgia,'Times New Roman',serif;
     overflow:hidden;user-select:none;}

/* ── OUTER WRAP ── */
#wrap{
    display:flex;flex-direction:column;align-items:center;
    padding:12px 8px;position:relative;
}

/* ── BOOK CONTAINER ── */
#book-outer{
    position:relative;width:100%;max-width:680px;
}

/* ── OPEN BOOK ── */
#book{
    display:flex;width:100%;min-height:360px;
    filter:drop-shadow(0 12px 28px rgba(0,0,0,0.45));
    position:relative;
}

/* ── PAGE SHARED ── */
.page{
    flex:1;position:relative;overflow:hidden;
    padding:22px 20px 40px 22px;min-height:360px;
}

/* ── LEFT PAGE ── */
#page-1{
    background:linear-gradient(105deg,#f0ddb0 0%,#fdf3e3 40%,#fdf8f0 100%);
    border-radius:8px 0 0 8px;
    border:1.5px solid #c4a35a;border-right:none;
}

/* ── RIGHT PAGE ── */
#page-2{
    background:linear-gradient(255deg,#f0ddb0 0%,#fdf3e3 40%,#fdf8f0 100%);
    border-radius:0 8px 8px 0;
    border:1.5px solid #c4a35a;border-left:none;
}

/* ── SPINE ── */
#spine{
    width:20px;flex-shrink:0;
    background:linear-gradient(to bottom,#7a5c10,#c4a35a 25%,#f5d278 50%,#c4a35a 75%,#7a5c10);
    box-shadow:inset -2px 0 6px rgba(0,0,0,0.25),inset 2px 0 6px rgba(0,0,0,0.25);
    z-index:5;
}

/* ── INNER BORDER DECORATION ── */
.page::before{
    content:'';position:absolute;inset:8px;
    border:1.5px solid #c4a35a50;border-radius:4px;pointer-events:none;
}

/* ── PAGE NUMBER ── */
.pg-num{
    text-align:center;font-size:10px;color:#8b6914;
    font-style:italic;letter-spacing:1px;margin-bottom:4px;
}

/* ── STARS ROW ── */
.stars-row{
    text-align:center;font-size:13px;margin-bottom:5px;
    letter-spacing:4px;
}
.star{
    cursor:pointer;display:inline-block;
    transition:transform 0.2s,filter 0.2s;
    color:#c4a35a;
}
.star:hover,.star.lit{
    color:#fbbf24;filter:drop-shadow(0 0 6px #fbbf24);
    transform:scale(1.4) rotate(15deg);
}

/* ── CHAPTER TITLE ── */
.ch-title{
    text-align:center;font-size:14px;font-weight:bold;
    color:#5c3d0e;line-height:1.4;margin-bottom:6px;
}

/* ── ORNAMENTAL DIVIDER ── */
.ornament{
    text-align:center;color:#8b6914;font-size:13px;
    letter-spacing:3px;margin:4px 0 6px;
}

/* ── CHARACTER DISPLAY ── */
#char-row{
    display:flex;justify-content:center;align-items:center;
    gap:12px;margin:4px 0 8px;
}
.char{
    font-size:2rem;cursor:pointer;
    transition:transform 0.2s;display:inline-block;
}
.char:hover{transform:scale(1.3) rotate(-10deg);}
.char.bounce{animation:bounce 0.5s ease;}
@keyframes bounce{
    0%{transform:scale(1);}
    30%{transform:scale(1.4) rotate(15deg);}
    60%{transform:scale(0.9) rotate(-5deg);}
    100%{transform:scale(1);}
}
.vs-text{font-size:11px;color:#8b6914;font-style:italic;}

/* ── STORY TEXT ── */
.story-body{
    font-size:13px;line-height:1.85;color:#2c1810;
    text-align:justify;
}

/* ── DROP CAP ── */
.drop-cap{
    float:left;font-size:44px;line-height:0.75;
    padding-right:5px;padding-top:6px;
    color:#8b6914;font-weight:bold;
}

/* ── END ORNAMENT ── */
.end-orn{
    text-align:center;color:#8b6914;
    font-size:12px;letter-spacing:3px;
    margin-top:8px;display:none;
}

/* ── BOTTOM CONTROLS ── */
#controls{
    display:flex;justify-content:space-between;align-items:center;
    width:100%;max-width:680px;margin-top:10px;gap:8px;
}

/* ── NAV BUTTONS ── */
.nav-btn{
    padding:8px 18px;border-radius:24px;border:2px solid #c4a35a;
    background:linear-gradient(135deg,#8b6914,#c4a35a);
    color:#fdf3e3;font-size:13px;font-weight:bold;cursor:pointer;
    font-family:Georgia,serif;letter-spacing:0.5px;
    box-shadow:0 3px 8px rgba(0,0,0,0.25);
    transition:all 0.15s;
}
.nav-btn:hover{transform:translateY(-2px);filter:brightness(1.15);}
.nav-btn:active{transform:translateY(0);}
.nav-btn:disabled{opacity:0.35;cursor:not-allowed;transform:none;}

/* ── READ ALOUD BUTTON ── */
#read-btn{
    padding:8px 16px;border-radius:24px;
    border:2px solid #3b82f6;
    background:linear-gradient(135deg,#1d4ed8,#3b82f6);
    color:white;font-size:12px;cursor:pointer;
    font-family:Georgia,serif;
    box-shadow:0 3px 8px rgba(59,130,246,0.3);
    transition:all 0.15s;
}
#read-btn:hover{transform:translateY(-2px);filter:brightness(1.15);}

/* ── PAGE INDICATOR ── */
#page-indicator{
    font-size:11px;color:#8b6914;font-style:italic;
    text-align:center;min-width:80px;
}

/* ── PAGE FLIP ANIMATION ── */
.page.flip-out{animation:flipOut 0.3s ease forwards;}
.page.flip-in{animation:flipIn 0.3s ease forwards;}
@keyframes flipOut{
    0%{opacity:1;transform:perspective(800px) rotateY(0deg);}
    100%{opacity:0;transform:perspective(800px) rotateY(-15deg);}
}
@keyframes flipIn{
    0%{opacity:0;transform:perspective(800px) rotateY(15deg);}
    100%{opacity:1;transform:perspective(800px) rotateY(0deg);}
}

/* ── SPARKLE PARTICLES ── */
.sparkle{
    position:fixed;pointer-events:none;z-index:9999;
    font-size:14px;animation:sparkleAnim 0.8s ease forwards;
}
@keyframes sparkleAnim{
    0%{opacity:1;transform:scale(1) translate(0,0);}
    100%{opacity:0;transform:scale(0) translate(var(--tx),var(--ty));}
}

/* ── MAGIC WAND CURSOR TRAIL ── */
.trail{
    position:fixed;pointer-events:none;z-index:9998;
    width:6px;height:6px;border-radius:50%;
    animation:trailFade 0.6s ease forwards;
}
@keyframes trailFade{
    0%{opacity:0.9;transform:scale(1);}
    100%{opacity:0;transform:scale(0);}
}
</style>
</head>
<body>

<div id="wrap">

  <!-- THE OPEN BOOK -->
  <div id="book-outer">
    <div id="book">

      <!-- LEFT PAGE -->
      <div class="page" id="page-1">
        <div class="pg-num" id="pg-num-1">~ Page 1 ~</div>
        <div class="stars-row" id="stars-1">
          <span class="star" onclick="litStar(this)">✦</span>
          <span class="star" onclick="litStar(this)">✦</span>
          <span class="star" onclick="litStar(this)">✦</span>
        </div>
        <div class="ch-title" id="ch-title">📖 Loading...</div>
        <div class="ornament">~ ❧ ~</div>
        <div id="char-row">
          <span class="char" id="hero-char" onclick="bounceChar(this)">""" + hero_emoji + """</span>
          <span class="vs-text">✦ vs ✦</span>
          <span class="char" id="monster-char" onclick="bounceChar(this)">""" + monster_emoji + """</span>
        </div>
        <div class="story-body" id="body-1"></div>
        <div class="end-orn" id="end-orn-1"></div>
      </div>

      <!-- SPINE -->
      <div id="spine"></div>

      <!-- RIGHT PAGE -->
      <div class="page" id="page-2">
        <div class="pg-num" id="pg-num-2">~ Page 2 ~</div>
        <div class="stars-row" id="stars-2">
          <span class="star" onclick="litStar(this)">✦</span>
          <span class="star" onclick="litStar(this)">✦</span>
          <span class="star" onclick="litStar(this)">✦</span>
        </div>
        <div class="story-body" id="body-2"></div>
        <div class="end-orn" id="end-orn-2"></div>
      </div>

    </div>
  </div>

  <!-- CONTROLS -->
  <div id="controls">
    <button class="nav-btn" id="prev-btn" onclick="prevPage()" disabled>◀ Previous</button>
    <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
      <div id="page-indicator">Page 1 of 1</div>
      <button id="read-btn" onclick="readPage()">🔊 Read This Page</button>
    </div>
    <button class="nav-btn" id="next-btn" onclick="nextPage()">Next ▶</button>
  </div>

</div>

<script>
// ── STORY DATA ──────────────────────────────────────────────────────────────
var RAW = \"""" + clean + """\";

// ── PARSE STORY INTO CHUNKS ─────────────────────────────────────────────────
function parseStory(text){
    var lines = text.split('<br>').map(function(l){return l.trim();}).filter(function(l){return l.length>0;});
    var title = '';
    var paras = [];
    lines.forEach(function(line){
        if(line.match(/^#+/)){
            title = line.replace(/^#+/,'').replace(/[*_]/g,'').trim();
        } else {
            paras.push(line);
        }
    });
    return {title:title, paras:paras};
}

// ── SPLIT PARAGRAPHS INTO PAGES (4 paragraphs per page spread) ─────────────
var parsed = parseStory(RAW);
var PARAS = parsed.paras;
var TITLE = parsed.title || 'A Quantum Adventure';
var CHUNK = 4; // paragraphs per page-spread (left+right = 1 spread)
var SPREADS = [];

for(var i=0;i<PARAS.length;i+=CHUNK){
    SPREADS.push(PARAS.slice(i,i+CHUNK));
}
if(SPREADS.length===0) SPREADS.push(['Once upon a time...']);

var currentSpread = 0;

// ── RENDER CURRENT SPREAD ───────────────────────────────────────────────────
function renderSpread(){
    var spread = SPREADS[currentSpread];
    var mid = Math.ceil(spread.length/2);
    var leftParas = spread.slice(0,mid);
    var rightParas = spread.slice(mid);

    // Set title on spread 0
    if(currentSpread===0){
        document.getElementById('ch-title').textContent = TITLE;
        document.getElementById('char-row').style.display='flex';
    } else {
        document.getElementById('ch-title').textContent = TITLE;
        document.getElementById('char-row').style.display='none';
    }

    // Build left page HTML
    var leftHTML = '';
    leftParas.forEach(function(p,i){
        if(i===0 && currentSpread===0 && p.length>0){
            leftHTML += '<span class="drop-cap">'+p.charAt(0)+'</span>'+p.slice(1)+'<br><br>';
        } else {
            leftHTML += p+'<br><br>';
        }
    });

    // Build right page HTML
    var rightHTML = '';
    rightParas.forEach(function(p){
        rightHTML += p+'<br><br>';
    });

    // Animate page flip
    var p1 = document.getElementById('page-1');
    var p2 = document.getElementById('page-2');
    p1.classList.add('flip-out');
    p2.classList.add('flip-out');
    setTimeout(function(){
        document.getElementById('body-1').innerHTML = leftHTML;
        document.getElementById('body-2').innerHTML = rightHTML;

        // Page numbers
        var spreadNum = currentSpread+1;
        document.getElementById('pg-num-1').textContent = '~ Page '+(spreadNum*2-1)+' ~';
        document.getElementById('pg-num-2').textContent = '~ Page '+(spreadNum*2)+' ~';
        document.getElementById('page-indicator').textContent =
            'Spread '+(currentSpread+1)+' of '+SPREADS.length;

        // Show "The End" on last spread
        var isLast = (currentSpread===SPREADS.length-1);
        document.getElementById('end-orn-1').style.display='none';
        document.getElementById('end-orn-2').style.display = isLast?'block':'none';
        document.getElementById('end-orn-2').textContent = isLast?'~ The End ✦ ~':'';

        p1.classList.remove('flip-out');
        p2.classList.remove('flip-out');
        p1.classList.add('flip-in');
        p2.classList.add('flip-in');
        setTimeout(function(){
            p1.classList.remove('flip-in');
            p2.classList.remove('flip-in');
        },350);
    },280);

    // Update buttons
    document.getElementById('prev-btn').disabled = (currentSpread===0);
    document.getElementById('next-btn').disabled = (currentSpread===SPREADS.length-1);
}

// ── NAV FUNCTIONS ────────────────────────────────────────────────────────────
function nextPage(){
    if(currentSpread<SPREADS.length-1){
        currentSpread++;
        renderSpread();
        spawnSparkles(window.innerWidth/2, window.innerHeight/2, 8);
    }
}
function prevPage(){
    if(currentSpread>0){
        currentSpread--;
        renderSpread();
        spawnSparkles(window.innerWidth/2, window.innerHeight/2, 8);
    }
}

// ── READ ALOUD ───────────────────────────────────────────────────────────────
function readPage(){
    window.speechSynthesis.cancel();
    var spread = SPREADS[currentSpread];
    var text = spread.join(' ').replace(/<br>/g,' ').replace(/[*_#]/g,'');
    var msg = new SpeechSynthesisUtterance(text);
    msg.rate = 0.88;
    msg.pitch = 1.1;
    msg.volume = 1.0;
    window.speechSynthesis.speak(msg);
    document.getElementById('read-btn').textContent = '🔊 Reading...';
    msg.onend = function(){ document.getElementById('read-btn').textContent = '🔊 Read This Page'; };
}

// ── STAR INTERACTION ─────────────────────────────────────────────────────────
function litStar(el){
    el.classList.toggle('lit');
    spawnSparkles(
        el.getBoundingClientRect().left + 8,
        el.getBoundingClientRect().top + 8,
        5
    );
}

// ── CHARACTER BOUNCE ─────────────────────────────────────────────────────────
function bounceChar(el){
    el.classList.remove('bounce');
    void el.offsetWidth; // reflow trick to restart animation
    el.classList.add('bounce');
    spawnSparkles(
        el.getBoundingClientRect().left + 20,
        el.getBoundingClientRect().top + 10,
        8
    );
    setTimeout(function(){ el.classList.remove('bounce'); },600);
}

// ── SPARKLE PARTICLES ────────────────────────────────────────────────────────
var SPARKLE_CHARS = ['✨','⭐','🌟','💫','✦','★','✺'];
function spawnSparkles(x, y, count){
    for(var i=0;i<count;i++){
        (function(){
            var el = document.createElement('div');
            el.className = 'sparkle';
            el.textContent = SPARKLE_CHARS[Math.floor(Math.random()*SPARKLE_CHARS.length)];
            var angle = Math.random()*Math.PI*2;
            var dist = 30+Math.random()*50;
            el.style.left = x+'px';
            el.style.top = y+'px';
            el.style.setProperty('--tx', Math.cos(angle)*dist+'px');
            el.style.setProperty('--ty', Math.sin(angle)*dist+'px');
            el.style.animationDelay = (Math.random()*0.2)+'s';
            document.body.appendChild(el);
            setTimeout(function(){ el.remove(); },900);
        })();
    }
}

// ── MAGIC CURSOR TRAIL ───────────────────────────────────────────────────────
var TRAIL_COLORS = ['#fbbf24','#60a5fa','#10b981','#f97316','#a78bfa'];
var trailCount = 0;
document.addEventListener('mousemove',function(e){
    if(trailCount%3!==0){ trailCount++; return; } // only every 3rd move
    trailCount++;
    var el = document.createElement('div');
    el.className = 'trail';
    el.style.left = e.clientX+'px';
    el.style.top = e.clientY+'px';
    el.style.background = TRAIL_COLORS[Math.floor(Math.random()*TRAIL_COLORS.length)];
    document.body.appendChild(el);
    setTimeout(function(){ el.remove(); },650);
});

// ── INIT ─────────────────────────────────────────────────────────────────────
renderSpread();
</script>
</body>
</html>
""", height=520, scrolling=False)



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
