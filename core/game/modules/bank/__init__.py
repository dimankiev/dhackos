import random as _rnd

from . import accounting


class Bank:
    __cold_wallet: accounting.Wallet
    __accounts: list[accounting.Account] = []
    # [0] - deposit rate, [1] - borrow rate
    __rates: list[float]

    def __init__(self, data: dict | list[tuple[list[float], list[tuple[list[bytes], float]], float]] = None) -> None:
        self.__rates = [round(_rnd.uniform(5.01, 8.99), 2), round(_rnd.uniform(9.01, 12.99), 2)]
        if not hasattr(self, '__cold_wallet'):
            self.__cold_wallet = accounting.Wallet()
            self.__cold_wallet.set_balance(1000000)
        if data is dict:
            self.__accounts.append(accounting.Account())
            self.load_bank_data_legacy(data)
        elif data is not None:
            self.accounts_load(data)
        else:
            self.__accounts.append(accounting.Account())

    def get_rates(self) -> list[float]:
        return self.__rates

    def load_bank_data_legacy(self, data: dict) -> None:
        if self.__accounts[0] is not None and isinstance(self.__accounts[0], accounting.Account):
            self.__accounts[0].wallet(0).set_balance(data['balance'])
            if data.get('borrowed') is not None and data.get('borrowed') > 0:
                self.__accounts[0].history().record_add(
                    accounting.HistoryRecordType.BorrowTake, data['borrowed'], data['borrow_time']
                )

    def accounts_load(self, accounts: list[tuple[list[float], list[tuple[list[bytes], float]], float]]) -> None:
        self.__accounts.clear()
        for account in accounts:
            self.__accounts.append(accounting.Account(account))

    def accounts_export(self) -> list[tuple[list[float], list[tuple[list[bytes], float]], float]]:
        data: list[tuple[list[float], list[tuple[list[bytes], float]], float]] = []
        for account in self.__accounts:
            data.append(account.export_data())
        return data

    def remove_account(self, acc_no: int) -> None:
        eth_to_move = self.__accounts[acc_no].wallet(0).get_balance()
        self.__cold_wallet.set_balance(eth_to_move, True)
        self.__accounts.pop(acc_no)

    def account(self, acc_no: int) -> accounting.Account:
        return self.__accounts[acc_no]

    def borrow_take(self, acc_no: int, amount: float) -> bool:
        account = self.__accounts[acc_no]
        capacity = account.borrowing_capacity()
        if capacity == 0:
            return False
        if amount > capacity:
            return False
        account.wallet(0).set_balance(amount, True)
        account.history().record_add(accounting.HistoryRecordType.BorrowTake, amount)
        account.debt_update(amount, True)
        return True

    def borrow_return(self, acc_no: int, amount: float) -> bool:
        account = self.__accounts[acc_no]
        if amount < 0:
            return False
        if account.wallet(0).get_balance() < amount:
            return False
        account.wallet(0).set_balance(0 - amount, True)
        account.history().record_add(accounting.HistoryRecordType.BorrowReturn, amount)
        account.debt_update(0 - amount)
        return True

    def perform_lifecycle(self) -> None:
        for account in self.__accounts:
            balance = account.wallet(0).get_balance()
            account.wallet(0).set_balance((balance / 100) * self.__rates[0], True)
            account.debt_charge(self.__rates[1])
