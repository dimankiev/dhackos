import getpass as pwd
import random as rnd
import threading, progressbar, time, shelve, hashlib, base64, string, datetime, platform, math
from psutil import *
from os import stat, remove
import os
from colorama import Fore, Back, Style, init
from math import pi
from typing import List, Union
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style as pStyle
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
sr = Style.RESET_ALL
init()
class lanhunt:


    lh_cmd_list = {
        "0": "help - show available commands",
        "1": "fly - initiate drone lan searching in a flight",
        "2": "search - search a vulnerable devices",
        "3": "show_targets - shows you the target list",
        "4": "hack - initiate vulnerable devices hack",
        "5": "exit - stop all processes, transfer stolen ETH and fly home",
        "6": "--Drone status is not freezing, it's updating--"
    }


    def initDrone():
        global drone_power, drone_battery, drone_main
        game_power = 0
        if game_power == 0:
            game_power = 1
            drone_battery = threading.Thread(target=lanhunt.droneBattery)
            drone_battery.daemon = True
            drone_battery.start()
            drone_main = threading.Thread(target=lanhunt.mainDrone)
            drone_main.daemon = True
            drone_main.start()


    def md5str(string, salt):
        hash = str(str(string) + str(salt))
        hash = hashlib.md5(hash.encode()).hexdigest()
        return hash


    def bottom_toolbar():
        return [('class:bottom-toolbar', str(lanhunt.getDroneStatus(drone_task)))]


    def initLanHuntCLI():
        global lh_msg, lh_style
        lh_style = pStyle.from_dict({
        # User input (default text).
        '':          '#c635f9',

        # Prompt.
        'username': 'ansiblue',
        'at':       'ansicyan',
        'colon':    '#ffffff',
        'pound':    '#ffffff',
        'host':     'ansiblue', # bg:#444400
        'path':     'ansicyan underline',
        'bottom-toolbar': 'ansiblue bg:#ffffff'
        })
        lh_msg = [
            ('class:username', "lanhunt"),
            ('class:at',       '@'),
            ('class:host',     "drone"),
            ('class:colon',    ':'),
            ('class:path',     '~'),
            ('class:pound',    '# '),

        ]


    def droneBattery():
        global battery
        battery = 100
        while True:
            time.sleep(60)
            if battery != 10:
                battery -= 1
            else:
                break


    def mainDrone():
        global drone_task, balance, drone_list
        drone_task = "idle"
        while True:
            #print(str(drone_task))
            #try:
            if drone_task == "fly" and battery > 10:
                time.sleep(15)
                drone_list = "flied"
                drone_task = "idle"
            elif drone_task == "search" and battery > 10:
                time.sleep(10)
                drone_list = {"0": {"hostname": "Main Router", "ip": "192.168.0.1", "os": "Linux 2.6.36", "wallet": "N/A"}}
                for i in range(1,rnd.randint(2,10)):
                    drone_list[str(i)] = {"hostname": str("android-" + str(lanhunt.md5str(str(rnd.randint(1,1000000)),str(rnd.randint(1,1000000))))[:-22]), "ip": "192.168.0." + str(i), "os": "Android 4." + str(rnd.randint(0,4)), "wallet": float('{0:.6f}'.format(rnd.uniform(0,balance + 10)))}
                drone_task = "idle"
            elif drone_task == "hack" and battery > 10:
                time.sleep(5 * (len(drone_list) - 1))
                for i in range(1,(len(drone_list)-1)):
                    #print(str(drone_list))
                    #print(str(drone_list[str(i)]["wallet"]))
                    #print(str(drone_list[str(i)]))
                    balance += float(drone_list[str(i)]["wallet"])
                    drone_list[str(i)]["wallet"] = 0
                    i += 1
                drone_task = "idle"
            elif drone_task == "exit":
                drone_task = "idle"
                break
            else:
                time.sleep(1)
                    #drone_task = "idle"
            #except Exception as e:
            #    print(str(e))
        return balance


    def getDroneStatus(drone_task):
        if drone_task == "fly":
            return str("[LanHuntDrone]: Looking for a lan...")
        elif drone_task == "search":
            return str("[LanHuntDrone]: Searching a targets...")
        elif drone_task == "hack":
            return str("[LanHuntDrone]: Hacking the targets...")
        elif drone_task == "exit":
            return str("[LanHuntDrone]: Fly home...")
        elif drone_task == "idle":
            return str("[LanHuntDrone]: %s" % str('{0:.6f}'.format(balance)) + " ETH")
        else:
            return str("[LanHuntDrone]: %s" % str('{0:.6f}'.format(balance)) + " ETH")


    def mainLanHuntCLI():
        global balance, drone_task, drone_list
        balance = 0.0
        drone_list = False
        drone_task = "idle"
        lanhunt.initLanHuntCLI()
        lanhunt.initDrone()
        lanHuntCLI = PromptSession()
        while True:
            if battery > 10:
                lh_cmd = str(lanHuntCLI.prompt(lh_msg, bottom_toolbar=lanhunt.bottom_toolbar, refresh_interval=0.5, style=lh_style, auto_suggest=AutoSuggestFromHistory())).lower()
            else:
                print(Fore.YELLOW + "[LanHuntDroneGuard] Battery is low ! Drone is fly home...")
                lh_cmd = "exit"
            if len(lh_cmd) > 16:
                lh_cmd = lh_cmd[:-(len(lh_cmd) - 16)]
            if lh_cmd == "":
                continue
            elif lh_cmd == "exit":
                print(Fore.YELLOW + "All ETH is transfered to your main wallet. " + str(balance) + "ETH Transfered to your wallet." + sr)
                print(Fore.RED + "Closing connections...\nExiting..." + sr)
                drone_task = "exit"
                break
            elif lh_cmd == "help":
                for i in range(0,len(lanhunt.lh_cmd_list)):
                    print(Fore.YELLOW + lanhunt.lh_cmd_list[str(i)] + sr)
                    i += 1
            elif lh_cmd == "fly":
                try:
                    if drone_list == False and drone_list != "flied":
                        drone_task = "fly"
                    elif drone_list == False and drone_list == "flied":
                        print(Fore.RED + "\nDrone is already flied !\nPlease, perform a search to find the targets." + sr)
                except Exception as e:
                    print(Fore.RED + "\nDrone is already flied !\nPlease, perform a search to find the targets.\n%s" % str(e) + sr)
            elif lh_cmd == "hack":
                try:
                    if drone_list and drone_list != "flied":
                        drone_task = "hack"
                    else:
                        print(Fore.RED + "\nTarget list is empty !\nPlease, perform a search to find the targets." + sr)
                except Exception as e:
                    print(Fore.RED + "\nTarget list is empty !\nPlease, perform a search to find the targets.\n%s" % str(e) + sr)
            elif lh_cmd == "search":
                try:
                    if drone_list and drone_list != "flied":
                        print(Fore.RED + "\nTarget list is already exists !\nPlease, perform a hack to get their ETH." + sr)
                    else:
                        drone_task = "search"
                except Exception as e:
                    drone_task = "search"
                    print("%s\n%s" % str(e))
            elif lh_cmd == "show_targets":
                try:
                    if drone_list and drone_list != "flied":
                        for i in range(0,len(drone_list)):
                            print(Style.NORMAL + Fore.GREEN + "[Target: %d]" % i)
                            for param in drone_list[str(i)]:
                                print(Style.BRIGHT + str(param) + ": " + str(drone_list[str(i)][str(param)]))
                    else:
                        print(Fore.RED + "\nTarget list is empty !\nPlease, perform a search to find the targets." + sr)
                except Exception as e:
                    print(Fore.RED + "\nTarget list is empty !\nPlease, perform a search to find the targets.\n%s" % str(e) + sr)
            elif lh_cmd == "balance":
                print(Fore.BLUE + "Drone balance is: %s ETH" % str(balance))
            else:
                print(Fore.RED + "Command %s is not found !" % lh_cmd + sr)
        return balance
