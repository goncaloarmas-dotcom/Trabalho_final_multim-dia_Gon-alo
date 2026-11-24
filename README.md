BRAIN TRAINING HUB

Disciplina:  Oficina de Multimédia - 12.º Ano - CRSI
Ano Letivo:  2026/2027
Autor:       Gonçalo Monteiro Borges Armas Gonçalves
Turma:       12A3
Link da Aplicação Web:  https://goncaloarmas-dotcom.github.io/Projeto_Multimedia/


1. VISÃO GERAL DO PROJETO

Descrição:
O Brain Training Hub é um dashboard web com três jogos curtos de raciocínio, reflexos e memória. No fim dos três jogos, o utilizador recebe uma pontuação total sobre 30, uma percentagem e uma classificação, e o melhor resultado fica guardado no navegador.

Proposta escolhida:
Proposta 1 — Dashboard Web de Ferramentas Multimédia com IA.

Tecnologias utilizadas:
  - Python 3 (biblioteca standard, sem Flask e sem dependências externas): servidor web, API JSON e TODA a lógica dos jogos.
  - HTML e CSS: estrutura e design do site (mantidos exatamente como na versão original).
  - JavaScript (mínimo): apenas para o que só o navegador consegue fazer — mostrar o estado no ecrã, animações, sons e comunicação com o Python.

Versão 2.0 — conversão para Python:
O projeto original era feito só em HTML, CSS e JavaScript (a lógica dos jogos estava em JavaScript). Nesta versão a lógica passou para Python e o JavaScript ficou reduzido a uma camada fina de navegador. O design e as funcionalidades são os mesmos.


2. ESTRUTURA DO CÓDIGO E FUNCIONALIDADES INTEGRADAS

O projeto mistura exercícios adaptados das fichas de Python com um jogo novo criado com IA.

QUEM FAZ O QUÊ

  Python (pasta game/)                       JavaScript (static/app.js)
  - escolhe o número secreto                 - desenha o ecrã a partir dos dados do Python
  - decide se o palpite é alto/baixo/certo   - desenha a contagem decrescente do círculo
  - mede o tempo de cada desafio (10 s)      - animações (explosão, susto, luzes)
  - valida as respostas (acentos, variantes) - sons gerados no navegador
  - gera e confere as sequências de memória  - guarda o recorde no navegador (localStorage)
  - calcula pontos, total, % e classificação - envia as ações do jogador ao Python
  - decide o que é "novo recorde"

JOGOS

  1) Logic Challenge
     Origem: Adaptado da ficha "Adivinha o número"
     Conceitos de Python trabalhados: Aleatoriedade, if / elif / else, comparações, limite de tentativas
     Pontuação: Até 10 pontos (10 na 1.ª tentativa, menos 1 por tentativa)
     Código: classe LogicGame em game/engine.py

  2) Reaction Challenge
     Origem: Adaptado da ficha do quiz de perguntas, ampliado com IA
     Conceitos de Python trabalhados: Strings (normalização das respostas), listas (banco de desafios), condições, módulo time
     Pontuação: 2 pontos por resposta certa (5 desafios de 10 segundos)
     Código: classe ReactionGame em game/engine.py; banco de perguntas em game/data.py; validação em game/answers.py
     O tempo é medido pelo Python (time.monotonic): uma resposta fora do tempo não conta, mesmo que esteja certa.

  3) Memory Sequence
     Origem: Jogo novo, criado com IA
     Conceitos de Python trabalhados: Listas (a sequência), lógica de jogo, módulo random
     Pontuação: 1 ponto por ronda (máximo 10)
     Código: classe MemoryGame em game/engine.py

FUNCIONALIDADES DO SITE

  - Página inicial com cartões de apresentação dos jogos e botão para começar.
  - Barra de progresso (Lógica → Reação → Memória → Final).
  - Cronómetro circular no Reaction Challenge, com animação de aviso e de explosão quando o tempo acaba.
  - Sons (gerados no navegador) e efeito visual quando o utilizador erra.
  - Validação inteligente de respostas: aceita maiúsculas/minúsculas, acentos e variantes (por exemplo, "quarta", "quarta-feira").
  - Resultados finais com anel de pontuação, detalhe por jogo e revisão das respostas.
  - Recorde pessoal guardado no navegador.
  - Nota a esclarecer que a classificação mede apenas o desempenho nos jogos, não a inteligência nem o QI.

Classificação final (percentagem do total de 30):
  0–20% Iniciante · 21–40% Em desenvolvimento · 41–60% Bom desempenho · 61–80% Desempenho elevado · 81–100% Mestre do raciocínio


3. ESTRUTURA DE FICHEIROS DO REPOSITÓRIO

  main.py               – ponto de entrada: arranca o servidor (python3 main.py)
  game/
    __init__.py
    engine.py           – lógica dos 3 jogos, pontuação, tempo e classificação (Python)
    data.py             – banco de desafios do Reaction Challenge (Python)
    answers.py          – validação/normalização das respostas (Python)
    api.py              – API JSON e gestão das sessões de jogo (Python)
    server.py           – servidor HTTP com a biblioteca standard (sem Flask)
  static/
    index.html          – estrutura das páginas (igual à versão original)
    style.css           – cores, layout, animações e responsividade (igual à versão original)
    app.js              – camada de navegador: ecrã, animações, sons e chamadas ao Python
  tests/
    test_game.py        – 28 testes automáticos (lógica, tempo, API, servidor, jogo completo)
  pyproject.toml        – metadados do projeto Python (sem dependências)
  .gitignore
  README.md             – este relatório de projeto

Não existe pasta de assets: os sons são gerados no navegador e os ícones são emojis.
Não é necessário instalar nada: só é preciso Python 3.11 ou superior.


4. INSTALAÇÃO E EXECUÇÃO

4.1 No computador (opcional)
  1. Instalar Python 3.11 ou superior (https://www.python.org).
  2. Abrir um terminal na pasta do projeto.
  3. Executar:      python3 main.py        (no Windows: py main.py)
  4. Abrir no navegador:  http://localhost:8000
  Para usar outra porta:  PORT=5000 python3 main.py

4.2 Testes automáticos
  python3 -m unittest discover -s tests -v


5. REGISTO DE UTILIZAÇÃO DA IA

Ferramentas usadas:
  - ChatGPT — para organizar as ideias do projeto.
  - Claude e Antigravity — para escrever e corrigir o código.


5.1 Prompt inicial (versão Streamlit — registo histórico)

O primeiro prompt, enviado à IA, pedia a aplicação completa em Python com Streamlit. Esta versão foi depois substituída por HTML/CSS/JavaScript e, mais tarde, convertida para o Python + HTML + CSS atual (ver 5.4). Resumo do que continha:

  - Aplicação chamada BRAIN TRAINING HUB, com três jogos (Logic Challenge, Quick Quiz, Reaction Challenge) e classificação final sobre 30 pontos. (Na versão final o Quick Quiz foi substituído pelo Memory Sequence.)
  - Código simples e organizado, adequado a um aluno do 12.º ano, com comentários em português.
  - Design moderno e tecnológico: fundo escuro, roxo neon como cor principal, azul como secundária, cartões arredondados e interface responsiva.
  - Regras detalhadas de cada jogo, de pontuação e de navegação entre páginas, sem pontos duplicados.

Prompt completo:

  Quero que desenvolvas o código completo de uma aplicação Web chamada BRAIN TRAINING HUB, utilizando Python e Streamlit.

  Este projeto é um trabalho escolar de Multimédia do 12.º ano, com o tema Python, Web UI e Inteligência Artificial.

  IMPORTANTE: O código deve ser adequado ao nível de um aluno do 12.º ano. Deve ser simples, organizado, funcional e explicado, evitando programação excessivamente avançada.

  1. Objetivo da aplicação — Criar um Dashboard Web interativo que reúna três jogos de inteligência e raciocínio: Logic Challenge, Quick Quiz e Reaction Challenge. O utilizador deverá completar os três jogos e receber uma classificação final baseada nos pontos obtidos.

  2. Tecnologias obrigatórias — Python, Streamlit, HTML/CSS através dos recursos do Streamlit, módulo random, módulo time, st.session_state para guardar os resultados durante a sessão. Não utilizar bases de dados, sistemas de contas, autenticação ou bibliotecas desnecessárias.

  3. Design e identidade visual — Design moderno, tecnológico e profissional. Fundo preto ou azul muito escuro, roxo neon como cor principal, azul como cor secundária, texto branco e cinzento claro, cartões com cantos arredondados, botões modernos, espaçamento organizado, interface responsiva. A página inicial deve apresentar o nome, um slogan, uma descrição da plataforma, três cartões (um por jogo), o botão START CHALLENGE e a explicação do sistema de pontuação.

  4. Jogo 1 — Logic Challenge — Adivinhação numérica: número aleatório entre 1 e 100, 10 tentativas, mensagens "Demasiado alto!" e "Demasiado baixo!", mensagem de vitória e fim de jogo se não acertar. Pontuação: 10 pontos à primeira tentativa, menos um ponto por tentativa, 0 sem acertar. Usar random, if/elif/else, ciclo for ou equivalente, break, variáveis e comparações.

  5. Jogo 2 — Quick Quiz — Cinco perguntas de cultura geral (ciência, matemática, geografia, tecnologia, cultura geral), quatro opções cada, apenas uma correta, feedback e pontuação final. 2 pontos por resposta certa, máximo 10. Usar listas, strings, variáveis, condições e contagem de pontos.

  6. Jogo 3 — Reaction Challenge — Cinco desafios de raciocínio rápido (operações matemáticas, padrões e lógica), com limite de 10 segundos cada. Registar o momento em que o desafio começa e verificar o tempo decorrido quando o utilizador submete a resposta. 2 pontos por resposta correta dentro do tempo, máximo 10. Usar o módulo time. Não inventar um cronómetro automático se a tecnologia não o permitir; implementar uma solução funcional e explicar qualquer limitação.

  7. Sistema de navegação — Ordem: página inicial, Logic Challenge, Quick Quiz, Reaction Challenge, resultados finais. Guardar em st.session_state o número secreto, tentativas, respostas, pontuações, estado de conclusão de cada jogo e página atual. Os resultados não podem desaparecer ao mudar de página. Impedir pontos duplicados por submeter várias vezes a mesma resposta. Botões para avançar entre jogos e para repetir a experiência.

  8. Classificação final — Somar os três jogos (máximo 30), converter em percentagem e classificar: 0–20% Iniciante, 21–40% Em desenvolvimento, 41–60% Inteligência média, 61–80% Inteligência elevada, 81–100% Génio. A página final mostra a pontuação de cada jogo, o total, a percentagem, a classificação e o botão PLAY AGAIN, com uma nota a esclarecer que a classificação mede apenas o desempenho nos jogos e não mede cientificamente a inteligência ou o QI.

  9. Requisitos técnicos — Funcionar com streamlit run app.py, usar st.set_page_config, código organizado em secções, comentários em português, sem erros de sintaxe, sem variáveis desnecessárias, sem dependências em falta nem funcionalidades pagas.

  10. Formato da resposta — Código completo de app.py, explicação simples das partes principais, lista de funcionalidades, instruções para testar e lista de possíveis erros com soluções. Sem omitir partes do código.

5.2 Prompt para ampliação e construção de funcionalidades

Depois de a primeira versão estar criada, o principal pedido foi para corrigir a ligação entre os ficheiros:

  "Quero que interligues corretamente os ficheiros para que o site funcione como deve ser."

Pedi ainda à IA para acrescentar elementos novos, como a barra do tempo e os efeitos de som e de imagem quando o utilizador erra (resumo do pedido). O jogo Memory Sequence foi criado com IA como jogo novo.


5.3 Dificuldades e erros corrigidos com a IA

O maior problema foi que, originalmente, o site não funcionava porque os vários ficheiros (HTML, CSS e JavaScript) não estavam bem interligados. O HTML não carregava corretamente o CSS e o JavaScript, e partes do código procuravam elementos e ficheiros que não existiam.

Pedi à IA para interligar os ficheiros corretamente. A solução foi organizar o projeto em ficheiros separados, cada um com uma função (estrutura, estilo, dados e lógica), e garantir que o index.html os carrega pela ordem certa. Depois disso, o site passou a funcionar como previsto.


5.4 Conversão para Python (versão 2.0)

Pedi à IA para converter o projeto de JavaScript para Python, mantendo o design, a estrutura e as funcionalidades, com estas regras: usar o máximo de Python possível; toda a mecânica, validação de respostas, pontuações e classificação em Python; JavaScript apenas para interações do navegador; não usar Flask; README atualizado.

O que mudou:
  - A lógica dos jogos, o banco de perguntas e a validação de respostas passaram de JavaScript (app.js e data.js) para Python (game/engine.py, game/data.py e game/answers.py).
  - Foi criado um servidor Python simples (game/server.py e game/api.py) com a biblioteca standard.
  - O app.js ficou só com a parte do navegador e o data.js deixou de existir.
  - O tempo de 10 segundos do Reaction Challenge passou a ser medido pelo servidor Python.
  - O index.html e o style.css mantêm-se iguais (só foi retirada a linha que carregava o data.js).
  - Foram acrescentados testes automáticos.
  - Pequena correção: ao jogar novamente, a mensagem do jogo anterior deixou de aparecer no Logic Challenge.


5.5 Otimização de Layout

Mantive sempre o layout original proposto pela IA, porque o design inicial já correspondia à minha ideia. Apenas pedi alterações em algumas decorações:

  - a barra do tempo do Reaction Challenge;
  - o som quando o utilizador erra;
  - o efeito visual quando o utilizador erra.


6. REFLEXÃO CRÍTICA E APRENDIZAGEM

O que correu melhor:
O design correu muito bem. A IA conseguiu fazer a minha ideia logo à primeira, e por isso mantive o layout original durante todo o projeto, mudando apenas alguns pormenores de decoração.

Maior dificuldade:
A maior dificuldade foi encontrar a ideia perfeita para o trabalho. Do lado técnico, o problema que mais me atrasou foi o site não funcionar porque os ficheiros não estavam bem interligados, mas ficou resolvido ao pedir à IA para os ligar corretamente.

Como a Inteligência Artificial mudou a minha forma de programar:
A IA ajuda imenso na programação. Mesmo alguém com poucas capacidades, como eu e os meus colegas, consegue fazer coisas extraordinárias. Mudou a forma como trabalho: em vez de começar do zero, descrevo bem a ideia e depois vou testando, corrigindo e pedindo melhorias. Percebi também que é preciso testar e entender o que a IA escreve, porque foi preciso detetar o problema dos ficheiros e pedir a correção certa.
