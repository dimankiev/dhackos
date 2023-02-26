try:
    import json
    import os

except Exception as e:
    print("\nPlease, use the commands below to install required modules: ")
    print("""
 pip install "module name that printed below"
 Example: pip install progressbar2
 """)
    print(str(e))
    exit()


class Strings:
    def __init__(self) -> None:
        self.__strings: dict[str, dict] = {}
        # TODO: Load strings without specifying the path for each file (dir enum)
        self.__strings_to_load = [
            ('bank_help', 'assets/strings/commands/bank.json'),
            ('about', 'assets/strings/about_info.json'),
            ('cmds', 'assets/strings/commands/system.json'),
            ('dhackosf_cmds', 'assets/strings/commands/dhackosf.json'),
            ('stats_desc', 'assets/strings/stats.json'),
            ('miner_desc', 'assets/strings/miner/minerdesc.json'),
            ('miner_components', 'assets/strings/miner/components.json'),
            ('tcmds', 'assets/strings/targets/t_commands.json'),
            ('target_desc', 'assets/strings/targets/targetdesc.json'),
        ]
        for strings_metadata in self.__strings_to_load:
            self.__load(strings_metadata[0], strings_metadata[1])

    def __load(self, section: str, path_to_strings: str):
        with open(os.path.join(*path_to_strings.split('/'))) as file:
            content = file.read()
            parsed = json.loads(content)
            self.__strings[section] = {}
            self.__strings[section].update(parsed)

    def get(self, section: str, key: str) -> str:
        return self.__strings.get(section).get(key)

    def get_section(self, section: str) -> dict:
        return self.__strings.get(section)


companies = ["BG", "Namlung", "Benovo", "Rony", "nSidia", "FBI", "CIA", "Calve", "Babebook", "Foogle",
             "Introversion Software", "Memla Rotors", "aaa114-project", "Fibrosoft", "MotoLearn Inc.", "Pharma",
             "Testle", "Unknown", "RoogeeR", "Ethereum", "Bitcoin", "Entel", "AMB", "ASIC", "Telegram", "LinkedOut",
             "Outagram", "DEFCON", "SCP", "HackNet", "Python", "Foogle Project Ni", "DDoS Booster Ltd.", "LMAO",
             "NoTeam", "ST corp.", "dHackOS"]