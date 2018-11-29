try:
    import getpass as pwd
    import random as rnd
    import threading, progressbar, time, imp, hashlib, base64, string, datetime, platform
    from psutil import *
    from os import stat, remove
    from colorama import Fore, Back, Style, init
    from math import pi
    from typing import List, Union
except Exception as e:
    print("\nPlease, use the commands below to install required modules: ")
    print("""
 pip install "module name that printed below"
 Example: pip install progressbar2
 """)
    print(str(e))
    exit()
sr = Style.RESET_ALL
init()
version = "0.2.4b"
print(Fore.GREEN + "Welcome to dHackOS Boot Interface !")
print("Initializing dimankiev's Hack OS...")
print(Fore.YELLOW + "Loading configuration...")
companies = ["LG", "Samsung", "Lenovo", "Sony", "nVidia", "FBI", "CIA", "Valve", "Facebook", "Google",
             "Introversion Software", "Tesla Motors", "aaa114-project", "Microsoft", "SoloLearn Inc.", "Pharma",
             "Nestle", "Unknown", "Doogee", "Ethereum", "Ethereum", "Intel", "AMD", "ASIC", "Telegram", "LinkedIn",
             "Instagram", "DEFCON", "SCP", "HackNet", "Python", "Google Project Fi", "DDoS Booter Ltd.", "Valve", "Steam", "ST corp.", "dHackOS"]
bank_help = {
    "help": " - list available commands",
    "borrow": " - borrow allowed amount of ETH",
    "deposit": " - deposit ETH to bank balance",
    "withdraw": " - withdraw ETH from bank balance",
    "info": " - show your bank account info",
    "exit": " - close the bank CLI"
}
about = {
    "dHackOS v.": version,
    "Author :": "dimankiev",
    "Idea :": "dimankiev",
    "Code :": "dimankiev",
    "Game mechanics :": "dimankiev",
    "Website :": "http://aaa114-project.tk",
    "E-Mail :": "dimankiev@gmail.com",
    "Secret Alpha testing :": "TapTrue (https://t.me/tapTrue)",
    "Pre-release beta testing :": "LINKI (https://t.me/LINKICoder)",
    "Telegram group :": "https://t.me/dhackos",
    "GitHub :": "https://github.com/dimankiev/dhackos"
}
debug_info = {
    "Version :": str("\n  dHackOS v." + version),
    "OS :": str("\n  " + platform.system() + " " + platform.release()),
    "RAM :": str("\n  Total : " + '{0:.2f}'.format(float(virtual_memory()[0] / 1073741824)) + " GB\n  Used : " + '{0:.2f}'.format(float(virtual_memory()[3] / 1073741824)) + " GB\n  Free : " + '{0:.2f}'.format(float(virtual_memory()[1] / 1073741824)) + " GB")
}
cmds = {
    "apps": " - list of installed apps + levels",
    "help": " - list of console commands",
    "shutdown": " - shutdown dHackOS",
    "scan": " - scan subnet and search for vulnerable servers",
    "scan_target": " - scan an IP and gather information about target server",
    "balance": " - opens Ethereum wallet where you can see your Ethereum balance",
    "load_list": " - shows you targets list",
    "dhackosf": " - start the dHackOS exploitation framework",
    "upgrade": " - launch dHackOS programs upgrade CLI",
    "stats": " - shows your stats",
    "change_ip_v": " - move from IPv4 (old IP version) to IPv6 (new IP version) (Can't be undone)",
    "version": " - version of dHackOS",
    "update_ip": " - replacing your ip with new one",
    "miner": " - show last 10 mined blocks (short log)",
    "rescan_subnet": " - rescans subnet to find new targets",
    "news": " - show latest cyber security news",
    "debug_info": " - shows you debug information",
    "miner_info": " - shows you your miner components",
    "buy_miner": " - buy one more miner",
    "bank": " - alpha pre-release (not finished yet)"
}
dhackosf_cmds = {
    "help": " - dhackosf cmd list",
    "load_modules": " - load dHackOSf modules",
    "scan": " - scan current target",
    "connect": " - establish the connection with a target",
    "bypass": " - start firewall bypassing process",
    "bruteforce": " - bruteforce the hash",
    "get_hash": " - get root password hash",
    "shell": " - initialize a shell on a target system",
    "exit": " - exit from dhackosf"
}
stats_desc = {
    "eth_earned": "Ethereums earned: ",
    "shacked": "Servers hacked: ",
    "xp": "Experience earned: ",
    "rep": "Reputation earned: ",
    "scans": "Scans done: ",
    "level": "Your level: ",
    "symbols": "Symbols typed (when calling commands): ",
    "launches": "How many times dHackOS launched: ",
    "miners": "Miners injected into target servers: ",
    "proxy": "Servers in your proxy chain: ",
    "ownminers": "Your own miners: "
}
miner_desc = {
    "cpu": "CPU:",
    "ram": "RAM:",
    "gpu": "GPU:",
    "software": "Miner v."
}
miner_components = {
    "cpu1": "Intel Pentium IV",
    "cpu2": "Intel Pentium Gold G5500",
    "cpu3": "Intel Core 2 Duo E6600",
    "cpu4": "Intel Core i3-2100",
    "cpu5": "Intel Core i3-2130",
    "cpu6": "Intel Core i5-2500K",
    "cpu7": "Intel Core i7-8705G",
    "cpu8": "Intel Core i7-9700K",
    "cpu9": "Intel Core i9-9900K",
    "cpu10": "Intel Xeon Platinum 8180",
    "gpu1": "nVidia Quadro FX 330",
    "gpu2": "nVidia Quadro FX 1700",
    "gpu3": "nVidia Quadro FX 5800",
    "gpu4": "nVidia GTX 480",
    "gpu5": "nVidia GTX 660 Ti",
    "gpu6": "nVidia GTX 780 Ti",
    "gpu7": "nVidia GTX 950",
    "gpu8": "nVidia GTX 980 Ti",
    "gpu9": "nVidia GTX 1080 Ti",
    "gpu10": "nVidia RTX 2080 Ti",
    "ram1": "Avant 1024 Mb",
    "ram2": "Avant 2GB",
    "ram3": "Kingston DDR4 4GB",
    "ram4": "Kingston DDR4 8GB",
    "ram5": "Corsair DDR4 8GB 2.4Ghz",
    "ram6": "Corsair DDR4 2x8GB",
    "ram7": "Corsair DDR4 16GB",
    "ram8": "Corsair 2x16GB",
    "ram9": "Corsair 32 GB",
    "ram10": "Samsung DDR4 128GB",
    "software1": "1.1",
    "software2": "1.2",
    "software3": "1.3",
    "software4": "2.0",
    "software5": "2.0.5",
    "software6": "2.1.2",
    "software7": "3.0.1",
    "software8": "3.2",
    "software9": "3.5",
    "software10": "4.0b"
}
tcmds = {
    "Employee OS v.8.1 Pro - ": "Commands List: ",
    "wallet": " - personal employee wallet CLI",
    "developer_mode": " - not accessible for you command (don't use it)",
    "exit": " - exit from console",
    "inject": " - [dHackOSf] #INJECT_MINER (dhackosf injected command)",
    "proxy": " - [dHackOSf] #INJECT_PROXY (dhackosf injected command)",
    "Your apps for work": " - are available on your desktop !"
}
target_desc = {
    "ip": "IP address:", "firewall": "Firewall:", "ethereums": "Ethereum balance:", "company": "Company:",
    "port": "Port:", "service": "Service:", "k": "Server ID: ", "miner_injected": "Miner injected (1 - Yes|0 - No): ", "dev": "Is agent: ", "xp": "XP: ", "ipv6": "Encrypted: ", "password": "dHackNET ID: ", "proxy": "In proxy chain: "
}


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
    global success_sload
    try:
        f = open(filename)
        global data
        data = imp.load_source('data', '', f)
        f.close()
        success_sload = 1
    except:
        success_sload = 0


def loadGame(username):
    global player, apps, stats, success_load, minehistory, targets, ips, miner, bank
    success_load = 0
    try:
        getVarFromFile(str(username) + ".bin")
        player = data.player
        apps = data.apps
        stats = data.stats
        minehistory = data.minehistory
        targets = data.targets
        ips = data.ips
        miner = data.miner
        bank = data.bank
        saveinfo = data.saveinfo
        if saveinfo["version"] != version:
            compatibility = data.incopatible_version
        print(Fore.GREEN + Style.BRIGHT + "Welcome " + player["username"] + "!" + sr)
        if md5(pwd.getpass("Please enter your password: "), "dhackos") != player["password"]:
            print(Fore.RED + "The password is wrong !\n" + sr)
            success_load = 0
        else:
            addInStats("launches", 1, int)
            off_earn_k = time.time() - saveinfo["timestamp"]
            miner_power = float((rnd.uniform(0.0000001, 0.0005) * rnd.randint(25,100)) * miner["cpu"] * miner["gpu"] * miner["ram"] * miner["software"] * 20000)
            mined = float(rnd.uniform(0.0000000001, 0.00000005) * stats["miners"] * (stats["ownminers"] ** 3) + rnd.uniform(0.0000000001, 0.00000005 * miner["software"]) * miner_power * (miner_power / 20000))
            player["ethereums"] += mined * off_earn_k
            print(Fore.MAGENTA + Style.BRIGHT + "Offline earnings: %s ETH" % str('{0:.10f}'.format(float(mined * off_earn_k))) + sr)
            success_load = 1
    except Exception as e:
        print(Fore.RED + "Save is missing or corrupted !\nSave version may be old\n%s" % e + sr)


def saveGame(username):
    saveinfo = {"version": str(version), "timestamp": time.time()}
    try:
        save = open(str(username) + ".bin", "w")
        save.write("player = " + str(player) + "\n" + "apps = " + str(apps) + "\n" + "stats = " + str(stats) + "\n" + "minehistory = " + str(minehistory) + "\n" + "targets = " + str(targets) + "\n" + "ips = " + str(ips) + "\n" + "miner = " + str(miner) + "\n" + "saveinfo = " + str(saveinfo) + "\n" + "bank = " + str(bank))
        save.close()
    except PermissionError:
        print("Save failed ! Please check your read/write permissions\n(If you a Linux or Android user, check chmod or try to launch this game as root)")


def newGame():
    while True:
        global player, apps, stats, minehistory, news, miner, bank
        news = {}
        player = {"ethereums": 350.0, "ip": genIP(), "dev": 0, "ipv6": 0, "xp": 0, "sentence": 0}
        player["username"] = str(input("Please enter your username: ").lower())
        player["password"] = str(pwd.getpass("Please enter your password: ").lower())
        if len(player["password"]) < 6:
            print(
                Fore.RED + "Password can't be less than 6 symbols, please choose another password\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" + sr)
        elif player["password"] != pwd.getpass("Please repeat your password: ").lower() and len(
                player["password"]) >= 6:
            print(Fore.RED + "Passwords do not match !\nPlease try again\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-" + sr)
        else:
            player["password"] = md5(player["password"], "dhackos")
            apps = {"scanner": 1, "spam": 1, "bruteforce": 1, "sdk": 1, "ipspoofing": 1, "dechyper": 1}
            stats = {"eth_earned": 0.0, "shacked": 0, "xp": 0, "rep": 0, "scans": 0, "level": 1, "symbols": 0,
                     "launches": 0, "miners": 1, "ownminers": 1, "proxy": 0}
            miner = {"cpu": 1, "gpu": 1, "ram": 1, "software": 1}
            bank = {"balance": 0, "borrowed": 0, "deposit_rate": rnd.randint(5,9), "credit_rate": rnd.randint(9,13), "max_borrow": 300, "borrow_time": 0}
            addInStats("launches", 1, int)
            genTargetsList()
            break


def bankWork():
    global bank, player
    while True:
        time.sleep(60)
        if bank["borrowed"] > 0:
            bank["borrowed"] += float((bank["borrowed"] / 100) * bank["credit_rate"])
            bank["balance"] += float((bank["balance"] / 100) * bank["deposit_rate"])
            if bank["borrowed"] >= bank["balance"] and bank["balance"] != 0:
                bank["borrowed"] -= bank["balance"]
                bank["balance"] = 0
            elif bank["borrowed"] < bank["balance"] and bank["balance"] != 0:
                bank["balance"] -= bank["borrowed"]
                bank["borrowed"] = 0
            elif bank["borrowed"] > 0 and bank["balance"] == 0 and bank["borrow_time"] != 30:
                bank["borrow_time"] += 1
                if bank["borrow_time"] > 25:
                    print(Fore.RED + "\nYou have %d mins to pay off your debts before the bank confiscates your ETH !" % (30 - bank["borrow_time"]) + sr)
            elif bank["borrow_time"] == 30 and bank["borrowed"] > 0 and player["ethereums"] > 0:
                bank["borrowed"] -= player["ethereums"]
                bank["borrowed"] -= bank["balance"]
                player["ethereums"] = 0
                bank["borrow_time"] = 0
                print(Fore.RED + "\nBank confiscated all your money !\nYour borrow is: %s ETH" % str('{0:.6f}'.format(bank["borrowed"])))
            else:
                print(Fore.RED + "\nYou have %d mins to pay off your debts before the bank confiscates your ETH !" % (30 - bank["borrow_time"]) + sr)
        else:
            bank["balance"] += float((bank["balance"] / 100) * bank["deposit_rate"])
            bank["max_borrow"] += bank["balance"] / 100

def addInStats(param, value, type):
    try:
        stats[param] = stats[param] + type(value)
    except:
        print(Fore.RED + "addInStats() function error. Please contact administrator" + sr)


def levelCheck():
    if (player["xp"] // 1000) >= 1:
        stats["level"] = stats["level"] + (player["xp"] // 1000)
        player["xp"] = 0
        award = 10 * stats["level"]
        player["ethereums"] = float(player["ethereums"] + award)
        print(Style.BRIGHT + Fore.GREEN + str(stats["level"]) + " level reached !\n You had been awarded by " + str(award) + " ETH !\n Congrats !" + sr)

def showVoc(vocabulary, description, additional, color):
    if description == None and additional == None:
        for param in vocabulary:
            print(color + Style.BRIGHT + param + Style.NORMAL + " " + str(vocabulary[param]) + sr)
    elif description == None and additional != None:
        for param in vocabulary:
            print(
                color + Style.BRIGHT + param + Style.NORMAL + " " + str(vocabulary[param]) + " " + str(additional) + sr)
    elif description != None and additional == None:
        for param in vocabulary:
            if param == "k":
                print(color + Style.BRIGHT + description[param] + Style.NORMAL + "DHACK17" + str(
                    vocabulary[param]) * 2 + sr)
            else:
                print(color + Style.BRIGHT + description[param] + Style.NORMAL + " " + str(vocabulary[param]) + sr)
    else:
        for param in vocabulary:
            print(Fore.color + Style.BRIGHT + description[param] + Style.NORMAL + " " + str(
                vocabulary[param]) + " " + str(additional) + sr)


def md5(string, salt):
    hash = str(string + salt)
    hash = hashlib.md5(hash.encode()).hexdigest()
    return hash


def genTarget(k, ip):
    target = {}
    min = (apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4
    if k == 1:
        target["firewall"] = min
    else:
        target["firewall"] = rnd.randint(min,(min + (rnd.randint(1, min)) + k))
    target = {"ip": ip,
              "ethereums": rnd.uniform((apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4,
                                      pi * float(target["firewall"]) + float(k)),
              "company": companies[rnd.randint(0, int(len(companies) - 1))], "port": rnd.randint(1, 65535), "service": "OpenSSH",
              "firewall": target["firewall"], "k": k, "miner_injected": 0, "proxy": 0}
    return target;


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
    global tracing, connection
    tracing = int((stats["proxy"] + apps["ipspoofing"]) / ((2 * stats["level"])) + rnd.randint(0,10))
    if tracing <= 13:
        #print(str(tracing) + "sec calculated") #debug_info
        tracing = 13
    while True:
        if connection == 1 and tracing != 0:
            time.sleep(1)
            tracing -= 1
        else:
            break

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
    print(Fore.RED + Style.BRIGHT + "Don't use this function if it's not necessary !")
    if input("Are you sure ?(Yes/No): ").lower() == "yes":
        print(Fore.GREEN + "Changing...")
        for i in progressbar.progressbar(range(100)): time.sleep(0.1)
        player["ipv6"] = ipv
        genTargetsList()
        if ipv == 0:
            print("Connecting to IPv4 network...")
        else:
            print("Connecting to IPv6 network...")
        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
        player["ip"] = genIP()
        bot["ip"] = genIP()
        print(".::SUCCESS::." + sr)
        print(Fore.GREEN + "Your IP: " + Style.BRIGHT + str(player["ip"]) + sr)
    else:
        print(Fore.RED + ".::ABORTED::." + sr)

def searchTargets(is_bot):
    global player_target_list, bot_target_list, bot_target
    if is_bot == 0:
        print(Fore.WHITE + Back.BLUE + Style.BRIGHT + "dHackOS Scanner v.0.5-r.4" + sr)
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
        print(Fore.GREEN + "Targets found !\nIP list:" + Style.BRIGHT)
        for i in range(0, len(player_target_list)): print(str(i) + ". " + player_target_list[int(i)])
        print(Style.NORMAL + "Please choose the IP, launch " + Style.BRIGHT + "dHackOSf" + Style.NORMAL + " and enter the IP what you choosen" + sr)
    else:
        bot_target_list = loadTargetList()
        bot_target = targets[bot_target_list[rnd.randint(0,(len(bot_target_list) - 1))]]
        return bot_target


def initGame():
    global game_started, target, gentargets, news_show, player_target_list, miner_cl, tbr, game_bot, tracing
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


def mineEthereum():
    global minehistory, minelog, mined, miner_enroll
    miner_enroll = 0
    minehistory = {"1": "", "2": "", "3": "", "4": "", "5": "", "6": "", "7": "", "8": "", "9": "", "10": ""}
    minelog = 11
    firststart = 1
    while True:
        time.sleep(1)
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
        miner_power = float((rnd.uniform(0.0000001, 0.0005) * rnd.randint(25,100)) * miner["cpu"] * miner["gpu"] * miner["ram"] * miner["software"] * collective_power)
        mined = float(rnd.uniform(0.0000000001, 0.00000005) * stats["miners"] * (stats["ownminers"] ** 3) + rnd.uniform(0.0000000001, 0.00000005 * miner["software"]) * miner_power * (miner_power / collective_power))
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


print(Fore.GREEN + ".::SUCCESS::." + sr)
while True:
    sol = input("load save or start new session ? (Save/New): ").lower()
    if sol == "sav" or sol == "save" or sol == "sv" or sol == "sve":
        print(Fore.GREEN + "[dHackOS LOGIN]" + sr)
        username = str(input("Please enter your username: ").lower())
        print("Please wait..." + Fore.GREEN + "\n.::LOADING::." + sr)
        loadGame(username)
        if success_load == 1:
            print(sr + Fore.GREEN + ".::SUCCESS::.")
            print("Your IP: " + Style.BRIGHT + player["ip"] + sr)
            initGame()
            break
        else:
            continue
    elif sol == "new" or sol == "nw" or sol == "nwe" or sol == "n":
        newGame()
        print(sr + Fore.GREEN + ".::SUCCESS::.")
        print("Your IP: " + Style.BRIGHT + str(player["ip"]) + sr)
        initGame()
        break
    else:
        print(Fore.RED + "Unknown input ! Please, try again" + sr)
sol = None
while True:
    if player["sentence"] == 3:
        player["sentence"] = rnd.randint((player["sentence"] + 1),10)
        print(Fore.RED + "You has been sentenced for " + str(player["sentence"]) + " years" + sr)
        showVoc(stats, stats_desc, None, Fore.GREEN)
        print(Fore.RED + "[GAME OVER]" + sr)
        saveGame(str(player["username"]))
        break
    elif player["sentence"] > 3:
        print(Fore.RED + "You has been sentenced for " + str(player["sentence"]) + " years" + sr)
        showVoc(stats, stats_desc, None, Fore.GREEN)
        print(Fore.RED + "[GAME OVER]" + sr)
        saveGame(str(player["username"]))
        break
    else:
        if player["dev"] == 1:
            cmd = input(player["ip"] + "@" + player["username"] + ":/dev# ").lower()
        else:
            cmd = input(player["ip"] + "@" + player["username"] + ":~# ").lower()
    levelCheck()
    addInStats("symbols", len(cmd), int)
    if cmd == "help":
        showVoc(cmds, None, None, Fore.YELLOW)
    elif cmd == "apps":
        showVoc(apps, None, "lvl", Fore.YELLOW)
    elif cmd == "balance":
        print(Style.BRIGHT + Fore.MAGENTA + Back.BLUE + "Ethereum Core v.13 CLI" + sr)
        print(Fore.BLUE + "Connecting...")
        time.sleep(1)
        print(Fore.BLUE + Style.BRIGHT + "Your balance is: " + Fore.MAGENTA + str(
            player["ethereums"]) + Fore.MAGENTA + " " + Back.BLUE + "ETH" + sr)
    elif cmd == "scan":
        searchTargets(0)
    elif cmd == "upgrade":
        print(Fore.WHITE + Back.GREEN + "dHackOS upgrade CLI v.0.9-r.3" + sr)
        showVoc(apps, None, "lvl", Fore.GREEN)
        print(Fore.GREEN + "-=-=-=-=-=-=-=-=-=-=-" + Style.BRIGHT)
        while True:
            print("Please choose the program which you want to upgrade or type exit\nPrint all to upgrade all programs simultaneously")
            program = input("What we're going to upgrade today ? ").lower()
            try:
                if program != "all" and program != "exit":
                    apps[program] = ((apps[program] + 1) - 1)
            except Exception as e:
                print(Fore.RED + "Program not found or unknown input !\n" + str(e) + Fore.GREEN)
                continue
            if program != "exit":
                while True:
                    try:
                        cost = float(0)
                        levels = int(input("How many levels do you want to upgrade (1-∞): "))
                        if levels <= 0:
                            print(Fore.RED + "This value can't be zero or be less than zero" + Fore.GREEN)
                            break
                        if program == "all":
                            cost = float(0)
                            for app in apps:
                                cost += float(pi * (float(apps[app]) + levels))
                        else:
                            cost = float(pi * (apps[program] + levels))
                        print("Upgrade of " + str(program) + " will cost you " + str(cost) + " ETH.")
                        if input("Upgrade (Y/N): ").lower() == "y":
                            if player["ethereums"] >= cost:
                                player["ethereums"] = float(float(player["ethereums"]) - float(cost))
                                if program == "all":
                                    for app in apps:
                                        apps[app] += levels
                                else:
                                    apps[program] = int(int(apps[program]) + int(levels))
                                print(".::SUCCESS::.")
                                break
                            else:
                                print(Fore.RED + "Insufficient balance !" + Fore.GREEN)
                                break
                        else:
                            print(Fore.RED + "Upgrade aborted !" + Fore.GREEN)
                            break
                    except Exception as e:
                        print(Fore.RED + "Program not found or unknown input !\n" + str(e) + Fore.GREEN)
                        break
            elif program == "exit":
                print("Stopping... " + sr)
                break
            else:
                print(Fore.RED + "Unknown input !" + Fore.GREEN)
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
                print(Fore.GREEN + "Done !")
                break
        print(Fore.CYAN + str(len(ips)) + " servers in subnet" + sr)
    elif cmd == "load_list":
        if player_target_list != []:
            print(Fore.GREEN + "IP list:" + Style.BRIGHT)
            for i in range(0,len(player_target_list)):
                print(str(i) + ". " + player_target_list[int(i)])
            print(Style.NORMAL + "Please choose the IP, launch dHackOSf and enter the IP what you choosen" + sr)
        else:
            print(Fore.RED + "There is no targets in your list ! Type scan to find one." + sr)
    elif cmd == "dhackosf":
        print(Fore.WHITE + Back.RED + Style.BRIGHT + "dHackOS Exploit Framework v.0.9-r.2" + sr)
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
                print(Fore.RED + Style.BRIGHT + "Tutorial:\nSelect an IP from your previous scan results\nType exit to stop the dHackOSf !" + Fore.GREEN)
                target_ip = str(input("Please enter the target IP: ").lower())
                if target_ip == "exit":
                    print("Stopping the dHackOSf..." + sr)
                    time.sleep(1)
                    break
                else:
                    try:
                        target = targets[target_ip]
                    except:
                        print(Fore.RED + "Wrong IP entered !" + sr)
                        break
                print("dHackOSf is initializing !\nPlease wait..." + Fore.GREEN)
                time.sleep(1)
            else:
                if scan_done == True and fw_bypassed == True and modules_loaded == True and connected == True:
                    all_done = True
                df_cmd = input("dhackosf (%s) > " % df_status).lower()
                if df_cmd == "help":
                    showVoc(dhackosf_cmds, None, None, Fore.YELLOW)
                    print(Fore.RED + "Don't forget to load dhackosf modules" + Fore.GREEN + Style.BRIGHT)
                elif df_cmd == "connect":
                    if fw_bypassed == True and scan_done == True and connected == False:
                        print(Fore.CYAN + "Connecting..." + Style.BRIGHT)
                        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                        connected = True
                        print(Fore.YELLOW + "Now you can retrieve the root hash !" + Fore.GREEN + Style.BRIGHT)
                        df_status = str(target_ip)
                    elif connected == True:
                        print(Fore.RED + "You've already connected !" + Fore.GREEN + Style.BRIGHT)
                    else:
                        print(Fore.RED + "Scan target first !\nThen bypass the firewall !\nThen connect..." + Fore.GREEN + Style.BRIGHT)
                elif df_cmd == "bypass":
                    if fw_bypassed == False and scan_done == True:
                        print(Fore.CYAN + "Bypassing firewall..." + Style.BRIGHT)
                        for i in progressbar.progressbar(range(100)): time.sleep(float((target["firewall"] / apps["ipspoofing"]) / 10))
                        fw_bypassed = True
                        print(Fore.YELLOW + "Now you can connect to the target !" + Fore.GREEN + Style.BRIGHT)
                    elif fw_bypassed == True:
                        print(Fore.RED + "Firewall is already bypassed !" + Fore.GREEN + Style.BRIGHT)
                    else:
                        print(Fore.RED + "Please scan the target first !" + Fore.GREEN + Style.BRIGHT)
                elif df_cmd == "scan":
                    if scan_done == False and modules_loaded == True:
                        print(Fore.GREEN + "Scanning target..." + Style.BRIGHT)
                        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                        showVoc(target, target_desc, None, Fore.GREEN)
                        print(Fore.YELLOW + "Now you can bypass the firewall !" + Fore.GREEN + Style.BRIGHT)
                        scan_done = True
                    elif scan_done == True:
                        print(Fore.RED + "Scan is already done !" + Fore.GREEN + Style.BRIGHT)
                    else:
                        print(Fore.RED + "Please load modules first !" + Fore.GREEN + Style.BRIGHT)
                elif df_cmd == "exit":
                    print(Fore.RED + "Exiting..." + sr)
                    break
                elif df_cmd == "load_modules":
                    if modules_loaded == False:
                        print(Fore.RED + "Loading dHackOSf modules..." + Style.BRIGHT)
                        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                        showVoc(apps, None, "[OK]", Fore.RED)
                        modules_loaded = True
                        print(Fore.YELLOW + "Now you can start the scan" + Fore.GREEN + Style.BRIGHT)
                    else:
                        print(Fore.RED + "Modules is already loaded !" + Fore.GREEN + Style.BRIGHT)
                elif df_cmd == "get_hash":
                    if hash_got == False and all_done == True:
                        print(Fore.CYAN + "Retrieving root hash..." + Fore.GREEN + Style.BRIGHT)
                        for i in progressbar.progressbar(range(100)): time.sleep(float((target["firewall"] / apps["sdk"]) / 10))
                        hash_got = str(md5(target["ip"], str(rnd.randint(0, 10000))))
                        print(Fore.GREEN + "Success !\nHash: " + Style.BRIGHT + hash_got)
                        print(Fore.YELLOW + "Now you can start bruteforce process !" + Fore.GREEN + Style.BRIGHT)
                    elif hash_got != False:
                        print(Fore.RED + "Hash has been already retrieved !" + Fore.GREEN + Style.BRIGHT)
                    else:
                        print(Fore.RED + "Please load modules first !\nThen scan target\nThen bypass the firewall\nThen - connect and get the hash" + Fore.GREEN + Style.BRIGHT)
                elif df_cmd == "bruteforce":
                    if all_done == True and hash_got != False and hash_got != True:
                        print("Bruteforcing..." + Style.BRIGHT)
                        for i in progressbar.progressbar(range(100)): time.sleep(float(((pi + target["firewall"]) / apps["bruteforce"]) / 10))
                        hack_chance = (apps["bruteforce"] + apps["sdk"] + apps["ipspoofing"] + apps["dechyper"]) // 4
                        fw_vs_player = target["firewall"] - hack_chance
                        hack_done = True
                        hash_got = True
                        print(Fore.YELLOW + "Now you can initialize shell on target server !" + Fore.GREEN + Style.BRIGHT)
                    elif hash_got == False:
                        print(Fore.RED + "Please, get the hash first !" + Fore.GREEN + Style.BRIGHT)
                    else:
                        print(Fore.RED + "Hash is already bruteforced !" + Fore.GREEN + Style.BRIGHT)
                elif df_cmd == "shell" and hack_done == True:  
                    if hack_chance >= fw_vs_player and hack_done == True:
                        print(Style.BRIGHT + "Successful !")
                        print("Root access granted !")
                        xp = rnd.randint(0, 200)
                        addInStats("xp", xp, int)
                        player["xp"] = player["xp"] + xp
                        connection = 1
                        trace = threading.Thread(target=traceStart) #target balance reset
                        trace.daemon = True
                        trace.start()
                        print(Fore.YELLOW + "You have " + str(tracing) + "sec before local admin trace you ! (Connection will be lost and ETHs seized by FBI)" + Fore.GREEN)
                        while True:
                            tcmd = input(target["ip"] + "@root:/# ").lower()
                            if tracing == 0 or tracing <= 1:
                                print(Fore.RED + "Connection was refused by local administrator...\nAttempting to revive remote session...")
                                time.sleep(1)
                                player["ethereums"] = 0
                                stats["miners"] = 0
                                player["sentence"] += 1
                                addInStats("shacked", 1, int)
                                connection = 0
                                print("[dHackOSf] ERROR. FIREWALL IS BLOCKING SESSION !" + Fore.YELLOW + "\n[dHackOS Corp] Your ETHs was seized by the FBI and injected miners deleted.\nYou will be sentenced after 3 FBI warnings.\nYou have " + str(player["sentence"]) + " warnings. Be careful." + sr)
                                break
                            elif tcmd == "help":
                                print(Fore.RED + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + Fore.GREEN + Style.BRIGHT)
                                showVoc(tcmds, None, None, Fore.GREEN)
                                print(Fore.RED + Style.BRIGHT + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + Fore.GREEN + Style.BRIGHT)
                            elif tcmd == "wallet":
                                print(Fore.RED + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + Fore.GREEN + Style.BRIGHT)
                                print("Your balance is: " + str(target["ethereums"]) + " ETH" + Fore.RED)
                                print(".::dHackOSf detected an Ethereum address field::.\nWallet dechypering...")
                                for i in progressbar.progressbar(range(100)): time.sleep(float(((pi + target["firewall"]) / apps["dechyper"]) / 10))
                                print(".::dHackOSf injected code which changes all typed addresses with your for this input field. Just press enter::." + Fore.YELLOW)
                                wcmd = input("Please enter the Ethereum wallet address to send money to: ")
                                print(Fore.RED + ".::Replacing addresses::.")
                                for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                                player["ethereums"] = player["ethereums"] + target["ethereums"]
                                addInStats("eth_earned", target["ethereums"], float)
                                target["ethereums"] = 0.0
                                print(Fore.YELLOW + "Transfer successful !")
                                print("Closing wallet..." + Fore.GREEN)
                                print(Fore.RED + "-==CONSOLE USING IS NOT RECOMMENDED FOR EMPLOYEE==-" + Fore.GREEN)
                            elif tcmd == "exit":
                                print(Fore.CYAN + "Spamming...")
                                earn = pi / (100 / (apps["spam"] + apps["ipspoofing"]))
                                player["ethereums"] = player["ethereums"] + earn
                                addInStats("shacked", 1, int)
                                addInStats("eth_earned", earn, float)
                                print(Fore.GREEN + "Success. Earned from spam: " + Fore.RED + str(earn) + " " + Back.YELLOW + "ETH" + sr)
                                print(Fore.RED + "[dHackOSf] Console closed ! Disconnecting..." + sr)
                                break
                            elif tcmd == "developer_mode":
                                print(Fore.RED + "[Employee OS v.8.1 Pro] DEVELOPER MODE ACCESSED ! YOUR EMPLOYER WAS NOTICED !\nBlocking PC...\nClosing Internet connections...")
                                for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                                print("[dHackOSf] CONNECTION FAILURE !\n[dHackOSf] REMOTE CONTROL TROJAN DELETED LOGS AND SELF-DELETED" + sr)
                                break
                            elif tcmd == "inject":
                                print(Fore.RED + "dHackOSf miner injector v.0.1-r3")
                                if target["miner_injected"] == 0:
                                    for i in progressbar.progressbar(range(100)): time.sleep(0.04)
                                    stats["miners"] = stats["miners"] + 1
                                    print(Fore.GREEN + "Miner injected into kernel !")
                                    target["miner_injected"] = 1
                                else:
                                    print(Fore.RED + "Miner has been already injected into kernel !" + Fore.GREEN)
                            elif tcmd == "proxy":
                                print(Fore.CYAN + "dHackOSf proxy init v.0.1.9-r1")
                                if target["proxy"] == 0:
                                    for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                                    stats["proxy"] = stats["proxy"] + 1
                                    print(Fore.GREEN + "Proxy initialized !")
                                    target["proxy"] = 1
                                else:
                                    print(Fore.RED + "Proxy has been already initialized on this server !" + Fore.GREEN)
                            else:
                                print(Fore.RED + "Unknown input !" + Fore.GREEN)
                    else:
                        print(Fore.RED + "Bruteforce unsuccesful !")
                        hack_end = True
                    targets[target["ip"]] = target
                    print("Disconnected from " + target["ip"])
                    print("Don't forget to start scan to find new target" + sr)
                    break
                elif df_cmd == "shell" and hack_done != True:
                    print(Fore.RED + "Please bruteforce the hash first !" + Fore.GREEN)
                else:
                    print(Fore.RED + "Unknown input !" + Fore.GREEN)
    elif cmd == "shutdown":
        sol = input("Save session ?(Yes/No): ").lower()
        if sol == "yes" or sol == "ys" or sol == "y":
            print(Fore.RED + "Stopping all processes...\nShutting down...")
            saveGame(str(player["username"]))
            print(Fore.GREEN + "Bye-Bye :)" + sr)
        else:
            print(Fore.RED + "Stopping all processes...\nShutting down...\n" + Fore.GREEN + "Bye-Bye :)" + sr)
        break
    elif cmd == "dev_mode":
        print(Fore.RED + "Developers only can access this command !")
        devpass = md5(pwd.getpass("Please enter developer password: "), "")
        if devpass == "f4e7be3ed7ad0ee61fbb0d227fcc4153":
            print(Fore.GREEN + "Developer Mode Activated !")
            print(Fore.RED + "If you don't how to use dev mode, you're crazy or cheater !" + Fore.GREEN)
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
                    print(Fore.RED + ".::DATA INPUT MODE IS DEACTIVATED::." + sr)
                    player["password"] = md5(player["password"], "dhackos")
                elif dev_cmd == "set_eth":
                    player["ethereums"] = float(input("Please, enter NEW player ETH balance: "))
                elif dev_cmd == "sentenceme":
                    sentencesure = input("Are you sure ?(Yes, I am sure what will be after this action./No): ")
                    if sentencesure == "Yes, I am sure what will be after this action.":
                        player["sentenceme"] = 3
                        print(Fore.RED + "[DONE]" + Fore.GREEN)
                    else:
                        print(Fore.RED + "[ABORTED]" + Fore.GREEN)
                elif dev_cmd == "exit":
                    print(Fore.RED + "Exiting..." + sr)
                    break
                else:
                    print(Fore.RED + "Unknown input !" + Fore.GREEN)
            player["dev"] = 1
        else:
            print(Fore.RED + "Wrong dev password ! Don't try again later !" + sr)
    elif cmd == "change_ip_v":
        if player["ipv6"] == 1:
            changeIPv(0)
        else:
            changeIPv(1)
    elif cmd == "update_ip":
        print(Fore.GREEN + "Reconnecting...")
        for i in progressbar.progressbar(range(100)): time.sleep(0.02)
        player["ip"] = genIP()
        print(".::SUCCESS::." + sr)
        print(Fore.GREEN + "Your IP: " + Style.BRIGHT + str(player["ip"]) + sr)
    elif cmd == "miner":
        print(Fore.GREEN + "Last 10 enrollments from your miner" + sr)
        miner_enroll = 1
        try:
            for i in range(1,11):
                print(Fore.GREEN + Style.BRIGHT + str(i) + Style.NORMAL + minehistory[str(i)] + sr)
            miner_enroll = 0
        except:
            print(Fore.YELLOW + "Please wait for 10 seconds, miner is connecting to the mining pool transaction history..." + sr)
            miner_enroll = 0
    elif cmd == "news":
        print(Fore.GREEN + "Latest cyber security news:" + sr)
        news_show = 1
        try:
            for i in range(1,11):
                current_news = news[str(i)]
                print(Fore.GREEN + Style.BRIGHT + current_news["time"] + Style.NORMAL + current_news["accident"] + sr)
            news_show = 0
        except Exception as e:
            print(Fore.YELLOW + "Please wait for " + str(int(accident_n * 5)) + " seconds, news service is initializing..." + sr)
            news_show = 0
        news_show = 0
    elif cmd == "version":
        showVoc(about, None, None, Fore.GREEN)
    elif cmd == "debug_info":
        showVoc(debug_info, None, None, Fore.MAGENTA)
    elif cmd == "scan_target":
        target = {}
        while True:
            if target == {}:
                print(Fore.RED + Style.BRIGHT + "Tutorial:\nSelect an IP from your previous scan results\nType exit to stop the dHackOS Scanner !" + Fore.GREEN)
                target_ip = str(input("Please enter the target IP: "))
                if target_ip == "exit":
                    print("Stopping the dHackOS Scanner..." + sr)
                    time.sleep(1)
                    break
                else:
                    try:
                        target = targets[target_ip]
                    except:
                        print(Fore.RED + "Wrong IP entered !" + sr)
                        break
                print("Scanning process is started !\nPlease wait...")
            else:
                print(Fore.GREEN + "Scanning target...")
                for i in progressbar.progressbar(range(100)): time.sleep(0.02)
                showVoc(target, target_desc, None, Fore.GREEN)
                break
    elif cmd == "miner_shop":
        print(Fore.WHITE + Back.GREEN + "dHackOS Miner CLI v.0.9-r.3" + sr)
        print(Fore.GREEN + "-=-=-=-=-=-=-=-=-=-=-" + Style.BRIGHT)
        while True:
            print("Please choose what you want to upgrade or type exit\nPrint all to upgrade all simultaneously")
            minecp = input("What we're going to upgrade today ? ").lower()
            try:
                if minecp != "all" and minecp != "exit":
                    miner[minecp] = ((miner[minecp] + 1) - 1)
            except Exception as e:
                print(Fore.RED + "Nothing was found or unknown input !\n" + str(e) + Fore.GREEN)
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
                                    print(Fore.RED + "Max level reached for:\n%s" % miner_components[minecomp + str(miner[minecomp])] + Fore.GREEN)
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
                                            print(Style.NORMAL + "New %s %s" % (miner_desc[minecomp], miner_components[minecomp + str(miner[minecomp])]) + Style.BRIGHT)
                                        else:
                                            print(Fore.RED + "There is no available upgrades for:\n%s" % miner_components[minecomp + str(miner[minecomp])] + Fore.GREEN)
                                else:
                                    miner[minecp] += 1
                                    print("New %s %s" % (miner_desc[str(minecp)], miner_components[minecp + str(miner[minecp])]))
                                print(".::SUCCESS::.")
                                break
                            else:
                                print(Fore.RED + "Insufficient balance !" + Fore.GREEN)
                                break
                        else:
                            print(Fore.RED + "Upgrade aborted !" + Fore.GREEN)
                            break
                    except Exception as e:
                        print(Fore.RED + "Component not found or unknown input !\n" + str(e) + Fore.GREEN)
                        break
            elif minecp == "exit":
                print("Stopping... " + sr)
                break
            else:
                print(Fore.RED + "Unknown input !" + Fore.GREEN)
    elif cmd == "buy_miner":
        cost = float(0)
        for minecomp in miner:
            #cost += float(pi * (float(miner_cost[str(miner[minecomp])]) + 1))
            cost += float(pi * (float(miner[minecomp]) + 1) * stats["level"])
        cost = cost * stats["ownminers"]
        print(Fore.GREEN + "It will cost you %d ETH" % cost)
        sol = str(input("Buy one more miner ?(Yes/No): ")).lower()
        if sol == "y" or sol == "yes":
            if player["ethereums"] >= cost:
                player["ethereums"] -= cost
                stats["ownminers"] += 1
                print("Success !" + sr)
            else:
                print(Fore.RED + "Insufficient balance !" + sr)
        else:
            print(Fore.RED + "Aborted !" + sr)
    elif cmd == "miner_info":
    	for minecomp in miner:
    		print(Fore.GREEN + "%s %s" % (miner_desc[minecomp],miner_components[minecomp + str(miner[minecomp])]))
    	print("Temperature: %d °C\nCPU Load: %s %%" % (rnd.randint(65,75),str('{0:.2f}'.format(rnd.uniform(90,99)))) + sr)
    elif cmd == "bank":
        print(Fore.YELLOW + "Welcome to DarkNet Bank !\n" + sr)
        #bank = {"balance": 0, "borrowed": 0, "deposit_rate": rnd.randint(5,9), "credit_rate": rnd.randint(9,13), "max_borrow": 300, "borrow_time": 0}
        while True:
            bcmd = str(input("BankCLI (main) > ")).lower()
            if bcmd == "help":
                showVoc(bank_help,None,None,Fore.YELLOW)
            elif bcmd == "info":
                print(Fore.GREEN + "Your IP: %s\nBank balance: %s\nBorrowed: %s\nDeposit rate: %d%%/min\nCredit rate: %d%%/min" % (player["ip"],str('{0:.6f}'.format(bank["balance"])),str('{0:.6f}'.format(bank["borrowed"])),bank["deposit_rate"],bank["credit_rate"]) + sr)
            elif bcmd == "borrow":
                while True:
                    print(Fore.YELLOW + "\nMax amount of ETH which you can borrow: %s ETH\nYour current ETH balance: %s ETH\nBank balance: %s ETH" % (str(str('{0:.6f}'.format(bank["max_borrow"]))),str(str('{0:.6f}'.format(player["ethereums"]))),str(str('{0:.6f}'.format(bank["balance"])))) + sr)
                    try:
                        borrow = float(input("How many ETH you want to borrow ?(Numeric): "))
                        if borrow <= bank["max_borrow"] and bank["borrowed"] == 0:
                            player["ethereums"] += borrow
                            bank["borrowed"] += borrow
                            print(Fore.GREEN + "Successful !" + sr)
                            break
                        elif bank["borrowed"] > 0:
                            print(Fore.RED + "Borrow exists !\nOperation aborted !" + sr)
                        elif borrow == "exit":
                            break
                        else:
                            print(Fore.RED + "Insufficient balance !\nOperation aborted !" + sr)
                            break
                    except:
                        print(Fore.RED + "Non-numeric value entered !\nOperation aborted !" + sr)
                        break
            elif bcmd == "deposit":
                while True:
                    print(Fore.YELLOW + "\nYour current ETH balance: %s ETH\nBank balance: %s ETH" % (str(str('{0:.6f}'.format(player["ethereums"]))),str(str('{0:.6f}'.format(bank["balance"])))) + sr)
                    try:
                        deposit = float(input("How many ETH you want to deposit ?(Numeric): "))
                        if deposit <= player["ethereums"] and bank["borrowed"] == 0:
                            bank["balance"] += deposit
                            player["ethereums"] -= deposit
                            bank["max_borrow"] += float(deposit / 100)
                            print(Fore.GREEN + "Successful !" + sr)
                            break
                        elif deposit <= player["ethereums"] and bank["borrowed"] > 0:
                            bank["borrowed"] -= deposit
                            player["ethereums"] -= deposit
                            bank["max_borrow"] += float(deposit / 100)
                            print(Fore.GREEN + "Successful !\nNow your borrow is: %s ETH" % str('{0:.6f}'.format(bank["borrowed"])) + sr)
                            break
                        elif deposit == "exit":
                            break
                        else:
                            print(Fore.RED + "Insufficient balance !\nDeposit aborted !" + sr)
                            break
                    except Exception as e:
                        print(Fore.RED + "Non-numeric value entered !\nOperation aborted !" + sr)
                        print(str(e))
                        break
            elif bcmd == "withdraw":
                while True:
                    print(Fore.YELLOW + "\nYour current ETH balance: %s ETH\nBank balance: %s ETH" % (str(str('{0:.6f}'.format(player["ethereums"]))),str(str('{0:.6f}'.format(bank["balance"])))) + sr)
                    try:
                        withdraw = float(input("How many ETH you want to withdraw ?(Numeric): "))
                        if withdraw <= bank["balance"]:
                            bank["balance"] -= withdraw
                            player["ethereums"] += withdraw
                            print(Fore.GREEN + "Successful !" + sr)
                            break
                        elif withdraw == "exit":
                            break
                        else:
                            print(Fore.RED + "Insufficient balance !\nWithdraw aborted !" + sr)
                            break
                    except:
                        print(Fore.RED + "Non-numeric value entered !\nOperation aborted !" + sr)
                        break
            elif bcmd == "exit":
                print(Fore.RED + "Closing DarkNet Bank CLI..." + sr)
                break
            else:
                print(Fore.RED + "Unknown input !" + sr)
    else:
        print(Fore.RED + "Unknown input. Please try again" + sr)
print("disconnected...")