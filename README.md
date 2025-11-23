# 🚩 Ultimate Retro Minesweeper

A faithful yet modernized recreation of the classic Windows 95/XP Minesweeper, built entirely in Python with Pygame. 

This project goes beyond a simple clone; it includes advanced features like a logic-based **Analysis Engine**, **No-Guessing Mode**, **Replay System**, and **Retro Themes**, all contained within a single script without external assets.

## ✨ Key Features

### 🎮 Core Experience
* **Classic Gameplay:** Authentic mechanics and feel of the original game.
* **Single-File Architecture:** No images or sound files required. All assets (graphics, sounds) are procedurally generated in code.
* **Difficulty Levels:** Beginner, Intermediate, Expert, and fully **Customizable** board size/mines.

### 🚀 Modern Enhancements
* **Analysis Helper:** A real-time "Blind Analysis" engine that highlights 100% safe cells (Green), confirmed mines (Red), and risky areas (Yellow) based on pure logic.
* **Tutorial Mode:** Visual feedback system to help players understand patterns.
* **No Guessing Mode:** Generates solvable boards where 50/50 guesses are never required.
* **Autopilot (AI Solver):** Press `SPACE` to let the AI execute a logically safe move for you.
* **Replay System:** Watch a replay of your game after winning or losing.
* **Advanced Stats:** Tracks 3BV, Efficiency, and Clicks per Second (CPS).

### 🎨 Visuals & Audio
* **Theme System:** Switch between **Classic**, **Dark Mode**, **Windows XP**, **Matrix**, and **Hotdog Stand** themes.
* **Particle Effects:** Satisfying pixel explosions and confetti effects.
* **Sound Synthesizer:** Retro square-wave sound effects generated in real-time.

### 🌍 Localization
* **Multi-Language Support:** Fully localized in **English** (Default) and **Turkish**.

## 🛠️ Installation & Usage

1.  **Prerequisites:** You need Python installed.
2.  **Install Pygame:**
    ```bash
    pip install pygame
    ```
3.  **Run the Game:**
    ```bash
    python minesweeper.py
    ```

## ⌨️ Controls

| Key / Action | Function |
| :--- | :--- |
| **Left Click** | Reveal Cell |
| **Right Click** | Flag / Question Mark |
| **F2** | New Game |
| **SPACE** | **Autopilot** (AI makes a move) |
| **P** | Pause Game |
| **R (Button)** | Replay Last Game (After Game Over) |
| **Menu** | Access Settings, Themes, and Difficulty |

## 🧠 Analysis System Logic

The built-in **Analysis Helper** uses an iterative logic engine that simulates a human player's perspective. It does *not* cheat by looking at the mine map.
* **Green Overlay:** 100% Safe. The engine proved logically that no mine can exist here.
* **Red Overlay:** 100% Mine. The engine proved a mine must exist here.
* **Yellow Overlay:** Ambiguous/Risk. Requires more information to solve.

## 🏆 High Scores

Scores are saved locally in `highscores.json`. The leaderboard tracks:
* Time
* 3BV (Bechtel's Board Benchmark)
* Efficiency Percentage

---

<sub>Prepared with the help of Gemini 3 Pro.</sub>
