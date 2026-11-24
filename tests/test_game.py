"""Testes do Brain Training Hub. Executar: python3 -m unittest discover -s tests -v"""

import json
import random
import unittest

from game.answers import check_reaction_answer, normalize_answer
from game import bridge
from game.data import REACTION_BANK
from game.engine import GameSession, LogicGame, MemoryGame, ReactionGame, rating_for


class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


class AnswerTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize_answer("  Júpiter! "), "jupiter")
        self.assertEqual(normalize_answer("Quarta-Feira"), "quarta feira")

    def test_every_challenge_accepts_its_own_answers(self):
        for c in REACTION_BANK:
            self.assertTrue(check_reaction_answer(c["answer"], c), c["question"])
            for alt in c["acceptable"]:
                self.assertTrue(check_reaction_answer(alt, c), (c["question"], alt))

    def test_rejects_wrong_and_empty(self):
        c = {"question": "q", "answer": "45", "acceptable": ["45"]}
        for bad in ("", "   ", "46", None, "450"):
            self.assertFalse(check_reaction_answer(bad, c))

    def test_flexible_variants(self):
        quarta = next(c for c in REACTION_BANK if c["answer"] == "Quarta-feira")
        for ok in ("quarta", "QUARTA FEIRA", "quartafeira", "Quarta-feira."):
            self.assertTrue(check_reaction_answer(ok, quarta), ok)
        horas = next(c for c in REACTION_BANK if c["answer"] == "8 horas")
        for ok in ("8", "8h", "8 horas", "oito"):
            self.assertTrue(check_reaction_answer(ok, horas), ok)
        euros = next(c for c in REACTION_BANK if c["answer"] == "13 euros")
        for ok in ("13", "13€", "13 eur", "treze"):
            self.assertTrue(check_reaction_answer(ok, euros), ok)


class LogicTests(unittest.TestCase):
    def game(self, secret):
        g = LogicGame(random.Random(1))
        g._secret = secret
        return g

    def test_scoring_by_attempt(self):
        for tries in range(1, 11):
            g = self.game(50)
            for _ in range(tries - 1):
                g.guess(1)
            r = g.guess(50)
            self.assertEqual(r["status"], "win")
            self.assertEqual(g.score, 11 - tries)

    def test_hints_and_range(self):
        g = self.game(50)
        self.assertEqual(g.guess(80)["status"], "high")
        self.assertEqual(g.hi, 79)
        self.assertEqual(g.guess(20)["status"], "low")
        self.assertEqual(g.lo, 21)
        self.assertEqual([x["hint"] for x in g.guesses], ["down", "up"])

    def test_invalid_does_not_consume_try(self):
        g = self.game(50)
        for bad in (0, 101, 5.5, "abc", "", None, True, float("inf"), -3):
            self.assertEqual(g.guess(bad)["status"], "invalid", bad)
        self.assertEqual(g.tries, 0)
        self.assertEqual(g.guess("50")["status"], "win")  # texto numérico é aceite

    def test_lose_after_ten(self):
        g = self.game(50)
        for _ in range(10):
            r = g.guess(1)
        self.assertEqual(r["status"], "lose")
        self.assertTrue(g.done)
        self.assertEqual(g.score, 0)
        self.assertIn("50", r["message"])
        self.assertEqual(g.guess(50)["status"], "finished")
        self.assertEqual(g.score, 0)


class ReactionTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.g = ReactionGame(random.Random(3), self.clock)

    def current(self):
        return self.g.challenges[self.g.index]

    def test_five_correct_is_ten_points(self):
        for i in range(5):
            d = self.g.next_challenge()
            self.assertEqual(d["index"], i + 1)
            self.clock.t += 2
            r = self.g.answer(self.current()["answer"])
            self.assertTrue(r["ok"])
        self.assertEqual(self.g.score, 10)
        self.assertTrue(r["finished"])
        self.assertTrue(self.g.next_challenge()["finished"])

    def test_wrong_answer(self):
        self.g.next_challenge()
        r = self.g.answer("zzz")
        self.assertEqual((r["status"], self.g.score), ("wrong", 0))

    def test_late_answer_is_timeout_even_if_correct(self):
        self.g.next_challenge()
        self.clock.t += 12
        r = self.g.answer(self.current()["answer"])
        self.assertEqual(r["status"], "timeout")
        self.assertEqual(self.g.score, 0)

    def test_answer_within_grace_counts(self):
        self.g.next_challenge()
        self.clock.t += 10.3
        self.assertTrue(self.g.answer(self.current()["answer"])["ok"])

    def test_client_cannot_force_early_timeout_and_timer_is_not_resettable(self):
        self.g.next_challenge()
        self.clock.t += 3
        self.assertEqual(self.g.answer("", timeout=True)["status"], "pending")
        again = self.g.next_challenge()            # recarregar não reinicia o tempo
        self.assertAlmostEqual(again["remaining"], 7, places=1)
        self.clock.t += 7
        self.assertEqual(self.g.answer("", timeout=True)["status"], "timeout")

    def test_no_double_scoring(self):
        self.g.next_challenge()
        ans = self.current()["answer"]
        self.assertTrue(self.g.answer(ans)["ok"])
        self.assertEqual(self.g.answer(ans)["status"], "idle")
        self.assertEqual(self.g.score, 2)

    def test_distinct_challenges(self):
        qs = [c["question"] for c in self.g.challenges]
        self.assertEqual(len(set(qs)), 5)


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.m = MemoryGame(random.Random(5), self.clock)

    def play_round(self, d):
        self.clock.t += (d["delay_ms"] + d["lead_ms"] + len(d["sequence"]) * d["step_ms"]) / 1000 + 0.1
        r = None
        for pad in d["sequence"]:
            r = self.m.press(pad)
        return r

    def test_perfect_game_scores_ten(self):
        d = self.m.start()
        self.assertEqual(d["round"], 1)
        for n in range(1, 11):
            r = self.play_round(d)
            if n < 10:
                self.assertEqual(r["result"], "round_complete")
                self.assertEqual(r["round"], n + 1)
                d = r
        self.assertEqual(r["result"], "perfect")
        self.assertEqual(self.m.score, 10)

    def test_wrong_press_ends_game_keeps_score(self):
        d = self.m.start()
        d = self.play_round(d)           # ronda 1 certa
        self.clock.t += 5
        wrong = (d["sequence"][0] + 1) % 4
        r = self.m.press(wrong)
        self.assertEqual(r["result"], "wrong")
        self.assertEqual(self.m.score, 1)
        self.assertEqual(self.m.press(0)["result"], "ignored")

    def test_input_before_sequence_shown_is_ignored(self):
        d = self.m.start()
        self.assertEqual(self.m.press(d["sequence"][0])["result"], "ignored")

    def test_bad_pad_values(self):
        d = self.m.start()
        self.clock.t += 5
        for bad in (-1, 4, "x", None):
            self.assertEqual(self.m.press(bad)["result"], "ignored")


class ResultsTests(unittest.TestCase):
    def test_ratings(self):
        cases = {0: "Iniciante", 20: "Iniciante", 21: "Em desenvolvimento", 40: "Em desenvolvimento",
                 41: "Bom desempenho", 60: "Bom desempenho", 61: "Desempenho elevado",
                 80: "Desempenho elevado", 81: "Mestre do raciocínio", 100: "Mestre do raciocínio"}
        for pct, name in cases.items():
            self.assertEqual(rating_for(pct), name, pct)

    def test_totals_and_record(self):
        s = GameSession(random.Random(1))
        s.logic.score, s.reaction.score, s.memory.score = 7, 6, 5
        r = s.results(previous_best=10)
        self.assertEqual((r["total"], r["percent"]), (18, 60))
        self.assertEqual(r["rating_text"], "60% · Bom desempenho")
        self.assertTrue(r["is_record"])
        self.assertEqual(r["record_text"], "Novo recorde! Anterior: 10/30")
        self.assertEqual(r["best"], 18)
        self.assertFalse(s.results(previous_best=18)["is_record"])
        self.assertEqual(s.results(previous_best=0)["record_text"], "Primeiro recorde guardado!")
        self.assertEqual(s.results(previous_best="lixo")["best"], 18)

    def test_zero_is_no_record(self):
        self.assertFalse(GameSession().results(0)["is_record"])


class BridgeTests(unittest.TestCase):
    """A ponte é o que o navegador (Pyodide) chama: recebe e devolve JSON em texto."""

    def setUp(self):
        self.clock = FakeClock()
        bridge._session = GameSession(random.Random(7), self.clock)

    def call(self, route, **payload):
        return json.loads(bridge.handle(route, json.dumps(payload)))

    def test_new_returns_config_and_fresh_state(self):
        d = self.call("new")
        self.assertEqual(d["config"]["reaction_limit"], 10)
        self.assertEqual(d["logic"]["tries"], 0)

    def test_errors_never_raise(self):
        self.assertIn("error", self.call("xyz"))
        self.assertIn("error", json.loads(bridge.handle("results", "[]")))
        self.assertIn("error", json.loads(bridge.handle("results", "{nao json")))
        self.assertEqual(self.call("logic/guess", guess=500)["status"], "invalid")

    def test_full_game_through_bridge(self):
        # Logic: busca binária só com as pistas devolvidas
        lo, hi = 1, 100
        while True:
            mid = (lo + hi) // 2
            r = self.call("logic/guess", guess=mid)
            if r["status"] == "win":
                break
            lo, hi = (mid + 1, hi) if r["status"] == "low" else (lo, mid - 1)
        logic_score = r["view"]["score"]
        self.assertGreaterEqual(logic_score, 4)

        # Reaction: 4 certas e 1 fora de tempo
        bank = {c["question"]: c["answer"] for c in REACTION_BANK}
        for i in range(5):
            q = self.call("reaction/next")
            self.assertEqual(q["index"], i + 1)
            self.clock.t += 12 if i == 4 else 2
            r = self.call("reaction/answer", answer=bank[q["question"]])
        self.assertEqual(r["status"], "timeout")
        self.assertTrue(r["finished"])

        # Memory: 3 rondas certas e falha
        m = self.call("memory/start")
        for n in range(3):
            self.clock.t += (m["delay_ms"] + m["lead_ms"] + len(m["sequence"]) * m["step_ms"]) / 1000 + 0.1
            for pad in m["sequence"]:
                r = self.call("memory/press", pad=pad)
            self.assertEqual(r["result"], "round_complete")
            m = r
        self.clock.t += 10
        r = self.call("memory/press", pad=(m["sequence"][0] + 1) % 4)
        self.assertEqual((r["result"], r["score"]), ("wrong", 3))

        res = self.call("results", best=0)
        self.assertEqual(res["total"], logic_score + 8 + 3)
        self.assertEqual(len(res["review"]), 5)
        self.assertTrue(res["is_record"])

    def test_new_resets_everything(self):
        self.call("logic/guess", guess=50)
        self.call("new")
        self.assertEqual(bridge._session.logic.tries, 0)

    def test_python_files_loaded_by_app_js_exist(self):
        import os, re
        root = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(root, "app.js"), encoding="utf-8") as fh:
            js = fh.read()
        files = re.search(r"PY_FILES = \[(.*?)\]", js).group(1)
        for name in re.findall(r'"([^"]+)"', files):
            self.assertTrue(os.path.isfile(os.path.join(root, "game", name)), name)


if __name__ == "__main__":
    unittest.main()
