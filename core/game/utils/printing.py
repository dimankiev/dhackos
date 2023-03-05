from colorama import Style, Fore

SR = Style.RESET_ALL
SB = Style.BRIGHT
GR = Fore.GREEN
YW = Fore.YELLOW
RD = Fore.RED
BL = Fore.BLUE
WT = Fore.WHITE


def print_vocabulary(vocabulary, description, additional, color):
    if description is None and additional is None:
        for param in vocabulary:
            print(color + SB + param + Style.NORMAL + " " + str(vocabulary[param]) + SR)
    elif description is None and additional is not None:
        for param in vocabulary:
            print(
                color + SB + param + Style.NORMAL + " " + str(vocabulary[param]) + " " + str(additional) + SR)
    elif description is not None and additional is None:
        for param in vocabulary:
            if param == "k":
                print(color + SB + description[param] + Style.NORMAL + "DHACK33" + str(
                    vocabulary[param]) * 2 + SR)
            elif param == "eth_earned":
                print(color + SB + description[param] + Style.NORMAL + " " + str(
                    '{0:.8f}'.format(vocabulary[param])) + SR)
            else:
                print(color + SB + description[param] + Style.NORMAL + " " + str(vocabulary[param]) + SR)
    else:
        for param in vocabulary:
            print(Fore.color + SB + description[param] + Style.NORMAL + " " + str(
                vocabulary[param]) + " " + str(additional) + SR)
