def render_quantumcraft_elementary():
    """K-5: QuantumCraft — 2D side-scrolling Minecraft-style PQC game."""
    import streamlit as st
    import streamlit.components.v1 as components

    st.subheader("⛏️ QuantumCraft — Crypto Kingdom!")
    st.markdown(
        "Mine crypto blocks, build your quantum-safe fortress, and survive the night! "
        "**Arrow keys** to move and jump. **Click** a block to mine it. "
        "**1-9** to select hotbar. **Right-click** to place blocks."
    )

    components.html(r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#020d14;font-family:'Segoe UI',sans-serif;overflow:hidden;}
#wrap{display:flex;flex-direction:column;align-items:center;padding:6px;}

/* GAME CANVAS */
#cv{border:2px solid #10b981;border-radius:8px;display:block;
    box-shadow:0 0 20px rgba(16,185,129,0.2);cursor:crosshair;}

/* HUD ROW */
#hud{display:flex;justify-content:space-between;align-items:center;
    width:560px;padding:4px 8px;background:#071520;
    border:1px solid #1a3a5a;border-radius:8px;margin-bottom:4px;}
.hud-hearts{font-size:14px;letter-spacing:2px;}
.hud-stat{font-size:10px;color:#60a5fa;}
.hud-stat b{color:white;}
#hud-msg{font-size:10px;color:#34d399;text-align:center;max-width:200px;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}

/* HOTBAR */
#hotbar{display:flex;gap:3px;margin-top:4px;
    background:#071520;border:1px solid #1a3a5a;
    border-radius:8px;padding:4px;}
.hslot{width:44px;height:44px;border:2px solid #334155;border-radius:6px;
    background:#0a1f35;display:flex;flex-direction:column;
    align-items:center;justify-content:center;
    cursor:pointer;position:relative;transition:all 0.1s;}
.hslot:hover{border-color:#3b82f6;}
.hslot.active{border-color:#fbbf24;background:#1a1500;}
.hslot .hs-emoji{font-size:18px;}
.hslot .hs-count{font-size:8px;color:#94a3b8;position:absolute;
    bottom:2px;right:4px;}
.hslot .hs-num{font-size:7px;color:#475569;position:absolute;top:1px;left:3px;}

/* CRAFT PANEL */
#craft-panel{display:none;position:fixed;top:50%;left:50%;
    transform:translate(-50%,-50%);
    background:#071520;border:2px solid #1d4ed8;border-radius:12px;
    padding:16px;z-index:100;min-width:260px;}
#craft-panel h3{color:#60a5fa;margin-bottom:10px;font-size:13px;}
.recipe{display:flex;align-items:center;gap:8px;padding:6px;
    border:1px solid #1a3a5a;border-radius:6px;margin-bottom:4px;
    cursor:pointer;transition:all 0.1s;}
.recipe:hover{background:#0a1f35;border-color:#3b82f6;}
.recipe-emoji{font-size:18px;}
.recipe-info{font-size:10px;color:#94a3b8;flex:1;}
.recipe-info b{color:white;font-size:11px;display:block;}
.recipe-btn{padding:3px 8px;background:#1d4ed8;border:none;
    border-radius:4px;color:white;font-size:9px;cursor:pointer;}
#craft-close{padding:6px 14px;background:#334155;border:none;
    border-radius:6px;color:white;cursor:pointer;margin-top:8px;
    font-size:11px;width:100%;}

/* FACT TOAST */
#fact-toast{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);
    background:#071520ee;border:1px solid #3b82f6;border-radius:8px;
    padding:8px 14px;font-size:10px;color:#93c5fd;
    z-index:50;opacity:0;transition:opacity 0.3s;
    max-width:320px;text-align:center;pointer-events:none;}
#fact-toast.show{opacity:1;}
</style>
</head>
<body>
<div id="wrap">

  <!-- HUD -->
  <div id="hud">
    <div>
      <div class="hud-hearts" id="hearts">❤️❤️❤️❤️❤️</div>
    </div>
    <div id="hud-msg">⛏️ Mine blocks! Arrow keys to move, click to mine!</div>
    <div style="display:flex;gap:10px;">
      <div class="hud-stat">Score <b id="h-score">0</b></div>
      <div class="hud-stat">Day <b id="h-day">1</b></div>
      <div class="hud-stat">Depth <b id="h-depth">0</b></div>
    </div>
  </div>

  <!-- CANVAS -->
  <canvas id="cv" width="560" height="380"></canvas>

  <!-- HOTBAR -->
  <div id="hotbar"></div>

</div>

<!-- CRAFT PANEL -->
<div id="craft-panel">
  <h3>🔬 PQC Crafting Lab</h3>
  <div id="recipes"></div>
  <button id="craft-close" onclick="closeCraft()">✕ Close</button>
</div>

<!-- FACT TOAST -->
<div id="fact-toast"></div>

<script>
// ── CONSTANTS ─────────────────────────────────────────────────────────────────
const CV = document.getElementById('cv');
const CX = CV.getContext('2d');
const W = 560, H = 380;
const TS = 28; // tile size in pixels
const COLS = 80; // world width in tiles
const ROWS = 40; // world height in tiles
const VIEW_W = Math.ceil(W/TS)+2; // visible columns
const VIEW_H = Math.ceil(H/TS)+2; // visible rows

// ── BLOCK DEFINITIONS ────────────────────────────────────────────────────────
// Each block has: color, emoji, solid, mineable, drop item, hardness, points
const BLOCKS = {
    air:     {color:'',        emoji:'',   solid:false, mineable:false},
    sky:     {color:'#0a1628', emoji:'',   solid:false, mineable:false},
    grass:   {color:'#166534', emoji:'🌿',  solid:true,  mineable:true,  drop:'grass',   hard:1, pts:2},
    dirt:    {color:'#7c4f2a', emoji:'',   solid:true,  mineable:true,  drop:'dirt',    hard:1, pts:1},
    stone:   {color:'#475569', emoji:'',   solid:true,  mineable:true,  drop:'stone',   hard:3, pts:3},
    kyber:   {color:'#10b981', emoji:'🔐',  solid:true,  mineable:true,  drop:'kyber',   hard:2, pts:15},
    lattice: {color:'#3b82f6', emoji:'🏗️',  solid:true,  mineable:true,  drop:'lattice', hard:3, pts:20},
    hash:    {color:'#8b5cf6', emoji:'#️⃣',  solid:true,  mineable:true,  drop:'hash',    hard:4, pts:25},
    diamond: {color:'#06b6d4', emoji:'💎',  solid:true,  mineable:true,  drop:'diamond', hard:5, pts:50},
    bedrock: {color:'#1e293b', emoji:'',   solid:true,  mineable:false},
    placed:  {color:'#1d4ed8', emoji:'🔵',  solid:true,  mineable:true,  drop:'kyber',   hard:1, pts:0},
    shield:  {color:'#10b981', emoji:'🛡️',  solid:true,  mineable:true,  drop:'kyber',   hard:2, pts:0},
    torch:   {color:'#f97316', emoji:'🔆',  solid:false, mineable:true,  drop:'torch',   hard:1, pts:1},
    tree:    {color:'#854d0e', emoji:'🌲',  solid:true,  mineable:true,  drop:'wood',    hard:2, pts:5},
    leaf:    {color:'#166534', emoji:'🍃',  solid:false, mineable:true,  drop:'leaf',    hard:1, pts:1},
};

// ── PQC FACTS ────────────────────────────────────────────────────────────────
const FACTS = [
    '🔐 Kyber Crystal uses lattice math — the same FIPS 203 standard protecting the internet!',
    '🏗️ Lattice Stone represents the math behind ALL 4 NIST PQC algorithms!',
    '#️⃣ Hash Block uses SHA-3 — the avalanche effect means one change flips 50% of bits!',
    '💎 Quantum Diamond is rarer than regular diamonds because good PQC is hard to find!',
    '🛡️ Your Kyber Shield uses ML-KEM — it stops Shor Bot attacks completely!',
    '👾 Shor Bots use Shor\'s Algorithm to try and break your blocks — but Kyber stops them!',
    '⛏️ In real life cryptographers "mine" for mathematical patterns too!',
    '🌙 Shor Bots only come at night — just like real cyber attacks peak at night!',
    '🔆 Torches give light — encryption "illuminates" data by making it unreadable to hackers!',
    '🏰 Your quantum fortress uses the same principles as NSM-10 — the US quantum security law!',
];

// ── CRAFTING RECIPES ─────────────────────────────────────────────────────────
// Format: {name, emoji, needs:{item:count}, makes:{item:count}, description}
const RECIPES = [
    {
        name:'Kyber Shield',emoji:'🛡️',
        needs:{kyber:3},
        makes:{shield_block:1},
        desc:'3 Kyber → 1 Shield Block. Stops Shor Bots!'
    },
    {
        name:'Quantum Zapper',emoji:'⚡',
        needs:{kyber:2,lattice:1},
        makes:{zapper:1},
        desc:'2 Kyber + 1 Lattice → Zapper weapon!'
    },
    {
        name:'Hash Torch',emoji:'🔆',
        needs:{hash:1,wood:1},
        makes:{torch:4},
        desc:'1 Hash + 1 Wood → 4 Torches for light!'
    },
    {
        name:'PQC Armor',emoji:'🥷',
        needs:{diamond:2,kyber:1},
        makes:{armor:1},
        desc:'2 Diamond + 1 Kyber → Full quantum armor!'
    },
    {
        name:'Lattice Wall',emoji:'🏗️',
        needs:{lattice:2},
        makes:{placed:4},
        desc:'2 Lattice → 4 sturdy wall blocks!'
    },
];

// ── GAME STATE ────────────────────────────────────────────────────────────────
let world = []; // 2D array [row][col] = block type string
let player = {
    x: 10 * TS,     // pixel x position
    y: 5 * TS,      // pixel y position
    vx: 0,          // horizontal velocity
    vy: 0,          // vertical velocity
    w: 20,          // width
    h: 26,          // height
    onGround: false,
    facing: 1,      // 1=right, -1=left
    hp: 5,
    maxHp: 5,
    hasArmor: false,
    hasZapper: false,
    mineProgress: 0,
    mineTarget: null,
    mineTimer: null,
};
let camera = {x: 0, y: 0}; // top-left pixel of camera view
let hotbar = [
    {item:'kyber', count:0},
    {item:'dirt',  count:0},
    {item:'stone', count:0},
    {item:'lattice',count:0},
    {item:'hash',  count:0},
    {item:'torch', count:0},
    {item:'',count:0},
    {item:'',count:0},
    {item:'',count:0},
];
let activeSlot = 0;
let inventory = {}; // item name → count
let enemies = [];
let particles = [];
let score = 0;
let day = 1;
let dayTime = 0; // 0-1, 0=noon, 0.5=midnight
let DAY_LENGTH = 1800; // frames per full cycle
let gameOver = false;
let craftOpen = false;
let keys = {};
let mouseWorld = {x:0, y:0}; // mouse position in world coords
let mineBlock = null; // block being mined {tx, ty, progress, maxProgress}
let factTimeout = null;

// ── WORLD GENERATION ─────────────────────────────────────────────────────────
function generateWorld(){
    // Initialize all air
    for(let r=0;r<ROWS;r++){
        world[r]=[];
        for(let c=0;c<COLS;c++) world[r][c]='sky';
    }

    // Generate terrain height using sine waves for hills
    const heights = [];
    for(let c=0;c<COLS;c++){
        const h = Math.floor(
            12 +
            Math.sin(c*0.15)*3 +
            Math.sin(c*0.08)*2 +
            Math.sin(c*0.3)*1.5
        );
        heights.push(h);
    }

    // Fill terrain
    for(let c=0;c<COLS;c++){
        const surfaceRow = heights[c];
        for(let r=0;r<ROWS;r++){
            if(r < surfaceRow) continue; // air/sky above surface
            if(r === surfaceRow) { world[r][c]='grass'; continue; }
            if(r <= surfaceRow+3) { world[r][c]='dirt'; continue; }
            if(r === ROWS-1) { world[r][c]='bedrock'; continue; }
            // Underground blocks with depth-based rarity
            const depth = r - surfaceRow;
            const rng = Math.random();
            if(depth>15 && rng<0.04) world[r][c]='diamond';
            else if(depth>10 && rng<0.07) world[r][c]='hash';
            else if(depth>6  && rng<0.09) world[r][c]='lattice';
            else if(depth>3  && rng<0.12) world[r][c]='kyber';
            else world[r][c]='stone';
        }
    }

    // Add trees on surface
    for(let c=2;c<COLS-2;c++){
        if(Math.random()<0.08 && world[heights[c]][c]==='grass'){
            const th = heights[c];
            const treeH = 3 + Math.floor(Math.random()*2);
            for(let i=1;i<=treeH;i++) world[th-i][c]='tree';
            // Leaves
            for(let dr=-1;dr<=1;dr++) for(let dc=-2;dc<=2;dc++){
                const lr=th-treeH+dr, lc=c+dc;
                if(lr>=0&&lc>=0&&lc<COLS&&world[lr][lc]==='sky')
                    world[lr][lc]='leaf';
            }
        }
    }

    // Spawn player at surface
    const spawnCol = 8;
    player.x = spawnCol * TS;
    player.y = (heights[spawnCol]-2) * TS;
    player.vx=0; player.vy=0;
    camera.x = player.x - W/2;
    camera.y = player.y - H/2;
}

// ── TILE HELPERS ──────────────────────────────────────────────────────────────
function getTile(tx,ty){
    if(tx<0||ty<0||tx>=COLS||ty>=ROWS) return 'bedrock';
    return world[ty]?.[tx]||'air';
}
function setTile(tx,ty,type){
    if(tx<0||ty<0||tx>=COLS||ty>=ROWS) return;
    world[ty][tx]=type;
}
function isSolid(tx,ty){
    return BLOCKS[getTile(tx,ty)]?.solid||false;
}

// ── PHYSICS ───────────────────────────────────────────────────────────────────
const GRAVITY = 0.45;
const JUMP_FORCE = -9;
const MOVE_SPEED = 3;
const MAX_FALL = 14;

function updatePlayer(){
    if(gameOver) return;

    // Horizontal movement
    let dx = 0;
    if(keys['ArrowLeft']||keys['a']) dx=-MOVE_SPEED;
    if(keys['ArrowRight']||keys['d']) dx=MOVE_SPEED;
    if(dx!==0) player.facing=dx>0?1:-1;
    player.vx=dx;

    // Jump
    if((keys['ArrowUp']||keys['w']||keys[' '])&&player.onGround){
        player.vy=JUMP_FORCE;
        player.onGround=false;
    }

    // Gravity
    player.vy=Math.min(player.vy+GRAVITY, MAX_FALL);

    // Move X
    player.x+=player.vx;
    resolveCollisionX();

    // Move Y
    player.y+=player.vy;
    player.onGround=false;
    resolveCollisionY();

    // Camera follows player smoothly
    const targetCX=player.x-W/2+player.w/2;
    const targetCY=player.y-H/2+player.h/2;
    camera.x+=(targetCX-camera.x)*0.1;
    camera.y+=(targetCY-camera.y)*0.1;
    // Clamp camera
    camera.x=Math.max(0,Math.min(COLS*TS-W,camera.x));
    camera.y=Math.max(0,Math.min(ROWS*TS-H,camera.y));

    // Depth display
    const playerTileY=Math.floor((player.y+player.h)/TS);
    const depth=Math.max(0,playerTileY-12);
    document.getElementById('h-depth').textContent=depth;
}

function getPlayerTiles(){
    // Returns all tile coords the player overlaps
    const x1=Math.floor(player.x/TS);
    const x2=Math.floor((player.x+player.w-1)/TS);
    const y1=Math.floor(player.y/TS);
    const y2=Math.floor((player.y+player.h-1)/TS);
    return {x1,x2,y1,y2};
}

function resolveCollisionX(){
    const {x1,x2,y1,y2}=getPlayerTiles();
    if(player.vx>0){
        for(let ty=y1;ty<=y2;ty++){
            if(isSolid(x2,ty)){
                player.x=x2*TS-player.w;
                player.vx=0; break;
            }
        }
    } else if(player.vx<0){
        for(let ty=y1;ty<=y2;ty++){
            if(isSolid(x1,ty)){
                player.x=(x1+1)*TS;
                player.vx=0; break;
            }
        }
    }
}

function resolveCollisionY(){
    const {x1,x2,y1,y2}=getPlayerTiles();
    if(player.vy>0){
        for(let tx=x1;tx<=x2;tx++){
            if(isSolid(tx,y2)){
                player.y=y2*TS-player.h;
                player.vy=0;
                player.onGround=true;
                break;
            }
        }
    } else if(player.vy<0){
        for(let tx=x1;tx<=x2;tx++){
            if(isSolid(tx,y1)){
                player.y=(y1+1)*TS;
                player.vy=0; break;
            }
        }
    }
}

// ── ENEMY AI ─────────────────────────────────────────────────────────────────
function spawnEnemy(){
    // Spawn off screen left or right
    const side=Math.random()<0.5?-1:1;
    const spawnX=(camera.x+side*(W+50));
    const spawnTX=Math.floor(spawnX/TS);
    // Find surface at that column
    let spawnTY=0;
    for(let r=0;r<ROWS;r++){
        if(isSolid(spawnTX,r)){spawnTY=r-1;break;}
    }
    enemies.push({
        x:spawnTX*TS, y:spawnTY*TS,
        vx:side<0?1.2:-1.2, vy:0,
        w:20, h:26,
        hp:3, onGround:false,
        attackTimer:0,
    });
}

function updateEnemies(){
    const isNight=dayTime>0.45&&dayTime<0.95;
    // Spawn enemies at night
    if(isNight&&enemies.length<3+Math.floor(day/2)&&Math.random()<0.01){
        spawnEnemy();
    }
    // Remove enemies that wander too far
    enemies=enemies.filter(e=>Math.abs(e.x-player.x)<W*2);

    enemies.forEach(e=>{
        // Gravity
        e.vy=Math.min(e.vy+GRAVITY,MAX_FALL);

        // Move toward player
        const dx=player.x-e.x;
        if(Math.abs(dx)>10) e.vx=dx>0?1.5:-1.5;

        // Jump over walls
        if(e.onGround){
            const dirX=e.vx>0?1:-1;
            const frontTX=Math.floor((e.x+e.w*0.5+dirX*16)/TS);
            const frontTY=Math.floor((e.y+e.h-4)/TS);
            if(isSolid(frontTX,frontTY)) e.vy=JUMP_FORCE*0.8;
        }

        // Move
        e.x+=e.vx;
        // Simple X collision
        const etx1=Math.floor(e.x/TS), etx2=Math.floor((e.x+e.w-1)/TS);
        const ety1=Math.floor(e.y/TS), ety2=Math.floor((e.y+e.h-1)/TS);
        if(e.vx>0){for(let ty=ety1;ty<=ety2;ty++){if(isSolid(etx2,ty)){e.x=etx2*TS-e.w;e.vx*=-1;break;}}}
        else{for(let ty=ety1;ty<=ety2;ty++){if(isSolid(etx1,ty)){e.x=(etx1+1)*TS;e.vx*=-1;break;}}}

        e.y+=e.vy; e.onGround=false;
        const etx1b=Math.floor(e.x/TS), etx2b=Math.floor((e.x+e.w-1)/TS);
        const ety2b=Math.floor((e.y+e.h-1)/TS), ety1b=Math.floor(e.y/TS);
        if(e.vy>0){for(let tx=etx1b;tx<=etx2b;tx++){if(isSolid(tx,ety2b)){e.y=ety2b*TS-e.h;e.vy=0;e.onGround=true;break;}}}
        else{for(let tx=etx1b;tx<=etx2b;tx++){if(isSolid(tx,ety1b)){e.y=(ety1b+1)*TS;e.vy=0;break;}}}

        // Attack player
        const dist=Math.hypot(player.x-e.x,player.y-e.y);
        e.attackTimer++;
        if(dist<30&&e.attackTimer>60){
            e.attackTimer=0;
            if(!player.hasArmor) player.hp=Math.max(0,player.hp-1);
            else player.hp=Math.max(0,player.hp-0.5);
            updateHearts();
            spawnParticles(player.x+10,player.y+10,'#ef4444',5);
            showMsg('💀 Shor Bot attack! '+(player.hasArmor?'Armor reduced damage!':'Craft armor for protection!'));
            if(player.hp<=0){
                gameOver=true;
                showMsg('💀 GAME OVER! Press R to restart');
            }
        }
    });
}

// ── MINING ────────────────────────────────────────────────────────────────────
function startMining(tx,ty){
    const bt=getTile(tx,ty);
    const bd=BLOCKS[bt];
    if(!bd||!bd.mineable) return;
    mineBlock={tx,ty,progress:0,maxProgress:bd.hard*8};
}

function updateMining(){
    if(!mineBlock) return;
    mineBlock.progress++;

    // Particle spray while mining
    if(mineBlock.progress%3===0){
        const wx=mineBlock.tx*TS-camera.x+TS/2;
        const wy=mineBlock.ty*TS-camera.y+TS/2;
        spawnParticlesScreen(wx,wy,BLOCKS[getTile(mineBlock.tx,mineBlock.ty)]?.color||'#888',3);
    }

    if(mineBlock.progress>=mineBlock.maxProgress){
        // Break the block!
        const bt=getTile(mineBlock.tx,mineBlock.ty);
        const bd=BLOCKS[bt];
        setTile(mineBlock.tx,mineBlock.ty,'sky');
        if(bd.drop){
            addToInventory(bd.drop,1);
            score+=bd.pts||0;
            document.getElementById('h-score').textContent=score;
        }
        spawnParticles(mineBlock.tx*TS+TS/2, mineBlock.ty*TS+TS/2, bd.color||'#888', 8);
        // PQC fact for special blocks
        if(['kyber','lattice','hash','diamond'].includes(bt)){
            showFact(FACTS[Math.floor(Math.random()*FACTS.length)]);
        }
        showMsg('⛏️ Mined '+bt+'! +'+(bd.pts||0)+' pts');
        mineBlock=null;
        updateHotbarUI();
    }
}

// ── INVENTORY ─────────────────────────────────────────────────────────────────
function addToInventory(item,count){
    inventory[item]=(inventory[item]||0)+count;
    // Auto-add to hotbar if slot is empty or matching
    for(let i=0;i<hotbar.length;i++){
        if(hotbar[i].item===item){ hotbar[i].count++; updateHotbarUI(); return; }
    }
    for(let i=0;i<hotbar.length;i++){
        if(!hotbar[i].item){ hotbar[i].item=item; hotbar[i].count=1; updateHotbarUI(); return; }
    }
}

function placeBlock(tx,ty){
    if(getTile(tx,ty)!=='sky') return;
    const slot=hotbar[activeSlot];
    if(!slot.item||slot.count<=0) return;
    // Map item name to tile type
    const itemToTile={
        kyber:'placed', dirt:'dirt', stone:'stone',
        lattice:'placed', grass:'grass',
        torch:'torch', placed:'placed', shield_block:'shield',
    };
    const tileType=itemToTile[slot.item]||slot.item;
    if(!BLOCKS[tileType]) return;
    setTile(tx,ty,tileType);
    slot.count--;
    if(slot.count<=0){ slot.item=''; slot.count=0; }
    updateHotbarUI();
    showMsg('🔵 Placed '+tileType+'!');
}

// ── CRAFTING ──────────────────────────────────────────────────────────────────
function openCraft(){
    craftOpen=true;
    const panel=document.getElementById('craft-panel');
    const rDiv=document.getElementById('recipes');
    panel.style.display='block';
    rDiv.innerHTML='';
    RECIPES.forEach(r=>{
        const canCraft=Object.entries(r.needs).every(([item,cnt])=>(inventory[item]||0)>=cnt);
        const div=document.createElement('div');
        div.className='recipe';
        div.style.opacity=canCraft?'1':'0.4';
        div.innerHTML=`
            <span class="recipe-emoji">${r.emoji}</span>
            <div class="recipe-info">
                <b>${r.name}</b>
                ${r.desc}
            </div>
            ${canCraft?`<button class="recipe-btn" onclick="doCraft('${r.name}')">Craft!</button>`:'<span style="font-size:9px;color:#475569">Need more items</span>'}
        `;
        rDiv.appendChild(div);
    });
}

function doCraft(name){
    const r=RECIPES.find(r=>r.name===name);
    if(!r) return;
    const canCraft=Object.entries(r.needs).every(([item,cnt])=>(inventory[item]||0)>=cnt);
    if(!canCraft){ showMsg('❌ Not enough materials!'); return; }
    // Consume
    Object.entries(r.needs).forEach(([item,cnt])=>{ inventory[item]-=cnt; });
    // Give
    Object.entries(r.makes).forEach(([item,cnt])=>{
        if(item==='armor'){ player.hasArmor=true; showMsg('🥷 PQC Armor equipped! Shor Bots deal less damage!'); }
        else if(item==='zapper'){ player.hasZapper=true; showMsg('⚡ Quantum Zapper ready! Press Z to use!'); }
        else addToInventory(item,cnt);
    });
    showFact(FACTS[Math.floor(Math.random()*FACTS.length)]);
    closeCraft();
    updateHotbarUI();
}

function closeCraft(){ craftOpen=false; document.getElementById('craft-panel').style.display='none'; }

// ── DAY/NIGHT CYCLE ───────────────────────────────────────────────────────────
function updateDayNight(){
    dayTime=(dayTime+1/DAY_LENGTH)%1;
    if(dayTime<0.01&&day>0){
        day++; document.getElementById('h-day').textContent=day;
        enemies=[];
        if(day>1) showMsg('🌅 Day '+day+'! Survived the night! More enemies coming...');
    }
}

function getSkyColor(){
    // dayTime 0=noon 0.25=sunset 0.5=midnight 0.75=sunrise
    if(dayTime<0.25){
        // noon to sunset
        const t=dayTime/0.25;
        return lerpColor('#1a3a6e','#8b4513',t);
    } else if(dayTime<0.5){
        // sunset to midnight
        const t=(dayTime-0.25)/0.25;
        return lerpColor('#8b4513','#020408',t);
    } else if(dayTime<0.75){
        // midnight to sunrise
        const t=(dayTime-0.5)/0.25;
        return lerpColor('#020408','#4a2060',t);
    } else {
        // sunrise to noon
        const t=(dayTime-0.75)/0.25;
        return lerpColor('#4a2060','#1a3a6e',t);
    }
}

function lerpColor(c1,c2,t){
    const r1=parseInt(c1.slice(1,3),16), g1=parseInt(c1.slice(3,5),16), b1=parseInt(c1.slice(5,7),16);
    const r2=parseInt(c2.slice(1,3),16), g2=parseInt(c2.slice(3,5),16), b2=parseInt(c2.slice(5,7),16);
    const r=Math.round(r1+(r2-r1)*t);
    const g=Math.round(g1+(g2-g1)*t);
    const b=Math.round(b1+(b2-b1)*t);
    return `rgb(${r},${g},${b})`;
}

// ── PARTICLES ─────────────────────────────────────────────────────────────────
function spawnParticles(wx,wy,color,n){
    for(let i=0;i<n;i++){
        const a=Math.random()*Math.PI*2, s=1+Math.random()*3;
        particles.push({wx,wy,vx:Math.cos(a)*s,vy:Math.sin(a)*s-1,
            r:2+Math.random()*2,alpha:1,color});
    }
}
function spawnParticlesScreen(sx,sy,color,n){
    // Screen coords version
    spawnParticles(sx+camera.x,sy+camera.y,color,n);
}

// ── DRAW ──────────────────────────────────────────────────────────────────────
function draw(){
    CX.clearRect(0,0,W,H);

    // Sky
    CX.fillStyle=getSkyColor();
    CX.fillRect(0,0,W,H);

    // Stars at night
    if(dayTime>0.4&&dayTime<0.9){
        const starAlpha=Math.min(1,(dayTime-0.4)/0.1)*Math.min(1,(0.9-dayTime)/0.1);
        CX.fillStyle=`rgba(255,255,255,${starAlpha*0.8})`;
        for(let s=0;s<40;s++){
            const sx=(s*137+50)%W, sy=(s*97+20)%H*0.4;
            CX.fillRect(sx,sy,1,1);
        }
    }

    // Sun/Moon
    if(dayTime<0.5){
        // Sun
        const sunX=W*(dayTime/0.5);
        const sunY=H*0.2-Math.sin(dayTime/0.5*Math.PI)*H*0.3;
        CX.fillStyle='#fde68a'; CX.beginPath();
        CX.arc(sunX,sunY,14,0,Math.PI*2); CX.fill();
    } else {
        // Moon
        const moonX=W*((dayTime-0.5)/0.5);
        const moonY=H*0.2-Math.sin((dayTime-0.5)/0.5*Math.PI)*H*0.3;
        CX.fillStyle='#e2e8f0'; CX.beginPath();
        CX.arc(moonX,moonY,10,0,Math.PI*2); CX.fill();
    }

    // Draw visible tiles
    const startTX=Math.floor(camera.x/TS);
    const startTY=Math.floor(camera.y/TS);
    const endTX=Math.min(COLS,startTX+VIEW_W+1);
    const endTY=Math.min(ROWS,startTY+VIEW_H+1);

    for(let ty=Math.max(0,startTY);ty<endTY;ty++){
        for(let tx=Math.max(0,startTX);tx<endTX;tx++){
            const bt=getTile(tx,ty);
            if(bt==='sky'||bt==='air') continue;
            const bd=BLOCKS[bt];
            if(!bd) continue;

            const sx=tx*TS-camera.x;
            const sy=ty*TS-camera.y;

            // Block background
            if(bd.color){
                CX.fillStyle=bd.color;
                CX.fillRect(sx,sy,TS,TS);
            }

            // Block border for solid blocks
            if(bd.solid){
                CX.strokeStyle='rgba(0,0,0,0.25)';
                CX.lineWidth=0.5;
                CX.strokeRect(sx,sy,TS,TS);
            }

            // Block emoji
            if(bd.emoji){
                CX.font='14px serif';
                CX.textAlign='center';
                CX.textBaseline='middle';
                CX.fillText(bd.emoji,sx+TS/2,sy+TS/2);
            }

            // Mine progress overlay
            if(mineBlock&&mineBlock.tx===tx&&mineBlock.ty===ty){
                const pct=mineBlock.progress/mineBlock.maxProgress;
                CX.fillStyle=`rgba(0,0,0,${pct*0.7})`;
                CX.fillRect(sx,sy,TS,TS);
                // Crack lines
                CX.strokeStyle='rgba(255,255,255,0.5)';
                CX.lineWidth=1;
                for(let ci=0;ci<Math.floor(pct*5);ci++){
                    CX.beginPath();
                    CX.moveTo(sx+5+ci*5,sy+5);
                    CX.lineTo(sx+8+ci*5,sy+TS-5);
                    CX.stroke();
                }
            }
        }
    }

    // Draw particles
    particles.forEach(p=>{
        const sx=p.wx-camera.x, sy=p.wy-camera.y;
        CX.beginPath(); CX.arc(sx,sy,p.r,0,Math.PI*2);
        CX.fillStyle=p.color+Math.floor(p.alpha*255).toString(16).padStart(2,'0');
        CX.fill();
    });

    // Draw enemies
    enemies.forEach(e=>{
        const sx=e.x-camera.x, sy=e.y-camera.y;
        // Shadow
        CX.fillStyle='rgba(0,0,0,0.3)';
        CX.ellipse(sx+e.w/2,sy+e.h+2,e.w/2,4,0,0,Math.PI*2);
        CX.fill();
        // Body
        CX.font='22px serif';
        CX.textAlign='center'; CX.textBaseline='bottom';
        CX.fillText('👾',sx+e.w/2,sy+e.h);
        // HP bar
        CX.fillStyle='#1e293b'; CX.fillRect(sx,sy-6,e.w,3);
        CX.fillStyle='#ef4444'; CX.fillRect(sx,sy-6,e.w*(e.hp/3),3);
    });

    // Draw player
    const px=player.x-camera.x;
    const py=player.y-camera.y;
    // Shadow
    CX.fillStyle='rgba(0,0,0,0.25)';
    CX.ellipse(px+player.w/2,py+player.h+2,player.w/2,4,0,0,Math.PI*2);
    CX.fill();
    // Player body
    CX.save();
    CX.font='22px serif';
    CX.textAlign='center'; CX.textBaseline='bottom';
    if(player.facing<0){
        CX.scale(-1,1);
        CX.fillText(player.hasArmor?'🥷':'🧑‍💻',-(px+player.w/2),py+player.h);
    } else {
        CX.fillText(player.hasArmor?'🥷':'🧑‍💻',px+player.w/2,py+player.h);
    }
    CX.restore();

    // Mining cursor highlight
    const mtx=Math.floor((mouseWorld.x)/TS);
    const mty=Math.floor((mouseWorld.y)/TS);
    const msx=mtx*TS-camera.x, msy=mty*TS-camera.y;
    if(msx>=-TS&&msx<W+TS&&msy>=-TS&&msy<H+TS){
        CX.strokeStyle='rgba(255,255,255,0.4)';
        CX.lineWidth=2;
        CX.strokeRect(msx,msy,TS,TS);
    }

    // Dark night overlay
    if(dayTime>0.45&&dayTime<0.95){
        const nightAlpha=Math.min(0.55,
            Math.min((dayTime-0.45)/0.1,(0.95-dayTime)/0.1)*0.55);
        CX.fillStyle=`rgba(0,0,20,${nightAlpha})`;
        CX.fillRect(0,0,W,H);
    }

    // Game over screen
    if(gameOver){
        CX.fillStyle='rgba(0,0,0,0.75)';
        CX.fillRect(0,0,W,H);
        CX.fillStyle='#ef4444'; CX.font='bold 28px sans-serif';
        CX.textAlign='center'; CX.fillText('💀 GAME OVER',W/2,H/2-20);
        CX.fillStyle='white'; CX.font='14px sans-serif';
        CX.fillText('Score: '+score+' | Day: '+day,W/2,H/2+10);
        CX.fillStyle='#60a5fa';
        CX.fillText('Press R to restart',W/2,H/2+35);
    }
}

// ── UI UPDATES ────────────────────────────────────────────────────────────────
function updateHearts(){
    const h=document.getElementById('hearts');
    const full=Math.floor(player.hp);
    const half=player.hp%1>=0.5?1:0;
    const empty=player.maxHp-full-half;
    h.textContent='❤️'.repeat(full)+(half?'🤍':'')+'🖤'.repeat(empty);
}

function updateHotbarUI(){
    const hb=document.getElementById('hotbar');
    hb.innerHTML='';
    hotbar.forEach((slot,i)=>{
        const div=document.createElement('div');
        div.className='hslot'+(i===activeSlot?' active':'');
        div.innerHTML=`
            <span class="hs-num">${i+1}</span>
            <span class="hs-emoji">${slot.item?(BLOCKS[slot.item+'_block']||BLOCKS[slot.item])&&(BLOCKS[slot.item]?.emoji||'📦'):''}${slot.item&&!BLOCKS[slot.item]?'📦':''}</span>
            <span style="font-size:8px;color:#94a3b8">${slot.item||''}</span>
            ${slot.count>0?`<span class="hs-count">${slot.count}</span>`:''}
        `;
        div.onclick=()=>{ activeSlot=i; updateHotbarUI(); };
        hb.appendChild(div);
    });
}

function showMsg(msg){ document.getElementById('hud-msg').textContent=msg; }

let factTimer=null;
function showFact(text){
    const el=document.getElementById('fact-toast');
    el.textContent=text; el.classList.add('show');
    if(factTimer) clearTimeout(factTimer);
    factTimer=setTimeout(()=>el.classList.remove('show'),4500);
}

// ── INPUT ─────────────────────────────────────────────────────────────────────
document.addEventListener('keydown',e=>{
    keys[e.key]=true;
    if(e.key==='r'||e.key==='R'){ if(gameOver) initGame(); }
    if(e.key==='c'||e.key==='C'){ craftOpen?closeCraft():openCraft(); }
    if(e.key==='z'||e.key==='Z'){
        if(player.hasZapper&&enemies.length>0){
            const nearest=enemies.reduce((a,b)=>
                Math.hypot(a.x-player.x,a.y-player.y)<Math.hypot(b.x-player.x,b.y-player.y)?a:b);
            nearest.hp-=2;
            spawnParticles(nearest.x+10,nearest.y+10,'#fbbf24',10);
            if(nearest.hp<=0) enemies=enemies.filter(e=>e!==nearest);
            showMsg('⚡ Quantum Zapper fired!');
        }
    }
    // 1-9 hotbar
    if(e.key>='1'&&e.key<='9'){ activeSlot=parseInt(e.key)-1; updateHotbarUI(); }
    e.preventDefault();
});
document.addEventListener('keyup',e=>{ keys[e.key]=false; });

// Mouse for mining and placing
CV.addEventListener('mousemove',e=>{
    const r=CV.getBoundingClientRect();
    const mx=(e.clientX-r.left)*(W/r.width);
    const my=(e.clientY-r.top)*(H/r.height);
    mouseWorld.x=mx+camera.x;
    mouseWorld.y=my+camera.y;
});

CV.addEventListener('mousedown',e=>{
    if(craftOpen) return;
    const r=CV.getBoundingClientRect();
    const mx=(e.clientX-r.left)*(W/r.width);
    const my=(e.clientY-r.top)*(H/r.height);
    const tx=Math.floor((mx+camera.x)/TS);
    const ty=Math.floor((my+camera.y)/TS);

    if(e.button===0){
        // Left click = mine
        const bt=getTile(tx,ty);
        const bd=BLOCKS[bt];
        if(bd&&bd.mineable) startMining(tx,ty);
    } else if(e.button===2){
        // Right click = place
        placeBlock(tx,ty);
    }
});

CV.addEventListener('mouseup',e=>{
    if(e.button===0) mineBlock=null;
});

CV.addEventListener('contextmenu',e=>e.preventDefault());

// ── INIT ─────────────────────────────────────────────────────────────────────
function initGame(){
    generateWorld();
    enemies=[]; particles=[];
    score=0; day=1; dayTime=0;
    gameOver=false; craftOpen=false;
    player.hp=5; player.hasArmor=false; player.hasZapper=false;
    inventory={};
    hotbar=hotbar.map(()=>({item:'',count:0}));
    mineBlock=null;
    document.getElementById('h-score').textContent=0;
    document.getElementById('h-day').textContent=1;
    updateHearts();
    updateHotbarUI();
    showMsg('⛏️ Click blocks to mine! Arrow keys to move. C to craft. Right-click to place!');
}

// ── GAME LOOP ─────────────────────────────────────────────────────────────────
let frame=0;
function loop(){
    requestAnimationFrame(loop);
    if(!gameOver){
        updatePlayer();
        updateEnemies();
        updateDayNight();
        updateMining();
        // Update particles
        particles.forEach(p=>{
            p.wx+=p.vx; p.wy+=p.vy; p.vy+=0.1;
            p.alpha-=0.03; p.r*=0.96;
        });
        particles=particles.filter(p=>p.alpha>0);
        frame++;
    }
    draw();
}

initGame();
loop();
</script>
</body>
</html>
""", height=520)
