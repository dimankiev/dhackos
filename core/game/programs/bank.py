import core.game.modules.bank as banking
from core.game import player as _player
from core.game.utils import strings as _strings
from core.game.utils import printing
import time


def program_run(strings: _strings.Strings, bank: banking.Bank, player: _player.Player, stats: _player.Stats) -> None:
    while True:
        bcmd = str(input("BankCLI (main) > ")).lower()
        if bcmd == "help":
            printing.print_vocabulary(strings.get_section('bank_help'), None, None, printing.YW)
        elif bcmd == "info":
            rates = bank.get_rates()
            balance = bank.account(player.bank_acc_no).wallet(0).get_balance()
            print(printing.GR + "Your IP: %s\nBank balance: %s\nDeposit rate: %d%%/hour" % (
                player.ip, str('{0:.8f}'.format(balance)), rates[0]) + printing.SR)
        elif bcmd == "borrow":
            while True:
                borrow_capacity = bank.account(0).borrowing_capacity()
                account = bank.account(player.bank_acc_no)
                wallet = account.wallet(0)
                balance = wallet.get_balance()
                print(printing.YW + "\nMax amount of ETH which you can borrow: %s ETH\n"
                           "Your current ETH balance: %s ETH\nBank balance: %s ETH" %
                      (str(str('{0:.6f}'.format(borrow_capacity))),
                       str(str('{0:.6f}'.format(player.ethereums))),
                       str(str('{0:.6f}'.format(balance)))) + printing.SR)
                try:
                    borrow = float(input("How many ETH you want to borrow ?(Numeric, 0 to abort): "))
                    if borrow == 0:
                        print(printing.RD + "Operation aborted!" + printing.SR)
                    success = bank.borrow_take(player.bank_acc_no, borrow)
                    if success:
                        print(printing.GR + "Successful!" + printing.SR)
                    else:
                        if borrow_capacity == 0:
                            print(printing.RD + "You have debt or not you're not eligible for debt.\nOperation aborted !"
                                  + printing.SR)
                    break
                except:
                    print(printing.RD + "Operation aborted due to an error!" + printing.SR)
                    break
        elif bcmd == "deposit":
            while True:
                wallet = bank.account(player.bank_acc_no).wallet(0)
                balance = wallet.get_balance()
                print(
                    printing.YW + "\nYour current ETH balance: %s ETH\n"
                                  "Bank balance: %s ETH\nType 'all' to deposit all ETH\n" % (
                        str(str('{0:.8f}'.format(player.ethereums))),
                        str(str('{0:.8f}'.format(balance)))) + printing.SR)
                try:
                    try:
                        deposit = input("How many ETH you want to deposit ?(Numeric): ")
                        deposit = float(deposit)
                    except:
                        if str(deposit) == "all":
                            deposit = float(player.ethereums)
                        else:
                            print(printing.RD + "Unknown input!" + printing.SR)
                            break
                    if deposit <= player.ethereums:
                        wallet.deposit(deposit)
                        player.ethereums -= deposit
                        print(printing.YW + "Saving your money...")
                        time.sleep(1)
                        print(printing.GR + "Successful! " + printing.SR + str(
                            '{0:.8f}'.format(deposit) + "ETH " + printing.YW + "deposited.\n" + printing.SR))
                        break

                    elif deposit == "exit":
                        break
                    else:
                        print(printing.RD + "Insufficient balance !\nDeposit aborted !" + printing.SR)
                        break
                except Exception as e:
                    print(printing.RD + "Non-numeric value entered !\nOperation aborted !" + printing.SR)
                    print(str(e))
                    break
        elif bcmd == "withdraw":
            while True:
                wallet = bank.account(player.bank_acc_no).wallet(0)
                balance = wallet.get_balance()
                print(printing.YW + "\nYour current ETH balance: %s ETH\nBank balance: %s ETH" % (
                    str(str('{0:.8f}'.format(player.ethereums))),
                    str(str('{0:.8f}'.format(balance)))) + printing.SR)
                try:
                    withdraw = float(input("How many ETH you want to withdraw ?(Numeric): "))
                    if withdraw <= balance:
                        wallet.withdraw(withdraw)
                        player.ethereums += withdraw
                        stats.update(_player.StatsTypes.eth_earned, withdraw)
                        print(printing.GR + "Successful!" + printing.SR)
                        break
                    elif withdraw == "exit":
                        break
                    else:
                        print(printing.RD + "Insufficient balance!\nWithdraw aborted!" + printing.SR)
                        break
                except:
                    print(printing.RD + "Non-numeric value entered!\nOperation aborted!" + printing.SR)
                    break
        elif bcmd == "exit":
            print(printing.RD + "Closing DarkNet Bank CLI..." + printing.SR)
            break
        else:
            print(printing.RD + "Unknown input !" + printing.SR)