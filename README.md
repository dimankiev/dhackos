Hacker Simulator 2 (dHackOS)
=============
[Hacker Simulator 2][1] - Reincarnation of [Hacker Simulator 1](https://github.com/dimankiev/hacker_sim)

Written using Python 3.6.

Bots, subnets, tracing, upgrades, comfortable prompt, miners, and a lot of interesting things included in this game.

Actual version: 0.3.3b

Installation (Android)
-----------------------
1. Download and install the [Termux app][2].

2. Don't forget to give [Termux][2] the "Data/SD/Memory access" rights (If your Android version >= 5.0).

3. Launch [Termux][2].

4. Use `cd ~` command to go to Termux home directory.

5. Use `pkg install python` command to install Python (It's needed to launch the game).

6. Install required modules by commands below:
   ```
   apt-get install python-dev clang libcrypt-dev
   pkg install play-audio
   pip install -r requirements.txt
   ```
7. Use `git clone https://github.com/dimankiev/dhackos.git` command to download the game

8. Use `cd dhackos` and `python dhackos.py` commands to start the game

9. Game will tell you which modules are not installed if you didn't installed them.

10. Have a good time :D

Installation (Windows)
-----------------------
1. Download and install (with administrator rights) the [Python][3] (Python version must be >= 3.5).

2. Install required modules by commands below:
   ```
   pip install playsound
   pip install -r requirements.txt
   ```
3. Download the game archive [HERE][4] and unzip it to any folder (Example: `C:\Games\dHackOS`)

4. Check that you are administrator of your PC or move the game into your user account desktop.

5. Open cmd and use the commands below to launch the game:
   ```
   cd {FOLDER_WHERE_YOU_EXTRACTED_THE_GAME_ARCHIVE}\dhackos
   python dhackos.py
   ```
6. Game will tell you which modules are not installed if you didn't installed them.

7. Have a good time :D

Getting started
----------------
1. Create a dHackOS account at start of the game or load the previous game
   - Password can't be less than 6 symbols
   - Please don't forget the password, because it will be used to load saves
   - When you shutting down the dHackOS (game), you can save it
   - Don't try to edit the save, because you can corrupt it

2. Commands:
   ```
    apps - list of installed apps + levels
    help - list of console commands
    shutdown - shutdown dHackOS
    scan - scan subnet and search for vulnerable servers
    scan_target - scan an IP and gather information about target server
    balance - opens Ethereum wallet where you can see your Ethereum balance
    load_list - shows you targets list
    dhackosf - start the dHackOS exploitation framework
    upgrade - launch dHackOS programs upgrade CLI
    stats - shows your stats
    change_ip_v - move from IPv4 (old IP version) to IPv6 (new IP version) (Can't be undone)
    version - version of dHackOS
    update_ip - replacing your ip with new one
    miner - show last 10 mined blocks (short log)
    rescan_subnet - rescans subnet to find new targets
    news - show latest cyber security news
    debug_info - shows you debug information
    miner_info - shows you your miner components
    miner_shop
    buy_miner - buy one more miner
    bank - DarkNet Bank CLI
    hilo_game - High/Low Bet Game
    lanhunt - LanHunt Drone System CLI (BETA)
    miner_stat - Show miner power status
    miner_cfg - Switch the miner power on/off
    clear - Clean the screen
   ```

3. Use `scan` to find first targets.

4. Then, select and IP and remember it.

5. Launch dHackOS Exploitation Framework by `dhackosf` command, then enter IP that you remembered. dHackOSf will be launched, then type `help` to see the dHackOSf commands list.

6. Don't forget to upgrade your apps

7. You can see your statistics by `stats` command

Requirements
----------------------

1. Python version >= 3.6

2. Install required modules by commands below:
   ```
   pip install -r requirements.txt
   ```

Links
----------
- [dimankiev (Telegram)](https://t.me/dimankiev)
- [dhackos (Telegram)](https://t.me/dhackos)

Maintainers
-------------------
- Dmytro Nelipa [(Telegram)](https://t.me/dimankiev) [(GitHub)](https://github.com/dimankiev)

Contributors
-------------------
- Eight Nice [(Telegram)](https://t.me/eightnice)

Alpha-testers
-------------------
- [Taptrue(Telegram)](https://t.me/taptrue)

License
---------
Hacker Simulator is BSD-3-Clause Licensed  
Copyright © 2018-2024 dimankiev

[1]: https://github.com/dimankiev/dhackos
[2]: https://termux.com/
[3]: https://www.python.org/downloads/windows/
[4]: https://github.com/dimankiev/dhackos/archive/master.zip
[5]: https://dimankiev.github.io/dhackos/
