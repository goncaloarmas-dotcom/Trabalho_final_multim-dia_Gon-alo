# BRAIN TRAINING HUB

**Disciplina:** Oficina de Multimédia - 12.º Ano - CRSI  
**Ano Letivo:** 2026/2027  
**Autor:** Gonçalo Monteiro Borges Armas Gonçalves  
**Turma:** 12A3  
**Link da Aplicação Web:** [Brain Training Hub](https://goncaloarmas-dotcom.github.io/Trabalho_final_multim-dia_Gon-alo/)

## 1. Visão Geral do Projeto

### Descrição

O Brain Training Hub é um dashboard web que reúne três jogos curtos de lógica, raciocínio, reflexos e memória. No final, o utilizador recebe uma pontuação total até 30 pontos, uma percentagem e uma classificação; o seu melhor resultado fica guardado no navegador.

### Proposta Escolhida

**Proposta 1 — Dashboard Web de Ferramentas Multimédia com IA.**

## 2. Estrutura do Código e Funcionalidades Integradas

O projeto combina exercícios adaptados das fichas de Python com um jogo novo desenvolvido com o apoio da Inteligência Artificial. A lógica dos jogos, a validação das respostas e o cálculo das pontuações são feitos em Python. O JavaScript assegura a comunicação com o navegador e apresenta os elementos visuais e interativos.

### Tecnologias utilizadas

- **Python 3:** implementa a lógica dos jogos, a validação das respostas, a gestão do tempo e o cálculo dos resultados.
- **Pyodide:** permite executar Python diretamente no navegador.
- **HTML e CSS:** definem a estrutura, o aspeto visual e a adaptação a diferentes ecrãs.
- **JavaScript:** gere a apresentação dos dados, as animações, os sons e a comunicação entre a página e o código Python.
- **GitHub Pages:** aloja a aplicação web.

O projeto está organizado para que o GitHub Pages disponibilize os ficheiros da aplicação e o Pyodide execute o código Python no navegador. Para carregar o Pyodide e os recursos associados, é necessária uma ligação à Internet.

### Jogos integrados

**1. Logic Challenge**

- **Origem:** exercício adaptado da ficha «Adivinha o número».
- **Conceitos de Python:** aleatoriedade, condições (`if`, `elif` e `else`), comparações e limite de tentativas.
- **Funcionamento:** o utilizador tenta descobrir um número secreto.
- **Pontuação:** até 10 pontos, começando em 10 na primeira tentativa e diminuindo um ponto por cada tentativa adicional.
- **Código:** classe `LogicGame`, em `game/engine.py`.

**2. Reaction Challenge**

- **Origem:** exercício adaptado da ficha do quiz de perguntas e ampliado com o apoio da IA.
- **Conceitos de Python:** strings, listas, condições e módulo `time`.
- **Funcionamento:** o utilizador responde a cinco desafios, cada um com um limite de 10 segundos. O tempo é controlado através de `time.monotonic()`, pelo que uma resposta submetida fora do prazo não é considerada válida.
- **Pontuação:** 2 pontos por resposta correta, até um máximo de 10.
- **Código:** classe `ReactionGame`, em `game/engine.py`; desafios em `game/data.py`; validação em `game/answers.py`.

**3. Memory Sequence**

- **Origem:** jogo novo criado com o apoio da IA.
- **Conceitos de Python:** listas, lógica de jogo e módulo `random`.
- **Funcionamento:** o utilizador acompanha e reproduz sequências de memória.
- **Pontuação:** 1 ponto por ronda, até um máximo de 10.
- **Código:** classe `MemoryGame`, em `game/engine.py`.

### Funcionalidades principais

- Página inicial com cartões de apresentação dos três jogos e botão para iniciar.
- Barra de progresso que acompanha as etapas: Lógica, Reação, Memória e Resultados.
- Cronómetro circular no Reaction Challenge, com animações de aviso e de fim do tempo.
- Efeitos sonoros e visuais quando o utilizador erra.
- Validação de respostas que reconhece maiúsculas, minúsculas, acentos e algumas variantes de escrita.
- Ecrã de resultados com pontuação total, percentagem, classificação, resultados por jogo e revisão das respostas.
- Registo do melhor resultado no navegador, através de `localStorage`.
- Nota informativa que esclarece que a classificação representa apenas o desempenho nos jogos e não mede cientificamente a inteligência ou o QI.

A classificação final é calculada com base na percentagem da pontuação máxima de 30 pontos:

| Percentagem | Classificação |
|---|---|
| 0–20% | Iniciante |
| 21–40% | Em desenvolvimento |
| 41–60% | Bom desempenho |
| 61–80% | Desempenho elevado |
| 81–100% | Mestre do raciocínio |

## 3. Registo de Utilização da IA

### Ferramentas utilizadas

- **ChatGPT:** apoio à organização das ideias e definição do projeto.
- **Claude e Antigravity:** apoio à escrita, desenvolvimento e correção do código.

### Prompt inicial para criação da aplicação

O primeiro pedido à IA foi para desenvolver uma aplicação em Python com Streamlit. Esta foi a versão inicial do projeto, que mais tarde evoluiu para a aplicação web atual.

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

### Prompt para conversão Web/HTML e Python

Ao longo do desenvolvimento, a aplicação foi adaptada de uma versão inicial em Streamlit para uma aplicação web com HTML, CSS e JavaScript. Mais tarde, foi pedida a conversão da lógica dos jogos para Python e a adaptação para publicação no GitHub Pages, através do Pyodide:

> Converter o projeto de JavaScript para Python, mantendo o design, a estrutura e as funcionalidades. Utilizar o máximo de Python possível: a mecânica dos jogos, a validação das respostas, as pontuações e a classificação devem ficar em Python; o JavaScript deve ficar responsável pelas interações do navegador. Adaptar também a solução para funcionar no GitHub Pages, recorrendo ao Pyodide.

### Prompt para ampliação e construção de funcionalidades

Para corrigir a ligação entre os ficheiros do projeto, foi utilizado o seguinte pedido:

> Quero que interligues corretamente os ficheiros para que o site funcione como deve ser.

Também foram pedidos elementos adicionais, como a barra de tempo do Reaction Challenge e os efeitos sonoros e visuais quando o utilizador erra. O jogo Memory Sequence foi criado com o apoio da IA.

### Dificuldades e erros corrigidos com a IA

Uma das principais dificuldades técnicas surgiu quando os ficheiros HTML, CSS, JavaScript e Python não estavam corretamente interligados. Por esse motivo, a página não carregava alguns recursos e partes do código procuravam elementos ou ficheiros que não existiam.

Com o apoio da IA, a estrutura foi reorganizada e as ligações entre os ficheiros foram corrigidas. Durante a evolução do projeto, a lógica dos jogos, os dados dos desafios e a validação das respostas foram também organizados em módulos Python separados. Foram ainda acrescentados testes automáticos e corrigida uma situação em que, ao iniciar um novo jogo, continuava a aparecer uma mensagem da partida anterior no Logic Challenge.

### Otimização de Layout

O design inicial correspondeu à ideia pretendida, pelo que a estrutura visual foi mantida ao longo do desenvolvimento. As alterações pedidas à IA incidiram sobretudo em elementos de interação e decoração: a barra de tempo do Reaction Challenge, o som reproduzido quando o utilizador erra e o respetivo efeito visual.

## 4. Estrutura de Ficheiros do Repositório

A aplicação está organizada nos seguintes ficheiros e pastas:

```text
BRAIN TRAINING HUB/
├── index.html
├── style.css
├── app.js
├── game/
│   ├── __init__.py
│   ├── engine.py
│   ├── data.py
│   ├── answers.py
│   └── bridge.py
├── tests/
│   └── test_game.py
├── .nojekyll
├── .gitignore
└── README.md
```

- **`index.html`** — estrutura da página web e carregamento dos recursos necessários.
- **`style.css`** — cores, disposição dos elementos, animações e adaptação a diferentes ecrãs.
- **`app.js`** — comunicação com o Python, apresentação dos ecrãs, animações e sons.
- **`game/__init__.py`** — identifica a pasta `game` como um módulo Python.
- **`game/engine.py`** — lógica dos três jogos, gestão do tempo, pontuação e classificação.
- **`game/data.py`** — conjunto de desafios do Reaction Challenge.
- **`game/answers.py`** — validação e normalização das respostas.
- **`game/bridge.py`** — comunicação entre o JavaScript e o Python, através dos dados trocados em formato JSON.
- **`tests/test_game.py`** — testes automáticos da lógica, do tempo, da comunicação e do funcionamento dos jogos.
- **`.nojekyll`** — ficheiro utilizado na publicação através do GitHub Pages.
- **`.gitignore`** — indica os ficheiros que devem ser ignorados pelo Git.
- **`README.md`** — documento de apresentação e descrição do projeto.

## 5. Reflexão Crítica e Aprendizagem

O que correu melhor durante o desenvolvimento foi a concretização do design e da ideia visual do projeto. A primeira proposta de layout correspondeu ao que pretendia, pelo que apenas foram necessários alguns ajustes nos elementos de interação, como o cronómetro e os efeitos associados às respostas erradas.

A maior dificuldade foi encontrar uma ideia adequada para o trabalho. Já durante a implementação, o problema mais complicado foi garantir que os diferentes ficheiros comunicavam corretamente. Essa situação foi ultrapassada com a reorganização do código e a correção das ligações entre os ficheiros.

A Inteligência Artificial mudou a minha forma de programar, porque me permitiu transformar uma ideia numa aplicação funcional de forma mais orientada. Em vez de começar sempre do zero, passei a descrever o que pretendia, testar o resultado e pedir correções ou melhorias quando necessário. Também percebi que a IA não substitui a necessidade de compreender e testar o código: é importante identificar os erros, perceber o que não está a funcionar e saber explicar à IA o que precisa de ser corrigido.
