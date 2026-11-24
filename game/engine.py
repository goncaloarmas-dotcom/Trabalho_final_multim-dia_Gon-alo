"""Motor dos três jogos do Brain Training Hub.

Toda a mecânica vive aqui: números secretos, sequências, tempo, validação,
pontuação e classificação. O navegador (JavaScript) apenas mostra o estado
e envia as ações do jogador.
"""

import math
import random
import time

from .answers import check_reaction_answer
from .data import REACTION_BANK

MAX_PER_GAME = 10
MAX_TOTAL = 30


def to_int(value):
    """Converte o valor recebido num inteiro, ou devolve None se não for válido."""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, (float, str)):
        try:
            number = float(value.strip() if isinstance(value, str) else value)
        except ValueError:
            return None
        if math.isfinite(number) and number.is_integer():
            return int(number)
    return None


# =============================================================================
# 1. LOGIC CHALLENGE - adivinha o número
# =============================================================================
class LogicGame:
    LOW, HIGH, MAX_TRIES = 1, 100, 10

    def __init__(self, rng):
        self._secret = rng.randint(self.LOW, self.HIGH)
        self.lo, self.hi = self.LOW, self.HIGH
        self.tries = 0
        self.score = 0
        self.done = False
        self.won = False
        self.guesses = []  # [{"n": int, "hint": "ok" | "up" | "down"}]

    def view(self):
        if self.done:
            range_text = f"Tentativas usadas: {self.tries}"
        else:
            range_text = f"O número está entre {self.lo} e {self.hi}"
        return {
            "lo": self.lo, "hi": self.hi, "tries": self.tries,
            "max_tries": self.MAX_TRIES, "done": self.done, "won": self.won,
            "score": self.score, "guesses": list(self.guesses),
            "range_text": range_text,
        }

    def _reply(self, status, message, kind):
        return {"status": status, "message": message, "type": kind, "view": self.view()}

    def guess(self, value):
        if self.done:
            return self._reply("finished", "O jogo já terminou.", "warning")
        n = to_int(value)
        if n is None or not self.LOW <= n <= self.HIGH:
            return self._reply("invalid", "Escreve um número inteiro entre 1 e 100.", "warning")

        self.tries += 1
        if n == self._secret:
            self.guesses.append({"n": n, "hint": "ok"})
            self.score = self.MAX_TRIES + 1 - self.tries  # 10 na 1.ª, menos 1 por tentativa
            self.done = self.won = True
            return self._reply(
                "win", f"Acertaste em {self.tries} tentativa(s) e ganhaste {self.score} pontos.",
                "success")

        if n > self._secret:
            self.hi = min(self.hi, n - 1)
            self.guesses.append({"n": n, "hint": "down"})
            status, message = "high", "Demasiado alto. Tenta um número menor."
        else:
            self.lo = max(self.lo, n + 1)
            self.guesses.append({"n": n, "hint": "up"})
            status, message = "low", "Demasiado baixo. Tenta um número maior."

        kind = "warning"
        if self.tries >= self.MAX_TRIES:
            self.done = True
            status, kind = "lose", "error"
            message = f"Sem tentativas. O número secreto era {self._secret}. 0 pontos."
        return self._reply(status, message, kind)


# =============================================================================
# 2. REACTION CHALLENGE - 5 desafios de 10 segundos (o tempo é medido aqui)
# =============================================================================
class ReactionGame:
    TOTAL = 5
    LIMIT = 10.0          # segundos por desafio
    POINTS = 2            # pontos por resposta certa
    GRACE = 0.75          # tolerância à latência da rede
    EARLY = 0.5           # o cliente pode declarar "tempo esgotado" até 0,5 s mais cedo

    def __init__(self, rng, clock=time.monotonic):
        self._clock = clock
        self.challenges = rng.sample(REACTION_BANK, self.TOTAL)
        self.index = 0
        self.score = 0
        self.answers = []  # [{"q", "a", "c", "ok", "t"}]
        self._active = False
        self._started_at = 0.0

    def _payload(self, remaining):
        return {
            "finished": False,
            "index": self.index + 1,
            "total": self.TOTAL,
            "score": self.score,
            "limit": self.LIMIT,
            "remaining": remaining,
            "question": self.challenges[self.index]["question"],
            "progress_text": f"Desafio {self.index + 1} de {self.TOTAL} · {self.score} pontos",
        }

    def next_challenge(self):
        """Inicia o cronómetro do desafio atual (ou devolve o tempo que resta se já iniciou)."""
        if self.index >= self.TOTAL:
            return {"finished": True}
        if not self._active:
            self._active = True
            self._started_at = self._clock()
        remaining = max(0.0, self.LIMIT - (self._clock() - self._started_at))
        return self._payload(round(remaining, 3))

    def answer(self, text, timeout=False):
        if not self._active:
            return {"status": "idle"}
        elapsed = self._clock() - self._started_at
        if timeout and elapsed < self.LIMIT - self.EARLY:
            return {"status": "pending", "remaining": round(self.LIMIT - elapsed, 3)}

        challenge = self.challenges[self.index]
        timed_out = timeout or elapsed > self.LIMIT + self.GRACE
        given = str(text or "").strip()[:80]
        ok = (not timed_out) and check_reaction_answer(given, challenge)
        shown = min(self.LIMIT, max(0.0, elapsed))

        if ok:
            self.score += self.POINTS
            status, kind = "correct", "success"
            message = f"Correto em {shown:.1f} s! +{self.POINTS} pontos."
        elif timed_out:
            status, kind = "timeout", "error"
            message = f"Tempo esgotado. A resposta era «{challenge['answer']}»."
        else:
            status, kind = "wrong", "error"
            message = f"Incorreto. A resposta era «{challenge['answer']}»."

        self.answers.append({
            "q": challenge["question"],
            "a": "Tempo esgotado" if timed_out else (given or "Sem resposta"),
            "c": challenge["answer"], "ok": ok, "t": shown,
        })
        self.index += 1
        self._active = False
        return {
            "status": status, "ok": ok, "timed_out": timed_out, "type": kind,
            "message": message, "elapsed": round(shown, 2),
            "correct_answer": challenge["answer"], "score": self.score,
            "finished": self.index >= self.TOTAL,
            "delay_ms": 1900 if timed_out else 1400,
        }


# =============================================================================
# 3. MEMORY SEQUENCE - sequência de cores (a sequência e a validação são aqui)
# =============================================================================
class MemoryGame:
    MAX_ROUNDS = 10
    PADS = 4
    LEAD_MS, STEP_MS, FLASH_MS = 700, 650, 380
    INTRO = "Memoriza a sequência e repete-a. Cada ronda vale 1 ponto (máx. 10)."

    def __init__(self, rng, clock=time.monotonic):
        self._rng = rng
        self._clock = clock
        self.reset()

    def reset(self):
        self.seq = []
        self.pos = 0
        self.score = 0
        self.over = False
        self._ready_at = float("inf")

    def _new_round(self, delay_ms):
        self.seq.append(self._rng.randrange(self.PADS))
        self.pos = 0
        n = len(self.seq)
        self._ready_at = self._clock() + (delay_ms + self.LEAD_MS + n * self.STEP_MS) / 1000
        return {
            "round": n, "sequence": list(self.seq), "delay_ms": delay_ms,
            "lead_ms": self.LEAD_MS, "step_ms": self.STEP_MS, "flash_ms": self.FLASH_MS,
            "watch_text": f"Ronda {n} · Observa…", "turn_text": f"Ronda {n} · A tua vez!",
            "score": self.score,
        }

    def start(self):
        self.reset()
        return self._new_round(delay_ms=300)

    def _end(self, message):
        self.over = True
        return {"finished": True, "score": self.score,
                "message": f"{message} Pontuação: {self.score} / {MAX_PER_GAME}."}

    def press(self, pad):
        # só aceita cliques depois de a sequência ter sido mostrada (0,4 s de tolerância)
        pad = to_int(pad)
        if self.over or not self.seq or pad is None or not 0 <= pad < self.PADS \
                or self._clock() < self._ready_at - 0.4:
            return {"result": "ignored"}

        if pad != self.seq[self.pos]:
            return {"result": "wrong", **self._end("Falhaste a sequência.")}

        self.pos += 1
        if self.pos < len(self.seq):
            return {"result": "continue"}

        self.score = len(self.seq)
        if self.score >= self.MAX_ROUNDS:
            return {"result": "perfect", **self._end("Sequência perfeita!")}
        return {"result": "round_complete", "finished": False, **self._new_round(delay_ms=900)}


# =============================================================================
# Sessão de jogo e resultados finais
# =============================================================================
def rating_for(pct):
    if pct <= 20:
        return "Iniciante"
    if pct <= 40:
        return "Em desenvolvimento"
    if pct <= 60:
        return "Bom desempenho"
    if pct <= 80:
        return "Desempenho elevado"
    return "Mestre do raciocínio"


class GameSession:
    def __init__(self, rng=None, clock=time.monotonic):
        rng = rng or random.Random()
        self.logic = LogicGame(rng)
        self.reaction = ReactionGame(rng, clock)
        self.memory = MemoryGame(rng, clock)

    def results(self, previous_best=0):
        prev = to_int(previous_best)
        prev = prev if prev is not None and 0 <= prev <= MAX_TOTAL else 0

        games = [("Logic Challenge", self.logic.score),
                 ("Reaction Challenge", self.reaction.score),
                 ("Memory Sequence", self.memory.score)]
        total = sum(v for _, v in games)
        pct = total / MAX_TOTAL * 100
        rating = rating_for(pct)

        is_record = total > prev and total > 0
        record_text = ""
        if is_record:
            record_text = f"Novo recorde! Anterior: {prev}/{MAX_TOTAL}" if prev \
                else "Primeiro recorde guardado!"

        review = []
        for i, r in enumerate(self.reaction.answers, 1):
            detail = f" ({r['t']:.1f} s)" if r["ok"] else f" (certa: {r['c']})"
            review.append({"text": f"Reação {i}: {r['q']} → {r['a']}{detail}", "ok": r["ok"]})

        return {
            "total": total, "max_total": MAX_TOTAL, "percent": round(pct),
            "rating": rating, "rating_text": f"{pct:.0f}% · {rating}",
            "games": [{"name": n, "value": v, "max": MAX_PER_GAME, "percent": v * 10}
                      for n, v in games],
            "is_record": is_record, "record_text": record_text,
            "best": max(prev, total), "review": review,
        }
