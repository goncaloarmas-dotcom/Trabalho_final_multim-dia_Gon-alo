"""Banco de desafios do Reaction Challenge (portado de data.js)."""


def _c(question, answer, acceptable=None):
    """Cria um desafio. Se não houver lista de respostas aceites, usa a resposta certa."""
    return {
        "question": question,
        "answer": answer,
        "acceptable": list(acceptable) if acceptable else [answer],
    }


REACTION_BANK = [
    # --- Matemática mental ---
    _c("Quanto é 17 + 28?", "45"),
    _c("Quanto é 12 × 12?", "144"),
    _c("Quanto é 200 - 76?", "124"),
    _c("Quanto é 81 ÷ 9?", "9"),
    _c("Quanto é 15 × 6?", "90"),
    _c("Quanto é 250 + 175?", "425"),
    _c("Quanto é metade de 186?", "93"),
    _c("Quanto é 11 × 11?", "121"),
    _c("Quanto é 1000 - 375?", "625"),
    _c("Quanto é 144 ÷ 8?", "18"),
    _c("Quanto é 8 × 9?", "72"),
    _c("Quanto é 15 × 4?", "60"),
    _c("Quanto é 100 - 37?", "63"),
    _c("Quanto é 144 ÷ 9?", "16"),
    _c("Quanto é 7²?", "49"),
    _c("Quanto é 25 × 4?", "100"),

    # --- Sequências numéricas e padrões ---
    _c("Completa: 2, 6, 10, 14, ...", "18"),
    _c("Completa: 2, 4, 8, 16, ...", "32"),
    _c("Completa: 5, 10, 15, 20, ...", "25"),
    _c("Completa: 1, 4, 9, 16, ...", "25"),
    _c("Completa: 3, 6, 12, 24, ...", "48"),
    _c("Completa: 100, 90, 80, 70, ...", "60"),
    _c("Completa: 1, 1, 2, 3, 5, 8, ...", "13"),
    _c("Completa: 10, 20, 30, 40, ...", "50"),
    _c("Completa: 2, 5, 8, 11, ...", "14"),
    _c("Completa: 50, 45, 40, 35, ...", "30"),

    # --- Raciocínio lógico ---
    _c("Qual não pertence ao grupo: maçã, banana, cenoura, pera?", "Cenoura", ["cenoura"]),
    _c("Se ontem foi segunda-feira, que dia será amanhã?", "Quarta-feira",
       ["quarta-feira", "quarta feira", "quarta", "quartafeira"]),
    _c("Tenho 3 maçãs e dou 1. Quantas me restam?", "2", ["2", "duas", "2 macas"]),
    _c("Quantos meses têm 28 dias?", "12", ["12", "todos", "todos os 12", "12 meses", "os 12"]),
    _c("Se um relógio marca 3 horas, qual será a hora daqui a 5 horas?", "8 horas",
       ["8", "8h", "8 horas", "oito"]),
    _c("Um pai tem 40 anos e o filho 10. Daqui a 5 anos, qual será a diferença de idades?",
       "30 anos", ["30", "30 anos", "trinta"]),
    _c("Se hoje é domingo, que dia foi anteontem?", "Sexta-feira",
       ["sexta-feira", "sexta feira", "sexta", "sextafeira"]),
    _c("Qual não pertence ao grupo: cão, gato, leão, carro?", "Carro", ["carro"]),

    # --- Cultura geral ---
    _c("Qual é a capital de Portugal?", "Lisboa", ["lisboa"]),
    _c("Qual é o maior planeta do Sistema Solar?", "Júpiter", ["jupiter", "júpiter"]),
    _c("Quantos dias tem uma semana?", "7", ["7", "sete", "7 dias"]),
    _c("Qual é o oceano entre a Europa e a América?", "Atlântico",
       ["atlantico", "atlântico", "oceano atlantico"]),
    _c("Qual é a língua oficial do Brasil?", "Português", ["portugues", "português"]),
    _c("Quantas cores tem tradicionalmente o arco-íris?", "7", ["7", "sete", "7 cores"]),
    _c("Qual é a capital de França?", "Paris", ["paris"]),

    # --- Desafios rápidos ---
    _c("Quantas letras tem a palavra COMPUTADOR?", "10", ["10", "dez", "10 letras"]),
    _c("Qual é o contrário de aumentar?", "Diminuir", ["diminuir", "reduzir", "baixar"]),
    _c("Qual é a terceira letra do alfabeto?", "C", ["c"]),
    _c("Quantos segundos existem num minuto?", "60", ["60", "sessenta", "60 segundos", "60s"]),
    _c("Qual é o dobro de 37?", "74"),
    _c("Se tens 20 euros e gastas 7, quanto sobra?", "13 euros",
       ["13", "13€", "13 euros", "treze"]),
    _c("Quanto é 6 × 7?", "42"),
    _c("Quanto é 50 ÷ 2?", "25"),
    _c("Qual é o triplo de 9?", "27"),
    _c("Quantos lados tem um quadrado?", "4", ["4", "quatro"]),
    _c("Quanto é 100 ÷ 4?", "25"),
    _c("Qual é o contrário de quente?", "Frio", ["frio"]),
    _c("Quantas horas tem um dia?", "24", ["24", "vinte e quatro", "24 horas", "24h"]),
    _c("Quanto é 9 × 9?", "81"),
]
