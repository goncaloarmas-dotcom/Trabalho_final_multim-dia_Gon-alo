"""Ponte entre o navegador e o Python.

O app.js (através do Pyodide) chama `handle(rota, json)` e recebe um JSON com o
novo estado do jogo. Não há servidor: este módulo corre no próprio navegador.
"""

import json

from .engine import MAX_PER_GAME, MAX_TOTAL, GameSession, LogicGame, MemoryGame, ReactionGame

CONFIG = {
    "logic_max_tries": LogicGame.MAX_TRIES,
    "reaction_total": ReactionGame.TOTAL,
    "reaction_limit": ReactionGame.LIMIT,
    "memory_max_rounds": MemoryGame.MAX_ROUNDS,
    "max_per_game": MAX_PER_GAME,
    "max_total": MAX_TOTAL,
    "memory_intro": MemoryGame.INTRO,
}

# Cada rota recebe a sessão e o corpo do pedido e devolve um dicionário.
ROUTES = {
    "logic/guess": lambda s, p: s.logic.guess(p.get("guess")),
    "reaction/next": lambda s, p: s.reaction.next_challenge(),
    "reaction/answer": lambda s, p: s.reaction.answer(p.get("answer"), p.get("timeout") is True),
    "memory/start": lambda s, p: s.memory.start(),
    "memory/press": lambda s, p: s.memory.press(p.get("pad")),
    "results": lambda s, p: s.results(p.get("best", 0)),
}

_session = GameSession()


def handle(route, payload_json="{}"):
    """Executa uma ação do jogo e devolve o resultado em JSON (texto)."""
    global _session
    try:
        payload = json.loads(payload_json or "{}")
        if not isinstance(payload, dict):
            raise ValueError("pedido inválido")
        if route == "new":
            _session = GameSession()
            data = {"config": CONFIG, "logic": _session.logic.view()}
        elif route in ROUTES:
            data = ROUTES[route](_session, payload)
        else:
            data = {"error": "rota desconhecida"}
    except Exception as exc:  # um erro nunca deve bloquear o jogo
        data = {"error": str(exc)}
    return json.dumps(data, ensure_ascii=False)
