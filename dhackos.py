try:
    import sys
    import getpass as pwd
    import random as rnd
    import threading, progressbar, time, shelve, hashlib, base64, string, datetime, platform, math
    from psutil import *
    from os import stat, remove
    import os
    import json
    import traceback
    from colorama import Fore, Back, Style, init
    from math import pi
    from typing import List, Union
    from prompt_toolkit.shortcuts import prompt
    from prompt_toolkit.styles import Style as pStyle
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import InMemoryHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from introd import intro, intro_nosound, clear_tty, say
    from soundwork import *

except Exception as e:
    print("\nPlease, use the commands below to install required modules: ")
    print("""
 pip install "module name that printed below"
 Example: pip install progressbar2
 """)
    print(str(e))
    exit()

from core.game.utils import ip as ip_generator
from core.game.utils import strings as _strings
from core.game.utils.printing import SR, SB, GR, YW, RD, BL, WT, print_vocabulary

from core.game.modules import bank as banking

from core.game.programs.lanhunter import lanhunt
from core.game.programs.bank import program_run as bank_program

from core.game import player as _player

player = _player.Player()
stats = _player.Stats()
bank = banking.Bank()

init()

miner_power_status = "on"
version = "0.3.3b"

clear_tty()
while True:
    enable_sound = str(input("Enable sound? (yes/no): ").lower())
    if enable_sound == "yes" or enable_sound == "y":
        intro()
        break
    elif enable_sound == "no" or enable_sound == "n":
        intro_nosound()
        break
    else:
        print(RD + "Unknown input. Yes or no?" + SR)


strings = _strings.Strings()

debug_info = {
    "Version :": str("\n  dHackOS v." + version),
    "OS :": str("\n  " + platform.system() + " " + platform.release()),
    "RAM :": str("\n  Total : " + '{0:.2f}'.format(
        float(virtual_memory()[0] / 1073741824)) + " GB\n  Used : " + '{0:.2f}'.format(
        float(virtual_memory()[3] / 1073741824)) + " GB\n  Free : " + '{0:.2f}'.format(
        float(virtual_memory()[1] / 1073741824)) + " GB")
}


def gen_ip():
    if sol == "New" or sol == "new":
        ip = ip_generator.gen_ip_v4()
    elif player.ipv6 == 1:
        ip = ip_generator.gen_ip_v6()
    else:
        ip = ip_generator.gen_ip_v4()
    return ip


def getVarFromFile(filename):
    data: shelve.Shelf
    try:
        data = shelve.open("saves/" + filename + ".db")
        success_sload = 1
    except:
        success_sload = 0
        data.close()
    return data, success_sload


def gamesave_load(username):
    global apps, success_load, minehistory, targets, ips, miner, anticheat, miner_power_status, off_earn_k, miner_power, mined, bank_off_earn_k, path, saveinfo
    success_load = 0
    try:
        with open(os.path.join('saves', username + '.md5'), 'r') as f:
            hashsum = str(f.readline())
            try:
                checksum = md5SaveCheckSum(os.path.join('saves', username + '.db'), username, 0)
            except:
                success_load = 0
            f.close()
        if hashsum != checksum:
            print(GR + SB + "\n[INTEGRITY_CHECK] " + Style.NORMAL + "Save is: " + SB + RD + "MODIFIED\n" + SR)
            anticheat = 0
        else:
            print(GR + SB + "\n[INTEGRITY_CHECK] " + Style.NORMAL + "Save is: " + SB + "OK\n" + SR)
            anticheat = 1
        data_loaded, data_load_success = getVarFromFile(str(username))
        if data_load_success == 1:
            player.load(data_loaded['player'])
            apps = data_loaded['apps']
            stats.load(data_loaded['stats'])
            minehistory = data_loaded['minehistory']
            targets = data_loaded['targets']
            ips = data_loaded['ips']
            miner = data_loaded['miner']
            if data_loaded.get('bank') is not None:
                bank.load_bank_data_legacy(data_loaded['bank'])
            if data_loaded.get('bank_accounts') is not None:
                bank.accounts_load(data_loaded['bank_accounts'])
            saveinfo = data_loaded['saveinfo']
            miner_power_status = data_loaded['miner_power_status']
            data_loaded.close()
        else:
            data_loaded.close()
        if saveinfo["version"] != version:
            print(RD + SB + f"Your save is outdated. Save version is {saveinfo['version']}" + SR)

        if md5(pwd.getpass("Please enter your password: "), "dhackos") != player.password:
            print(RD + "The password is wrong !\n" + SR)
            success_load = 0
        else:
            stats.update(_player.StatsTypes.game_launches, 1)
            off_earn_k = time.time() - saveinfo["timestamp"]
            miner_power = float(
                (rnd.uniform(0.0000001, 0.0005) * rnd.randint(25, 100)) * miner["cpu"] * miner["gpu"] * miner["ram"] *
                miner["software"] * 200)
            miners_total = stats.get(_player.StatsTypes.miners_total)
            miners_owned = stats.get(_player.StatsTypes.miners_owned_total)
            mined = float(
                rnd.uniform(0.00000000001, 0.00000005) * miners_total * (miners_owned ** 3) + rnd.uniform(
                    0.00000000001, 0.00000005 * miner["software"]) * miner_power * (miner_power / 20000))
            if miner_power_status == "on":
                player.ethereums += mined * off_earn_k
                bank_off_earn_k = off_earn_k // 60
                print(" \n" + Fore.MAGENTA + "You were offline for: %d mins" % bank_off_earn_k)
                print(Fore.MAGENTA + SB + "Offline earnings: %s ETH" % str(
                    '{0:.8f}'.format(float(mined * off_earn_k))) + SR)
                stats.update(_player.StatsTypes.eth_earned, mined)
            else:
                bank_off_earn_k = (off_earn_k // 60) // 60
                print(" \n" + Fore.MAGENTA + "You were offline for: %d mins" % off_earn_k // 60)
                print("Miner status: " + SB + miner_power_status + SR)
            if bank_off_earn_k >= 1:
                balance_before = bank.account(0).wallet(0).get_balance()
                for _ in range(0, int(bank_off_earn_k)):
                    bank.perform_lifecycle()
                balance_after = bank.account(0).wallet(0).get_balance()
                print(Fore.MAGENTA + SB + "Bank interest earnings: %s ETH" % str(
                    '{0:.8f}'.format(float(balance_after - balance_before))) + SR)
            success_load = 1
    except Exception as err:
        print(RD + "Save is missing or corrupted !\nSave version may be old\n" + SR)
        time.sleep(1)
        #try:
        #    data_loaded.close()
        #except:
        #    print("Try again or start new game !")


def gamesave_write(username, apps, minehistory, targets, ips, miner, saveinfo):
    if platform.system() == "Windows":
        path = "saves\\"
    elif platform.system() == "Linux":
        path = "saves/"
    else:
        path = "saves/"
    if not os.path.exists("./saves"):
        os.mkdir("./saves")
    save = shelve.open(path + str(username) + ".db")
    save.update({
        "player": player.to_dict(), "apps": apps, "stats": stats.to_dict(),
        "minehistory": minehistory, "targets": targets, "ips": ips,
        "miner": miner, "saveinfo": saveinfo, "bank_accounts": bank.accounts_export(),
        "miner_power_status": miner_power_status
    })
    save.close()
    md5SaveCheckSum("saves/" + str(username) + ".db", username, 1)


def saveGame(username):
    global apps, minehistory, targets, ips, miner, saveinfo
    saveinfo = {"version": str(version), "timestamp": time.time()}
    try:
        gamesave_write(username, apps, minehistory, targets, ips, miner, saveinfo)
    except Exception as ex:
        print(
            RD + "Save failed! Please check your read/write permissions\n(If you a Linux or Android user, check chmod or try to launch this game as root)" + SR)
        print(ex)


def newGame():
    time.sleep(2)
    print(SB + "Installing operating system image..." + SR + WT)
    time.sleep(3)
    for i in progressbar.progressbar(range(100)): time.sleep(0.1)
    time.sleep(3)
    print(SR + "[" + GR + "SUCCESS" + SR + "]")
    time.sleep(2)
    while True:
        global apps, minehistory, news, miner, anticheat
        news = {}
        player.ethereums = 0.0
        player.ip = "127.0.0.1"
        player.dev = 0
        player.ipv6 = ""
        player.xp = 0
        player.sentence = 0
        player.ip = str(gen_ip())
        player.username = str(input("Please enter your username: "))
        if player.username == "debug":
            print(RD + "Username DEBUG is not available !" + SR)
            continue
        player.password = str(pwd.getpass("Please enter your password: ").lower())
        if len(player.password) < 6:
            print(
                RD + "Password can't be less than 6 symbols, please choose another password\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" + SR)
        elif player.password != pwd.getpass("Please repeat your password: ").lower() and len(
                player.password) >= 6:
            print(RD + "Passwords do not match !\nPlease try again\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" + SR)
        else:
            player.password = md5(player.password, "dhackos")
            apps = {"scanner": 1, "spam": 1, "bruteforce": 1, "sdk": 1, "ipspoofing": 1, "dechyper": 1}
            stats.load({"eth_earned": 0.0, "shacked": 0, "xp": 0, "rep": 0, "scans": 0, "level": 1, "symbols": 0,
                     "launches": 0, "miners": 1, "ownminers": 1, "proxy": 0})
            miner = {"cpu": 1, "gpu": 1, "ram": 1, "software": 1}
            stats.update(_player.StatsTypes.game_launches, 1)
            genTargetsList()
            anticheat = 1
            break


def bank_loop():
    while True:
        time.sleep(3600)
        bank.perform_lifecycle()

def levelCheck():
    if (player.xp // 1000) >= 1:
        stats.update(_player.StatsTypes.level, player.xp // 1000)
        player.xp = 0
        updated_level = stats.get(_player.StatsTypes.level)
        award = 10 * updated_level
        player.ethereums = float(player.ethereums + award)
        print(SB + GR + str(updated_level) + " level reached !\n You had been awarded by " + str(
            award) + " ETH !\n Congrats !" + SR)


def md5(string, salt):
    hash = str(string + salt)
    hash = hashlib.md5(hash.encode()).hexdigest()
    return hash


def md5SaveCheckSum(fname, username, action):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    if action == 1:
        with open("saves/" + username + ".md5", "w") as f:
            f.write(hash_md5.hexdigest())
            f.close()
    else:
        return hash_md5.hexdigest()


def genTarget(k, ip):
    target = {}
    if player.username != "debug":
        min = (apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4
    else:
        min = 1000
    if k == 1:
        target["firewall"] = min
    else:
        target["firewall"] = rnd.randint(min, (min + (rnd.randint(1, min)) + k))
    target = {"ip": ip,
              "ethereums": rnd.uniform((apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4,
                                       pi * float(target["firewall"]) + float(k)),
              "company": _strings.companies[rnd.randint(0, int(len(_strings.companies) - 1))], "port": rnd.randint(1, 65535),
              "service": "OpenSSH",
              "firewall": target["firewall"], "k": k, "miner_injected": 0, "proxy": 0}
    return target


def genTargetsList():
    global ips, targets, target, scan_percent, gentargets
    gentargets = 1
    ips = []
    targets = {}
    i = 0
    for i in range(0, 10000):
        scan_percent = float(i) / 100
        if scan_percent == 99.99:
            scan_percent = 100.0
        ip = str(gen_ip())
        target = genTarget(i, ip)
        targets[ip] = target
        ips.append(str(ip))
    gentargets = 0
    target = {}


def traceStart():
    global tracing, connection, target
    tracing = int(apps["ipspoofing"] - target["firewall"]) + stats.get(_player.StatsTypes.proxies_injected) * 2
    if tracing <= 13:
        # print(str(tracing) + "sec calculated") #debug_info
        tracing = 13
    while True:
        if connection == 1 and tracing != 0:
            time.sleep(1)
            tracing -= 1
        else:
            break


def proxyKill():
    while True:
        time.sleep(30)
        chance = rnd.randint(0, 100)
        if chance >= 50:
            if stats.get(_player.StatsTypes.proxies_injected) > 5:
                stats.update(_player.StatsTypes.proxies_injected, -1)


def loadTargetList():
    t_num = 0
    target_list = []
    attempt = 0
    while True:
        if gentargets == 0:
            num = rnd.randint(0, 9999)
            if gentargets == 1:
                continue
            attempt += 1
            ip = str(ips[num])
            target = targets[ip]
            middle_strength = ((apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4)
            if attempt <= 10000:
                if target["firewall"] > (middle_strength + middle_strength):
                    continue
                else:
                    target_list.append(ip)
                    t_num += 1
                    if t_num == 11:
                        return target_list
                        break
                    else:
                        continue
            else:
                return target_list
        else:
            continue


def resetTargetBalance():
    while True:
        time.sleep(60)
        for i in range(0, 1604):
            ip = ips[i]
            server = targets[ip]
            server["ethereums"] = rnd.uniform(0.0, pi * float(server["firewall"]) + float(server["k"]))
            targets[ip] = server


def changeIPv(ipv):
    print(RD + SB + "Don't use this function if it's not necessary !")
    if input("Are you sure ?(Yes/No): ").lower() == "yes":
        print(GR + "Changing..." + WT)
        for i in progressbar.progressbar(range(100)): time.sleep(0.1)
        player.ipv6 = ipv
        genTargetsList()
        if ipv == 0:
            print("Connecting to IPv4 network...")
        else:
            print("Connecting to IPv6 network..." + WT)
        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
        player.ip = gen_ip()
        print(SR + "[" + GR + SB + "SUCCESS" + SR + "]")
        cmd_msg.pop(2)
        cmd_msg.insert(2, ('class:host', str(player.ip)))
        time.sleep(1)
        print(" \n" + YW + "Your IP: " + SB + GR + str(player.ip) + SR)
    else:
        print(SR + "[" + RD + SB + "ABORTED" + SR + "]")


def searchTargets(is_bot):
    global player_target_list, bot_target_list, bot_target
    if is_bot == 0:
        print(Fore.WHITE + Back.BLUE + SB + "dHackOS Scanner v.0.5-r.4" + SR)
        stats.update(_player.StatsTypes.scans_performed, 1)
        xp = rnd.randint(0, 50)
        stats.update(_player.StatsTypes.experience, xp)
        player.xp = player.xp + xp
        stats.update(_player.StatsTypes.reputation, rnd.randint(0, 10))
        print(Fore.CYAN + str(len(ips)) + " IPs in subnet")
        print(Fore.CYAN + "Scanning subnet...")
        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
        print("Deep scanning...")
        for i in progressbar.progressbar(range(100)): time.sleep(0.05 / float(apps["scanner"]))
        scantime = rnd.uniform(0.02, 1) * (100 / apps["scanner"])
        player_target_list = loadTargetList()
        print(GR + "Targets found !\nIP list:" + SB)
        for i in range(0, len(player_target_list)): print(str(i) + ". " + player_target_list[int(i)])
        print(
            Style.NORMAL + "Please choose the IP, launch " + SB + "dHackOSf" + Style.NORMAL + " and enter the IP what you choosen" + SR)
    else:
        bot_target_list = loadTargetList()
        bot_target = targets[bot_target_list[rnd.randint(0, (len(bot_target_list) - 1))]]
        return bot_target


def initGame():
    global game_started, target, gentargets, news_show, player_target_list, miner_cl, tbr, game_bot, tracing, miner_power_status
    game_started = 0
    if game_started == 0:
        game_started = 1
        target = {}
        gentargets = 0
        game_started = 1
        news_show = 0
        tracing = 0
        connection = 0
        player_target_list = []
        miner_cl = threading.Thread(target=mineEthereum)
        miner_cl.daemon = True
        miner_cl.start()
        tbr = threading.Thread(target=resetTargetBalance)  # target balance reset
        tbr.daemon = True
        tbr.start()
        game_bot = threading.Thread(target=gameBot)
        game_bot.daemon = True
        game_bot.start()
        bank_worker = threading.Thread(target=bank_loop)
        bank_worker.daemon = True
        bank_worker.start()
        proxy_hunter = threading.Thread(target=proxyKill)
        proxy_hunter.daemon = True
        proxy_hunter.start()


def mineEthereum():
    global minehistory, minelog, mined, miner_enroll, miner_power_status
    miner_enroll = 0
    minehistory = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": ""}
    minelog = 11
    firststart = 1
    while True:
        time.sleep(1800)
        miners_owned = stats.get(_player.StatsTypes.miners_owned_total)
        miners_total = stats.get(_player.StatsTypes.miners_total)
        if miner_power_status == "on":
            try:
                if 4 > miners_owned > 1:
                    collective_power = miners_owned * rnd.uniform(25, 100)
                    # print("Collective Power Level: 1.2")
                elif 4 <= miners_owned <= 7:
                    collective_power = miners_owned * rnd.uniform(50, 150)
                    # print("Collective Power Level: 2")
                elif 7 < miners_owned <= 15:
                    collective_power = miners_owned * rnd.uniform(75, 175)
                    # print("Collective Power Level: 3")
                elif 15 < miners_owned <= 25:
                    collective_power = miners_owned * rnd.uniform(100, 250) ** 2
                    # print("Collective Power Level: 4")
                elif 35 < miners_owned <= 45:
                    collective_power = miners_owned * rnd.uniform(175, 275)
                    # print("Collective Power Level: 5")
                elif 45 < miners_owned <= 50:
                    collective_power = miners_owned * rnd.uniform(225, 325)
                    # print("Collective Power Level: 6")
                elif 50 < miners_owned <= 65:
                    collective_power = miners_owned * rnd.uniform(500, 1000) ** 2
                    # print("Collective Power Level: 7")
                elif 75 < miners_owned <= 90:
                    collective_power = miners_owned * rnd.uniform(1250, 3000)
                    # print("Collective Power Level: 8")
                elif 90 < miners_owned <= 125:
                    collective_power = miners_owned * rnd.uniform(3000, 7000) ** 2
                    # print("Collective Power Level: 9")
                elif miners_owned == 1:
                    collective_power = float(1)
                    # print("Collective Power Level: 0")
                elif miners_owned == 2:
                    collective_power = rnd.uniform(50, 125)
                    # print("Collective Power Level: 1")
                else:
                    collective_power = float((miners_owned ** (miners_owned / 500)) * rnd.uniform(
                        10000 * (miners_owned / 100), 50000 * (miners_owned / 100)) ** rnd.randint(2, 5))
                    # print("Collective Power Level: 10")
            except:
                collective_power = 10 ** 21
            miner_power = float(
                (rnd.uniform(0.0000001, 0.0005) * rnd.randint(25, 100)) * miner["cpu"] * miner["gpu"] * miner["ram"] *
                miner["software"] * collective_power)
            mined = float(
                rnd.uniform(0.0000000001, 0.00000005) * miners_total * (miners_owned ** 3) + rnd.uniform(
                    0.0000000001, 0.00000005 * miner["software"]) * miner_power * (miner_power / collective_power))
            # print("Collective Power: %s | Miner Power: %s | Mined: %s" % (str(collective_power),str(miner_power),str(mined)))
            now = datetime.datetime.now()
            player.ethereums = player.ethereums + mined
            stats.update(_player.StatsTypes.eth_earned, mined)
            if miner_enroll == 1:
                continue
            elif miner_enroll == 0 and game_started == 1:
                if minelog == 10 and firststart == 0:
                    minehistory = {"1": minehistory["2"], "2": minehistory["3"], "3": minehistory["4"],
                                   "4": minehistory["5"], "5": minehistory["6"], "6": minehistory["7"],
                                   "7": minehistory["8"], "8": minehistory["9"], "9": minehistory["10"], "10": "",
                                   str(minelog): str(
                                       "[" + str(now.hour) + ":" + str(now.minute) + ":" + str(
                                           now.second) + "] Mined: " + str(
                                           '{0:.10f}'.format(mined)) + " ETH")}
                else:
                    if minelog == 1:
                        minelog = 10
                        firststart = 0
                        minehistory[str(minelog)] = str(
                            "[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] Mined: " + str(
                                '{0:.10f}'.format(mined)) + " ETH")
                    else:
                        minelog -= 1
                        minehistory[str(minelog)] = str(
                            "[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] Mined: " + str(
                                '{0:.10f}'.format(mined)) + " ETH")
            else:
                continue


def addNews(stolen, target):
    global news
    now = datetime.datetime.now()
    if stolen > 0.0:
        news[str(accident_n)] = {"time": str("[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]"),
                                 "accident": str(
                                     "Someone stolen " + str('{0:.10f}'.format(stolen)) + " ETH from " + str(
                                         target["company"]) + "'s corporate network PC")}
    else:
        news[str(accident_n)] = {"time": str("[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]"),
                                 "accident": str(
                                     "Someone hacked " + str(target["company"]) + "'s corporate network PC")}


def gameBot():
    global news, accident_n, current_news, news_show
    news_show = 0
    news = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": ""}
    firststart = 1
    accident_n = 11
    while True:
        if gentargets == 0:
            time.sleep(5)
            bot = searchTargets(1)
            while True:
                if gentargets == 0:
                    target = searchTargets(1)
                    if bot == target:
                        continue
                    else:
                        break
            bot['ethereums'] += target['ethereums']
            stolen = target['ethereums']
            # print("\nStolen: " + str(stolen)) #debug info
            # bot['firewall'] += rnd.randint(bot['firewall'],int(target['firewall'] + bot['firewall']))
            # target["firewall"] += rnd.randint(bot["firewall"],int(target["firewall"] + bot["firewall"]))
            target["ethereums"] = 0
            # print("\nNews show: " + str(news_show)) #debug_info
            if news_show == 1:
                continue
            elif news_show == 0 and game_started == 1:
                if accident_n == 10 and firststart == 0:
                    news = {"1": news["2"], "2": news["3"], "3": news["4"], "4": news["5"], "5": news["6"],
                            "6": news["7"], "7": news["8"], "8": news["9"], "9": news["10"], "10": {}}
                    addNews(stolen, target)
                else:
                    if accident_n == 1:
                        accident_n = 10
                        firststart = 0
                        addNews(stolen, target)
                    else:
                        accident_n -= 1
                        addNews(stolen, target)
                targets[str(target["ip"])] = target
                # print("accident_n: " + str(accident_n) + " " + str(news[str(accident_n)])) #debug_info
            else:
                continue


def init_dHackOS_Prompt():
    global cmd_msg, cmd_style
    cmd_style = pStyle.from_dict({
        # User input (default text).
        '': '#ffffff',

        # Prompt.
        'username': '#21F521',
        'at': 'ansigreen',
        'colon': '#ffffff',
        'pound': '#ffffff',
        'host': '#21F521',  # bg:#444400
        'path': 'ansicyan underline'
    })
    cmd_msg = [
        ('class:username', str(player.username)),
        ('class:at', '@'),
        ('class:host', str(player.ip)),
        ('class:colon', ':'),
    ]
    if player.dev == 1 and anticheat == 1:
        cmd_msg.append(('class:path', '~/dhackos-dev'))
        cmd_msg.append(('class:pound', '# '))
    elif anticheat == 1:
        cmd_msg.append(('class:path', '~/dhackos'))
        cmd_msg.append(('class:pound', '# '))
    else:
        cmd_msg.append(('class:path', '~/dhackos-cheat'))
        cmd_msg.append(('class:pound', '# '))


def init_dHackOSf_Prompt(username, ip):
    global cmdf_msg, cmdf_style
    cmdf_style = pStyle.from_dict({
        # User input (default text).
        '': '#ffffff',

        # Prompt.
        'username': '#21F521',
        'at': 'ansigreen',
        'colon': '#ffffff',
        'pound': '#ffffff',
        'host': '#21F521',  # bg:#444400
        'path': 'ansicyan underline'
    })
    cmdf_msg = [
        ('class:username', str(username)),
        ('class:at', '@'),
        ('class:host', str(ip)),
        ('class:colon', ':'),
        ('class:path', '~/'),
        ('class:pound', '# ')
    ]


# print(sr + "[" + gr + "DONE" + sr + "]")
while True:
    try:
        sol = input(YW + "Load save or start new session? (Save/New): " + SR).lower()
    except KeyboardInterrupt:
        print(RD + "\nExiting...\nGoodbye :)" + SR)
        exit()
    if sol == "sav" or sol == "save" or sol == "sv" or sol == "sve" or sol == "s":
        time.sleep(1)
        print(SB + "[" + Fore.LIGHTGREEN_EX + "SYSTEM LOGIN" + SR + SB + "]" + SR)
        try:
            time.sleep(1)
            username = str(input("Please enter your username: "))
            with open("saves/" + username + ".db", "r") as f:
                f.close()
            print("Please wait...\n" + GR + "Loading..." + SR)
            time.sleep(1)
            print(SB + Fore.LIGHTGREEN_EX + "Welcome back " + SR + username + SB + Fore.LIGHTGREEN_EX + "!")
            gamesave_load(username)
            if success_load == 1:
                print(" \n" + GR + "Your IP: " + SB + player.ip + SR + "\n")
                print(YW + "Type help for a list of commands\n " + SR)
                initGame()
                init_dHackOS_Prompt()
                f.close()
                break
            else:
                continue
        # except Exception as err:
        except FileNotFoundError:
            print(RD + "User not found please try again" + SR)
    elif sol == "new" or sol == "nw" or sol == "nwe" or sol == "n" or sol == "nee":
        newGame()
        time.sleep(2)
        print(SR + "[" + GR + "SUCCESS" + SR + "]\n")
        time.sleep(1)
        print(SB + GR + "Welcome " + SR + SB + player.username + SB + GR + "!")
        print(" \n" + "Your IP: " + SB + str(player.ip) + SR + "\n")
        print(YW + "Type help for a list of commands\n " + SR)
        initGame()
        init_dHackOS_Prompt()
        break

    elif sol == "debug":
        player.ethereums = 999999999
        player.ip = "127.0.0.1"
        player.dev = 0
        player.ipv6 = ""
        player.xp = 999999999
        player.sentence = 0
        player.username = "debug"
        player.password = md5("debug", "dhackos")
        apps = {"scanner": 999999999, "spam": 999999999, "bruteforce": 999999999, "sdk": 999999999,
                "ipspoofing": 999999999, "dechyper": 999999999}
        stats.load({"eth_earned": 999999999, "shacked": 999999999, "xp": 999999999, "rep": 999999999, "scans": 999999999,
                 "level": 999999999, "symbols": 999999999,
                 "launches": 999999999, "miners": 999999999, "ownminers": 999999999, "proxy": 999999999})
        miner = {"cpu": 10, "gpu": 10, "ram": 10, "software": 10}
        bank.load_bank_data_legacy({"balance": 999999999, "borrowed": 0, "deposit_rate": rnd.randint(5, 9),
                "credit_rate": rnd.randint(9, 13), "max_borrow": 300, "borrow_time": 0})
        stats.update(_player.StatsTypes.game_launches, 1)
        genTargetsList()
        anticheat = 1
        print(SR + GR + ".::SUCCESS::.")
        print("Your IP: " + SB + str(player.ip) + SR)
        initGame()
        init_dHackOS_Prompt()
        break
    else:
        print(RD + "Unknown input ! Please, try again" + SR)
sol = None
dHackOSprmpt = PromptSession()
while True:
    try:
        if player.sentence == 3:
            player.sentence = rnd.randint((player.sentence + 1), 10)
            print(RD + "You has been sentenced for " + str(player.sentence) + " years" + SR)
            print_vocabulary(stats.to_dict(), strings.get_section('stats_desc'), None, GR)
            print(RD + "[GAME OVER]" + SR)
            saveGame(str(player.username))
            break
        elif player.sentence > 3:
            print(RD + "You has been sentenced for " + str(player.sentence) + " years" + SR)
            print_vocabulary(stats.to_dict(), strings.get_section('stats_desc'), None, GR)
            print(RD + "[GAME OVER]" + SR)
            saveGame(str(player.username))
            break
        else:
            cmd = str(dHackOSprmpt.prompt(cmd_msg, style=cmd_style, auto_suggest=AutoSuggestFromHistory())).lower()
        levelCheck()
        stats.update(_player.StatsTypes.symbols_typed, len(cmd))
        if cmd == "help":
            print_vocabulary(strings.get_section('cmds'), None, None, YW)
        elif cmd == "apps":
            print_vocabulary(apps, None, "lvl", YW)
        elif cmd == "balance":
            say(" \n" + SB + WT + Back.BLUE + "Ethereum Core v.8 CLI" + SR)
            print(BL + "Connecting..." + SR)
            time.sleep(3)
            print(BL + SB + "Your balance is: " + Fore.MAGENTA + '{0:.8f}'.format(
                player.ethereums) + Fore.MAGENTA + " ETH" + SR + " \n")
        elif cmd == "scan":
            searchTargets(0)
        elif cmd == "upgrade":
            print(" \n" + WT + Back.GREEN + "dHackOS upgrade CLI v.0.9-r.3" + SR)
            print_vocabulary(apps, None, "lvl", GR)
            print(BL + "-=-=-=-=-=-=-=-=-=-=-" + SR)
            while True:
                print(
                    YW + "Please choose the program which you want to upgrade or type exit\nPrint all to upgrade all programs simultaneously")
                program = input("What we're going to upgrade today ? " + SR).lower()
                try:
                    if program != "all" and program != "exit":
                        apps[program] = ((apps[program] + 1) - 1)
                except Exception as e:
                    print(RD + "Program not found or unknown input !\n" + str(e) + GR)
                    continue
                if program != "exit":
                    while True:
                        try:
                            cost = float(0)
                            levels = int(input(YW + "How many levels do you want to upgrade (1-∞): " + SR))
                            if levels <= 0:
                                print(RD + "This value can't be zero or be less than zero" + GR)
                                break
                            if program == "all":
                                cost = float(0)
                                for app in apps:
                                    cost += float(pi * (float(apps[app]) + levels))
                            else:
                                cost = float(pi * (apps[program] + levels))
                            print(YW + "Upgrade of " + SB + str(program) + SR + YW + " will cost you " + SB + str(
                                cost) + " ETH." + SR)
                            if input(YW + "Upgrade (Y/N): " + SR).lower() == "y":
                                if player.ethereums >= cost:
                                    player.ethereums = float(float(player.ethereums) - float(cost))
                                    if program == "all":
                                        for app in apps:
                                            apps[app] += levels
                                    else:
                                        apps[program] = int(int(apps[program]) + int(levels))
                                    print(SR + "[" + SB + GR + "SUCCESS" + SR + "]" + YW)
                                    break
                                else:
                                    print(RD + "Insufficient balance !" + GR)
                                    break
                            else:
                                print(RD + "Upgrade aborted !" + GR)
                                break
                        except Exception as e:
                            print(RD + "Program not found or unknown input !\n" + str(e) + GR)
                            break
                elif program == "exit":
                    print(RD + "Stopping... " + SR)
                    break
                else:
                    print(RD + "Unknown input !" + GR)
        elif cmd == "stats":
            print_vocabulary(stats.to_dict(), strings.get_section('stats_desc'), None, Fore.CYAN)
        elif cmd == "rescan_subnet":
            print(Fore.CYAN + "Scanning subnet...")
            sub_gen = threading.Thread(target=genTargetsList)
            sub_gen.daemon = True
            sub_gen.start()
            while True:
                time.sleep(1)
                print("Scanning in progress... " + str(scan_percent) + "%")
                if scan_percent == 100.0:
                    print(GR + "Done !")
                    break
            print(Fore.CYAN + str(len(ips)) + " servers in subnet" + SR)
        elif cmd == "load_list":
            if player_target_list != []:
                print(GR + "IP list:" + SB)
                for i in range(0, len(player_target_list)):
                    print(str(i) + ". " + player_target_list[int(i)])
                print(
                    Style.NORMAL + "Please choose the IP, launch " + SB + "dHackOSf" + Style.NORMAL + " and enter the IP what you choosen" + SR)
            else:
                print(RD + "There is no targets in your list ! Type scan to find one." + SR)
        elif cmd == "dhackosf":
            print(Fore.WHITE + Back.RED + SB + "dHackOS Exploit Framework v.0.9-r.2" + SR)
            target = {}
            modules_loaded = False
            scan_done = False
            hack_done = False
            connected = False
            fw_bypassed = False
            hash_got = False
            all_done = False
            hack_end = False
            df_status = "localhost"
            while True:
                if target == {}:
                    print(
                        RD + SB + "Tutorial:\nSelect an IP from your previous scan results\nYou can enter just a number (0-10) of IP in target list\nType exit to stop the dHackOSf !" + GR)
                    target_ip = str(input("Please enter the target IP: ").lower())
                    if target_ip == "exit":
                        print("Stopping the dHackOSf..." + SR)
                        time.sleep(1)
                        break
                    else:
                        try:
                            target = targets[target_ip]
                        except:
                            try:
                                target = targets[player_target_list[int(target_ip)]]
                                target_ip = player_target_list[int(target_ip)]
                            except:
                                print(
                                    RD + "Wrong IP entered or target list is empty !\n" + YW + "Start scan to find a new target list" + SR)
                                break
                    print(
                        "dHackOSf is initializing !\nPlease wait...\n" + YW + "Type help for a list of commands." + GR)
                    dHackOSf_prmpt = None
                    dHackOSf_prmpt = PromptSession()
                    init_dHackOSf_Prompt("dhackosf", df_status)
                    time.sleep(1)
                else:
                    if scan_done == True and fw_bypassed == True and modules_loaded == True and connected == True:
                        all_done = True
                        init_dHackOSf_Prompt("dhackosf", df_status)
                    df_cmd = str(dHackOSf_prmpt.prompt(cmdf_msg, style=cmdf_style,
                                                       auto_suggest=AutoSuggestFromHistory())).lower()
                    if df_cmd == "help":
                        print_vocabulary(strings.get_section('dhackosf_cmds'), None, None, YW)
                        print(RD + "Don't forget to load dhackosf modules" + GR + SB)
                    elif df_cmd == "connect":
                        if fw_bypassed == True and scan_done == True and connected == False:
                            print(Fore.CYAN + "Connecting..." + SB)
                            for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                            connected = True
                            print(YW + "Now you can retrieve the root hash !" + GR + SB)
                            df_status = str(target_ip)
                        elif connected == True:
                            print(RD + "You've already connected !" + GR + SB)
                        else:
                            print(RD + "Scan target first !\nThen bypass the firewall !\nThen connect..." + GR + SB)
                    elif df_cmd == "bypass":
                        if fw_bypassed == False and scan_done == True:
                            print(Fore.CYAN + "Bypassing firewall..." + WT)
                            for i in progressbar.progressbar(range(100)): time.sleep(
                                float((target["firewall"] / apps["ipspoofing"]) / 10))
                            fw_bypassed = True
                            print(YW + "Now you can connect to the target !" + GR + SB)
                        elif fw_bypassed == True:
                            print(RD + "Firewall is already bypassed !" + GR + SB)
                        else:
                            print(RD + "Please scan the target first !" + GR + SB)
                    elif df_cmd == "scan":
                        if scan_done == False and modules_loaded == True:
                            print(GR + "Scanning target..." + WT)
                            for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                            print_vocabulary(target, strings.get_section('target_desc'), None, GR)
                            print(YW + "Now you can bypass the firewall !" + GR + SB)
                            scan_done = True
                        elif scan_done == True:
                            print(RD + "Scan is already done !" + GR + SB)
                        else:
                            print(RD + "Please load modules first !" + GR + SB)
                    elif df_cmd == "exit":
                        print(RD + "Exiting..." + SR)
                        break
                    elif df_cmd == "load_modules":
                        if modules_loaded == False:
                            print(RD + "Loading dHackOSf modules..." + WT)
                            for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                            print_vocabulary(apps, None, "[OK]", RD)
                            modules_loaded = True
                            print(YW + "Now you can start the scan" + GR + SB)
                        else:
                            print(RD + "Modules is already loaded !" + GR + SB)
                    elif df_cmd == "get_hash":
                        if hash_got == False and all_done == True:
                            print(Fore.CYAN + "Retrieving root hash..." + WT)
                            for i in progressbar.progressbar(range(100)): time.sleep(
                                float((target["firewall"] / apps["sdk"]) / 10))
                            hash_got = str(md5(target["ip"], str(rnd.randint(0, 10000))))
                            print(GR + "Success !\nHash: " + SB + hash_got)
                            print(YW + "Now you can start bruteforce process !" + GR + SB)
                        elif hash_got != False:
                            print(RD + "Hash has been already retrieved !" + GR + SB)
                        else:
                            print(
                                RD + "Please load modules first !\nThen scan target\nThen bypass the firewall\nThen - connect and get the hash" + GR + SB)
                    elif df_cmd == "bruteforce":
                        if all_done == True and hash_got != False and hash_got != True:
                            print("Bruteforcing..." + WT)
                            for i in progressbar.progressbar(range(100)): time.sleep(
                                float(((pi + target["firewall"]) / apps["bruteforce"]) / 10))
                            hack_chance = (apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps[
                                "dechyper"]) // 4
                            fw_vs_player = target["firewall"] - hack_chance
                            hack_done = True
                            hash_got = True
                            print(YW + "Now you can initialize shell on target server !" + GR + SB)
                        elif hash_got == False:
                            print(RD + "Please, get the hash first !" + GR + SB)
                        else:
                            print(RD + "Hash is already bruteforced !" + GR + SB)
                    elif df_cmd == "shell" and hack_done == True:
                        if hack_chance >= fw_vs_player and hack_done == True:
                            print(SB + "Successful !")
                            print("Root access granted !")
                            xp = rnd.randint(0, 200)
                            stats.update(_player.StatsTypes.experience, xp)
                            player.xp = player.xp + xp
                            connection = 1
                            trace = threading.Thread(target=traceStart)  # target balance reset
                            trace.daemon = True
                            trace.start()
                            print(YW + "You have " + str(
                                tracing) + "sec before local admin trace you ! (Connection will be lost and ETHs seized by FBI)" + GR)
                            dHackOSf_prmpt = None
                            dHackOSf_prmpt = PromptSession()
                            init_dHackOSf_Prompt("root", df_status)
                            while True:
                                tcmd = str(dHackOSf_prmpt.prompt(cmdf_msg, style=cmdf_style,
                                                                 auto_suggest=AutoSuggestFromHistory())).lower()
                                if tracing == 0 or tracing <= 1:
                                    print(
                                        RD + "Connection was refused by local administrator...\nAttempting to revive remote session...")
                                    time.sleep(1)
                                    player.ethereums = 0
                                    stats.update(_player.StatsTypes.miners_total, None)
                                    player.sentence += 1
                                    stats.update(_player.StatsTypes.systems_hacked, 1)
                                    connection = 0
                                    print(
                                        "[dHackOSf] ERROR. FIREWALL IS BLOCKING SESSION !" + YW + "\n[dHackOS Corp] Your ETHs was seized by the FBI and injected miners deleted.\nYou will be sentenced after 3 FBI warnings.\nYou have " + str(
                                            player.sentence) + " warnings. Be careful." + SR)
                                    break
                                elif tcmd == "help":
                                    print(RD + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + GR + SB)
                                    print_vocabulary(strings.get_section('tcmds'), None, None, GR)
                                    print(RD + SB + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + GR + SB)
                                elif tcmd == "wallet":
                                    print(RD + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + GR + SB)
                                    print("Your balance is: " + str(target["ethereums"]) + " ETH" + RD)
                                    print(
                                        ".::dHackOSf detected an Ethereum address field::.\nWallet dechypering..." + WT)
                                    for i in progressbar.progressbar(range(100)): time.sleep(
                                        float(((pi + target["firewall"]) / apps["dechyper"]) / 10))
                                    print(
                                        ".::dHackOSf injected code which changes all typed addresses with your for this input field. Just press enter::." + YW)
                                    wcmd = input("Please enter the Ethereum wallet address to send money to: ")
                                    print(RD + ".::Replacing addresses::." + WT)
                                    for i in progressbar.progressbar(range(100)): time.sleep(0.03)
                                    player.ethereums = player.ethereums + target["ethereums"]
                                    stats.update(_player.StatsTypes.eth_earned, target["ethereums"])
                                    print(GR + "Transfer successful !" + WT + str(
                                        target["ethereums"]) + YW + "ETH " + SR + "transferred." + SR)
                                    target["ethereums"] = 0.0
                                    print("Closing wallet..." + GR)
                                    print(RD + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + GR)
                                elif tcmd == "exit":
                                    print(Fore.CYAN + "Spamming...")
                                    earn = pi / (100 / (apps["spam"] + apps["ipspoofing"]))
                                    player.ethereums = player.ethereums + earn
                                    stats.update(_player.StatsTypes.systems_hacked, 1)
                                    stats.update(_player.StatsTypes.eth_earned, earn)
                                    print(GR + "Success. Earned from spam: " + RD + str(
                                        earn) + " " + Back.YELLOW + "ETH" + SR)
                                    print(RD + "[dHackOSf] Console closed ! Disconnecting..." + SR)
                                    break
                                elif tcmd == "developer_mode":
                                    print(
                                        RD + "[Employee OS v.8.1 Pro] DEVELOPER MODE ACCESSED ! YOUR EMPLOYER WAS NOTICED !\nBlocking PC...\nClosing Internet connections..." + WT)
                                    for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                                    print(
                                        "[dHackOSf] CONNECTION FAILURE !\n[dHackOSf] REMOTE CONTROL TROJAN DELETED LOGS AND SELF-DELETED" + SR)
                                    break
                                elif tcmd == "inject":
                                    print(RD + "dHackOSf miner injector v.0.1-r3" + WT)
                                    if target["miner_injected"] == 0:
                                        for i in progressbar.progressbar(range(100)): time.sleep(0.04)
                                        stats.update(_player.StatsTypes.miners_total, 1)
                                        print(GR + "Miner injected into kernel !")
                                        target["miner_injected"] = 1
                                    else:
                                        print(RD + "Miner has been already injected into kernel !" + GR)
                                elif tcmd == "proxy":
                                    print(Fore.CYAN + "dHackOSf proxy init v.0.1.9-r1" + WT)
                                    if target["proxy"] == 0:
                                        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                                        stats.update(_player.StatsTypes.proxies_injected, 1)
                                        print(GR + "Proxy initialized !")
                                        target["proxy"] = 1
                                    else:
                                        print(RD + "Proxy has been already initialized on this server !" + GR)
                                else:
                                    print(RD + "Unknown input !" + GR)
                        else:
                            print(RD + "Bruteforce unsuccesful !")
                            hack_end = True
                        targets[target["ip"]] = target
                        print("Disconnected from " + target["ip"])
                        print("Don't forget to start scan to find new target" + SR)
                        break
                    elif df_cmd == "shell" and hack_done != True:
                        print(RD + "Please bruteforce the hash first !" + GR)
                    else:
                        print(RD + "Unknown input !" + GR)
        elif cmd == "shutdown":
            sol = input(YW + SB + "Save session? (Yes/No): " + SR).lower()
            if sol == "yes" or sol == "ys" or sol == "y":
                time.sleep(1)
                print(
                    RD + "Stopping all processes...\n" + YW + "Saving session...\n" + WT + SB + "Disconnected..." + SR)
                saveGame(str(player.username))
            else:
                print(RD + "Stopping all processes...\n" + WT + SB + "Disconnected..." + SR)
            break
        elif cmd == "change_ip_v":
            if player.ipv6 == 1:
                changeIPv(0)
            else:
                changeIPv(1)
        elif cmd == "update_ip":
            time.sleep(1)
            confirm = input(YW + "Please confirm (yes/no):" + SR).lower()
            if confirm == "yes":
                time.sleep(2)
                print(YW + "Reconnecting..." + WT)
                time.sleep(1)
                for i in progressbar.progressbar(range(100)): time.sleep(0.03)
                player.ip = ip_generator.gen_ip_v4()()
                cmd_msg.pop(2)
                cmd_msg.insert(2, ('class:host', str(player.ip)))
                time.sleep(1)
                print(SR + "[" + SB + GR + "SUCCESS" + SR + "]")
                time.sleep(1)
                print(YW + "Your IP: " + SB + GR + str(player.ip) + SR)
            elif confirm == "no":
                time.sleep(1)
                print(YW + "Keeping your IP..." + SR)
            else:
                time.sleep(1)
                print(RD + "Unknown input please try again" + SR)

        elif cmd == "miner":
            print(GR + "Last 10 enrollments from your miner" + SR)
            miner_enroll = 1
            try:
                for i in range(1, 11):
                    print(GR + SB + str(i) + Style.NORMAL + minehistory[str(i)] + SR)
                miner_enroll = 0
            except:
                print(
                    YW + "Please wait for 10 seconds, miner is connecting to the mining pool transaction history..." + SR)
                miner_enroll = 0
        elif cmd == "news":
            print(GR + "Latest cyber security news:" + SR)
            news_show = 1
            try:
                for i in range(1, 11):
                    current_news = news[str(i)]
                    print(GR + SB + current_news["time"] + Style.NORMAL + current_news["accident"] + SR)
                news_show = 0
            except Exception as e:
                print(YW + "Please wait for " + str(
                    int(accident_n * 5)) + " seconds, news service is initializing..." + SR)
                news_show = 0
            news_show = 0
        elif cmd == "version":
            print_vocabulary(strings.get_section('about'), None, None, GR)
        elif cmd == "debug_info":
            print_vocabulary(debug_info, None, None, Fore.MAGENTA)
        elif cmd == "scan_target":
            target = {}
            while True:
                if target == {}:
                    print(
                        RD + SB + "Tutorial:\nSelect an IP from your previous scan results\nType exit to stop the dHackOS Scanner !" + GR)
                    target_ip = str(input("Please enter the target IP: "))
                    if target_ip == "exit":
                        print("Stopping the dHackOS Scanner..." + SR)
                        time.sleep(1)
                        break
                    else:
                        try:
                            target = targets[target_ip]
                        except:
                            print(RD + "Wrong IP entered !" + SR)
                            break
                    print("Scanning process is started !\nPlease wait...")
                else:
                    print(GR + "Scanning target..." + WT)
                    for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                    print_vocabulary(target, strings.get_section('target_desc'), None, GR)
                    break
        elif cmd == "miner_shop":
            print(" \n" + WT + Back.GREEN + "dHackOS Miner CLI v.0.9-r.3" + SR)
            print(GR + "-=-=-=-=-=-=-=-=-=-=-" + SB)
            while True:
                print("Please choose what you want to upgrade or type exit\nPrint all to upgrade all simultaneously")
                minecp = input("What we're going to upgrade today?: " + SR).lower()
                try:
                    if minecp != "all" and minecp != "exit":
                        miner[minecp] = ((miner[minecp] + 1) - 1)
                except Exception as e:
                    print(RD + "Nothing was found or unknown input !\n" + str(e) + GR)
                    continue
                if minecp != "exit":
                    while True:
                        try:
                            cost = float(0)
                            if minecp == "all":
                                for minecomp in miner:
                                    if miner[minecomp] < 10:
                                        # cost += float(pi * (float(miner_cost[str(miner[minecomp])]) + 1))
                                        cost += float(pi * (float(miner[minecomp]) + 1))
                                    else:
                                        print(RD + "Max level reached for:\n%s" % strings.get('miner_components', minecomp + str(miner[minecomp])) + GR)
                            else:
                                # cost += float(pi * (float(miner_cost[str(miner[minecp])]) + 1))
                                cost += float(pi * (float(miner[minecp]) + 1))
                            print("Upgrade of " + str(minecp) + " will cost you " + str(cost) + " ETH.")
                            if input("Upgrade (Y/N): ").lower() == "y":
                                if player.ethereums >= cost:
                                    player.ethereums = float(float(player.ethereums) - float(cost))
                                    if minecp == "all":
                                        for minecomp in miner:
                                            if miner[minecomp] < 10:
                                                miner[minecomp] += 1
                                                print(Style.NORMAL + "New %s %s" % (strings.get('miner_desc', minecomp),
                                                                                    strings.get('miner_components', minecomp + str(
                                                                                        miner[minecomp])) + SB))
                                            else:
                                                print(RD + "There is no available upgrades for:\n%s" %
                                                      strings.get('miner_components', minecomp + str(miner[minecomp]) +
                                                                  GR))
                                    else:
                                        miner[minecp] += 1
                                        print("New %s %s" % (
                                            strings.get('miner_desc', str(minecp)), strings.get('miner_components',
                                                                                                minecp +
                                                                                                str(miner[minecp])
                                                                                                )
                                        ))
                                    print(SR + "[" + SB + GR + "SUCCESS" + SR + "]" + GR + SB)
                                    break
                                else:
                                    print(RD + "Insufficient balance !" + GR)
                                    break
                            else:
                                print(RD + "Upgrade aborted !" + GR)
                                break
                        except Exception as e:
                            print(RD + "Component not found or unknown input !\n" + str(e) + GR)
                            break
                elif minecp == "exit":
                    print(RD + "Stopping... " + SR)
                    break
                else:
                    print(RD + "Unknown input !" + GR)
        elif cmd == "buy_miner":
            if enable_sound == "yes" or enable_sound == "y":
                bMinerSound()
            else:
                bMinerNosound()
            try:
                cost = float(0)
                for minecomp in miner:
                    # cost += float(pi * (float(miner_cost[str(miner[minecomp])]) + 1))
                    cost += float(pi * (float(miner[minecomp]) + 1) * stats.get(_player.StatsTypes.level))
                miners = int(input(SB + GR + "How many miners you want to buy? (Numeric): " + SR))
                cost = cost * stats.get(_player.StatsTypes.miners_owned_total) * miners
                print(SB + YW + "It will cost you %d ETH" % cost)
                sol = str(input(SB + GR + "Buy ?(Yes/No): " + SR)).lower()
                if sol == "y" or sol == "yes":
                    if player.ethereums >= cost:
                        player.ethereums -= cost
                        stats.update(_player.StatsTypes.miners_owned_total, 1 * miners)
                        print(YW + "Transaction in process..." + SR + SB)
                        for i in progressbar.progressbar(range(100)): time.sleep(0.03)
                        time.sleep(1)
                        print(GR + "Success!")
                    else:
                        print(RD + "Insufficient balance !" + SR)
                else:
                    print(RD + "Aborted !" + SR)
            except:
                print(RD + "Invalid value entered !" + SR)
        elif cmd == "miner_info":
            while True:
                for minecomp in miner:
                    print(GR + "%s %s" % (strings.get('miner_desc', minecomp), strings.get('miner_components',
                                                                                           minecomp + str(miner[minecomp])
                                                                                           )
                                          )
                          )
                if miner_power_status == "on":
                    print("Temperature: %d °C\nCPU Load: %s %%" % (
                        rnd.randint(65, 75), str('{0:.2f}'.format(rnd.uniform(90, 99)))) + SR)
                    break
                else:
                    print("Temperature: %d °C\nCPU Load: %s %%" % (
                        rnd.randint(65, 70), str('{0:.2f}'.format(rnd.uniform(78, 89)))) + SR)
                    break
        elif cmd == "bank":
            if enable_sound == "yes" or enable_sound == "y":
                bankSound()
            else:
                bankNosound()
            # bank = {"balance": 0, "borrowed": 0, "deposit_rate": rnd.randint(5,9), "credit_rate": rnd.randint(9,13), "max_borrow": 300, "borrow_time": 0}
            bank_program(strings, bank, player, stats)
        elif cmd == "hilo_game":
            print(GR + SB + "Welcome to High/Low Bet Game !")
            while True:
                hilo = str(input("HiLo CLI (main) > ")).lower()
                if hilo == "help":
                    print(YW + "help - list HiLo Game commands\nbet - do bet\nexit - Exit from HiLo Game" + GR)
                elif hilo == "bet":
                    try:
                        print("Your balance: %s" % str('{0:.6f}'.format(player.ethereums)))
                        bet = float(input("How many ETH you want to bet ?(Numeric): "))
                        if bet > player.ethereums:
                            print(RD + "Insufficient balance !" + GR)
                            continue
                        player.ethereums -= bet
                        bet_event = str(input("Next number will be lower or higher than 50 ?(lo/hi): ")).lower()
                        if bet_event == "hi" or bet_event == "lo" and bet >= 0:
                            while True:
                                num = rnd.randint(0, 100)
                                if num != 50:
                                    break
                            print("Number is: %d" % num)
                            status = (num > 50)
                            if bet_event == "lo" and status == False:
                                player.ethereums += bet * 2
                                print("You won %s ETH !" % str(bet * 2))
                                stats.update(_player.StatsTypes.eth_earned, (bet * 2))
                            elif bet_event == "hi" and status == True:
                                player.ethereums += bet * 2
                                print("You won %s ETH !" % str(bet * 2))
                                stats.update(_player.StatsTypes.eth_earned, (bet * 2))
                            else:
                                print(RD + "You lose !" + GR)
                        else:
                            print(RD + "Unknown input !" + GR)
                    except:
                        print(RD + "Non-numeric ETH value entered !" + GR)
                        continue
                elif hilo == "exit":
                    print(RD + "Closing the HiLo Game... " + SR)
                    break
                else:
                    print(RD + "Unknown input !" + GR)
        elif cmd == "lanhunt":
            player.ethereums += lanhunt.mainLanHuntCLI()
        elif cmd == "debug":
            f = open("variables_dbg_out.txt", "w")
            f.write(str("\n=========LOCALS=========\n" + str(locals()) + "\n" + "=========GLOBALS=========\n" + str(
                globals()) + "\n" + "=========DIR=========\n" + str(dir())))
            f.close()
        elif cmd == "miner_stat":
            time.sleep(1)
            if miner_power_status == "on":
                print(SR + YW + "Miner status: " + SB + GR + str(miner_power_status) + SR)
            else:
                print(SR + YW + "Miner status: " + SB + RD + str(miner_power_status))
        elif cmd == "miner_cfg":
            cfgcfg = str(input("Miner (on/off): ")).lower()
            if cfgcfg == "off":
                miner_power_status = "off"
            elif cfgcfg == "on":
                miner_power_status = "on"
            else:
                print(RD + "Unknown input. Please try again" + SR)
        elif cmd == "clear":
            clear_tty()

        else:
            print(RD + "Unknown input. Please try again" + SR)
    except KeyboardInterrupt:
        time.sleep(1)
        print(RD + "\nAll programs stopped !\nTo exit from dHackOS, type shutdown !" + SR)
print(RD + "Shutting down...")
