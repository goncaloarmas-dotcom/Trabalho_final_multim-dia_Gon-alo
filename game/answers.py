"""Validação inteligente de respostas (portada de data.js)."""

import re
import unicodedata

_NUM_WITH_UNIT = re.compile(
    r"^(\d+)\s*(horas|anos|euros|dias|minutos|macas|cores|letras|s|h)?$", re.IGNORECASE
)


def normalize_answer(text):
    """Remove acentos, maiúsculas, pontuação, aspas e normaliza espaços/traços."""
    if text is None:
        return ""
    t = unicodedata.normalize("NFD", str(text).strip().lower())
    t = "".join(ch for ch in t if not unicodedata.combining(ch))  # acentos
    t = re.sub(r"['\"“”‘’`]", "", t)                              # aspas
    t = re.sub(r"[.,!?;:]", "", t)                                # pontuação
    t = re.sub(r"[-_–—]", " ", t)                                 # traços -> espaço
    return re.sub(r"\s+", " ", t).strip()


def strip_all_spaces(text):
    """Comparação sem espaços (ex.: "quarta feira" vs "quartafeira")."""
    return normalize_answer(text).replace(" ", "")


def check_reaction_answer(user_answer, challenge):
    """Devolve True se a resposta do utilizador for aceite para o desafio."""
    raw = str(user_answer or "").strip()
    if not raw:
        return False

    norm_user = normalize_answer(raw)
    compact_user = strip_all_spaces(raw)

    # 1. Igualdade direta normalizada
    if norm_user == normalize_answer(challenge["answer"]) or \
            compact_user == strip_all_spaces(challenge["answer"]):
        return True

    # 2. Lista de respostas aceites
    for alt in challenge.get("acceptable", []):
        if norm_user == normalize_answer(alt) or compact_user == strip_all_spaces(alt):
            return True

    # 3. Respostas numéricas com/sem unidades ("8 horas" -> "8", "13 euros" -> "13")
    match = _NUM_WITH_UNIT.match(challenge["answer"])
    if match:
        n = match.group(1)
        if norm_user in (n, f"{n}h", f"{n}€", f"{n} euros", f"{n} eur",
                         f"{n} horas", f"{n} anos", f"{n} dias"):
            return True

    return False
