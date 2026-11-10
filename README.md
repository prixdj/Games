# Games
A collection of *Pygame* games that I made.

## Skills Demonstrated Across All Games
 - **Languages, Libraries & Tools**: Python, Pygame-CE, GitHub, Git, PyInstaller, Ruff
 - **Concepts & Practices**: Object-Oriented Programming, Dependency Injection, Data Persistence, Cross-Platform Distribution

## Getting Started
### Requirements
 - **Python 3.10+**
 - **pip**
 - **Pygame-CE**

### General Setup
This will allow you to run any game from source, given you have **Python (3.10+)** and **pip**.

**IMPORTANT: You do not need to do this if you will only download the Windows or MacOS release of a game.**

1. **Open a terminal or an app that access the terminal.**

2. **Clone the repository.**
 *Optional: Put the path of where you want the repository folder to be at the end of the command.*
           *If you do not do this, it will create the folder in your current directory.*
```bash
git clone https://github.com/prixdj/Games.git
```

3. **Navigate to the repository folder.**
 *Note: If you had put the path of where you wanted the repository folder to be, you must change your directory to there first.*
```bash
cd Games
```

4. **Create a python environment.**
 - If you are on **Windows**, run:
```bash
python -m venv .venv
.venv\Scripts\activate
```
 - If you are on **MacOS** or **Linux**, run:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. **Install requirements: Pygame-CE**
```bash
python -m pip install -r requirements.txt
```

### Specific Game Setup
How to run a specific game.

#### Using the Game's Release
1. Navigate to the **releases** tab and **find the game's latest Release**.
2. Follow the instructions *based on your operating system* to play.
*Note: Only Windows and MacOS are supported for game releases. Linux users must run from source code.*

### Running from Source Code
You must be in the **Games** directory in your terminal and in the same environment from **General Setup**.

Then, run:
```bash
python game_name/game_name.py
```
Replace *game_name* with the actual game name.

**Note: For MacOS users, the game may take 20-30 seconds to load the first time as your operating system checks for malware.**

## Disclaimers
### AI
 - **No AI** was used for any code generation or checking code unless otherwise specified.
 - AI was **only used for learning** about code.

### Usage of Third Party Assets, Software or Libraries
 - **Pygame Community Edition**
 - **Space Shooter Remastered Asset Pack** from *Kenney Assets*
 - **PyInstaller**