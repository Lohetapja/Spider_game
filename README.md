# Anette 🎮

Its is/was work in progress. 
A tiny Pygame experiment revived from my first-ever game project. Built with a lot of curiosity and “vibe coding.”  
1080×1080, 60 FPS, simple controls, and a few home-made assets.

Spider_game/
├─ src/
│  ├─ 2mblik_v5.py
│  └─ old_versions/
│      ├─ food_small.png
│      ├─ enemy_small.png
│      ├─ player_small.png
│      ├─ ground.jpg


## Demo
![Gameplay GIF](screenshots/gameplay.gif) - 

<img width="1084" height="1112" alt="image" src="https://github.com/user-attachments/assets/6be0824a-1ee4-4bf0-9735-8506b7e13ea1" />


## Features
- Pygame loop with 60 FPS clock
- Image loader with scaling and alpha
- Basic UI fonts (title + HUD)
- Simple input & collision stubs (easy to extend)

## Controls
- `W/A/S/D` or arrow keys – move
- `ESC` – quit

## Tech
- Python 3.10+ (works on 3.8+)
- Pygame 2.5+

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
