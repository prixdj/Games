<div align="center">
    <h1> Survoids <img src="assets/app_icon.ico" width="32" height="32" align="absmiddle" alt="Survoids Icon"/></h1>
    <blockquote> A <b>2D space-shooter roguelike</b> game inspired by <em>Asteroids</em> and <em>Vampire Survivors.</em></blockquote>
    <br>

![Made with Pygame-CE](https://img.shields.io/badge/Made_with-Pygame--CE-6AF02A?style=for-the-badge&logo=Python)
</div>

This game is adapted from a game I made using *Pygame Zero*.

The purpose of **Survoids** is to learn *Pygame-CE* and demonstrate my *Python* skills.

## Gameplay Features
<a id="gameplay-gif"></a>
<div align="center">
    <table>
        <tr>
            <td width="70%">
                <video src="https://github.com/user-attachments/assets/1a16b955-0748-4dcc-b1c2-f9080245589d">
                    mp4 demonstrating Survoids gameplay
                </video>
                <sub><em>Survoids Gameplay Demo</em></sub>
            </td>
        </tr>
    </table>
</div>
<br>

 - **[Fight](#in-game) endless waves of enemies of four types**
 - **[Move](#gameplay-gif) with space-like physics**
 - **[Level](#level-and-buff) up and choose an upgrade to your ship**
 - **[Collect](#level-and-buff) buffs dropped by enemies for temporary power**
 - **[Retry](#retry) to try and beat your previous runs**
 - **[Pause](#pause) the game if you need to take a break**
 - **[See](#previous-runs) all your previous runs**
 - **[Remap](#remap-controls) your controls to your choice**

## Skills Demonstrated
 - **Object-Oriented Programming**: Creating objects for sprites such as `Player`, `Enemy`, `Bullet` and `Text`.
 - **Data Persistence**: Saving permanent controls and run data to `controls.txt` and `game_results.txt`.
 - **Dependency Injection**: Passing data to and from functions and objects as they require it, having no global variables.
 - **Event-Driven Programming**: Handling player input in the main event loop every frame to trigger custom game events.
 - **State Management**: Tracking the game's state throughout execution using the `game_state` variable.

## How to Play
### Requirements
 - **[Git](https://git-scm.com/install/)**
 - **Python 3.10+**
 - **pip**
 - **Pygame-CE**

### Windows and MacOS Release
1. Navigate to the **releases** tab and find **Survoids - v1.0.0 Release**, or click **[here](https://github.com/prixdj/Games/releases/tag/Survoids-v1.0.0)**.
2. Follow the instructions *based on your operating system* to play.

### Source Code and Linux Users
This will allow you to run **Survoids** from source, given you have **Python (3.10+)** and **pip**.

**IMPORTANT: You do not need to do this if you will only download the Windows or macOS release of Survoids.**

1. **Open a terminal or an app that accesses the terminal.**

2. **Clone the repository.**

***Optional**: Put the path to where you want the cloned repository to be at the end of the command. If you do not do this, it will create the folder in your current directory.*
```bash
git clone https://github.com/prixdj/Games.git
```

3. **Navigate to the repository folder.**
```bash
cd Games
```
***Note**: If you had put the path to where you wanted the cloned repository to be, you must change your directory to there first. The following command is a template for steps **2** and **3** with `<path/to/your/folder>`.*
```bash
git clone https://github.com/prixdj/Games.git <path/to/your/folder>
cd <path/to/your/folder>/Games
```

4. **Create a python environment.**
 - If you are on **Windows**, **run**:
```bash
python -m venv .venv &&
.venv\Scripts\activate
```
 - If you are on **macOS** or **Linux**, **run**:
```bash
python3 -m venv .venv &&
source .venv/bin/activate
```

5. **Install requirements: Pygame-CE**
```bash
python -m pip install -r requirements.txt
```
6. **Run Survoids.**
```bash
python survoids.py
```
***Note for macOS users**: The first time you open Survoids, it may take 20-60 seconds to check for malware. Subsequent opens will take 2-3 seconds.*

## Gameplay Images
<div align="center">
    <kbd>
        <img src="assets/prev_main_screen.png" alt="Main Screen Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>The main screen of Survoids.</em></sub>
</div>
<br>

<a id="in-game"></a>
<div align="center">
    <kbd>
        <img src="assets/prev_in_game.png" alt="In Game Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>In game preview.</em></sub>
</div>
<br>

<a id="level-and-buff"></a>
<div align="center">
    <kbd>
        <img src="assets/prev_levels_and_buffs.png" alt="Levels and Buffs Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>Levelling up allows you to choose an upgrade, killing enemies may drop temporary buffs.</em></sub>
</div>
<br>

<div align="center">
    <kbd>
        <img src="assets/prev_boss.png" alt="Boss Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>Fight a huge boss enemy.</em></sub>
</div>
<br>

<a id="pause"></a>
<div align="center">
    <kbd>
        <img src="assets/prev_pausing.png" alt="Pause Menu Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>Pause the game if you need to take a break.</em></sub>
</div>
<br>

<a id="retry"></a>
<div align="center">
    <kbd>
        <img src="assets/prev_retry.png" alt="Retry Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>If you die, click retry to try again.</em></sub>
</div>
<br>

<a id="previous-runs"></a>
<div align="center">
    <kbd>
        <img src="assets/prev_previous_runs_screen.png" alt="Previous Runs Screen Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>See your previous runs.</em></sub>
</div>
<br>

<div align="center">
    <kbd>
        <img src="assets/prev_controls_screen.png" alt="Controls Screen Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>See the controls of the game.</em></sub>
</div>
<br>

<a id="remap-controls"></a>
<div align="center">
    <kbd>
        <img src="assets/prev_remapping_controls.png" alt="Remapping Controls Preview" width="600"/>
    </kbd>
    <br>
    <sub><em>Remap the controls to how you want them.</em></sub>
</div>

## Disclaimers
### Usage of Third Party Assets
 - **[Space Shooter Remastered Asset Pack](https://kenney.nl/assets/space-shooter-remastered)** from *Kenney Assets*

### License
This project is licensed under the **[MIT License](LICENSE)**.

## Development Environment
 - **Windows 10** and **macOS Tahoe 26+**
 - **Git v2.39.5 (macOS) and 2.54.0 (Windows)**
 - **Miniconda Python v3.13.5**
 - **pip v25.1**
 - **Pygame Community Edition v2.5.8**
 - **PyInstaller v6.22.3**
 - **Krita v5.2.3**
