"""API JSON do jogo (sem frameworks): recebe ações do navegador e devolve o estado.

A função `handle` não depende de HTTP, o que a torna fácil de testar.
"""

import secrets
import threading
import time

from .engine import MAX_PER_GAME, MAX_TOTAL, GameSession, LogicGame, MemoryGame, ReactionGame

SESSION_TTL = 2 * 60 * 60      # 2 horas sem atividade
MAX_SESSIONS = 5000


class SessionStore:
    """Guarda as sessões de jogo em memória (uma por separador/jogador)."""

    def __init__(self, ttl=SESSION_TTL, max_sessions=MAX_SESSIONS):
        self._ttl, self._max = ttl, max_sessions
        self._data = {}
        self.lock = threading.Lock()

    def _purge(self, now):
        for sid in [k for k, (_, seen) in self._data.items() if now - seen > self._ttl]:
            del self._data[sid]
        while len(self._data) >= self._max:  # remove a mais antiga
            del self._data[min(self._data, key=lambda k: self._data[k][1])]

    def create(self):
        now = time.monotonic()
        self._purge(now)
        sid = secrets.token_urlsafe(16)
        session = GameSession()
        self._data[sid] = (session, now)
        return sid, session

    def get(self, sid):
        entry = self._data.get(sid) if isinstance(sid, str) else None
        if entry is None:
            return None
        if time.monotonic() - entry[1] > self._ttl:
            del self._data[sid]
            return None
        self._data[sid] = (entry[0], time.monotonic())
        return entry[0]


CONFIG = {
    "logic_max_tries": LogicGame.MAX_TRIES,
    "reaction_total": ReactionGame.TOTAL,
    "reaction_limit": ReactionGame.LIMIT,
    "memory_max_rounds": MemoryGame.MAX_ROUNDS,
    "max_per_game": MAX_PER_GAME,
    "max_total": MAX_TOTAL,
    "memory_intro": MemoryGame.INTRO,
}

# Cada rota recebe a sessão e o corpo JSON e devolve um dicionário.
ROUTES = {
    "logic/guess": lambda s, p: s.logic.guess(p.get("guess")),
    "reaction/next": lambda s, p: s.reaction.next_challenge(),
    "reaction/answer": lambda s, p: s.reaction.answer(p.get("answer"), p.get("timeout") is True),
    "memory/start": lambda s, p: s.memory.start(),
    "memory/press": lambda s, p: s.memory.press(p.get("pad")),
    "results": lambda s, p: s.results(p.get("best", 0)),
}


def handle(route, payload, store):
    """Devolve (código_http, dicionário_json)."""
    if not isinstance(payload, dict):
        return 400, {"error": "pedido inválido"}
    with store.lock:
        if route == "new":
            sid, session = store.create()
            return 200, {"sid": sid, "config": CONFIG, "logic": session.logic.view()}
        action = ROUTES.get(route)
        if action is None:
            return 404, {"error": "rota desconhecida"}
        session = store.get(payload.get("sid"))
        if session is None:
            return 410, {"error": "sessão expirada"}
        return 200, action(session, payload)
