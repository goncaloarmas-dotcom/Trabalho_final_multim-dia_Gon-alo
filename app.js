"use strict";
/* Brain Training Hub - camada de navegador.
   Toda a lógica (regras, tempo, validação, pontuação) é feita em Python (pasta game/),
   executado no próprio navegador com o Pyodide. Este ficheiro apenas: carrega o Python,
   mostra o estado, anima, toca sons e envia as ações do jogador ao Python. */

const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const PAGES = ["home", "logic", "reaction", "memory", "results"];
const STEP = { logic: 1, reaction: 2, memory: 3, results: 4 };
const RING = 276.46;

let bridge = null, cfg = { reaction_limit: 10, logic_max_tries: 10 }, L = null;
let tick = null, wait = null, memT = [], busy = false, gen = 0;
let mem = { input: false }, memChain = Promise.resolve();

const getBest = () => { try { return +localStorage.getItem("bthBest3") || 0; } catch { return 0; } };
const setBest = (v) => { try { localStorage.setItem("bthBest3", v); } catch { /* ignora */ } };

/* ---------- Comunicação com o Python (Pyodide) ---------- */
const PY_FILES = ["__init__.py", "answers.py", "data.py", "engine.py", "bridge.py"];

async function loadPython() {
    const pyodide = await loadPyodide();
    pyodide.FS.mkdir("/app");
    pyodide.FS.mkdir("/app/game");
    for (const f of PY_FILES) {
        const r = await fetch("game/" + f);
        if (!r.ok) throw new Error("Não foi possível carregar game/" + f);
        pyodide.FS.writeFile("/app/game/" + f, await r.text());
    }
    pyodide.runPython("import sys\nsys.path.insert(0, '/app')");
    bridge = pyodide.pyimport("game.bridge");
}

async function api(route, data = {}) {
    try {
        const d = JSON.parse(bridge.handle(route, JSON.stringify(data)));
        if (d.error) throw new Error(d.error);
        return d;
    } catch (err) { console.error(err); alert("Ocorreu um erro no jogo. Recarrega a página."); return null; }
}

async function newGame() {
    const d = await api("new");
    if (!d) return false;
    cfg = d.config; L = d.logic;
    return true;
}

/* ---------- Efeitos (som e imagem) ---------- */
let scareT = null;
function scare() {
    const el = $("#scare");
    el.hidden = false;
    el.style.animation = "none"; void el.offsetWidth; el.style.animation = "";
    try {
        const ac = beep.ac || (beep.ac = new AudioContext()), o = ac.createOscillator(), g = ac.createGain();
        o.type = "sawtooth"; o.frequency.setValueAtTime(140, ac.currentTime); o.frequency.exponentialRampToValueAtTime(40, ac.currentTime + 0.8);
        g.gain.setValueAtTime(0.25, ac.currentTime); g.gain.linearRampToValueAtTime(0, ac.currentTime + 0.9);
        o.connect(g); g.connect(ac.destination); o.start(); o.stop(ac.currentTime + 0.9);
    } catch { /* sem som */ }
    clearTimeout(scareT); scareT = setTimeout(() => (el.hidden = true), 1000);
}

function fb(el, msg, type) { el.textContent = msg; el.className = `feedback ${type}`; el.hidden = false; }
function clearTimers() {
    clearInterval(tick); clearTimeout(wait); tick = wait = null; memT.forEach(clearTimeout); memT = [];
    $("#page-reaction").classList.remove("shake");
    $("#explosion").hidden = true;
}

function go(page) {
    gen++; busy = false;
    clearTimers();
    PAGES.forEach((p) => ($("#page-" + p).hidden = p !== page));
    $("#stepper").hidden = page === "home";
    $$("#stepper li").forEach((li, i) => {
        li.classList.toggle("active", i + 1 === STEP[page]);
        li.classList.toggle("done", i + 1 < STEP[page]);
    });
    window.scrollTo({ top: 0 });
    ({ logic: renderLogic, reaction: renderChallenge, memory: renderMemory, results: renderResults }[page] || (() => {}))();
}

/* ---------- 1. Logic ---------- */
function renderLogic() {
    $("#range-fill").style.left = `${L.lo - 1}%`;
    $("#range-fill").style.width = `${L.hi - L.lo + 1}%`;
    $("#range-text").textContent = L.range_text;
    $("#dots").replaceChildren(...Array.from({ length: L.max_tries }, (_, i) => Object.assign(document.createElement("span"), { className: i < L.tries ? "used" : "" })));
    $("#history").replaceChildren(...L.guesses.map((g) => Object.assign(document.createElement("span"), {
        className: "chip" + (g.hint === "ok" ? " ok" : ""), textContent: g.hint === "ok" ? `${g.n} ✓` : `${g.n} ${g.hint === "down" ? "↓" : "↑"}`,
    })));
    if (L.tries === 0) $("#logic-feedback").hidden = true;
    $("#logic-form").hidden = L.done;
    $("#logic-finished").hidden = !L.done;
    if (!L.done) $("#logic-guess").focus();
}

$("#logic-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = $("#logic-guess"), f = $("#logic-feedback");
    const d = await api("logic/guess", { guess: input.value });
    if (!d) return;
    fb(f, d.message, d.type);
    if (d.status === "invalid") return;
    L = d.view;
    input.value = "";
    renderLogic();
});

/* ---------- 3. Reaction ---------- */
function paintTimer(rem) {
    const limit = cfg.reaction_limit;
    $("#ring").style.strokeDashoffset = RING * (1 - rem / limit);
    $("#timer-value").textContent = rem.toFixed(1);
    const t = $("#timer");
    t.className = "timer" + (rem <= 3 ? " danger" : rem <= 5 ? " warn" : "");
    $("#timer-icon").textContent = rem <= 3 ? "💣" : rem <= 5 ? "⚠️" : "⏱️";
}

async function renderChallenge() {
    const g = gen;
    const d = await api("reaction/next");
    if (!d || g !== gen) return;
    if (d.finished) return go("memory");
    busy = false;
    $("#reaction-progress").textContent = d.progress_text;
    $("#reaction-question").textContent = d.question;
    $("#reaction-feedback").hidden = true;
    $("#explosion").hidden = true;
    const inp = $("#reaction-answer");
    inp.value = ""; inp.disabled = false;
    $("#reaction-form button").disabled = false;
    inp.focus();
    // o tempo oficial é medido pelo Python; aqui só se desenha a contagem decrescente
    const t0 = performance.now() - (cfg.reaction_limit - d.remaining) * 1000;
    paintTimer(d.remaining);
    clearInterval(tick);
    tick = setInterval(() => {
        const rem = Math.max(0, cfg.reaction_limit - (performance.now() - t0) / 1000);
        paintTimer(rem);
        if (rem <= 0) settle("", true);
    }, 50);
}

function boom() {
    const page = $("#page-reaction"), box = $("#explosion");
    page.classList.remove("shake"); void page.offsetWidth; page.classList.add("shake");
    const label = Object.assign(document.createElement("strong"), { textContent: "💥 BOOM!" });
    const parts = Array.from({ length: 16 }, (_, i) => {
        const p = document.createElement("span"), a = (i / 16) * 6.283, d = 70 + Math.random() * 110;
        p.className = "p"; p.textContent = ["🔥", "💥", "✨", "💨"][i % 4];
        p.style.setProperty("--x", `${Math.cos(a) * d}px`); p.style.setProperty("--y", `${Math.sin(a) * d * 0.5}px`);
        return p;
    });
    box.replaceChildren(label, ...parts); box.hidden = false;
}

async function settle(answer, timedOut) {
    if (busy) return;
    busy = true;
    const g = gen;
    clearInterval(tick);
    $("#reaction-answer").disabled = true;
    $("#reaction-form button").disabled = true;
    const d = await api("reaction/answer", { answer, timeout: timedOut });
    if (!d || g !== gen) return;
    if (d.status === "pending") {      // o Python ainda não considera o tempo esgotado
        busy = false;
        wait = setTimeout(() => settle("", true), Math.ceil(d.remaining * 1000) + 30);
        return;
    }
    if (d.status === "idle") return;
    const f = $("#reaction-feedback");
    if (!d.ok) scare();
    if (d.timed_out) { boom(); paintTimer(0); $("#timer-icon").textContent = "💥"; }
    fb(f, d.message, d.type);
    wait = setTimeout(() => (d.finished ? go("memory") : renderChallenge()), d.delay_ms);
}

$("#reaction-form").addEventListener("submit", (e) => {
    e.preventDefault();
    settle($("#reaction-answer").value, false);
});

/* ---------- 4. Memory Sequence ---------- */
const pads = $$(".pad");
const mt = (fn, ms) => memT.push(setTimeout(fn, ms));
function beep(i) {
    try {
        const ac = beep.ac || (beep.ac = new AudioContext()), o = ac.createOscillator(), g = ac.createGain();
        o.frequency.value = [330, 262, 392, 494][i]; g.gain.value = 0.07;
        o.connect(g); g.connect(ac.destination); o.start(); o.stop(ac.currentTime + 0.22);
    } catch { /* sem som */ }
}
function flashPad(i, ms = 380) { pads[i].classList.add("lit"); beep(i); mt(() => pads[i].classList.remove("lit"), ms); }

function renderMemory() {
    mem = { input: false };
    $("#mem-status").textContent = cfg.memory_intro || "";
    $("#mem-start").hidden = false; $("#mem-next").hidden = true;
}
function playRound(d) {            // a sequência e os tempos vêm do Python
    mem.input = false;
    mt(() => ($("#mem-status").textContent = d.watch_text), d.delay_ms);
    d.sequence.forEach((n, k) => mt(() => flashPad(n, d.flash_ms), d.delay_ms + d.lead_ms + k * d.step_ms));
    mt(() => { mem.input = true; $("#mem-status").textContent = d.turn_text; }, d.delay_ms + d.lead_ms + d.sequence.length * d.step_ms);
}
function memEnd(msg) {
    mem.input = false;
    $("#mem-status").textContent = msg;
    $("#mem-next").hidden = false; $("#mem-next").focus();
}
$("#mem-start").addEventListener("click", async () => {
    $("#mem-start").hidden = true;
    const g = gen, d = await api("memory/start");
    if (!d) { $("#mem-start").hidden = false; return; }
    if (g === gen) playRound(d);
});
async function sendPress(i, g) {
    if (!mem.input) return;
    const d = await api("memory/press", { pad: i });
    if (!d || g !== gen || d.result === "ignored" || d.result === "continue") return;
    if (d.result === "round_complete") return playRound(d);
    if (d.result === "wrong") scare();
    memEnd(d.message);             // "wrong" ou "perfect"
}
pads.forEach((p, i) => p.addEventListener("click", () => {
    if (!mem.input) return;
    flashPad(i, 200);
    const g = gen;
    memChain = memChain.then(() => sendPress(i, g));   // mantém a ordem dos cliques
}));
$("#mem-next").addEventListener("click", () => go("results"));

/* ---------- Resultados ---------- */
async function renderResults() {
    const g = gen;
    const d = await api("results", { best: getBest() });
    if (!d || g !== gen) return;
    $("#final-total").textContent = d.total;
    $("#final-rating").textContent = d.rating_text;
    $("#breakdown").replaceChildren(...d.games.map((game) => {
        const row = document.createElement("div"), fill = document.createElement("div"), bar = document.createElement("div");
        const name = Object.assign(document.createElement("span"), { textContent: game.name });
        const val = Object.assign(document.createElement("b"), { textContent: `${game.value}/${game.max}` });
        bar.className = "bar"; bar.appendChild(fill);
        row.append(name, bar, val);
        requestAnimationFrame(() => (fill.style.width = `${game.percent}%`));
        return row;
    }));
    const ring = $("#final-ring");
    ring.style.strokeDashoffset = 439.8;
    setTimeout(() => (ring.style.strokeDashoffset = 439.8 * (1 - d.total / d.max_total)), 80);

    const rec = $("#final-record");
    rec.hidden = !d.is_record;
    rec.textContent = d.record_text;
    if (d.is_record) { setBest(d.best); $("#best").textContent = d.best; }

    $("#review").replaceChildren(...d.review.map((r) =>
        Object.assign(document.createElement("p"), { className: r.ok ? "ok" : "no", textContent: r.text })));
}

/* ---------- Navegação ---------- */
async function restart() { if (bridge && await newGame()) go("home"); }
$("#start-button").addEventListener("click", () => { if (bridge) go("logic"); });
$("#to-quiz-button").addEventListener("click", () => go("reaction"));
$("#play-again-button").addEventListener("click", restart);
$("#brand").addEventListener("click", (e) => { e.preventDefault(); restart(); });

/* ---------- Arranque: carrega o Python e só depois liberta o botão ---------- */
$("#best").textContent = getBest();
(async () => {
    const btn = $("#start-button"), label = btn.textContent;
    btn.disabled = true; btn.textContent = "A carregar o Python…";
    try {
        await loadPython();
        await newGame();
        btn.disabled = false; btn.textContent = label;
    } catch (err) {
        console.error(err);
        btn.textContent = "Não foi possível carregar o Python. Verifica a ligação e recarrega a página.";
    }
})();
