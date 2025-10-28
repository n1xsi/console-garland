from colorama import init, Fore, Style
from random import choice
from time import sleep
import os


class Garland:
    """
    Класс Гирлянды
    
    garland_length - длина гирлянды
    """
    def __init__(self, garland_length: int = 25) -> None:
        self.colors = {
            "red": Fore.RED,
            "green": Fore.GREEN,
            "yellow": Fore.YELLOW,
            "blue": Fore.BLUE,
            "magenta": Fore.MAGENTA,
            "cyan": Fore.CYAN
        }

        self.bulb = "●"
        self.wire = "-"
        self.garland_length = garland_length
        self.garland = "-" + f"{self.bulb}-"*self.garland_length

    def print_garland(self) -> None:
        print(f"\r{self.garland}", end="")
        
    def colorize_random(self) -> str:
        garland = "-"
        for _ in range(self.garland_length):
            garland += f"{choice(list(self.colors.values()))}{self.bulb}"  # Добавление цветной "лампочки"
            garland += f"{Style.RESET_ALL}{self.wire}"                     # Добавление бесцветного "проводка"
        self.garland = garland


def clear_console():
    """Очищает консоль в зависимости от ОС"""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Главная функция, которая выводит гирлянду в консоль"""
    garland = Garland()
    
    print("🎄 Новогодняя гирлянда (Ctrl+C для выключения)")  
    try:
        while True:
            garland.colorize_random()
            garland.print_garland()
            sleep(0.3)
    except KeyboardInterrupt:
        print("\nГирлянда выключена!")


if __name__ == "__main__":
    init()
    clear_console()
    main()
