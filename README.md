# BRAIN TRAINING HUB

| | |
|---|---|
| **Disciplina** | Oficina de Multimédia - 12.º Ano - CRSI |
| **Ano Letivo** | 2026/2027 |
| **Autor** | Gonçalo Monteiro Borges Armas Gonçalves |
| **Turma** | 12A3 |
| **Link da Aplicação Web** | https://goncaloarmas-dotcom.github.io/Projeto_Multimedia/ |


## 1. Visão geral do projeto

O Brain Training Hub é um dashboard web com três jogos curtos de raciocínio, reflexos e memória. No fim dos três jogos, o utilizador recebe uma pontuação total sobre 30, uma percentagem e uma classificação. O melhor resultado fica guardado no navegador.

**Proposta escolhida:** Proposta 1 — Dashboard Web de Ferramentas Multimédia com IA.

## 2. Tecnologias utilizadas

| Tecnologia | Para que serve |
|---|---|
| **Python 3** | Servidor web, lógica dos jogos, pontuação, validação das respostas, medição do tempo e geração dos sons (tudo em `app.py`) |
| **HTML** | Estrutura das páginas (`index.html`) |
| **CSS** | Design, layout, cronómetro circular, animações (explosão, susto, sequência de cores) e responsividade |

Não há JavaScript nem dependências externas: o servidor usa apenas a biblioteca padrão do Python (`http.server`, `string.Template`, `wave`, etc.).

## 3. Jogos e funcionalidades

**1) Logic Challenge** — adaptado da ficha "Adivinha o número".
Conceitos de Python: aleatoriedade, `if / elif / else`, comparações, limite de tentativas.
Pontuação: até 10 pontos (10 na 1.ª tentativa, menos 1 por tentativa).

**2) Reaction Challenge** — adaptado da ficha do quiz de perguntas, ampliado com IA.
Conceitos de Python: strings (normalização das respostas), listas (banco de desafios), condições, módulo de tempo.
Pontuação: 2 pontos por resposta certa (5 desafios de 10 segundos).
O tempo é medido no servidor. O cronómetro circular é uma animação CSS, e quando os 10 segundos acabam a página pede ao servidor para dar o desafio como esgotado (`<meta http-equiv="refresh">`).

**3) Memory Sequence** — jogo novo, criado com IA.
Conceitos de Python: listas (a sequência), lógica de jogo.
Pontuação: 1 ponto por ronda (máximo 10).
A sequência é mostrada com animações CSS e os botões só ficam ativos quando ela termina.

**Funcionalidades do site**

- Página inicial com cartões de apresentação dos jogos e botão para começar.
- Barra de progresso (Lógica → Reação → Memória → Final).
- Cronómetro circular no Reaction Challenge, com aviso e explosão quando o tempo acaba.
- Sons (gerados pelo Python) e efeito visual quando o utilizador erra.
- Validação inteligente de respostas: aceita maiúsculas/minúsculas, acentos e variantes (por exemplo, "quarta", "quarta-feira").
- Resultados finais com anel de pontuação, detalhe por jogo e revisão das respostas.
- Recorde pessoal guardado no navegador (cookie).
- Nota a esclarecer que a classificação mede apenas o desempenho nos jogos, não a inteligência nem o QI.

**Limitações conhecidas (por não haver JavaScript):** o cronómetro mostra segundos inteiros enquanto corre; os sons tocam depois de cada ação (e não durante a animação da sequência); alguns navegadores bloqueiam a reprodução automática de som.

## 4. Instalação e execução

Requisitos: **Python 3.9 ou superior**. Não é preciso instalar bibliotecas.

```bash
python app.py        # em Linux/macOS pode ser: python3 app.py
```

Abrir no navegador: **http://localhost:8000**

Para usar outra porta: `PORT=8080 python app.py` (Linux/macOS) ou `set PORT=8080 && python app.py` (Windows).

## 5. Estrutura de ficheiros do repositório

```
brain-training-hub/
├── app.py       – Python: servidor, lógica dos jogos, pontuação, validação das respostas e sons
├── index.html   – HTML: moldura da página e um bloco <template> por ecrã (início, jogos, resultados)
├── style.css    – CSS: cores, layout, animações e responsividade
└── README.md    – este relatório de projeto
```

Não existe pasta de assets: os sons são gerados pelo Python e os ícones são emojis.

---

## 6. Registo de utilização da IA

**Ferramentas usadas:**

- ChatGPT — para organizar as ideias do projeto.
- Claude e Antigravity — para escrever e corrigir o código.

### 6.1 Prompt inicial

O primeiro prompt, enviado à IA, pedia a aplicação completa em **Python com Streamlit**. Resumo do que continha:

- Aplicação chamada BRAIN TRAINING HUB, com três jogos (Logic Challenge, Quick Quiz, Reaction Challenge) e classificação final sobre 30 pontos.
- Código simples e organizado, adequado a um aluno do 12.º ano, com comentários em português.
- Design moderno e tecnológico: fundo escuro, roxo neon como cor principal, azul como secundária, cartões arredondados e interface responsiva.
- Regras detalhadas de cada jogo, de pontuação e de navegação entre páginas, sem pontos duplicados.

Prompt completo:

> Quero que desenvolvas o código completo de uma aplicação Web chamada BRAIN TRAINING HUB, utilizando Python e Streamlit.
>
> Este projeto é um trabalho escolar de Multimédia do 12.º ano, com o tema Python, Web UI e Inteligência Artificial.
>
> IMPORTANTE: O código deve ser adequado ao nível de um aluno do 12.º ano. Deve ser simples, organizado, funcional e explicado, evitando programação excessivamente avançada.
>
> 1. Objetivo da aplicação — Criar um Dashboard Web interativo que reúna três jogos de inteligência e raciocínio: Logic Challenge, Quick Quiz e Reaction Challenge. O utilizador deverá completar os três jogos e receber uma classificação final baseada nos pontos obtidos.
>
> 2. Tecnologias obrigatórias — Python, Streamlit, HTML/CSS através dos recursos do Streamlit, módulo random, módulo time, st.session_state para guardar os resultados durante a sessão. Não utilizar bases de dados, sistemas de contas, autenticação ou bibliotecas desnecessárias.
>
> 3. Design e identidade visual — Design moderno, tecnológico e profissional. Fundo preto ou azul muito escuro, roxo neon como cor principal, azul como cor secundária, texto branco e cinzento claro, cartões com cantos arredondados, botões modernos, espaçamento organizado, interface responsiva. A página inicial deve apresentar o nome, um slogan, uma descrição da plataforma, três cartões (um por jogo), o botão START CHALLENGE e a explicação do sistema de pontuação.
>
> 4. Jogo 1 — Logic Challenge — Adivinhação numérica: número aleatório entre 1 e 100, 10 tentativas, mensagens "Demasiado alto!" e "Demasiado baixo!", mensagem de vitória e fim de jogo se não acertar. Pontuação: 10 pontos à primeira tentativa, menos um ponto por tentativa, 0 sem acertar. Usar random, if/elif/else, ciclo for ou equivalente, break, variáveis e comparações.
>
> 5. Jogo 2 — Quick Quiz — Cinco perguntas de cultura geral (ciência, matemática, geografia, tecnologia, cultura geral), quatro opções cada, apenas uma correta, feedback e pontuação final. 2 pontos por resposta certa, máximo 10. Usar listas, strings, variáveis, condições e contagem de pontos.
>
> 6. Jogo 3 — Reaction Challenge — Cinco desafios de raciocínio rápido (operações matemáticas, padrões e lógica), com limite de 10 segundos cada. Registar o momento em que o desafio começa e verificar o tempo decorrido quando o utilizador submete a resposta. 2 pontos por resposta correta dentro do tempo, máximo 10. Usar o módulo time. Não inventar um cronómetro automático se a tecnologia não o permitir; implementar uma solução funcional e explicar qualquer limitação.
>
> 7. Sistema de navegação — Ordem: página inicial, Logic Challenge, Quick Quiz, Reaction Challenge, resultados finais. Guardar em st.session_state o número secreto, tentativas, respostas, pontuações, estado de conclusão de cada jogo e página atual. Os resultados não podem desaparecer ao mudar de página. Impedir pontos duplicados por submeter várias vezes a mesma resposta. Botões para avançar entre jogos e para repetir a experiência.
>
> 8. Classificação final — Somar os três jogos (máximo 30), converter em percentagem e classificar: 0–20% Iniciante, 21–40% Em desenvolvimento, 41–60% Inteligência média, 61–80% Inteligência elevada, 81–100% Génio. A página final mostra a pontuação de cada jogo, o total, a percentagem, a classificação e o botão PLAY AGAIN, com uma nota a esclarecer que a classificação mede apenas o desempenho nos jogos e não mede cientificamente a inteligência ou o QI.
>
> 9. Requisitos técnicos — Funcionar com streamlit run app.py, usar st.set_page_config, código organizado em secções, comentários em português, sem erros de sintaxe, sem variáveis desnecessárias, sem dependências em falta nem funcionalidades pagas.
>
> 10. Formato da resposta — Código completo de app.py, explicação simples das partes principais, lista de funcionalidades, instruções para testar e lista de possíveis erros com soluções. Sem omitir partes do código.

### 6.2 Ampliação e construção de funcionalidades

Depois de a primeira versão estar criada, o principal pedido foi para corrigir a ligação entre os ficheiros:

> "Quero que interligues corretamente os ficheiros para que o site funcione como deve ser."

Pedi ainda à IA para acrescentar elementos novos, como a barra do tempo e os efeitos de som e de imagem quando o utilizador erra (resumo do pedido). O jogo Memory Sequence foi criado com IA como jogo novo.

### 6.3 Dificuldades e erros corrigidos com a IA

O maior problema foi que, originalmente, o site não funcionava porque os vários ficheiros não estavam bem interligados. O HTML não carregava corretamente o CSS e o código dos jogos, e partes do código procuravam elementos e ficheiros que não existiam. Pedi à IA para interligar os ficheiros corretamente e organizei o projeto em ficheiros separados, cada um com uma função. Depois disso, o site passou a funcionar como previsto.

### 6.4 Otimização de layout

Mantive sempre o layout original proposto pela IA, porque o design inicial já correspondia à minha ideia. Apenas pedi alterações em algumas decorações:

- a barra do tempo do Reaction Challenge;
- o som quando o utilizador erra;
- o efeito visual quando o utilizador erra.

### 6.5 Passagem da lógica para Python

A versão do projeto que eu tinha entregue tinha a lógica dos jogos escrita em JavaScript (`app.js` e `data.js`). Como a disciplina é de Python, pedi ao Claude para passar toda a lógica para Python, mantendo o HTML e o CSS no frontend. O resultado é a versão descrita neste relatório: um servidor em Python que gera as páginas HTML, com o CSS original (mais animações novas) e sem JavaScript. O Claude também testou os três jogos de ponta a ponta (pontuação, tempo limite, respostas repetidas, sequência de memória, recorde e resultados).

Como o frontend deixou de ter JavaScript, algumas coisas tiveram de ser feitas de outra forma: o cronómetro e a sequência de cores passaram a ser animações CSS, o tempo passou a ser medido no servidor e o recorde passou a ficar guardado num cookie. Estão descritas na secção 3.

## 7. Reflexão crítica e aprendizagem

**O que correu melhor:** o design correu muito bem. A IA conseguiu fazer a minha ideia logo à primeira, e por isso mantive o layout original durante todo o projeto, mudando apenas alguns pormenores de decoração.

**Maior dificuldade:** a maior dificuldade foi encontrar a ideia perfeita para o trabalho. Do lado técnico, o problema que mais me atrasou foi o site não funcionar porque os ficheiros não estavam bem interligados, mas ficou resolvido ao pedir à IA para os ligar corretamente.

**Como a Inteligência Artificial mudou a minha forma de programar:** a IA ajuda imenso na programação. Mudou a forma como trabalho: em vez de começar do zero, descrevo bem a ideia e depois vou testando, corrigindo e pedindo melhorias. Percebi também que é preciso testar e entender o que a IA escreve, porque foi preciso detetar o problema dos ficheiros e pedir a correção certa.
