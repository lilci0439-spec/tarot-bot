// СКРИПТ ЗАГРУЗКИ
setTimeout(() => {
    const splash = document.getElementById('splash');
    if(splash) {
        splash.classList.add('hide');
        setTimeout(() => splash.remove(), 500);
    }
}, 2000);

const tg = window.Telegram.WebApp;
tg.expand();

// =========================================
// ЛОГИКА ИГРЫ (CANVAS)
// =========================================
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
let player = { x: 2, y: 7 };
let stage = 1;
let record = Number(localStorage.getItem("oracleRecord") || 0);
let gameRunning = false;
let animationId = null;
let obstacles = [];
let gameOver = false;
const LANES = 5;
const ROWS = 8;

function resizeCanvas() {
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    canvas.width = rect.width * ratio;
    canvas.height = rect.height * ratio;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    drawGame();
}

window.addEventListener("resize", resizeCanvas);

function laneWidth() { return canvas.clientWidth / LANES; }
function rowHeight() { return canvas.clientHeight / ROWS; }
function playerPosition() { return { x: laneWidth() * (player.x + 0.5), y: rowHeight() * (player.y + 0.5) }; }
function laneCenterY(row) { return rowHeight() * (row + 0.5); }

document.querySelector('label[for="game-open"]').addEventListener('click', () => {
    setTimeout(() => {
        resizeCanvas();
        startGame();
    }, 100);
});

function startGame() {
    player = { x: 2, y: 7 };
    stage = 1;
    obstacles = [];
    gameOver = false;
    gameRunning = true;
    createObstacles();
    if (animationId) cancelAnimationFrame(animationId);
    animationId = requestAnimationFrame(gameLoop);
}

function createObstacles() {
    obstacles = [];
    for (let row = 1; row < ROWS - 1; row++) {
        if (Math.random() < 0.6) {
            obstacles.push({ x: Math.floor(Math.random() * LANES), y: row, color: ["#e63c61", "#e6ad3e", "#4168ed", "#c7b7d6"][Math.floor(Math.random() * 4)] });
        }
    }
}

function drawGame() {
    if (!canvas || !canvas.clientWidth) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Дорога
    ctx.fillStyle = "#25232c"; ctx.fillRect(0, 0, canvas.clientWidth, canvas.clientHeight);
    ctx.strokeStyle = "#b4a8b8"; ctx.lineWidth = 2; ctx.setLineDash([15, 15]);
    for (let i = 1; i < LANES; i++) { ctx.beginPath(); ctx.moveTo(i * laneWidth(), 0); ctx.lineTo(i * laneWidth(), canvas.clientHeight); ctx.stroke(); }
    ctx.setLineDash([]);

    // Машины
    for (const obs of obstacles) {
        const x = (obs.x + 0.5) * laneWidth(), y = laneCenterY(obs.y);
        ctx.fillStyle = obs.color; ctx.beginPath(); ctx.roundRect(x - laneWidth() * 0.35, y - 15, laneWidth() * 0.7, 30, 8); ctx.fill();
        ctx.fillStyle = "#222"; ctx.fillRect(x - laneWidth() * 0.2, y - 10, laneWidth() * 0.4, 8);
    }
    
    // Шар
    const w = canvas.clientWidth, h = canvas.clientHeight;
    ctx.fillStyle = "#555"; ctx.beginPath(); ctx.arc(w/2, h-20, 30, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = "#d3c6db"; ctx.stroke();

    // Заяц
    const pos = playerPosition();
    ctx.textAlign = "center"; ctx.font = "35px Arial"; ctx.fillText("🐇", pos.x, pos.y + 10);
}

function movePlayer(dx, dy) {
    if (!gameRunning || gameOver) return;
    const nextX = player.x + dx, nextY = player.y + dy;
    if (nextX >= 0 && nextX < LANES && nextY >= 0 && nextY < ROWS) {
        player.x = nextX; player.y = nextY;
        if (obstacles.some(o => o.x === player.x && o.y === player.y)) { endGame("Машина сбила зайца!"); return; }
        if (player.y === 0) { stage++; player = { x: 2, y: 7 }; createObstacles(); document.getElementById('distanceLabel').textContent = stage + " м"; }
        drawGame();
    }
}

function endGame(reason) {
    gameOver = true; gameRunning = false;
    if (animationId) cancelAnimationFrame(animationId);
    if (stage > record) { record = stage; localStorage.setItem("oracleRecord", record); }
    setTimeout(() => {
        tg.showAlert(reason + "\nПройдено: " + stage + " м");
        document.getElementById('game-open').checked = false;
    }, 100);
}

function gameLoop() { if (!gameRunning || gameOver) return; drawGame(); animationId = requestAnimationFrame(gameLoop); }

let touchStartX = 0, touchStartY = 0;
canvas.addEventListener("touchstart", e => { touchStartX = e.changedTouches[0].clientX; touchStartY = e.changedTouches[0].clientY; }, { passive: true });
canvas.addEventListener("touchend", e => {
    const dx = e.changedTouches[0].clientX - touchStartX, dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < 20) return;
    if (Math.abs(dx) > Math.abs(dy)) movePlayer(dx > 0 ? 1 : -1, 0); else movePlayer(0, dy > 0 ? 1 : -1);
}, { passive: true });

window.addEventListener("keydown", e => {
    const keys = { ArrowUp: [0,-1], ArrowDown: [0,1], ArrowLeft: [-1,0], ArrowRight: [1,0] };
    if (keys[e.key]) { e.preventDefault(); movePlayer(...keys[e.key]); }
});
