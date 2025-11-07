from colorama import init, Fore, Style
from keyboard import on_press_key
from random import choice
from time import sleep
import os


class Garland:
    """
    Класс Гирлянды с переключаемыми режимами анимации.
    
    garland_length - длина гирлянды
    """
    def __init__(self, garland_length: int = 25) -> None:
        self.colors = list(Fore.__dict__.values())[15:21] # [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]

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
    clear_console()
    garland = Garland()
    
    print("🎄 Гирлянда (ENTER - switch, Ctrl+C - exit)")  
    try:
        while True:
            garland.colorize_random()
            garland.print_garland()
            sleep(0.2)
    except KeyboardInterrupt:
        print("\nГирлянда выключена!")
    finally:
        print(Style.RESET_ALL)


if __name__ == "__main__":
    init(autoreset=True) # autoreset=True - чтобы не писать Style.RESET_ALL постоянно
    main()
