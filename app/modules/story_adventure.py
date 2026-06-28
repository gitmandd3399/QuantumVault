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
    """Renders story text inside a fairy tale book UI."""
    import streamlit.components.v1 as components

    clean = (story_text
             .replace("\\", "\\\\")
             .replace("`", "'")
             .replace("\n", "<br>")
             .replace('"', "'")
    )

    components.html("""
<!DOCTYPE html>
<html>
<head>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:transparent;font-family:Georgia,serif;}
#book-wrap{display:flex;justify-content:center;align-items:flex-start;padding:16px 8px;perspective:1500px;}
#book{display:flex;width:100%;max-width:660px;min-height:380px;position:relative;filter:drop-shadow(0 12px 30px rgba(0,0,0,0.45));}
#page-left{flex:1;background:linear-gradient(to right,#f5e6c8,#fdf3e3);border-radius:8px 0 0 8px;padding:26px 22px 26px 28px;position:relative;border:1px solid #c4a35a;border-right:none;min-height:380px;overflow:hidden;}
#page-right{flex:1;background:linear-gradient(to left,#f5e6c8,#fdf3e3);border-radius:0 8px 8px 0;padding:26px 28px 26px 22px;position:relative;border:1px solid #c4a35a;border-left:none;min-height:380px;overflow:hidden;}
#spine{width:22px;background:linear-gradient(to bottom,#7a5c10 0%,#c4a35a 20%,#f5d278 50%,#c4a35a 80%,#7a5c10 100%);box-shadow:inset -2px 0 4px rgba(0,0,0,0.3),inset 2px 0 4px rgba(0,0,0,0.3);position:relative;z-index:10;}
#page-left::before,#page-right::before{content:'';position:absolute;inset:8px;border:1.5px solid #c4a35a60;border-radius:4px;pointer-events:none;}
.page-num{text-align:center;font-size:10px;color:#8b6914;margin-bottom:6px;font-style:italic;letter-spacing:1px;}
.stars{text-align:center;font-size:11px;color:#8b6914;margin-bottom:6px;letter-spacing:3px;}
.chapter-title{text-align:center;font-size:14px;font-weight:bold;color:#5c3d0e;margin-bottom:8px;line-height:1.4;}
.divider{text-align:center;color:#8b6914;font-size:14px;margin:6px 0;letter-spacing:3px;}
.hero-badge{text-align:center;font-size:1.8rem;margin:6px 0 2px;}
.hero-name{text-align:center;font-size:10px;color:#8b6914;font-style:italic;letter-spacing:1px;margin-bottom:10px;}
.story-text{font-size:13px;line-height:1.8;color:#2c1810;text-align:justify;}
.drop-cap{float:left;font-size:46px;line-height:0.75;padding-right:5px;padding-top:6px;color:#8b6914;font-weight:bold;}
.end-div{text-align:center;color:#8b6914;font-size:13px;margin-top:10px;letter-spacing:3px;}
</style>
</head>
<body>
<div id="book-wrap">
  <div id="book">
    <div id="page-left">
      <div class="page-num">~ Page 1 ~</div>
      <div class="stars">✦ ✦ ✦</div>
      <div class="chapter-title" id="story-title">Loading...</div>
      <div class="divider">~ ❧ ~</div>
      <div class="hero-badge">""" + hero_emoji + " ⚔️ " + monster_emoji + """</div>
      <div class="hero-name">A Quantum Monster Adventure</div>
      <div class="story-text" id="story-left"></div>
    </div>
    <div id="spine"></div>
    <div id="page-right">
      <div class="page-num">~ Page 2 ~</div>
      <div class="stars">✦ ✦ ✦</div>
      <div class="story-text" id="story-right"></div>
      <div class="end-div" id="end-div" style="display:none">~ The End ✦ ~</div>
    </div>
  </div>
</div>
<script>
var fullStory = """" + clean + """";
function parseStory(text) {
    var lines = text.split('<br>').filter(function(l){return l.trim();});
    var title = '';
    var body = [];
    for (var i=0;i<lines.length;i++) {
        var line = lines[i].trim();
        if (line.indexOf('#') === 0) { title = line.replace(/^#+/,'').trim(); }
        else if (line) { body.push(line); }
    }
    return {title:title, body:body};
}
function renderBook() {
    var parsed = parseStory(fullStory);
    document.getElementById('story-title').innerHTML = parsed.title || 'A Quantum Adventure';
    var mid = Math.ceil(parsed.body.length / 2);
    var leftLines = parsed.body.slice(0, mid);
    var rightLines = parsed.body.slice(mid);
    var leftHTML = '';
    leftLines.forEach(function(line, i) {
        if (i===0 && line.length>0) {
            leftHTML += '<span class="drop-cap">'+line.charAt(0)+'</span>'+line.slice(1)+'<br><br>';
        } else { leftHTML += line+'<br><br>'; }
    });
    document.getElementById('story-left').innerHTML = leftHTML;
    var rightHTML = '';
    rightLines.forEach(function(line){rightHTML += line+'<br><br>';});
    document.getElementById('story-right').innerHTML = rightHTML;
    document.getElementById('end-div').style.display='block';
}
renderBook();
</script>
</body>
</html>
""", height=460, scrolling=True)


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
