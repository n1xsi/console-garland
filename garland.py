from colorama import init, Fore, Style
from keyboard import on_press_key
from random import choice
from time import sleep
import os


class Garland:
    """
    Класс Гирлянды с переключаемыми режимами анимации.

    garland_length - длина гирлянды (желательно нечётное число, чтобы гирлянда кончалась "-")
    """

    def __init__(self, garland_length: int = 51) -> None:
        self.garland_length = garland_length
        self.bulb, self.wire = "●", "-"
        
        # Список цветов для лампочек (исключая серые цвета)
        self.colors = [c for i, c in enumerate(Fore.__dict__.values()) if i not in [0, 4, 10, 14, 15]]
        self.bulb_colors = self._initialize_colors()

        self.current_mode_index = 0
        self.modes = [
            self._mode_full_random
        ]

    def _initialize_colors(self) -> list:
        """Генерирует последовательность цветов без повторения соседних."""
        colors = [choice(self.colors)]
        for _ in range(self.garland_length - 1):
            colors.append(choice([c for c in self.colors if c != colors[-1]]))
        return colors
    
    def switch_mode(self) -> None:
        """Переключает режим анимации."""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
    
    def update_and_get_string(self) -> str:
        """Вызывает текущий метод анимации и возвращает готовую строку гирлянды."""
        current_mode_function = self.modes[self.current_mode_index]
        return current_mode_function()
    
    ##### Режимы анимации #####
    
    def _mode_full_random(self) -> str:
        """Режим 1: Случайное раскрасшивание лампочек всеми цветами."""
        colored_garland = [f"{Style.RESET_ALL}{self.wire}" if i%2==0 else f"{choice(self.colors)}{self.bulb}" for i in range(self.garland_length)]  
        return "".join(colored_garland)


def clear_console():
    """Очищает консоль."""
    os.system('cls||clear')


def main():
    """Главная функция, которая имитирует работу гирлянды."""
    clear_console()
    garland = Garland()
    
    # Настройка обработчика нажатия клавиши: смена режима анимации гирлянды на "Enter"
    on_press_key("enter", lambda _: garland.switch_mode())
    
    print("🎄 Гирлянда (ENTER - switch, Ctrl+C - exit)")
    
    try:
        while True:
            # Получение актуального состояния гирлянды в виде строки
            garland_str = garland.update_and_get_string()
            
            # Вывод строки, возвращая курсор в начало
            print(f"\r{garland_str}", end="")
            
            # Небольшая задержка для контроля скорости анимации
            sleep(0.2)
            
    except KeyboardInterrupt:
        # Нажатие Ctrl+C вызыает исключение, которое прекращает цикл
        print("\nГирлянда выключена!")
        
    finally:
        # Точный сброс цвета консоли
        print(Style.RESET_ALL)


if __name__ == "__main__":
    """Запуск программы."""
    init(autoreset=True)  # autoreset для автоматического сброса цвета консоли
    main()
