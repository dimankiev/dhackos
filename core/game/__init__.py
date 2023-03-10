from psutil import *
import platform
import threading
from collections.abc import Callable

from . import player as _player
from core.game.modules import bank as banking


class Game:
    __threads: list[threading.Thread] = []

    player: _player.Player
    stats: _player.Stats
    bank: banking.Bank

    anti_cheat: int = 0
    load_success: int = 0
    save_info: dict

    version: str = '0.3.6b'

    # LEGACY COMPATIBILITY VARS

    is_started: int = 0
    apps: dict[str, int] = {}
    miner: dict[str, int] = {}
    miner_enroll: int = 0
    miner_history: any
    miner_power_status: str = 'on'
    targets: dict[str, dict] = {}
    ips: list[str] = []
    news: dict[str, any] = {}

    def __init__(self) -> None:
        self.player = _player.Player()
        self.stats = _player.Stats()

    def thread_add(self, func: Callable) -> None:
        thread = threading.Thread(target=func)
        thread.daemon = True
        thread.start()
        self.__threads.append(thread)

    def get_debug_info(self) -> dict:
        return {
            "Version :": str("\n  dHackOS v." + self.version),
            "OS :": str("\n  " + platform.system() + " " + platform.release()),
            "RAM :": str("\n  Total : " + '{0:.2f}'.format(
                float(virtual_memory()[0] / 1073741824)) + " GB\n  Used : " + '{0:.2f}'.format(
                float(virtual_memory()[3] / 1073741824)) + " GB\n  Free : " + '{0:.2f}'.format(
                float(virtual_memory()[1] / 1073741824)) + " GB")
        }
