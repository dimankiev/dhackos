import enum


class Player:
    # Player username
    username: str
    # Player password md5 hashsum
    password: str
    # Player ethereum cryptocurrency balance
    ethereums: float
    # How much the player was sentenced
    sentence: int
    # Player ip
    ip: str
    # Player ipv6
    ipv6: str
    # Player experience
    xp: int
    # Player dev mode flag
    dev: int

    def __init__(self) -> None:
        pass

    def load(self, data: dict | object) -> None:
        self.username = data['username']
        self.password = data['password']
        self.ethereums = float(data['ethereums'])
        self.sentence = int(data['sentence'])
        self.ip = data['ip']
        self.ipv6 = data['ipv6']
        self.xp = int(data['xp'])
        self.dev = int(data['dev'])

    def to_dict(self) -> dict:
        return {
            'username': self.username, 'password': self.password, 'ethereums': self.ethereums,
            'sentence': self.sentence, 'ip': self.ip, 'ipv6': self.ipv6, 'xp': self.xp, 'dev': self.dev
        }


class StatsTypes(enum.IntEnum):
    eth_earned = 0
    systems_hacked = 1
    experience = 2
    reputation = 3
    level = 4
    symbols_typed = 5
    game_launches = 6
    miners_total = 7
    miners_owned_total = 8
    proxies_injected = 9
    scans_performed = 10


class Stats:
    # Stats array
    __stats: list[int | float] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self) -> None:
        pass

    @staticmethod
    def __stat_type_convert(stat: any, value: int | float):
        if not isinstance(value, type(stat)):
            raise Exception('Player stats type mismatch')
        return type(stat)(value)

    def update(self, stat_type: StatsTypes, value: None | int | float) -> None:
        if isinstance(stat_type, StatsTypes):
            if value is None:
                self.__stats[stat_type.value] = 0
            else:
                self.__stats[stat_type.value] += self.__stat_type_convert(self.__stats[stat_type.value], value)

    def get(self, stat_type: StatsTypes) -> int | float:
        return self.__stats[stat_type.value]

    def load(self, data: dict | object) -> None:
        self.__stats[StatsTypes.game_launches.value] = data['launches']
        self.__stats[StatsTypes.eth_earned.value] = data['eth_earned']
        self.__stats[StatsTypes.symbols_typed.value] = data['symbols']
        self.__stats[StatsTypes.systems_hacked.value] = data['shacked']
        self.__stats[StatsTypes.proxies_injected.value] = data['proxy']
        self.__stats[StatsTypes.level.value] = data['level']
        self.__stats[StatsTypes.miners_owned_total.value] = data['ownminers']
        self.__stats[StatsTypes.miners_total.value] = data['miners']
        self.__stats[StatsTypes.scans_performed.value] = data['scans']
        self.__stats[StatsTypes.reputation.value] = data['rep']
        self.__stats[StatsTypes.experience.value] = data['xp']

    def to_dict(self) -> dict:
        return {
            'launches': self.__stats[StatsTypes.game_launches.value],
            'eth_earned': self.__stats[StatsTypes.eth_earned.value],
            'symbols': self.__stats[StatsTypes.symbols_typed.value],
            'shacked': self.__stats[StatsTypes.systems_hacked.value],
            'proxy': self.__stats[StatsTypes.proxies_injected.value],
            'level': self.__stats[StatsTypes.level.value],
            'miners': self.__stats[StatsTypes.miners_total.value],
            'ownminers': self.__stats[StatsTypes.miners_owned_total.value],
            'scans': self.__stats[StatsTypes.scans_performed.value],
            'rep': self.__stats[StatsTypes.reputation.value],
            'xp': self.__stats[StatsTypes.experience.value]
        }
