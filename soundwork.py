import os
from colorama import Fore, Style, init
import progressbar
import time
from playsound import playsound

yw = Fore.YELLOW
gr = Fore.GREEN
bl = Fore.BLUE
sr = Style.RESET_ALL
sb = Style.BRIGHT

init()

def bMiner_nosound():
    time.sleep(1)
    print(" \n" + yw + "Connecting to www.minershop.org... Connected." + sr)
    time.sleep(2)
    print(gr + " HTTP request sent, awaiting response... 200 OK")
    time.sleep(1)
    print("Lenght: 10701 (10k) [text/html]\n Saving to: 'index.html'" +sr + sb)
    time.sleep(1)
    for i in progressbar.progressbar(range(100)): time.sleep(0.03)
    time.sleep(1)
    print(sr + gr + "Saved to 'index.html'\n" + sr)
    time.sleep(1)
    print(sb + bl + "[-=-=-Miner Shop-=-=-]" + sr)

def bMinerSound():
    time.sleep(1)
    print(" \n" + yw + "Connecting to www.minershop.org... Connected." + sr)
    time.sleep(2)
    print(gr + " HTTP request sent, awaiting response... 200 OK")
    time.sleep(1)
    print("Lenght: 10701 (10k) [text/html]\n Saving to: 'index.html'" +sr + sb)
    time.sleep(1)
    playsound(os.path.join('.', 'sounds', 'connect1.mp3'), block=False)
    playsound(os.path.join('.', 'sounds', 'connect2.mp3'), block=False)
    for i in progressbar.progressbar(range(100)): time.sleep(0.03)
    time.sleep(1)
    print(sr + gr + "Saved to 'index.html'\n" + sr)
    time.sleep(1)
    print(sb + bl + "[-=-=-Miner Shop-=-=-]" + sr)

def bankSound():
    print(" \n" + yw + "Connecting to your Darknet Bank account..." + sr + sb)
    time.sleep(1)
    playsound(os.path.join('.', 'sounds', 'connect1.mp3'), block=False)
    playsound(os.path.join('.', 'sounds', 'connect2.mp3'), block=False)
    time.sleep(0.4)
    for i in progressbar.progressbar(range(100)): time.sleep(0.015)
    time.sleep(1)
    print(sr + gr + "Connected!\n" + sr)
    time.sleep(1)
    print(yw + "Welcome to DarkNet Bank!\n" + sr)

def bankNosound():
    print(" \n" + yw + "Connecting to your Darknet Bank account..." + sr + sb)
    time.sleep(1)
    for i in progressbar.progressbar(range(100)): time.sleep(0.015)
    time.sleep(1)
    print(sr + gr + "Connected!\n" + sr)
    time.sleep(1)
    print(yw + "Welcome to DarkNet Bank!\n" + sr)
