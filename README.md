# 🎮 Tic Tac Toe — Modern Pygame Edition

A fully-featured Tic Tac Toe game built with **Pygame**, featuring a clean modern UI, an unbeatable AI opponent, animated gameplay, match history, and score tracking.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) ![Pygame](https://img.shields.io/badge/Pygame-2.x-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🤖 **AI opponent** — 3 difficulty levels with Minimax + Alpha-Beta pruning
- 👥 **2-Player mode** — local multiplayer on the same screen
- 🎨 **Modern UI** — clean flat design with X in blue and O in coral themes
- 💥 **Animations** — pop-in scale animation when placing marks, win line strike-through
- 🏆 **Score tracker** — persistent X wins / Draws / O wins across rounds
- 📋 **Match history** — last 3 game results shown with round number and opponent
- 🟢 **Status indicator** — pulsing dot (green = your turn, amber = AI thinking, red = game over)
- 🔄 **Auto-advance** — next round starts automatically after win or draw
- ⌨️ **Keyboard support** — press ESC to quit

---

## 🖥️ Preview

```
┌─────────────────────────────────────────┐
│           Tic Tac Toe                   │
│  [ 2 Players ]  [ vs AI ]               │
│  [ Easy ] [ Medium ] [ Hard ]           │
│                                         │
│  X wins: 3   Draws: 1   O wins: 2      │
│                                         │
│  ┌───────┬───────┬───────┐             │
│  │   X   │       │   O   │             │
│  ├───────┼───────┼───────┤             │
│  │       │   X   │       │             │
│  ├───────┼───────┼───────┤             │
│  │   O   │       │   X   │  ← wins!   │
│  └───────┴───────┴───────┘             │
│                                         │
│  Match history: X wins · Draw · O wins  │
└─────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install pygame
```

### Run

```bash
python tic_tac_toe.py
```

---

## 🤖 AI Difficulty Levels

| Level | Behaviour |
|-------|-----------|
| **Easy** | Picks a random empty cell |
| **Medium** | 50% random, 50% optimal — beatable |
| **Hard** | Perfect Minimax + Alpha-Beta pruning — unbeatable |

> The Hard AI will never lose. Best you can do is force a draw!

---

## 🎮 How to Play

1. Select **2 Players** or **vs AI** using the pill buttons at the top
2. If playing vs AI, choose your difficulty — Easy, Medium, or Hard
3. Click any empty cell on the board to place your mark
4. First to get 3 in a row (horizontal, vertical, or diagonal) wins
5. The game auto-resets after each round — scores carry over
6. Hit **New game** to restart the current round, or **Reset all** to clear everything

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| `pygame` | Window, rendering, event loop, animations |
| `math` | Sine-based dot pulse animation |
| `random` | Easy / Medium AI move randomisation |

---

## 🏗️ Code Architecture

```
tic_tac_toe.py
├── Constants & palette     — colors, board dimensions, fonts
├── Helpers                 — rrect(), blit_text(), lerp_col()
├── Game logic              — check_winner(), is_draw(), available()
├── Minimax AI              — minimax() with alpha-beta pruning, best_move()
├── class Button            — reusable hover+click UI button
└── class Game
    ├── __init__()          — setup, initial state
    ├── new_game()          — reset board for next round
    ├── play()              — handle a move, check win/draw, trigger AI
    ├── update()            — animations, AI delay timer
    ├── draw()              — full frame render (score, board, history, status)
    ├── handle()            — event loop, button clicks, cell clicks
    └── run()               — main game loop
```

---

## 📁 Project Structure

```
tic_tac_toe.py      # Single-file application — just run it
README.md           # This file
```

---

## 🌐 Platform Support

| OS | Status |
|----|--------|
| Windows 10/11 | ✅ Full support |
| macOS 12+ | ✅ Full support |
| Linux (Ubuntu, Arch) | ✅ Full support |

---

## 🤝 Contributing

PRs welcome! Ideas for future features:
- Sound effects on move and win
- Animated confetti on victory
- Online multiplayer via sockets
- 4x4 or 5x5 board variant

---

## 📄 License

MIT License — free to use and modify.

---

> Built with Python & Pygame — zero web dependencies, runs anywhere 🎮
