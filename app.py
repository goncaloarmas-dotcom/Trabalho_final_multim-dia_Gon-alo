"""Brain Training Hub - aplicação web em Python (apenas biblioteca padrão).

Ficheiros do projeto:
  app.py     - servidor, lógica dos jogos, pontuação, validação e sons (este ficheiro)
  index.html - estrutura das páginas (moldura + um bloco <template> por ecrã)
  style.css  - design, animações e responsividade

Executar:  python app.py   e abrir  http://localhost:8000
"""

import html
import io
import math
import os
import random
import re
import secrets
import struct
import time
import unicodedata
import wave
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from string import Template
from urllib.parse import parse_qs, urlsplit

BASE = Path(__file__).resolve().parent


# ===========================================================================
# DADOS: banco de desafios e validação de respostas
# ===========================================================================
# Cada desafio: pergunta, resposta certa e lista de respostas aceitáveis.
reaction_bank = [
    # --- Matemática mental ---
    {"question": "Quanto é 17 + 28?", "answer": "45", "acceptable": ["45"]},
    {"question": "Quanto é 12 × 12?", "answer": "144", "acceptable": ["144"]},
    {"question": "Quanto é 200 - 76?", "answer": "124", "acceptable": ["124"]},
    {"question": "Quanto é 81 ÷ 9?", "answer": "9", "acceptable": ["9"]},
    {"question": "Quanto é 15 × 6?", "answer": "90", "acceptable": ["90"]},
    {"question": "Quanto é 250 + 175?", "answer": "425", "acceptable": ["425"]},
    {"question": "Quanto é metade de 186?", "answer": "93", "acceptable": ["93"]},
    {"question": "Quanto é 11 × 11?", "answer": "121", "acceptable": ["121"]},
    {"question": "Quanto é 1000 - 375?", "answer": "625", "acceptable": ["625"]},
    {"question": "Quanto é 144 ÷ 8?", "answer": "18", "acceptable": ["18"]},
    {"question": "Quanto é 8 × 9?", "answer": "72", "acceptable": ["72"]},
    {"question": "Quanto é 15 × 4?", "answer": "60", "acceptable": ["60"]},
    {"question": "Quanto é 100 - 37?", "answer": "63", "acceptable": ["63"]},
    {"question": "Quanto é 144 ÷ 9?", "answer": "16", "acceptable": ["16"]},
    {"question": "Quanto é 7²?", "answer": "49", "acceptable": ["49"]},
    {"question": "Quanto é 25 × 4?", "answer": "100", "acceptable": ["100"]},

    # --- Sequências numéricas e padrões ---
    {"question": "Completa: 2, 6, 10, 14, ...", "answer": "18", "acceptable": ["18"]},
    {"question": "Completa: 2, 4, 8, 16, ...", "answer": "32", "acceptable": ["32"]},
    {"question": "Completa: 5, 10, 15, 20, ...", "answer": "25", "acceptable": ["25"]},
    {"question": "Completa: 1, 4, 9, 16, ...", "answer": "25", "acceptable": ["25"]},
    {"question": "Completa: 3, 6, 12, 24, ...", "answer": "48", "acceptable": ["48"]},
    {"question": "Completa: 100, 90, 80, 70, ...", "answer": "60", "acceptable": ["60"]},
    {"question": "Completa: 1, 1, 2, 3, 5, 8, ...", "answer": "13", "acceptable": ["13"]},
    {"question": "Completa: 10, 20, 30, 40, ...", "answer": "50", "acceptable": ["50"]},
    {"question": "Completa: 2, 5, 8, 11, ...", "answer": "14", "acceptable": ["14"]},
    {"question": "Completa: 50, 45, 40, 35, ...", "answer": "30", "acceptable": ["30"]},

    # --- Raciocínio lógico ---
    {
        "question": "Qual não pertence ao grupo: maçã, banana, cenoura, pera?",
        "answer": "Cenoura",
        "acceptable": ["cenoura"],
    },
    {
        "question": "Se ontem foi segunda-feira, que dia será amanhã?",
        "answer": "Quarta-feira",
        "acceptable": ["quarta-feira", "quarta feira", "quarta", "quartafeira"],
    },
    {
        "question": "Tenho 3 maçãs e dou 1. Quantas me restam?",
        "answer": "2",
        "acceptable": ["2", "duas", "2 macas"],
    },
    {
        "question": "Quantos meses têm 28 dias?",
        "answer": "12",
        "acceptable": ["12", "todos", "todos os 12", "12 meses", "os 12"],
    },
    {
        "question": "Se um relógio marca 3 horas, qual será a hora daqui a 5 horas?",
        "answer": "8 horas",
        "acceptable": ["8", "8h", "8 horas", "oito"],
    },
    {
        "question": "Um pai tem 40 anos e o filho 10. Daqui a 5 anos, qual será a diferença de idades?",
        "answer": "30 anos",
        "acceptable": ["30", "30 anos", "trinta"],
    },
    {
        "question": "Se hoje é domingo, que dia foi anteontem?",
        "answer": "Sexta-feira",
        "acceptable": ["sexta-feira", "sexta feira", "sexta", "sextafeira"],
    },
    {
        "question": "Qual não pertence ao grupo: cão, gato, leão, carro?",
        "answer": "Carro",
        "acceptable": ["carro"],
    },

    # --- Cultura geral ---
    {"question": "Qual é a capital de Portugal?", "answer": "Lisboa", "acceptable": ["lisboa"]},
    {"question": "Qual é o maior planeta do Sistema Solar?", "answer": "Júpiter", "acceptable": ["jupiter", "júpiter"]},
    {"question": "Quantos dias tem uma semana?", "answer": "7", "acceptable": ["7", "sete", "7 dias"]},
    {"question": "Qual é o oceano entre a Europa e a América?", "answer": "Atlântico", "acceptable": ["atlantico", "atlântico", "oceano atlantico"]},
    {"question": "Qual é a língua oficial do Brasil?", "answer": "Português", "acceptable": ["portugues", "português"]},
    {"question": "Quantas cores tem tradicionalmente o arco-íris?", "answer": "7", "acceptable": ["7", "sete", "7 cores"]},
    {"question": "Qual é a capital de França?", "answer": "Paris", "acceptable": ["paris"]},

    # --- Desafios rápidos ---
    {"question": "Quantas letras tem a palavra COMPUTADOR?", "answer": "10", "acceptable": ["10", "dez", "10 letras"]},
    {"question": "Qual é o contrário de aumentar?", "answer": "Diminuir", "acceptable": ["diminuir", "reduzir", "baixar"]},
    {"question": "Qual é a terceira letra do alfabeto?", "answer": "C", "acceptable": ["c"]},
    {"question": "Quantos segundos existem num minuto?", "answer": "60", "acceptable": ["60", "sessenta", "60 segundos", "60s"]},
    {"question": "Qual é o dobro de 37?", "answer": "74", "acceptable": ["74"]},
    {"question": "Se tens 20 euros e gastas 7, quanto sobra?", "answer": "13 euros", "acceptable": ["13", "13€", "13 euros", "treze"]},
    {"question": "Quanto é 6 × 7?", "answer": "42", "acceptable": ["42"]},
    {"question": "Quanto é 50 ÷ 2?", "answer": "25", "acceptable": ["25"]},
    {"question": "Qual é o triplo de 9?", "answer": "27", "acceptable": ["27"]},
    {"question": "Quantos lados tem um quadrado?", "answer": "4", "acceptable": ["4", "quatro"]},
    {"question": "Quanto é 100 ÷ 4?", "answer": "25", "acceptable": ["25"]},
    {"question": "Qual é o contrário de quente?", "answer": "Frio", "acceptable": ["frio"]},
    {"question": "Quantas horas tem um dia?", "answer": "24", "acceptable": ["24", "vinte e quatro", "24 horas", "24h"]},
    {"question": "Quanto é 9 × 9?", "answer": "81", "acceptable": ["81"]},
]


# ---------------------------------------------------------------------------
# Validação inteligente de respostas
# ---------------------------------------------------------------------------

def normalize_answer(text):
    """Remove acentos, maiúsculas, pontuação e aspas; normaliza espaços e traços."""
    if text is None:
        return ""
    text = unicodedata.normalize("NFD", str(text).strip().lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")  # acentos
    text = re.sub(r"['\"“”‘’`]", "", text)       # aspas
    text = re.sub(r"[.,!?;:]", "", text)         # pontuação
    text = re.sub(r"[-_–—]", " ", text)          # traços -> espaço
    text = re.sub(r"\s+", " ", text)             # espaços múltiplos
    return text.strip()


def strip_all_spaces(text):
    """Comparação sem espaços (ex.: 'quarta feira' vs 'quartafeira')."""
    return re.sub(r"\s+", "", normalize_answer(text))


def check_reaction_answer(user_answer, challenge):
    """Devolve True se a resposta do utilizador for aceite para o desafio."""
    raw_user = str(user_answer or "").strip()
    if not raw_user:
        return False

    norm_user = normalize_answer(raw_user)
    compact_user = strip_all_spaces(raw_user)

    # 1. Igualdade direta com a resposta certa
    if norm_user == normalize_answer(challenge["answer"]) or compact_user == strip_all_spaces(challenge["answer"]):
        return True

    # 2. Lista de respostas aceitáveis
    for alt in challenge.get("acceptable", []):
        if norm_user == normalize_answer(alt) or compact_user == strip_all_spaces(alt):
            return True

    # 3. Respostas numéricas com/sem unidades (ex.: "8 horas" -> "8")
    match = re.match(
        r"^(\d+)\s*(horas|anos|euros|dias|minutos|macas|cores|letras|s|h)?$",
        challenge["answer"],
        re.IGNORECASE,
    )
    if match:
        n = match.group(1)
        if norm_user in (n, f"{n}h", f"{n}€", f"{n} euros", f"{n} eur",
                         f"{n} horas", f"{n} anos", f"{n} dias"):
            return True

    return False

# ===========================================================================
# SONS (gerados em memória)
# ===========================================================================
RATE = 22050
PAD_FREQS = [330, 262, 392, 494]


def _wav(samples):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, s)) * 32767)) for s in samples))
    return buf.getvalue()


def _pad_tone(freq):
    n = int(RATE * 0.22)
    return _wav(0.25 * math.sin(2 * math.pi * freq * i / RATE) * (1 - i / n) for i in range(n))


def _scare():
    """Onda dente-de-serra a descer de 140 Hz para 40 Hz (0,9 s)."""
    n = int(RATE * 0.9)
    out, phase = [], 0.0
    for i in range(n):
        t = i / n
        freq = 140 * (40 / 140) ** (t / 0.89 if t < 0.89 else 1)
        phase = (phase + freq / RATE) % 1.0
        out.append((2 * phase - 1) * 0.5 * (1 - t))
    return _wav(out)


SOUNDS = {f"pad{i}": _pad_tone(f) for i, f in enumerate(PAD_FREQS)}
SOUNDS["scare"] = _scare()

# ===========================================================================
# LÓGICA DOS JOGOS
# ===========================================================================
LIMIT = 10          # segundos por desafio e máximo de tentativas no Logic Challenge
ROUNDS = 5          # desafios no Reaction Challenge
GRACE = 0.75        # tolerância (s) para a latência da rede ao submeter
MEM_MAX = 10        # rondas máximas no Memory Sequence


def fresh():
    """Cria um estado novo para uma sessão de jogo."""
    return {
        # Logic
        "secret": random.randint(1, 100), "lo": 1, "hi": 100, "tries": 0,
        "logic": 0, "logic_done": False, "guesses": [], "logic_fb": None,
        # Reaction
        "cs": random.sample(reaction_bank, ROUNDS), "ci": 0, "react": 0,
        "ra": [], "t0": None, "last": None,
        # Memory
        "mem": {"seq": [], "pos": 0, "phase": "idle", "tone": None, "msg": ""},
        "mem_score": 0,
        # Susto pendente (som + imagem) para a próxima página
        "scare": False,
    }


# ---------------------------------------------------------------------------
# 1. Logic Challenge
# ---------------------------------------------------------------------------

def logic_guess(S, raw):
    if S["logic_done"]:
        return
    try:
        n = int(str(raw).strip())
    except ValueError:
        n = None
    if n is None or n < 1 or n > 100:
        S["logic_fb"] = ("Escreve um número inteiro entre 1 e 100.", "warning")
        return

    S["tries"] += 1
    S["guesses"].append(n)
    if n == S["secret"]:
        S["logic"] = 11 - S["tries"]
        S["logic_done"] = True
        S["logic_fb"] = (f"Acertaste em {S['tries']} tentativa(s) e ganhaste {S['logic']} pontos.", "success")
        return

    if n > S["secret"]:
        S["hi"] = min(S["hi"], n - 1)
        S["logic_fb"] = ("Demasiado alto. Tenta um número menor.", "warning")
    else:
        S["lo"] = max(S["lo"], n + 1)
        S["logic_fb"] = ("Demasiado baixo. Tenta um número maior.", "warning")
    if S["tries"] >= LIMIT:
        S["logic_done"] = True
        S["logic_fb"] = (f"Sem tentativas. O número secreto era {S['secret']}. 0 pontos.", "error")


# ---------------------------------------------------------------------------
# 2. Reaction Challenge (o tempo é medido no servidor)
# ---------------------------------------------------------------------------

def _settle(S, answer, timed_out, now):
    c = S["cs"][S["ci"]]
    elapsed = LIMIT if timed_out else min(LIMIT, now - S["t0"])
    ok = (not timed_out) and check_reaction_answer(answer, c)
    if ok:
        S["react"] += 2
    else:
        S["scare"] = True

    if timed_out:
        msg, kind = f"Tempo esgotado. A resposta era «{c['answer']}».", "error"
    elif ok:
        msg, kind = f"Correto em {elapsed:.1f} s! +2 pontos.", "success"
    else:
        msg, kind = f"Incorreto. A resposta era «{c['answer']}».", "error"

    S["ra"].append({
        "q": c["question"],
        "a": "Tempo esgotado" if timed_out else (answer.strip() or "Sem resposta"),
        "c": c["answer"], "ok": ok, "t": elapsed,
    })
    S["last"] = {"ok": ok, "timed_out": timed_out, "msg": msg, "kind": kind, "elapsed": elapsed}


def react_start(S, now):
    """Arranca o cronómetro do desafio atual (só uma vez por desafio)."""
    if S["t0"] is None and S["last"] is None and S["ci"] < ROUNDS:
        S["t0"] = now


def react_answer(S, answer, now):
    if S["t0"] is None or S["last"] is not None or S["ci"] >= ROUNDS:
        return
    _settle(S, answer, now - S["t0"] > LIMIT + GRACE, now)


def react_timeout(S, now):
    """Chamado pela página quando os 10 s acabam (meta refresh)."""
    if S["t0"] is None or S["last"] is not None or S["ci"] >= ROUNDS:
        return
    if now - S["t0"] >= LIMIT - 0.5:
        _settle(S, "", True, now)


def react_next(S):
    if S["last"] is not None:
        S["last"] = None
        S["t0"] = None
        S["ci"] += 1


# ---------------------------------------------------------------------------
# 3. Memory Sequence
# ---------------------------------------------------------------------------

def mem_start(S):
    S["mem"] = {"seq": [random.randint(0, 3)], "pos": 0, "phase": "show", "tone": None, "msg": ""}
    S["mem_score"] = 0


def mem_pad(S, i):
    m = S["mem"]
    if m["phase"] not in ("show", "input") or i not in (0, 1, 2, 3):
        return
    m["phase"] = "input"
    m["tone"] = i
    if i != m["seq"][m["pos"]]:
        m["phase"] = "end"
        m["msg"] = "Falhaste a sequência."
        S["scare"] = True
        return
    m["pos"] += 1
    if m["pos"] < len(m["seq"]):
        return
    S["mem_score"] = len(m["seq"])
    if len(m["seq"]) >= MEM_MAX:
        m["phase"] = "end"
        m["msg"] = "Sequência perfeita!"
        return
    m["seq"].append(random.randint(0, 3))   # próxima ronda, mais longa
    m["pos"] = 0
    m["phase"] = "show"


# ---------------------------------------------------------------------------
# Resultados
# ---------------------------------------------------------------------------

def compute_results(S):
    games = [("Logic Challenge", S["logic"]), ("Reaction Challenge", S["react"]), ("Memory Sequence", S["mem_score"])]
    total = sum(v for _, v in games)
    pct = total / 30 * 100
    if pct <= 20:
        rating = "Iniciante"
    elif pct <= 40:
        rating = "Em desenvolvimento"
    elif pct <= 60:
        rating = "Bom desempenho"
    elif pct <= 80:
        rating = "Desempenho elevado"
    else:
        rating = "Mestre do raciocínio"
    return games, total, pct, rating

# ===========================================================================
# PÁGINAS (templates do index.html)
# ===========================================================================
RING = 276.46       # circunferência do cronómetro (r = 44)
SCORE_RING = 439.8  # circunferência do anel de resultados (r = 70)
PAD_COLORS = ["#22c55e", "#ef4444", "#facc15", "#3b82f6"]
PAD_NAMES = ["Verde", "Vermelho", "Amarelo", "Azul"]
STEPS = ["Lógica", "Reação", "Memória", "Final"]

_cache = {}


def _load_templates():
    """Lê o index.html: a moldura da página e os blocos <template> de cada ecrã."""
    text = (BASE / "index.html").read_text(encoding="utf-8")
    pattern = re.compile(r'<template id="(\w+)">\n?(.*?)</template>\n?', re.S)
    for name, content in pattern.findall(text):
        _cache[name] = Template(content)
    _cache["base"] = Template(pattern.sub("", text))


def _tpl(name):
    if not _cache:
        _load_templates()
    return _cache[name]


def esc(text):
    return html.escape(str(text), quote=True)


def _feedback(msg, kind):
    return f'<p class="feedback {kind}" role="status">{esc(msg)}</p>'


def _stepper(step):
    if not step:
        return ""
    items = []
    for i, name in enumerate(STEPS, start=1):
        cls = "active" if i == step else "done" if i < step else ""
        items.append(f'<li class="{cls}">{name}</li>')
    return f'<ol class="stepper" aria-label="Progresso">{"".join(items)}</ol>'


def _scare(S):
    """Susto: imagem em ecrã inteiro e som. Mostrado uma única vez."""
    if not S.get("scare"):
        return "", ""
    S["scare"] = False
    return (
        '<div class="scare" aria-hidden="true"><span>💀</span></div>',
        '<audio src="/audio/scare.wav" autoplay></audio>',
    )


def page(S, best, content, step=0, head_extra="", extra_audio=""):
    scare, scare_audio = _scare(S)
    return _tpl("base").substitute(
        head_extra=head_extra, scare=scare, best=best, stepper=_stepper(step),
        content=content, audio=scare_audio + extra_audio,
    )


# ---------------------------------------------------------------------------

def home_page(S, best):
    return page(S, best, _tpl("home").substitute())


def logic_page(S, best):
    done = S["logic_done"]
    dots = "".join(f'<span class="{"used" if i < S["tries"] else ""}"></span>' for i in range(LIMIT))
    chips = []
    for n in S["guesses"]:
        if n == S["secret"]:
            chips.append(f'<span class="chip ok">{n} ✓</span>')
        else:
            chips.append(f'<span class="chip">{n} {"↓" if n > S["secret"] else "↑"}</span>')

    if done:
        form = ""
        finished = '<div><a class="btn wide" href="/reaction">Continuar para o Reaction Challenge</a></div>'
        range_text = f"Tentativas usadas: {S['tries']}"
    else:
        form = (
            '<form class="row" method="post" action="/logic">'
            '<input type="number" name="guess" min="1" max="100" step="1" inputmode="numeric" '
            'placeholder="O teu palpite" required autofocus aria-label="Palpite">'
            '<button class="btn" type="submit">Tentar</button></form>'
        )
        finished = ""
        range_text = f"O número está entre {S['lo']} e {S['hi']}"

    fb = _feedback(*S["logic_fb"]) if S["logic_fb"] else ""
    content = _tpl("logic").substitute(
        range_left=S["lo"] - 1, range_width=S["hi"] - S["lo"] + 1, range_text=range_text,
        dots=dots, form=form, feedback=fb, history="".join(chips), finished=finished,
    )
    return page(S, best, content, step=1)


# ---------------------------------------------------------------------------
# Reaction Challenge
# ---------------------------------------------------------------------------

_ICONS_RUNNING = (
    '<i class="ic ic-a" aria-hidden="true">⏱️</i>'
    '<i class="ic ic-b" aria-hidden="true">⚠️</i>'
    '<i class="ic ic-c" aria-hidden="true">💣</i>'
)


def _explosion():
    parts = []
    for i in range(16):
        a = i / 16 * 2 * math.pi
        d = 70 + random.random() * 110
        symbol = ["🔥", "💥", "✨", "💨"][i % 4]
        parts.append(
            f'<span class="p" style="--x:{math.cos(a) * d:.0f}px;--y:{math.sin(a) * d * 0.5:.0f}px">{symbol}</span>'
        )
    return f'<div class="explosion"><strong>💥 BOOM!</strong>{"".join(parts)}</div>'


def reaction_page(S, best):
    number, points = S["ci"] + 1, S["react"]
    last = S["last"]

    if last is None:
        c = S["cs"][S["ci"]]
        body = (
            '<form method="post" action="/reaction/answer">'
            f'<h3 class="question">{esc(c["question"])}</h3>'
            '<div class="row"><input type="text" name="answer" autocomplete="off" '
            'placeholder="A tua resposta" aria-label="Resposta" autofocus>'
            '<button class="btn" type="submit">Responder</button></div></form>'
        )
        # Quando os 10 s acabam, o navegador pede /reaction/timeout (meta refresh).
        head = f'<meta http-equiv="refresh" content="{LIMIT};url=/reaction/timeout">'
        content = _tpl("reaction").substitute(
            number=number, points=points, panel_class="", timer_class="running", offset="0",
            timer_text="", icons=_ICONS_RUNNING, explosion="", body=body,
        )
        return page(S, best, content, step=2, head_extra=head)

    # Feedback do desafio acabado de responder
    rem = max(0.0, LIMIT - last["elapsed"])
    cls = "danger" if rem <= 3 else "warn" if rem <= 5 else ""
    icon = "💥" if last["timed_out"] else "💣" if rem <= 3 else "⚠️" if rem <= 5 else "⏱️"
    delay = 1.9 if last["timed_out"] else 1.4
    body = _feedback(last["msg"], last["kind"]) + '<a class="btn wide" href="/reaction/next">Seguinte</a>'
    head = f'<meta http-equiv="refresh" content="{delay};url=/reaction/next">'
    content = _tpl("reaction").substitute(
        number=number, points=points, panel_class="shake" if last["timed_out"] else "",
        timer_class=f"static {cls}", offset=f"{RING * (1 - rem / LIMIT):.2f}",
        timer_text=f"{rem:.1f}", icons=f'<i class="ic-static" aria-hidden="true">{icon}</i>',
        explosion=_explosion() if last["timed_out"] else "", body=body,
    )
    return page(S, best, content, step=2, head_extra=head)


# ---------------------------------------------------------------------------
# Memory Sequence
# ---------------------------------------------------------------------------

def memory_page(S, best):
    m = S["mem"]
    phase = m["phase"]
    seq = m["seq"]
    n = len(seq)

    flash_ms, step_ms = 380, 650
    show_end = 700 + n * step_ms          # quando a sequência acaba de ser mostrada

    pads = []
    for i in range(4):
        anims = []
        if phase == "show":
            anims = [f"flash {flash_ms}ms {700 + k * step_ms}ms" for k, v in enumerate(seq) if v == i]
            anims.append(f"unlock 10ms {show_end}ms forwards")
        style = f"--c:{PAD_COLORS[i]}" + (f";animation:{','.join(anims)}" if anims else "")
        disabled = " disabled" if phase in ("idle", "end") else ""
        cls = "pad locked" if phase == "show" else "pad"
        pads.append(
            f'        <form method="post" action="/memory/pad" class="padform">'
            f'<button class="{cls}" name="pad" value="{i}" style="{style}" aria-label="{PAD_NAMES[i]}"{disabled}></button></form>'
        )

    start = next_btn = ""
    if phase == "idle":
        status = "Memoriza a sequência e repete-a. Cada ronda vale 1 ponto (máx. 10)."
        start = '<form method="post" action="/memory/start"><button class="btn wide" type="submit">Começar</button></form>'
    elif phase == "show":
        status = (
            f'<span class="obs" style="animation:fadeout 10ms {show_end}ms forwards">Ronda {n} · Observa…</span>'
            f'<span class="turn" style="animation:fadein 10ms {show_end}ms forwards">Ronda {n} · A tua vez!</span>'
        )
    elif phase == "input":
        status = f"Ronda {n} · A tua vez!"
    else:
        status = f"{m['msg']} Pontuação: {S['mem_score']} / 10."
        next_btn = '<a class="btn wide" href="/results">Ver resultado final</a>'

    audio = ""
    if m.get("tone") is not None:
        audio = f'<audio src="/audio/pad{m["tone"]}.wav" autoplay></audio>'
        m["tone"] = None

    content = _tpl("memory").substitute(status=status, pads="\n".join(pads), start=start, next=next_btn)
    return page(S, best, content, step=3, extra_audio=audio)


# ---------------------------------------------------------------------------
# Resultados
# ---------------------------------------------------------------------------

def results_page(S, best, previous):
    games, total, pct, rating = compute_results(S)
    record = ""
    if total > previous and total > 0:
        txt = f"Novo recorde! Anterior: {previous}/30" if previous else "Primeiro recorde guardado!"
        record = f'<p class="record">{txt}</p>'

    rows = "\n".join(
        f'        <div><span>{name}</span><div class="bar"><div style="--w:{v * 10}%"></div></div><b>{v}/10</b></div>'
        for name, v in games
    )
    review = "".join(
        f'<p class="{"ok" if r["ok"] else "no"}">Reação {i}: {esc(r["q"])} → {esc(r["a"])}'
        + (f' ({r["t"]:.1f} s)' if r["ok"] else f' (certa: {esc(r["c"])})') + "</p>"
        for i, r in enumerate(S["ra"], start=1)
    )
    content = _tpl("results").substitute(
        offset=f"{SCORE_RING * (1 - total / 30):.2f}", total=total, rating=f"{pct:.0f}% · {rating}",
        record=record, breakdown=rows, review=review,
    )
    return page(S, best, content, step=4)

# ===========================================================================
# SERVIDOR WEB
# ===========================================================================
MAX_SESSIONS = 500
BEST_COOKIE = "bthBest3"

SESSIONS = {}   # sid -> estado do jogo (em memória)


class Handler(BaseHTTPRequestHandler):
    server_version = "BrainTrainingHub/1.0"

    # ----- utilitários -----------------------------------------------------
    def _cookies(self):
        jar = cookies.SimpleCookie()
        try:
            jar.load(self.headers.get("Cookie", ""))
        except cookies.CookieError:
            pass
        return jar

    def _session(self):
        jar = self._cookies()
        sid = jar["sid"].value if "sid" in jar else None
        if sid not in SESSIONS:
            sid = secrets.token_urlsafe(16)
            if len(SESSIONS) >= MAX_SESSIONS:
                SESSIONS.pop(next(iter(SESSIONS)))
            SESSIONS[sid] = fresh()
            self._new_sid = sid
        return SESSIONS[sid], sid

    def _best(self):
        try:
            return max(0, min(30, int(self._cookies()[BEST_COOKIE].value)))
        except (KeyError, ValueError):
            return 0

    def _send(self, body, status=200, ctype="text/html; charset=utf-8", headers=()):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        if getattr(self, "_new_sid", None):
            self.send_header("Set-Cookie", f"sid={self._new_sid}; Path=/; HttpOnly; SameSite=Lax")
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def _redirect(self, location):
        self._send(b"", status=303, headers=[("Location", location)])

    def _form(self):
        length = min(int(self.headers.get("Content-Length") or 0), 4096)
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        return {k: v[0] for k, v in parse_qs(raw).items()}

    def log_message(self, fmt, *args):   # menos ruído na consola
        pass

    # ----- GET -------------------------------------------------------------
    def do_GET(self):
        self._new_sid = None
        path = urlsplit(self.path).path
        S, _ = self._session()
        best = self._best()
        now = time.monotonic()

        if path == "/style.css":
            return self._send((BASE / "style.css").read_bytes(), ctype="text/css; charset=utf-8")
        if path.startswith("/audio/") and path.endswith(".wav"):
            wav = SOUNDS.get(path[len("/audio/"):-4])
            return self._send(wav, ctype="audio/wav") if wav else self._send("Não encontrado", 404)

        if path == "/":
            return self._send(home_page(S, best))
        if path == "/reset":
            reset_game(S)
            return self._redirect("/")
        if path == "/logic":
            return self._send(logic_page(S, best))
        if path == "/reaction":
            if S["ci"] >= ROUNDS and S["last"] is None:
                return self._redirect("/memory")
            react_start(S, now)
            return self._send(reaction_page(S, best))
        if path == "/reaction/timeout":
            react_timeout(S, now)
            return self._redirect("/reaction")
        if path == "/reaction/next":
            react_next(S)
            return self._redirect("/reaction")
        if path == "/memory":
            return self._send(memory_page(S, best))
        if path == "/results":
            games_total = compute_results(S)[1]
            previous = best
            new_best = max(best, games_total)
            extra = []
            if new_best != best:
                extra.append(("Set-Cookie", f"{BEST_COOKIE}={new_best}; Path=/; Max-Age=31536000; SameSite=Lax"))
            return self._send(results_page(S, new_best, previous), headers=extra)
        self._send("Página não encontrada", 404)

    # ----- POST ------------------------------------------------------------
    def do_POST(self):
        self._new_sid = None
        path = urlsplit(self.path).path
        S, _ = self._session()
        form = self._form()
        now = time.monotonic()

        if path == "/start":
            reset_game(S)
            return self._redirect("/logic")
        if path == "/reset":
            reset_game(S)
            return self._redirect("/")
        if path == "/logic":
            logic_guess(S, form.get("guess", ""))
            return self._redirect("/logic")
        if path == "/reaction/answer":
            react_answer(S, form.get("answer", ""), now)
            return self._redirect("/reaction")
        if path == "/memory/start":
            if S["mem"]["phase"] == "idle":
                mem_start(S)
            return self._redirect("/memory")
        if path == "/memory/pad":
            try:
                mem_pad(S, int(form.get("pad", "-1")))
            except ValueError:
                pass
            return self._redirect("/memory")
        self._send("Página não encontrada", 404)


def reset_game(S):
    """Recomeça o jogo mantendo a mesma sessão."""
    S.clear()
    S.update(fresh())


def main():
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Brain Training Hub a correr em http://localhost:{port}  (Ctrl+C para parar)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor terminado.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
