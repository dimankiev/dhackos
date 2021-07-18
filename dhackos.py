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
    from introd import intro, intro_nosound, clearScreen, say
    from soundwork import *

except Exception as e:
    print("\nPlease, use the commands below to install required modules: ")
    print("""
 pip install "module name that printed below"
 Example: pip install progressbar2
 """)
    print(str(e))
    exit()
sr = Style.RESET_ALL
sb = Style.BRIGHT
gr = Fore.GREEN
yw = Fore.YELLOW
rd = Fore.RED
bl = Fore.BLUE
wt = Fore.WHITE

init()

from prog.lanhunter import lanhunt

miner_power_status = "off"
version = "0.3.3b"

clearScreen()
while True:
    enable_sound = str(input("Enable sound? (yes/no): ").lower())
    if enable_sound == "yes" or enable_sound == "y":
        intro()
        break
    elif enable_sound == "no" or enable_sound == "n":
        intro_nosound()
        break
    else:
        print(rd + "Unknown input. Yes or no?" + sr)



companies = ["LG", "Samsung", "Lenovo", "Sony", "nVidia", "FBI", "CIA", "Valve", "Facebook", "Google",
    "Introversion Software", "Tesla Motors", "aaa114-project", "Microsoft", "SoloLearn Inc.", "Pharma",
    "Nestle", "Unknown", "Doogee", "Ethereum", "Ethereum", "Intel", "AMD", "ASIC", "Telegram", "LinkedIn",
    "Instagram", "DEFCON", "SCP", "HackNet", "Python", "Google Project Fi", "DDoS Booter Ltd.", "Valve", "Steam", "ST corp.", "dHackOS"]

bank_help = {}
with open('./data/strings/commands/bank.json', 'r') as file:
    content = file.read()
    data = json.loads(content)
    bank_help.update(data)

about = {}
with open('./data/strings/about_info.json', 'r') as file:
    content = file.read()
    data = json.loads(content)
    about.update(data)

debug_info = {
    "Version :": str("\n  dHackOS v." + version),
    "OS :": str("\n  " + platform.system() + " " + platform.release()),
    "RAM :": str("\n  Total : " + '{0:.2f}'.format(float(virtual_memory()[0] / 1073741824)) + " GB\n  Used : " + '{0:.2f}'.format(float(virtual_memory()[3] / 1073741824)) + " GB\n  Free : " + '{0:.2f}'.format(float(virtual_memory()[1] / 1073741824)) + " GB")
}

cmds = {}
with open('./data/strings/commands/system.json', 'r') as file:
    content = file.read()
    data = json.loads(content)
    cmds.update(data)

dhackosf_cmds = {}
with open('./data/strings/commands/dhackosf.json', 'r') as file:
    content = file.read()
    data = json.loads(content)
    dhackosf_cmds.update(data)

stats_desc = {}
with open('./data/strings/stats.json', 'r') as file:
    content = file.read()
    data = json.loads(content)
    stats_desc.update(data)

miner_desc = {}
with open('./data/strings/miner/minerdesc.json', 'r') as file:
    content = file.read()
    data = json.loads(content)
    miner_desc.update(data)

miner_components = {}
with open('./data/strings/miner/components.json', 'r') as file:
    content = file.read()
    data = json.loads(content)
    miner_components.update(data)

tcmds = {}
with open('./data/strings/targets/t_commands.json', 'r') as file:
    content = file.read()
    data = json.loads(content)
    tcmds.update(data)

target_desc = {}
with open('./data/strings/targets/targetdesc.json') as file:
    content = file.read()
    data = json.loads(content)
    target_desc.update(data)


def genIPv4():
    ip = str(str(rnd.randint(172, 192)) + "." + str(rnd.randint(0, 255)) + "." + str(rnd.randint(0, 255)) + "." + str(
        rnd.randint(1, 255)))
    return ip

def genIPv6():
    M = 16 ** 4
    ip = "fd39:fffd:" + ":".join(("%x" % rnd.randint(0, M) for i in range(6)))
    return ip


def genIP():
    if sol == "New" or sol == "new":
        ip = genIPv4()
    elif player["ipv6"] == 1:
        ip = genIPv6()
    else:
        ip = genIPv4()
    return ip


def getVarFromFile(filename):
    global success_sload, data
    try:
        data = shelve.open("saves/" + filename + ".db")
        success_sload = 1
    except:
        success_sload = 0
        data.close()
    return success_sload


def loadGame(username):
    global player, data, apps, stats, success_load, minehistory, targets, ips, miner, bank, anticheat, miner_power_status, off_earn_k, miner_power, mined, bank_off_earn_k, path
    success_load = 0
    if platform.system() == "Windows":
        path = "saves\\"
    elif platform.system() == "Linux":
        path = "saves/"
    else:
        path = "saves/"
    try:
        with open(path + username + ".md5", "r") as f:
            hashsum = str(f.readline())
            try:
                checksum = md5SaveCheckSum("saves/" + str(username) + ".db", username, 0)
            except:
                success_load = 0
            f.close()
        if hashsum != checksum:
            print(gr + sb + "\n[INTEGRITY_CHECK] " + Style.NORMAL + "Save is: " + sb + rd + "MODIFIED\n" + sr)
            anticheat = 0
        else:
            print(gr + sb + "\n[INTEGRITY_CHECK] " + Style.NORMAL + "Save is: " + sb + "OK\n" + sr)
            anticheat = 1
        data_load = getVarFromFile(str(username))
        if data_load == 1:
            player = data["player"]
            apps = data['apps']
            stats = data['stats']
            minehistory = data['minehistory']
            targets = data['targets']
            ips = data['ips']
            miner = data['miner']
            bank = data['bank']
            saveinfo = data['saveinfo']
            miner_power_status = data['miner_power_status']
            data.close()
        else:
            data.close()
        if saveinfo["version"] != version:
            print(rd + sb + f"Your save is outdated. Save version is {saveinfo['version']}" + sr)

        if md5(pwd.getpass("Please enter your password: "), "dhackos") != player["password"]:
            print(rd + "The password is wrong !\n" + sr)
            success_load = 0
        else:
            addInStats("launches", 1, int)
            off_earn_k = time.time() - saveinfo["timestamp"]
            miner_power = float((rnd.uniform(0.0000001, 0.0005) * rnd.randint(25,100)) * miner["cpu"] * miner["gpu"] * miner["ram"] * miner["miner"] * 200)
            mined = float(rnd.uniform(0.00000000001, 0.00000005) * stats["miners"] * (stats["ownminers"] ** 3) + rnd.uniform(0.00000000001, 0.00000005 * miner["miner"]) * miner_power * (miner_power / 20000))
            if miner_power_status == "on":
                player["ethereums"] += mined * off_earn_k
                bank_off_earn_k = off_earn_k // 60
                print(" \n" + Fore.MAGENTA + "You were offline for: %d mins" % bank_off_earn_k)
                print(Fore.MAGENTA + sb + "Offline earnings: %s ETH" % str('{0:.8f}'.format(float(mined * off_earn_k))) + sr)
                addInStats("eth_earned", mined, float)
            else:
                bank_off_earn_k = off_earn_k // 60
                print(" \n" + Fore.MAGENTA + "You were offline for: %d mins" % bank_off_earn_k)
                print("Miner status: " + sb + miner_power_status + sr)
            if bank["balance"] > 0:
                if bank_off_earn_k >= 1:
                    bank_earnings = float((bank["balance"] / 100) * bank["deposit_rate"]) * bank_off_earn_k
                    bank["balance"] += bank_earnings
                    print(Fore.MAGENTA + sb + "Bank (deposit) earnings: %s ETH" % str('{0:.8f}'.format(float(bank_earnings))) + sr)
            success_load = 1
    except Exception as err:
        print(rd + "Save is missing or corrupted !\nSave version may be old\n" + sr)
        time.sleep(1)
        try:
            data.close()
        except:
            print("Try again or start new game !")


def saveWrite(username, player, apps, stats, minehistory, targets, ips, miner, saveinfo, bank):
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
        "player": player, "apps": apps, "stats": stats,
        "minehistory": minehistory, "targets": targets, "ips": ips,
        "miner": miner, "saveinfo": saveinfo, "bank": bank,
        "miner_power_status": miner_power_status
    })
    save.close()
    md5SaveCheckSum("saves/" + str(username) + ".db", username, 1)

def saveGame(username):
    global player, apps, stats, minehistory, targets, ips, miner, saveinfo, bank
    saveinfo = {"version": str(version), "timestamp": time.time()}
    try:
        saveWrite(username, player, apps, stats, minehistory, targets, ips, miner, saveinfo, bank)
    except Exception as ex:
        print(rd + "Save failed! Please check your read/write permissions\n(If you a Linux or Android user, check chmod or try to launch this game as root)" + sr)
        print(ex)


def newGame():
    time.sleep(2)
    print(sb + "Installing operating system image..." + sr + wt)
    time.sleep(3)
    for i in progressbar.progressbar(range(100)): time.sleep(0.1)
    time.sleep(3)
    print(sr + "[" + gr + "SUCCESS" + sr + "]")
    time.sleep(2)
    while True:
        global player, apps, stats, minehistory, news, miner, bank, anticheat
        news = {}
        player = {"ethereums": 0.0, "ip": "127.0.0.1", "dev": 0, "ipv6": 0, "xp": 0, "sentence": 0}
        player["ip"] = str(genIP())
        player["username"] = str(input("Please enter your username: "))
        if player["username"] == "debug":
            print(rd + "Username DEBUG is not available !" + sr)
            continue
        player["password"] = str(pwd.getpass("Please enter your password: ").lower())
        if len(player["password"]) < 6:
            print(
                rd + "Password can't be less than 6 symbols, please choose another password\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" + sr)
        elif player["password"] != pwd.getpass("Please repeat your password: ").lower() and len(
                player["password"]) >= 6:
            print(rd + "Passwords do not match !\nPlease try again\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" + sr)
        else:
            player["password"] = md5(player["password"], "dhackos")
            apps = {"scanner": 1, "spam": 1, "bruteforce": 1, "sdk": 1, "ipspoofing": 1, "dechyper": 1}
            stats = {"eth_earned": 0.0, "shacked": 0, "xp": 0, "rep": 0, "scans": 0, "level": 1, "symbols": 0,
                     "launches": 0, "miners": 1, "ownminers": 1, "proxy": 0}
            miner = {"cpu": 1, "gpu": 1, "ram": 1, "miner": 1}
            bank = {"balance": 0, "deposit_rate": rnd.randint(5,9)}
            addInStats("launches", 1, int)
            genTargetsList()
            anticheat = 1
            break


def bankWork():
    global bank, player
    while True:
        time.sleep(3600)
        bank["balance"] += float((bank["balance"] / 100) * bank["deposit_rate"])
        

def addInStats(param, value, type):
    try:
        stats[param] = stats[param] + type(value)
    except:
        print(rd + "addInStats() function error. Please contact administrator" + sr)


def levelCheck():
    if (player["xp"] // 1000) >= 1:
        stats["level"] = stats["level"] + (player["xp"] // 1000)
        player["xp"] = 0
        award = 10 * stats["level"]
        player["ethereums"] = float(player["ethereums"] + award)
        print(sb + gr + str(stats["level"]) + " level reached !\n You had been awarded by " + str(award) + " ETH !\n Congrats !" + sr)

def showVoc(vocabulary, description, additional, color):
    if description == None and additional == None:
        for param in vocabulary:
            print(color + sb + param + Style.NORMAL + " " + str(vocabulary[param]) + sr)
    elif description == None and additional != None:
        for param in vocabulary:
            print(
                color + sb + param + Style.NORMAL + " " + str(vocabulary[param]) + " " + str(additional) + sr)
    elif description != None and additional == None:
        for param in vocabulary:
            if param == "k":
                print(color + sb + description[param] + Style.NORMAL + "DHACK26" + str(
                    vocabulary[param]) * 2 + sr)
            elif param == "eth_earned":
                print(color + sb + description[param] + Style.NORMAL + " " + str(
                    '{0:.8f}'.format(vocabulary[param])) + sr)
            else:
                print(color + sb + description[param] + Style.NORMAL + " " + str(vocabulary[param]) + sr)
    else:
        for param in vocabulary:
            print(Fore.color + sb + description[param] + Style.NORMAL + " " + str(
                vocabulary[param]) + " " + str(additional) + sr)


def md5(string, salt):
    hash = str(string + salt)
    hash = hashlib.md5(hash.encode()).hexdigest()
    return hash


def md5SaveCheckSum(fname,username,action):
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
    if player["username"] != "debug":
        min = (apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4
    else:
        min = 1000
    if k == 1:
        target["firewall"] = min
    else:
        target["firewall"] = rnd.randint(min,(min + (rnd.randint(1, min)) + k))
    target = {"ip": ip,
              "ethereums": rnd.uniform((apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4,
                                      pi * float(target["firewall"]) + float(k)),
              "company": companies[rnd.randint(0, int(len(companies) - 1))], "port": rnd.randint(1, 65535), "service": "OpenSSH",
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
        ip = str(genIP())
        target = genTarget(i, ip)
        targets[ip] = target
        ips.append(str(ip))
    gentargets = 0
    target = {}


def traceStart():
    global tracing, connection, target
    tracing = int(apps["ipspoofing"] - target["firewall"]) + stats["proxy"] * 2
    if tracing <= 13:
        #print(str(tracing) + "sec calculated") #debug_info
        tracing = 13
    while True:
        if connection == 1 and tracing != 0:
            time.sleep(1)
            tracing -= 1
        else:
            break


def proxyKill():
    global stats
    while True:
        time.sleep(30)
        chance = rnd.randint(0,100)
        if chance >= 50:
            if stats["proxy"] > 5:
                stats["proxy"] -= 1


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
    print(rd + sb + "Don't use this function if it's not necessary !")
    if input("Are you sure ?(Yes/No): ").lower() == "yes":
        print(gr + "Changing..." + wt)
        for i in progressbar.progressbar(range(100)): time.sleep(0.1)
        player["ipv6"] = ipv
        genTargetsList()
        if ipv == 0:
            print("Connecting to IPv4 network...")
        else:
            print("Connecting to IPv6 network..." + wt)
        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
        player["ip"] = genIP()
        print(sr + "[" + gr + sb + "SUCCESS" + sr + "]")
        cmd_msg.pop(2)
        cmd_msg.insert(2, ('class:host', str(player["ip"])))
        time.sleep(1)
        print(" \n" + yw + "Your IP: " + sb + gr + str(player["ip"]) + sr)
    else:
        print(sr + "[" + rd + sb + "ABORTED" + sr + "]")


def searchTargets(is_bot):
    global player_target_list, bot_target_list, bot_target
    if is_bot == 0:
        print(Fore.WHITE + Back.BLUE + sb + "dHackOS Scanner v.0.5-r.4" + sr)
        addInStats("scans", 1, int)
        xp = rnd.randint(0, 50)
        addInStats("xp", xp, int)
        player["xp"] = player["xp"] + xp
        addInStats("rep", rnd.randint(0, 10), int)
        print(Fore.CYAN + str(len(ips)) + " IPs in subnet")
        print(Fore.CYAN + "Scanning subnet...")
        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
        print("Deep scanning...")
        for i in progressbar.progressbar(range(100)): time.sleep(0.05 / float(apps["scanner"]))
        scantime = rnd.uniform(0.02, 1) * (100 / apps["scanner"])
        player_target_list = loadTargetList()
        print(gr + "Targets found !\nIP list:" + sb)
        for i in range(0, len(player_target_list)): print(str(i) + ". " + player_target_list[int(i)])
        print(Style.NORMAL + "Please choose the IP, launch " + sb + "dHackOSf" + Style.NORMAL + " and enter the IP what you choosen" + sr)
    else:
        bot_target_list = loadTargetList()
        bot_target = targets[bot_target_list[rnd.randint(0,(len(bot_target_list) - 1))]]
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
        tbr = threading.Thread(target=resetTargetBalance) #target balance reset
        tbr.daemon = True
        tbr.start()
        game_bot = threading.Thread(target=gameBot)
        game_bot.daemon = True
        game_bot.start()
        bank_worker = threading.Thread(target=bankWork)
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
        time.sleep(1)
        if miner_power_status == "on":
            try:
                if stats["ownminers"] < 4 and stats["ownminers"] > 1:
                    collective_power = stats["ownminers"] * rnd.uniform(25,100)
                    #print("Collective Power Level: 1.2")
                elif stats["ownminers"] >= 4 and stats["ownminers"] <= 7:
                    collective_power = stats["ownminers"] * rnd.uniform(50,150)
                    #print("Collective Power Level: 2")
                elif stats["ownminers"] > 7 and stats["ownminers"] <= 15:
                    collective_power = stats["ownminers"] * rnd.uniform(75,175)
                    #print("Collective Power Level: 3")
                elif stats["ownminers"] > 15 and stats["ownminers"] <= 25:
                    collective_power = stats["ownminers"] * rnd.uniform(100,250) ** 2
                    #print("Collective Power Level: 4")
                elif stats["ownminers"] > 35 and stats["ownminers"] <= 45:
                    collective_power = stats["ownminers"] * rnd.uniform(175,275)
                    #print("Collective Power Level: 5")
                elif stats["ownminers"] > 45 and stats["ownminers"] <= 50:
                    collective_power = stats["ownminers"] * rnd.uniform(225,325)
                    #print("Collective Power Level: 6")
                elif stats["ownminers"] > 50 and stats["ownminers"] <= 65:
                    collective_power = stats["ownminers"] * rnd.uniform(500,1000) ** 2
                    #print("Collective Power Level: 7")
                elif stats["ownminers"] > 75 and stats["ownminers"] <= 90:
                    collective_power = stats["ownminers"] * rnd.uniform(1250,3000)
                    #print("Collective Power Level: 8")
                elif stats["ownminers"] > 90 and stats["ownminers"] <= 125:
                    collective_power = stats["ownminers"] * rnd.uniform(3000,7000) ** 2
                    #print("Collective Power Level: 9")
                elif stats["ownminers"] == 1:
                    collective_power = float(1)
                    #print("Collective Power Level: 0")
                elif stats["ownminers"] == 2:
                    collective_power = rnd.uniform(50,125)
                    #print("Collective Power Level: 1")
                else:
                    collective_power = float((stats["ownminers"] ** (stats["ownminers"] / 500)) * rnd.uniform(10000 * (stats["ownminers"]/100),50000 * (stats["ownminers"]/100)) ** rnd.randint(2,5))
                    #print("Collective Power Level: 10")
            except:
                collective_power = 10**21
            miner_power = float((rnd.uniform(0.0000001, 0.0005) * rnd.randint(25,100)) * miner["cpu"] * miner["gpu"] * miner["ram"] * miner["miner"] * collective_power)
            mined = float(rnd.uniform(0.0000000001, 0.00000005) * stats["miners"] * (stats["ownminers"] ** 3) + rnd.uniform(0.0000000001, 0.00000005 * miner["miner"]) * miner_power * (miner_power / collective_power))
            #print("Collective Power: %s | Miner Power: %s | Mined: %s" % (str(collective_power),str(miner_power),str(mined)))
            now = datetime.datetime.now()
            player["ethereums"] = player["ethereums"] + mined
            addInStats("eth_earned", mined, float)
            if miner_enroll == 1:
                continue
            elif miner_enroll == 0 and game_started == 1:
                if minelog == 10 and firststart == 0:
                    minehistory = {"1": minehistory["2"], "2": minehistory["3"], "3": minehistory["4"], "4": minehistory["5"], "5": minehistory["6"], "6": minehistory["7"], "7": minehistory["8"], "8": minehistory["9"], "9": minehistory["10"], "10": ""}
                    minehistory[str(minelog)] = str("[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] Mined: " + str('{0:.10f}'.format(mined)) + " ETH")
                else:
                    if minelog == 1:
                        minelog = 10
                        firststart = 0
                        minehistory[str(minelog)] = str("[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] Mined: " + str('{0:.10f}'.format(mined)) + " ETH")
                    else:
                        minelog -= 1
                        minehistory[str(minelog)] = str("[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "] Mined: " + str('{0:.10f}'.format(mined)) + " ETH")
            else:
                continue


def addNews(stolen,target):
    global news
    now = datetime.datetime.now()
    if stolen > 0.0:
        news[str(accident_n)] = { "time": str("[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]"), "accident": str("Someone stolen " + str('{0:.10f}'.format(stolen)) + " ETH from " + str(target["company"]) + "'s corporate network PC")}
    else:
        news[str(accident_n)] = { "time": str("[" + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) + "]"), "accident": str("Someone hacked " + str(target["company"]) + "'s corporate network PC")}


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
            #print("\nStolen: " + str(stolen)) #debug info
            #bot['firewall'] += rnd.randint(bot['firewall'],int(target['firewall'] + bot['firewall']))
            #target["firewall"] += rnd.randint(bot["firewall"],int(target["firewall"] + bot["firewall"]))
            target["ethereums"] = 0
            #print("\nNews show: " + str(news_show)) #debug_info 
            if news_show == 1:
                continue
            elif news_show == 0 and game_started == 1:
                if accident_n == 10 and firststart == 0:
                    news = {"1": news["2"], "2": news["3"], "3": news["4"], "4": news["5"], "5": news["6"], "6": news["7"], "7": news["8"], "8": news["9"], "9": news["10"], "10": {}}
                    addNews(stolen,target)
                else:
                    if accident_n == 1:
                        accident_n = 10
                        firststart = 0
                        addNews(stolen,target)
                    else:
                        accident_n -= 1
                        addNews(stolen,target)
                targets[str(target["ip"])] = target
                #print("accident_n: " + str(accident_n) + " " + str(news[str(accident_n)])) #debug_info
            else:
                continue


def init_dHackOS_Prompt():
    global cmd_msg, cmd_style
    cmd_style = pStyle.from_dict({
    # User input (default text).
    '':          '#ffffff',

    # Prompt.
    'username': '#21F521',
    'at':       'ansigreen',
    'colon':    '#ffffff',
    'pound':    '#ffffff',
    'host':     '#21F521', # bg:#444400
    'path':     'ansicyan underline'
    })
    cmd_msg = [
        ('class:username', str(player["username"])),
        ('class:at',       '@'),
        ('class:host',     str(player["ip"])),
        ('class:colon',    ':'),
    ]
    if player["dev"] == 1 and anticheat == 1:
        cmd_msg.append(('class:path',     '~/dhackos-dev'))
        cmd_msg.append(('class:pound',    '# '))
    elif anticheat == 1:
        cmd_msg.append(('class:path',     '~/dhackos'))
        cmd_msg.append(('class:pound',    '# '))
    else:
        cmd_msg.append(('class:path',     '~/dhackos-cheat'))
        cmd_msg.append(('class:pound',    '# '))


def init_dHackOSf_Prompt(username,ip):
    global cmdf_msg, cmdf_style
    cmdf_style = pStyle.from_dict({
    # User input (default text).
    '':          '#ffffff',

    # Prompt.
    'username': '#21F521',
    'at':       'ansigreen',
    'colon':    '#ffffff',
    'pound':    '#ffffff',
    'host':     '#21F521', # bg:#444400
    'path':     'ansicyan underline'
    })
    cmdf_msg = [
        ('class:username', str(username)),
        ('class:at',       '@'),
        ('class:host',     str(ip)),
        ('class:colon',    ':'),
        ('class:path',     '~/'),
        ('class:pound',    '# ')
    ]


#print(sr + "[" + gr + "DONE" + sr + "]")
while True:
    try:
        sol = input(yw + "Load save or start new session? (Save/New): " + sr).lower()
    except KeyboardInterrupt:
        print(rd + "\nExiting...\nGoodbye :)" + sr)
        exit()
    if sol == "sav" or sol == "save" or sol == "sv" or sol == "sve" or sol == "s":
        time.sleep(1)
        print(sb + "[" +  Fore.LIGHTGREEN_EX + "SYSTEM LOGIN" + sr + sb + "]" + sr)
        try:
            time.sleep(1)
            username = str(input("Please enter your username: "))
            with open("saves/" + username + ".db", "r") as f:
                f.close()
            print("Please wait...\n" + gr + "Loading..." + sr)
            time.sleep(1)
            print(sb + Fore.LIGHTGREEN_EX + "Welcome back " + sr + username + sb +  Fore.LIGHTGREEN_EX + "!")
            loadGame(username)
            if success_load == 1:
                print(" \n" + gr + "Your IP: " + sb + player["ip"] + sr + "\n")
                print(yw + "Type help for a list of commands\n " + sr)
                initGame()
                init_dHackOS_Prompt()
                f.close()
                break
            else:
                continue
        #except Exception as err:
        except FileNotFoundError:
            print(rd + "User not found please try again" + sr)
    elif sol == "new" or sol == "nw" or sol == "nwe" or sol == "n" or sol == "nee":
        newGame()
        time.sleep(2)
        print(sr + "[" + gr + "SUCCESS" + sr + "]\n")
        time.sleep(1)
        print(sb + gr + "Welcome " + sr + sb + player["username"] + sb + gr + "!")
        print(" \n" + "Your IP: " + sb + str(player["ip"]) + sr + "\n")
        print(yw + "Type help for a list of commands\n " + sr)
        initGame()
        init_dHackOS_Prompt()
        break

    elif sol == "debug":
        player = {"ethereums": 999999999, "ip": "127.0.0.1", "dev": 0, "ipv6": 0, "xp": 999999999, "sentence": 0, "username": "debug", "password": md5("debug", "dhackos")}
        apps = {"scanner": 999999999, "spam": 999999999, "bruteforce": 999999999, "sdk": 999999999, "ipspoofing": 999999999, "dechyper": 999999999}
        stats = {"eth_earned": 999999999, "shacked": 999999999, "xp": 999999999, "rep": 999999999, "scans": 999999999, "level": 999999999, "symbols": 999999999,
                 "launches": 999999999, "miners": 999999999, "ownminers": 999999999, "proxy": 999999999}
        miner = {"cpu": 10, "gpu": 10, "ram": 10, "software": 10}
        bank = {"balance": 999999999, "borrowed": 0, "deposit_rate": rnd.randint(5,9), "credit_rate": rnd.randint(9,13), "max_borrow": 300, "borrow_time": 0}
        addInStats("launches", 1, int)
        genTargetsList()
        anticheat = 1
        print(sr + gr + ".::SUCCESS::.")
        print("Your IP: " + sb + str(player["ip"]) + sr)
        initGame()
        init_dHackOS_Prompt()
        break
    else:
        print(rd + "Unknown input ! Please, try again" + sr)
sol = None
dHackOSprmpt = PromptSession()
while True:
    try:
        if player["sentence"] == 3:
            player["sentence"] = rnd.randint((player["sentence"] + 1),10)
            print(rd + "You has been sentenced for " + str(player["sentence"]) + " years" + sr)
            showVoc(stats, stats_desc, None, gr)
            print(rd + "[GAME OVER]" + sr)
            saveGame(str(player["username"]))
            break
        elif player["sentence"] > 3:
            print(rd + "You has been sentenced for " + str(player["sentence"]) + " years" + sr)
            showVoc(stats, stats_desc, None, gr)
            print(rd + "[GAME OVER]" + sr)
            saveGame(str(player["username"]))
            break
        else:
            cmd = str(dHackOSprmpt.prompt(cmd_msg, style=cmd_style, auto_suggest=AutoSuggestFromHistory())).lower()
        levelCheck()
        addInStats("symbols", len(cmd), int)
        if cmd == "help":
            showVoc(cmds, None, None, yw)
        elif cmd == "apps":
            showVoc(apps, None, "lvl", yw)
        elif cmd == "balance":
            say(" \n" + sb + wt + Back.BLUE + "Ethereum Core v.8 CLI" + sr)
            print(bl + "Connecting..." + sr)
            time.sleep(3)
            print(bl + sb + "Your balance is: " + Fore.MAGENTA + '{0:.8f}'.format(player["ethereums"]) + Fore.MAGENTA + " ETH" + sr + " \n")
        elif cmd == "scan":
            searchTargets(0)
        elif cmd == "upgrade":
            print(" \n" + wt + Back.GREEN + "dHackOS upgrade CLI v.0.9-r.3" + sr)
            showVoc(apps, None, "lvl", gr)
            print(bl + "-=-=-=-=-=-=-=-=-=-=-" + sr)
            while True:
                print(yw + "Please choose the program which you want to upgrade or type exit\nPrint all to upgrade all programs simultaneously")
                program = input("What we're going to upgrade today ? " + sr).lower()
                try:
                    if program != "all" and program != "exit":
                        apps[program] = ((apps[program] + 1) - 1)
                except Exception as e:
                    print(rd + "Program not found or unknown input !\n" + str(e) + gr)
                    continue
                if program != "exit":
                    while True:
                        try:
                            cost = float(0)
                            levels = int(input(yw + "How many levels do you want to upgrade (1-∞): " + sr))
                            if levels <= 0:
                                print(rd + "This value can't be zero or be less than zero" + gr)
                                break
                            if program == "all":
                                cost = float(0)
                                for app in apps:
                                    cost += float(pi * (float(apps[app]) + levels))
                            else:
                                cost = float(pi * (apps[program] + levels))
                            print(yw + "Upgrade of " + sb + str(program) + sr + yw + " will cost you " + sb + str(cost) + " ETH." + sr)
                            if input(yw + "Upgrade (Y/N): " + sr).lower() == "y":
                                if player["ethereums"] >= cost:
                                    player["ethereums"] = float(float(player["ethereums"]) - float(cost))
                                    if program == "all":
                                        for app in apps:
                                            apps[app] += levels
                                    else:
                                        apps[program] = int(int(apps[program]) + int(levels))
                                    print(sr + "[" + sb + gr + "SUCCESS" + sr + "]" + yw)
                                    break
                                else:
                                    print(rd + "Insufficient balance !" + gr)
                                    break
                            else:
                                print(rd + "Upgrade aborted !" + gr)
                                break
                        except Exception as e:
                            print(rd + "Program not found or unknown input !\n" + str(e) + gr)
                            break
                elif program == "exit":
                    print(rd + "Stopping... " + sr)
                    break
                else:
                    print(rd + "Unknown input !" + gr)
        elif cmd == "stats":
            showVoc(stats, stats_desc, None, Fore.CYAN)
        elif cmd == "rescan_subnet":
            print(Fore.CYAN + "Scanning subnet...")
            sub_gen = threading.Thread(target=genTargetsList)
            sub_gen.daemon = True
            sub_gen.start()
            while True:
                time.sleep(1)
                print("Scanning in progress... " + str(scan_percent) + "%")
                if scan_percent == 100.0:
                    print(gr + "Done !")
                    break
            print(Fore.CYAN + str(len(ips)) + " servers in subnet" + sr)
        elif cmd == "load_list":
            if player_target_list != []:
                print(gr + "IP list:" + sb)
                for i in range(0,len(player_target_list)):
                    print(str(i) + ". " + player_target_list[int(i)])
                print(Style.NORMAL + "Please choose the IP, launch " + sb + "dHackOSf" + Style.NORMAL + " and enter the IP what you choosen" + sr)
            else:
                print(rd + "There is no targets in your list ! Type scan to find one." + sr)
        elif cmd == "dhackosf":
            print(Fore.WHITE + Back.RED + sb + "dHackOS Exploit Framework v.0.9-r.2" + sr)
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
                    print(rd + sb + "Tutorial:\nSelect an IP from your previous scan results\nYou can enter just a number (0-10) of IP in target list\nType exit to stop the dHackOSf !" + gr)
                    target_ip = str(input("Please enter the target IP: ").lower())
                    if target_ip == "exit":
                        print("Stopping the dHackOSf..." + sr)
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
                                print(rd + "Wrong IP entered or target list is empty !\n" + yw + "Start scan to find a new target list" + sr)
                                break
                    print("dHackOSf is initializing !\nPlease wait...\n" + yw + "Type help for a list of commands." + gr)
                    dHackOSf_prmpt = None
                    dHackOSf_prmpt = PromptSession()
                    init_dHackOSf_Prompt("dhackosf",df_status)
                    time.sleep(1)
                else:
                    if scan_done == True and fw_bypassed == True and modules_loaded == True and connected == True:
                        all_done = True
                        init_dHackOSf_Prompt("dhackosf",df_status)
                    df_cmd = str(dHackOSf_prmpt.prompt(cmdf_msg, style=cmdf_style, auto_suggest=AutoSuggestFromHistory())).lower()
                    if df_cmd == "help":
                        showVoc(dhackosf_cmds, None, None, yw)
                        print(rd + "Don't forget to load dhackosf modules" + gr + sb)
                    elif df_cmd == "connect":
                        if fw_bypassed == True and scan_done == True and connected == False:
                            print(Fore.CYAN + "Connecting..." + sb)
                            for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                            connected = True
                            print(yw + "Now you can retrieve the root hash !" + gr + sb)
                            df_status = str(target_ip)
                        elif connected == True:
                            print(rd + "You've already connected !" + gr + sb)
                        else:
                            print(rd + "Scan target first !\nThen bypass the firewall !\nThen connect..." + gr + sb)
                    elif df_cmd == "bypass":
                        if fw_bypassed == False and scan_done == True:
                            print(Fore.CYAN + "Bypassing firewall..." + wt)
                            for i in progressbar.progressbar(range(100)): time.sleep(float((target["firewall"] / apps["ipspoofing"]) / 10))
                            fw_bypassed = True
                            print(yw + "Now you can connect to the target !" + gr + sb)
                        elif fw_bypassed == True:
                            print(rd + "Firewall is already bypassed !" + gr + sb)
                        else:
                            print(rd + "Please scan the target first !" + gr + sb)
                    elif df_cmd == "scan":
                        if scan_done == False and modules_loaded == True:
                            print(gr + "Scanning target..." + wt)
                            for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                            showVoc(target, target_desc, None, gr)
                            print(yw + "Now you can bypass the firewall !" + gr + sb)
                            scan_done = True
                        elif scan_done == True:
                            print(rd + "Scan is already done !" + gr + sb)
                        else:
                            print(rd + "Please load modules first !" + gr + sb)
                    elif df_cmd == "exit":
                        print(rd + "Exiting..." + sr)
                        break
                    elif df_cmd == "load_modules":
                        if modules_loaded == False:
                            print(rd + "Loading dHackOSf modules..." + wt)
                            for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                            showVoc(apps, None, "[OK]", rd)
                            modules_loaded = True
                            print(yw + "Now you can start the scan" + gr + sb)
                        else:
                            print(rd + "Modules is already loaded !" + gr + sb)
                    elif df_cmd == "get_hash":
                        if hash_got == False and all_done == True:
                            print(Fore.CYAN + "Retrieving root hash..." + wt)
                            for i in progressbar.progressbar(range(100)): time.sleep(float((target["firewall"] / apps["sdk"]) / 10))
                            hash_got = str(md5(target["ip"], str(rnd.randint(0, 10000))))
                            print(gr + "Success !\nHash: " + sb + hash_got)
                            print(yw + "Now you can start bruteforce process !" + gr + sb)
                        elif hash_got != False:
                            print(rd + "Hash has been already retrieved !" + gr + sb)
                        else:
                            print(rd + "Please load modules first !\nThen scan target\nThen bypass the firewall\nThen - connect and get the hash" + gr + sb)
                    elif df_cmd == "bruteforce":
                        if all_done == True and hash_got != False and hash_got != True:
                            print("Bruteforcing..." + wt)
                            for i in progressbar.progressbar(range(100)): time.sleep(float(((pi + target["firewall"]) / apps["bruteforce"]) / 10))
                            hack_chance = (apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4
                            fw_vs_player = target["firewall"] - hack_chance
                            hack_done = True
                            hash_got = True
                            print(yw + "Now you can initialize shell on target server !" + gr + sb)
                        elif hash_got == False:
                            print(rd + "Please, get the hash first !" + gr + sb)
                        else:
                            print(rd + "Hash is already bruteforced !" + gr + sb)
                    elif df_cmd == "shell" and hack_done == True:  
                        if hack_chance >= fw_vs_player and hack_done == True:
                            print(sb + "Successful !")
                            print("Root access granted !")
                            xp = rnd.randint(0, 200)
                            addInStats("xp", xp, int)
                            player["xp"] = player["xp"] + xp
                            connection = 1
                            trace = threading.Thread(target=traceStart) #target balance reset
                            trace.daemon = True
                            trace.start()
                            print(yw + "You have " + str(tracing) + "sec before local admin trace you ! (Connection will be lost and ETHs seized by FBI)" + gr)
                            dHackOSf_prmpt = None
                            dHackOSf_prmpt = PromptSession()
                            init_dHackOSf_Prompt("root",df_status)
                            while True:
                                tcmd = str(dHackOSf_prmpt.prompt(cmdf_msg, style=cmdf_style, auto_suggest=AutoSuggestFromHistory())).lower()
                                if tracing == 0 or tracing <= 1:
                                    print(rd + "Connection was refused by local administrator...\nAttempting to revive remote session...")
                                    time.sleep(1)
                                    player["ethereums"] = 0
                                    stats["miners"] = 0
                                    player["sentence"] += 1
                                    addInStats("shacked", 1, int)
                                    connection = 0
                                    print("[dHackOSf] ERROR. FIREWALL IS BLOCKING SESSION !" + yw + "\n[dHackOS Corp] Your ETHs was seized by the FBI and injected miners deleted.\nYou will be sentenced after 3 FBI warnings.\nYou have " + str(player["sentence"]) + " warnings. Be careful." + sr)
                                    break
                                elif tcmd == "help":
                                    print(rd + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + gr + sb)
                                    showVoc(tcmds, None, None, gr)
                                    print(rd + sb + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + gr + sb)
                                elif tcmd == "wallet":
                                    print(rd + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + gr + sb)
                                    print("Your balance is: " + str(target["ethereums"]) + " ETH" + rd)
                                    print(".::dHackOSf detected an Ethereum address field::.\nWallet dechypering..." + wt)
                                    for i in progressbar.progressbar(range(100)): time.sleep(float(((pi + target["firewall"]) / apps["dechyper"]) / 10))
                                    print(".::dHackOSf injected code which changes all typed addresses with your for this input field. Just press enter::." + yw)
                                    wcmd = input("Please enter the Ethereum wallet address to send money to: ")
                                    print(rd + ".::Replacing addresses::." + wt)
                                    for i in progressbar.progressbar(range(100)): time.sleep(0.03)
                                    player["ethereums"] = player["ethereums"] + target["ethereums"]
                                    addInStats("eth_earned", target["ethereums"], float)
                                    print(gr + "Transfer successful !" + wt + str(target["ethereums"]) + yw + "ETH " + sr + "transferred." + sr)
                                    target["ethereums"] = 0.0
                                    print("Closing wallet..." + gr)
                                    print(rd + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + gr)
                                elif tcmd == "exit":
                                    print(Fore.CYAN + "Spamming...")
                                    earn = pi / (100 / (apps["spam"] + apps["ipspoofing"]))
                                    player["ethereums"] = player["ethereums"] + earn
                                    addInStats("shacked", 1, int)
                                    addInStats("eth_earned", earn, float)
                                    print(gr + "Success. Earned from spam: " + rd + str(earn) + " " + Back.YELLOW + "ETH" + sr)
                                    print(rd + "[dHackOSf] Console closed ! Disconnecting..." + sr)
                                    break
                                elif tcmd == "developer_mode":
                                    print(rd + "[Employee OS v.8.1 Pro] DEVELOPER MODE ACCESSED ! YOUR EMPLOYER WAS NOTICED !\nBlocking PC...\nClosing Internet connections..." + wt)
                                    for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                                    print("[dHackOSf] CONNECTION FAILURE !\n[dHackOSf] REMOTE CONTROL TROJAN DELETED LOGS AND SELF-DELETED" + sr)
                                    break
                                elif tcmd == "inject":
                                    print(rd + "dHackOSf miner injector v.0.1-r3" + wt)
                                    if target["miner_injected"] == 0:
                                        for i in progressbar.progressbar(range(100)): time.sleep(0.04)
                                        stats["miners"] = stats["miners"] + 1
                                        print(gr + "Miner injected into kernel !")
                                        target["miner_injected"] = 1
                                    else:
                                        print(rd + "Miner has been already injected into kernel !" + gr)
                                elif tcmd == "proxy":
                                    print(Fore.CYAN + "dHackOSf proxy init v.0.1.9-r1" + wt)
                                    if target["proxy"] == 0:
                                        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                                        stats["proxy"] = stats["proxy"] + 1
                                        print(gr + "Proxy initialized !")
                                        target["proxy"] = 1
                                    else:
                                        print(rd + "Proxy has been already initialized on this server !" + gr)
                                else:
                                    print(rd + "Unknown input !" + gr)
                        else:
                            print(rd + "Bruteforce unsuccesful !")
                            hack_end = True
                        targets[target["ip"]] = target
                        print("Disconnected from " + target["ip"])
                        print("Don't forget to start scan to find new target" + sr)
                        break
                    elif df_cmd == "shell" and hack_done != True:
                        print(rd + "Please bruteforce the hash first !" + gr)
                    else:
                        print(rd + "Unknown input !" + gr)
        elif cmd == "shutdown":
            sol = input(yw+ sb + "Save session? (Yes/No): " + sr).lower()
            if sol == "yes" or sol == "ys" or sol == "y":
                time.sleep(1)
                print(rd + "Stopping all processes...\n" + yw + "Saving session...\n" + wt + sb + "Disconnected..." + sr)
                saveGame(str(player["username"]))
            else:
                print(rd + "Stopping all processes...\n" + wt + sb + "Disconnected..." + sr)
            break
        elif cmd == "dev_mode":
            print(rd + "Developers only can access this command !")
            devpass = md5(pwd.getpass("Please enter developer password: "), "")
            if devpass == "28eab4ff8df5a8f44e82f75a7d93b8b2":
                print(gr + "Developer Mode Activated !")
                print(rd + "If you don't how to use dev mode, you're crazy or cheater !" + gr)
                while True:
                    dev_cmd = input("dHackOS dev > ").lower()
                    if dev_cmd == "help":
                        print("data_input\nset_eth\nexit\nsentenceme")
                    elif dev_cmd == "data_input":
                        print(".::DATA INPUT MODE IS ACTIVATED::.")
                        print("player = " + str(player) + "\napps" + str(apps) + "\nstats" + str(stats))
                        for param in player:
                            vtype = type(player[param])
                            player[param] = vtype(input("player[" + str(param) + "] = "))
                            print(".::SUCCESS::.")
                        for param in apps:
                            vtype = type(apps[param])
                            apps[param] = vtype(input("apps[" + str(param) + "] = "))
                        for param in stats:
                            vtype = type(stats[param])
                            stats[param] = vtype(input("stats[" + str(param) + "] = "))
                        print(rd + ".::DATA INPUT MODE IS DEACTIVATED::." + sr)
                        player["password"] = md5(player["password"], "dhackos")
                    elif dev_cmd == "set_eth":
                        player["ethereums"] = float(input("Please, enter NEW player ETH balance: "))
                    elif dev_cmd == "sentenceme":
                        sentencesure = input("Are you sure ?(Yes, I am sure what will be after this action./No): ")
                        if sentencesure == "Yes, I am sure what will be after this action.":
                            player["sentenceme"] = 3
                            print(rd + "[DONE]" + gr)
                        else:
                            print(rd + "[ABORTED]" + gr)
                    elif dev_cmd == "exit":
                        print(rd + "Exiting..." + sr)
                        break
                    else:
                        print(rd + "Unknown input !" + gr)
                player["dev"] = 1
            else:
                print(rd + "Wrong dev password ! Don't try again later !" + sr)
        elif cmd == "change_ip_v":
            if player["ipv6"] == 1:
                changeIPv(0)
            else:
                changeIPv(1)
        elif cmd == "update_ip":
            time.sleep(1)
            confirm = input(yw + "Please confirm (yes/no):" + sr).lower()
            if confirm == "yes":
                time.sleep(2)
                print(yw + "Reconnecting..." + wt)
                time.sleep(1)
                for i in progressbar.progressbar(range(100)): time.sleep(0.03)
                player["ip"] = genIPv4()
                cmd_msg.pop(2)
                cmd_msg.insert(2, ('class:host', str(player["ip"])))
                time.sleep(1)
                print(sr + "[" + sb + gr + "SUCCESS" + sr + "]")
                time.sleep(1)
                print(yw + "Your IP: " + sb + gr + str(player["ip"]) + sr)
            elif confirm == "no":
                time.sleep(1)
                print(yw + "Keeping your IP..." + sr)
            else:
                time.sleep(1)
                print(rd + "Unknown input please try again" + sr)

        elif cmd == "miner":
            print(gr + "Last 10 enrollments from your miner" + sr)
            miner_enroll = 1
            try:
                for i in range(1,11):
                    print(gr + sb + str(i) + Style.NORMAL + minehistory[str(i)] + sr)
                miner_enroll = 0
            except:
                print(yw + "Please wait for 10 seconds, miner is connecting to the mining pool transaction history..." + sr)
                miner_enroll = 0
        elif cmd == "news":
            print(gr + "Latest cyber security news:" + sr)
            news_show = 1
            try:
                for i in range(1,11):
                    current_news = news[str(i)]
                    print(gr + sb + current_news["time"] + Style.NORMAL + current_news["accident"] + sr)
                news_show = 0
            except Exception as e:
                print(yw + "Please wait for " + str(int(accident_n * 5)) + " seconds, news service is initializing..." + sr)
                news_show = 0
            news_show = 0
        elif cmd == "version":
            showVoc(about, None, None, gr)
        elif cmd == "debug_info":
            showVoc(debug_info, None, None, Fore.MAGENTA)
        elif cmd == "scan_target":
            target = {}
            while True:
                if target == {}:
                    print(rd + sb + "Tutorial:\nSelect an IP from your previous scan results\nType exit to stop the dHackOS Scanner !" + gr)
                    target_ip = str(input("Please enter the target IP: "))
                    if target_ip == "exit":
                        print("Stopping the dHackOS Scanner..." + sr)
                        time.sleep(1)
                        break
                    else:
                        try:
                            target = targets[target_ip]
                        except:
                            print(rd + "Wrong IP entered !" + sr)
                            break
                    print("Scanning process is started !\nPlease wait...")
                else:
                    print(gr + "Scanning target..." + wt)
                    for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                    showVoc(target, target_desc, None, gr)
                    break
        elif cmd == "miner_shop":
            print(" \n" + wt + Back.GREEN + "dHackOS Miner CLI v.0.9-r.3" + sr)
            print(gr + "-=-=-=-=-=-=-=-=-=-=-" + sb)
            while True:
                print("Please choose what you want to upgrade or type exit\nPrint all to upgrade all simultaneously")
                minecp = input("What we're going to upgrade today?: " + sr).lower()
                try:
                    if minecp != "all" and minecp != "exit":
                        miner[minecp] = ((miner[minecp] + 1) - 1)
                except Exception as e:
                    print(rd + "Nothing was found or unknown input !\n" + str(e) + gr)
                    continue
                if minecp != "exit":
                    while True:
                        try:
                            cost = float(0)
                            if minecp == "all":
                                for minecomp in miner:
                                    if miner[minecomp] < 10:
                                        #cost += float(pi * (float(miner_cost[str(miner[minecomp])]) + 1))
                                        cost += float(pi * (float(miner[minecomp]) + 1))
                                    else:
                                        print(rd + "Max level reached for:\n%s" % miner_components[minecomp + str(miner[minecomp])] + gr)
                            else:
                                #cost += float(pi * (float(miner_cost[str(miner[minecp])]) + 1))
                                cost += float(pi * (float(miner[minecp]) + 1))
                            print("Upgrade of " + str(minecp) + " will cost you " + str(cost) + " ETH.")
                            if input("Upgrade (Y/N): ").lower() == "y":
                                if player["ethereums"] >= cost:
                                    player["ethereums"] = float(float(player["ethereums"]) - float(cost))
                                    if minecp == "all":
                                        for minecomp in miner:
                                            if miner[minecomp] < 10:
                                                miner[minecomp] += 1
                                                print(Style.NORMAL + "New %s %s" % (miner_desc[minecomp], miner_components[minecomp + str(miner[minecomp])]) + sb)
                                            else:
                                                print(rd + "There is no available upgrades for:\n%s" % miner_components[minecomp + str(miner[minecomp])] + gr)
                                    else:
                                        miner[minecp] += 1
                                        print("New %s %s" % (miner_desc[str(minecp)], miner_components[minecp + str(miner[minecp])]))
                                    print(sr + "[" + sb + gr + "SUCCESS" + sr + "]" + gr + sb)
                                    break
                                else:
                                    print(rd + "Insufficient balance !" + gr)
                                    break
                            else:
                                print(rd + "Upgrade aborted !" + gr)
                                break
                        except Exception as e:
                            print(rd + "Component not found or unknown input !\n" + str(e) + gr)
                            break
                elif minecp == "exit":
                    print(rd + "Stopping... " + sr)
                    break
                else:
                    print(rd + "Unknown input !" + gr)
        elif cmd == "buy_miner":
            if enable_sound == "yes" or enable_sound == "y":
                bMinerSound()
            else:
                bMinerNosound()
            try:
                cost = float(0)
                for minecomp in miner:
                    #cost += float(pi * (float(miner_cost[str(miner[minecomp])]) + 1))
                    cost += float(pi * (float(miner[minecomp]) + 1) * stats["level"])
                miners = int(input(sb + gr + "How many miners you want to buy? (Numeric): " + sr))
                cost = cost * stats["ownminers"] * miners
                print(sb + yw + "It will cost you %d ETH" % cost)
                sol = str(input(sb + gr + "Buy ?(Yes/No): " + sr)).lower()
                if sol == "y" or sol == "yes":
                    if player["ethereums"] >= cost:
                        player["ethereums"] -= cost
                        stats["ownminers"] += 1 * miners
                        print(yw + "Transaction in process..." + sr + sb)
                        for i in progressbar.progressbar(range(100)): time.sleep(0.03)
                        time.sleep(1)
                        print(gr + "Success!")
                    else:
                        print(rd + "Insufficient balance !" + sr)
                else:
                    print(rd + "Aborted !" + sr)
            except:
                print(rd + "Invalid value entered !" + sr)
        elif cmd == "miner_info":
            while True:
                for minecomp in miner:
                    print(gr + "%s %s" % (miner_desc[minecomp],miner_components[minecomp + str(miner[minecomp])]))
                if miner_power_status == "on":
                    print("Temperature: %d °C\nCPU Load: %s %%" % (rnd.randint(65,75),str('{0:.2f}'.format(rnd.uniform(90,99)))) + sr)
                    break
                else:
                    print("Temperature: %d °C\nCPU Load: %s %%" % (rnd.randint(65,70), str('{0:.2f}'.format(rnd.uniform(78, 89)))) + sr)
                    break
        elif cmd == "bank":
            if enable_sound == "yes" or enable_sound == "y":
                bankSound()
            else:
                bank_nosound()
            #bank = {"balance": 0, "borrowed": 0, "deposit_rate": rnd.randint(5,9), "credit_rate": rnd.randint(9,13), "max_borrow": 300, "borrow_time": 0}
            while True:
                bcmd = str(input("BankCLI (main) > ")).lower()
                if bcmd == "help":
                    showVoc(bank_help,None,None,yw)
                elif bcmd == "info":
                    print(gr + "Your IP: %s\nBank balance: %s\nDeposit rate: %d%%/hour" % (player["ip"],str('{0:.8f}'.format(bank["balance"])),bank["deposit_rate"]) + sr)
                #elif bcmd == "borrow":
                    #while True:
                        #print(yw + "\nMax amount of ETH which you can borrow: %s ETH\nYour current ETH balance: %s ETH\nBank balance: %s ETH" % (str(str('{0:.6f}'.format(bank["max_borrow"]))),str(str('{0:.6f}'.format(player["ethereums"]))),str(str('{0:.6f}'.format(bank["balance"])))) + sr)
                        #try:
                            #borrow = float(input("How many ETH you want to borrow ?(Numeric): "))
                            #if borrow <= bank["max_borrow"] and bank["borrowed"] == 0:
                                #player["ethereums"] += borrow
                                #bank["borrowed"] += borrow
                                #print(gr + "Successful !" + sr)
                                #break
                            #elif bank["borrowed"] > 0:
                                #print(rd + "Borrow exists !\nOperation aborted !" + sr)
                            #elif borrow == "exit":
                                #break
                            #else:
                                #print(rd + "Insufficient balance !\nOperation aborted !" + sr)
                                #break
                        #except:
                            #print(rd + "Non-numeric value entered !\nOperation aborted !" + sr)
                            #break
                elif bcmd == "deposit":
                    while True:
                        print(yw + "\nYour current ETH balance: %s ETH\nBank balance: %s ETH\nType 'all' to deposit all ETH\n" % (str(str('{0:.8f}'.format(player["ethereums"]))),str(str('{0:.8f}'.format(bank["balance"])))) + sr)
                        try:
                            try:
                                deposit = input("How many ETH you want to deposit ?(Numeric): ")
                                deposit = float(deposit)
                            except:
                                if str(deposit) == "all":
                                    deposit = float(player["ethereums"])
                                else:
                                    print(rd + "Unknown input!" + sr)
                                    break
                            if deposit <= player["ethereums"]:
                                bank["balance"] += deposit
                                player["ethereums"] -= deposit
                                print(yw + "Saving your money...")
                                time.sleep(1)
                                print(gr + "Successful! " + sr + str('{0:.8f}'.format(deposit) + "ETH " + yw + "deposited.\n" + sr))
                                break
                            
                            elif deposit == "exit":
                                break
                            else:
                                print(rd + "Insufficient balance !\nDeposit aborted !" + sr)
                                break
                        except Exception as e:
                            print(rd + "Non-numeric value entered !\nOperation aborted !" + sr)
                            print(str(e))
                            break
                elif bcmd == "withdraw":
                    while True:
                        print(yw + "\nYour current ETH balance: %s ETH\nBank balance: %s ETH" % (str(str('{0:.8f}'.format(player["ethereums"]))),str(str('{0:.8f}'.format(bank["balance"])))) + sr)
                        try:
                            withdraw = float(input("How many ETH you want to withdraw ?(Numeric): "))
                            if withdraw <= bank["balance"]:
                                bank["balance"] -= withdraw
                                player["ethereums"] += withdraw
                                addInStats("eth_earned", withdraw, float)
                                print(gr + "Successful !" + sr)
                                break
                            elif withdraw == "exit":
                                break
                            else:
                                print(rd + "Insufficient balance !\nWithdraw aborted !" + sr)
                                break
                        except:
                            print(rd + "Non-numeric value entered !\nOperation aborted !" + sr)
                            break
                elif bcmd == "exit":
                    print(rd + "Closing DarkNet Bank CLI..." + sr)
                    break
                else:
                    print(rd + "Unknown input !" + sr)
        elif cmd == "hilo_game":
            print(gr + sb + "Welcome to High/Low Bet Game !")
            while True:
                hilo = str(input("HiLo CLI (main) > ")).lower()
                if hilo == "help":
                    print(yw + "help - list HiLo Game commands\nbet - do bet\nexit - Exit from HiLo Game" + gr)
                elif hilo == "bet":
                    try:
                        print("Your balance: %s" % str('{0:.6f}'.format(player["ethereums"])))
                        bet = float(input("How many ETH you want to bet ?(Numeric): "))
                        if bet > player["ethereums"]:
                            print(rd + "Insufficient balance !" + gr)
                            continue
                        player["ethereums"] -= bet
                        bet_event = str(input("Next number will be lower or higher than 50 ?(lo/hi): ")).lower()
                        if bet_event == "hi" or bet_event == "lo" and bet >= 0:
                            while True:
                                num = rnd.randint(0,100)
                                if num != 50:
                                    break
                            print("Number is: %d" % num)
                            status = (num > 50)
                            if bet_event == "lo" and status == False:
                                player["ethereums"] += bet * 2
                                print("You won %s ETH !" % str(bet * 2))
                                addInStats("eth_earned", (bet * 2), float)
                            elif bet_event == "hi" and status == True:
                                player["ethereums"] += bet * 2
                                print("You won %s ETH !" % str(bet * 2))
                                addInStats("eth_earned", (bet * 2), float)
                            else:
                                print(rd + "You lose !" + gr)
                        else:
                            print(rd + "Unknown input !" + gr)
                    except:
                        print(rd + "Non-numeric ETH value entered !" + gr)
                        continue
                elif hilo == "exit":
                    print(rd + "Closing the HiLo Game... " + sr)
                    break
                else:
                    print(rd + "Unknown input !" + gr)
        elif cmd == "lanhunt":
            player["ethereums"] += lanhunt.mainLanHuntCLI()
        elif cmd == "debug":
            f = open("variables_dbg_out.txt", "w")
            f.write(str("\n=========LOCALS=========\n" + str(locals()) + "\n" + "=========GLOBALS=========\n" + str(globals()) + "\n" + "=========DIR=========\n" + str(dir())))
            f.close()
        elif cmd == "miner_stat":
            time.sleep(1)
            if miner_power_status == "on":
                print(sr + yw + "Miner status: " + sb + gr + str(miner_power_status) + sr)
            else:
                print(sr + yw + "Miner status: " + sb + rd + str(miner_power_status))
        elif cmd == "miner_cfg":
            cfgcfg = str(input("Miner (on/off): ")).lower()
            if cfgcfg == "off":
                miner_power_status = "off"
            elif cfgcfg == "on":
                miner_power_status = "on"
            else:
                print(rd + "Unknown input. Please try again" + sr)
        elif cmd == "clear":
            clearScreen()
            
        else:
            print(rd + "Unknown input. Please try again" + sr)
    except KeyboardInterrupt:
        time.sleep(1)
        print(rd + "\nAll programs stopped !\nTo exit from dHackOS, type shutdown !" + sr)
print(rd + "Shutting down...")
