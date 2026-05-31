# 🏃‍♂️ PythonRunner

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pygame](https://img.shields.io/badge/pygame-black?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

**PythonRunner** é um jogo do estilo *Endless Runner* com elementos de Quiz educativo, desenvolvido em Python usando a biblioteca Pygame. O jogo combina testes de reflexo em alta velocidade com perguntas sobre lógica de programação baseadas no próprio jogo.

Sobreviva a obstáculos imprevisíveis, colete *power-ups*, responda a perguntas sob pressão e derrote o Chefão implacável para provar seu conhecimento!

---

## ✨ Features e Mecânicas

* 🚀 **Dificuldade Progressiva:** O jogo acelera organicamente. Após derrotar o Chefão, o sistema entra no *Módulo de Alta Performance* (Fase 2) com um tema noturno e obstáculos ainda mais rápidos.
* 🛡️ **Power-Ups Dinâmicos:** * **Escudo (Ciano):** Absorve um impacto direto e destrói o obstáculo.
* ✴️ **Multiplicador (Amarelo):** Dobra os pontos ganhos durante 7 segundos.
* 👾 **Boss Fight - "O Auditor":** Após 45 segundos, enfrente um inimigo flutuante que dispara lasers de débito técnico teleguiados.
* 🧠 **Sistema de Quiz Integrado:** Responda perguntas temáticas para ganhar bónus ou penalizações de vida. O texto redimensiona-se automaticamente para caber no card.
* 💥 **Game Feel Avançado:** *Screen shake* (tremor de ecrã) nos impactos, sistema de partículas nas explosões, e *Juice* visual inspirado na paleta de cores do tema *Dracula*.

---

## 🎮 Como Jogar

O objetivo é sobreviver o máximo de tempo possível e acumular pontos. 

### Controlos:
* **Saltar:** `ESPAÇO`, `W` ou `Seta para Cima`
* **Deslizar (Slide):** `S` ou `Seta para Baixo` *(Útil para passar por baixo de obstáculos que voam em movimentos de onda)*
* **Responder Perguntas:** Teclas `A`, `B` ou `C` (quando a tela de pergunta aparecer).

---

## 🛠️ Instalação e Execução

### Para utilizadores Windows (Instalação com 1 Clique)
Se apenas quer jogar e não tem o Python configurado na sua máquina, siga estes passos:
1. Faça o download/clone desta pasta.
2. Dê um duplo clique no arquivo `setup.bat`.
   * *O script irá baixar o Python 3.12, instalar o gestor de pacotes `uv` e configurar o ambiente virtual do jogo automaticamente.*
3. Após a instalação, um novo ficheiro chamado `jogar.bat` será criado.
4. Clique em `jogar.bat` para iniciar o jogo!

### Para Desenvolvedores (Linux / Mac / Windows Manual)
O projeto utiliza o gerenciador de pacotes ultrarrápido [uv](https://github.com/astral-sh/uv).

1. Certifique-se de ter o `uv` instalado no seu sistema (via `curl` ou `pip`).
2. Clone o repositório e navegue até a pasta:
```bash
git clone https://github.com/muliroZ/PythonRunner
cd PythonRunner
```

3. Sincronize as dependências e crie o ambiente virtual:
```bash
uv sync

```


4. Execute o jogo:
```bash
uv run main.py

```



---

## 📝 Como adicionar as suas próprias perguntas

As perguntas estão completamente separadas do código fonte, permitindo que qualquer pessoa crie os seus próprios módulos de estudo.

Para editar ou adicionar novas perguntas, abra os ficheiros JSON na pasta `assets/`:

* `assets/perguntas.json` (Perguntas normais que aparecem a cada 1000 pontos)
* `assets/perguntas_boss.json` (Dilemas complexos que o Auditor faz durante a Boss Fight)

**Estrutura do JSON:**

```json
{
  "q": "Qual o foco da Sustentabilidade Verde no software?",
  "options": [
    "A) Eficiência de energia", 
    "B) Maximização de lucro", 
    "C) Layout bonito"
  ],
  "answer": "a"
}

```

*Atenção: A chave `"answer"` deve conter apenas a letra da opção correta em minúsculo ("a", "b" ou "c").*

---

## 📂 Arquitetura do Projeto

O código está organizado seguindo o padrão de Máquinas de Estado e Orientação a Objetos (Cenas e Sprites).

* `main.py` - Ponto de entrada.
* `src/game.py` - Classe principal que gere o *loop* do jogo, áudio e transições de cena.
* `src/scenes/` - Lógica isolada para Menu, Jogo, Game Over e Quiz.
* `src/spawner.py` - O "Diretor" do jogo, responsável por criar padrões e armadilhas duplas baseando-se na velocidade atual.
* `src/boss.py` - Lógica de movimento trigonométrico e disparos teleguiados do Boss.

---

### Equipe
* [Gustavo Vilela](https://github.com/Gustavo0606)
* [José Severo](https://github.com/Severoabreu)
* [Maria Carolina](https://github.com/CarolinaaCabral)
* [Mateus Aguiar](https://github.com/mateusaguiiiar)
* [Murilo Andrade](https://github.com/muliroZ)

---

*Desenvolvido como um projeto prático para a disciplina _DCExt III_ da Universidade de Pernambuco (UPE).*
