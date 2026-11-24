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

### Prompt para conversão Web/HTML

Durante o desenvolvimento, foi pedido à IA que adaptasse a aplicação para uma versão web com HTML, CSS e JavaScript, preservando o conceito, o design e as funcionalidades dos jogos. Posteriormente, foi solicitada a passagem da lógica dos jogos para Python, mantendo o JavaScript responsável pelas interações próprias do navegador. Para permitir a publicação no GitHub Pages, a solução passou a executar Python no navegador através do Pyodide.

### Prompt para ampliação e construção de funcionalidades

Foi pedido à IA que interligasse corretamente os ficheiros do projeto, de modo a garantir o funcionamento da aplicação. Também foram solicitadas melhorias na experiência de jogo, incluindo a barra de tempo do Reaction Challenge e efeitos sonoros e visuais quando o utilizador erra. O jogo Memory Sequence foi igualmente desenvolvido com o apoio da IA.

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
