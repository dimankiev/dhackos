import enum
import secrets
from Crypto.Hash import keccak
from coincurve import PublicKey
import datetime


class HistoryRecordType(enum.IntEnum):
    FundsAdd = 0
    FundsWithdraw = 1
    DepositAdd = 2
    DepositWithdraw = 3
    BorrowTake = 4
    BorrowReturn = 5


class HistoryRecord:
    timestamp: float
    type: HistoryRecordType
    amount: float

    def __init__(self, record_type: HistoryRecordType, amount: float, _ts_offset: float) -> None:
        self.timestamp = datetime.datetime.now().timestamp() - _ts_offset
        self.amount = amount
        self.type = record_type


class History:
    __records: list[HistoryRecord] = []
    __summary: list[float] = [float(0.0)] * len(HistoryRecordType)

    def __init__(self, data: list[float] = None) -> None:
        if data is not None and len(data) > 0:
            for index in range(0, len(data)):
                self.__summary[index] += data[index]

    def record_add(self, record_type: HistoryRecordType, amount: float, _legacy_secs_from_now: float = 0) -> None:
        self.__records.append(HistoryRecord(record_type, amount, _legacy_secs_from_now))

    def summarize(self) -> None:
        for record in self.__records:
            self.__summary[record.type.value] += record.amount
        self.__records.clear()

    def get_summary(self) -> list[float]:
        return self.__summary

    def export_data(self) -> list[tuple[str, float, float]]:
        data: list[tuple[str, float, float]] = []
        for record in self.__records:
            data.append((record.type.name, record.amount, record.timestamp))
        return data

    def import_data(self, data: list[tuple[str, float, float]]) -> None:
        for record in data:
            self.record_add(HistoryRecordType[record[0]], record[1], datetime.datetime.now().timestamp() - record[2])

    def export_summary(self) -> list[float]:
        self.summarize()
        return self.get_summary()

    def import_summary(self, data: list[float]) -> None:
        self.__summary = data


class Wallet:
    __enrolled: bool = False
    __data: list[bytes] = []
    __balance: float = 0

    def __init__(self, data: list[bytes] = None) -> None:
        if data is None or len(data) < 3:
            private_key = keccak.new(data=secrets.token_bytes(32), digest_bits=256).digest()
            public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
            address = keccak.new(data=public_key, digest_bits=256).digest()[-20:]
            self.__data = [private_key, public_key, address]
        else:
            self.__data = data

    def get_address(self) -> str:
        return '0x' + self.__data[2].hex()

    def get_balance(self) -> float:
        return self.__balance

    def set_balance(self, value: float, add=False) -> None:
        """
        Unsafe balance management function
        :param value:
        :param add:
        :return:
        """
        if add:
            self.__balance += value
        else:
            self.__balance = value

    def withdraw(self, value: float) -> bool:
        """
        Safe balance withdraw (False on insufficient balance)
        :param value: amount to be withdrawn
        :return: status of operation
        """
        # TODO: Make it dependent on target wallet
        if self.__balance >= value:
            self.__balance -= value
            return True
        else:
            return False

    def deposit(self, value: float) -> bool:
        # TODO: Make it dependent on source wallet
        self.__balance += value
        return True

    def enroll(self, safe: bool = False) -> list[bytes]:
        if self.__enrolled:
            return []
        if not safe:
            self.__enrolled = True
        return self.__data

    def is_enrolled(self) -> bool:
        return self.__enrolled


class Account:
    __borrow_limit: float = 0
    __history: History = History()
    __wallets: list[Wallet] = []
    __debt: float = 0

    def __init__(self, data: tuple[list[float], list[tuple[list[bytes], float]], float] = None):
        # Create primary wallet
        if data is not None:
            self.import_data(data)
        elif not hasattr(self, '__wallets') or self.__wallets[0] is None:
            self.__wallets.clear()
            self.__wallets.append(Wallet())

    def export_data(self) -> tuple[list[float], list[tuple[list[bytes], float]], float]:
        summary = self.__history.export_summary()
        wallets: list[tuple[list[bytes], float]] = []
        for wallet in self.__wallets:
            wallets.append((wallet.enroll(True), wallet.get_balance()))
        return summary, wallets, self.__debt

    def import_data(self, data: tuple[list[float], list[tuple[list[bytes], float]], float]) -> None:
        self.__history.import_summary(data[0])
        self.__wallets.clear()
        for wallet in data[1]:
            self.__wallets.append(Wallet(wallet[0]))
            self.__wallets[-1].set_balance(wallet[1])
        self.__debt = data[2]

    def borrowing_capacity(self) -> float:
        if self.__debt > 0:
            return 0
        self.__history.summarize()
        summary = self.__history.get_summary()
        self.__borrow_limit = (summary[HistoryRecordType.DepositAdd] + summary[HistoryRecordType.BorrowReturn]) - \
                              (summary[HistoryRecordType.FundsWithdraw] + summary[HistoryRecordType.BorrowTake]) + \
                              (summary[HistoryRecordType.FundsAdd] - summary[HistoryRecordType.FundsWithdraw])
        if self.__borrow_limit < 0:
            self.__borrow_limit = 0
        return self.__borrow_limit

    def debt_charge(self, interest: float) -> None:
        if self.__debt != 0:
            self.__debt += (self.__debt * 100) / interest

    def debt_update(self, amount: float, is_set=False):
        if is_set:
            self.__debt = amount
        else:
            self.__debt += amount

    def wallet(self, index: int) -> Wallet | None:
        if index >= len(self.__wallets):
            return None
        else:
            return self.__wallets[index]

    def history(self) -> History:
        return self.__history
