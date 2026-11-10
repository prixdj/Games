# Survoids
**Survoids** is a game inspired by *Asteroids* and *Vampire Survivors* that I adapted from a game I made in Year 11 using *Pygame Zero*.

## Skills Demonstrated in Survoids
 - **Data Persistence**: Saving controls and run data to `controls.txt` and `game_results.txt`.
 - **Dependency Injection**: Passing data to and from functions and objects as they require it, having no global variables.
 - **Event-Driven Programming**: Handling player input in the main event loop every frame to trigger custom game events.
 - **State Management**: Tracking the game's state throughout execution using the `game_state` variable.
 - **PEP 8 Compliance**: Ensuring best-practice code formatting through the use of Ruff.

## Gameplay Features
 - **Fight endless waves of enemies of four types**
 - **Move with space-like physics**
 - **Level up and choose an upgrade to your ship**
 - **Collect buffs dropped by enemies for temporary power**
 - **See all your previous runs**
 - **Remap your controls to your choice**

## Requirements
 - **Python 3.10+**
 - **pip**
 - **Pygame-CE**

## Running Survoids
### Windows and MacOS Release
1. Navigate to the **releases** tab and find **Survoids - v1.0.0 Release**.
2. Follow the instructions *based on your operating system* to play.

### Source Code and Linux Users
 - Follow the **General Setup instructions** in the **Games README.md**, then run:
```bash
python survoids/survoids.py
```

## Disclaimers
### AI Disclaimer
 - **No AI** was used for any code generation or checking code other than helping with path correction and PyInstaller.
 - AI was **used for learning** about code.

### Usage of Third Party Assets
 - **Space Shooter Remastered Asset Pack** from *Kenney Assets*

## Development Environment
 - **Miniconda Python v3.13.5**
 - **pip v25.1**
 - **Pygame Community Edition v2.5.8**
 - **PyInstaller v6.22.3**