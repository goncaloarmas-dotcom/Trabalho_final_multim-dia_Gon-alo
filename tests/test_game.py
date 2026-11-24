"""Testes do Brain Training Hub. Executar: python3 -m unittest discover -s tests -v"""

import json
import random
import threading
import unittest
import urllib.error
import urllib.request

from game.answers import check_reaction_answer, normalize_answer
from game.api import SessionStore, handle
from game.data import REACTION_BANK
from game.engine import GameSession, LogicGame, MemoryGame, ReactionGame, rating_for
from game.server import create_server


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


class ApiTests(unittest.TestCase):
    def test_session_flow_and_errors(self):
        store = SessionStore()
        st, d = handle("new", {}, store)
        self.assertEqual(st, 200)
        sid = d["sid"]
        self.assertEqual(handle("logic/guess", {"sid": sid, "guess": 500}, store)[1]["status"], "invalid")
        self.assertEqual(handle("logic/guess", {"sid": "nope"}, store)[0], 410)
        self.assertEqual(handle("xyz", {"sid": sid}, store)[0], 404)
        self.assertEqual(handle("results", [], store)[0], 400)

    def test_session_limit(self):
        store = SessionStore(max_sessions=3)
        for _ in range(10):
            handle("new", {}, store)
        self.assertLessEqual(len(store._data), 3)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = create_server("127.0.0.1", 0)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def get(self, path):
        try:
            with urllib.request.urlopen(self.base + path) as r:
                return r.status, r.headers, r.read()
        except urllib.error.HTTPError as e:
            return e.code, e.headers, e.read()

    def post(self, route, data):
        req = urllib.request.Request(self.base + "/api/" + route, json.dumps(data).encode(),
                                     {"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_static_files(self):
        st, h, body = self.get("/")
        self.assertEqual(st, 200)
        self.assertIn("text/html", h["Content-Type"])
        self.assertIn(b"Brain Training Hub", body)
        self.assertNotIn(b"data.js", body)
        self.assertIn("text/css", self.get("/style.css")[1]["Content-Type"])
        self.assertIn("javascript", self.get("/app.js")[1]["Content-Type"])
        self.assertEqual(self.get("/healthz")[0], 200)
        self.assertEqual(self.get("/nao-existe")[0], 404)

    def test_path_traversal_blocked(self):
        for p in ("/../main.py", "/%2e%2e/main.py", "/..%2fmain.py", "/../../etc/passwd"):
            self.assertNotEqual(self.get(p)[0], 200, p)
        self.assertNotIn(b"create_server", self.get("/../main.py")[2])

    def test_bad_requests(self):
        req = urllib.request.Request(self.base + "/api/new", b"{nao json", {"Content-Type": "application/json"})
        with self.assertRaises(urllib.error.HTTPError) as cm:
            urllib.request.urlopen(req)
        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(self.post("logic/guess", {"sid": "x"})[0], 410)

    def test_full_game_over_http(self):
        st, d = self.post("new", {})
        sid = d["sid"]
        self.assertEqual(d["config"]["reaction_limit"], 10)

        # Logic: busca binária a descobrir o número só com as pistas do servidor
        lo, hi = 1, 100
        while True:
            mid = (lo + hi) // 2
            _, r = self.post("logic/guess", {"sid": sid, "guess": mid})
            if r["status"] == "win":
                break
            lo, hi = (mid + 1, hi) if r["status"] == "low" else (lo, mid - 1)
        self.assertTrue(r["view"]["done"])
        logic_score = r["view"]["score"]
        self.assertGreaterEqual(logic_score, 4)

        # Reaction: responde às 5 perguntas usando o banco de dados
        bank = {c["question"]: c["answer"] for c in REACTION_BANK}
        for i in range(5):
            _, q = self.post("reaction/next", {"sid": sid})
            self.assertEqual(q["index"], i + 1)
            _, r = self.post("reaction/answer", {"sid": sid, "answer": bank[q["question"]]})
            self.assertTrue(r["ok"], r)
        self.assertTrue(r["finished"])
        self.assertTrue(self.post("reaction/next", {"sid": sid})[1]["finished"])

        # Memory: repete 3 rondas e falha de propósito
        import time
        _, m = self.post("memory/start", {"sid": sid})
        for n in range(1, 4):
            time.sleep((m["delay_ms"] + m["lead_ms"] + len(m["sequence"]) * m["step_ms"]) / 1000 + 0.05)
            for pad in m["sequence"]:
                _, r = self.post("memory/press", {"sid": sid, "pad": pad})
            self.assertEqual(r["result"], "round_complete")
            m = r
        time.sleep((m["delay_ms"] + m["lead_ms"] + len(m["sequence"]) * m["step_ms"]) / 1000 + 0.05)
        _, r = self.post("memory/press", {"sid": sid, "pad": (m["sequence"][0] + 1) % 4})
        self.assertEqual((r["result"], r["score"]), ("wrong", 3))

        _, res = self.post("results", {"sid": sid, "best": 0})
        self.assertEqual(res["total"], logic_score + 10 + 3)
        self.assertEqual(len(res["review"]), 5)
        self.assertTrue(res["is_record"])


if __name__ == "__main__":
    unittest.main()
