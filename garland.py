from colorama import init, Fore, Style
from random import choice


class Garland:
    def __init__(self, garland_length: int = 15):
        self.colors = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN,
            "white": Fore.WHITE,
        }

        self.bulb = "●"
        self.wire = "-"
        self.garland_length = garland_length

        # self.garland = "-" + f"{self.bulb}-"*self.garland_length


def main():
    garland = Garland(garland_length=1)
    print(garland.garland)


if __name__ == "__main__":
    init()
    main()
