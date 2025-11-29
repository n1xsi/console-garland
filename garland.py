from colorama import init, Fore, Style
from keyboard import on_press_key
from random import choice
from time import sleep
import os


class Garland:
    """
    Класс Гирлянды с переключаемыми режимами анимации.

    num_bulps - количество лампочек
    """

    def __init__(self, num_bulps: int):
        # Логические параметры
        self.garland_length = num_bulps*2 + 1  # Добавляем провода между лампочками и по краям
        self.bulb_on = "●"
        self.bulb_off = "○"
        self.wire = "-"
        
        # Генерация палитры (исключая тёмные и серые цвета)
        self.palette = [c for i, c in enumerate(Fore.__dict__.values()) if i not in [0, 4, 10, 14, 15]]
        
        # Статичные цвета для лампочек (чтобы гирлянда была "разноцветной", но постоянной)
        self.bulb_colors = self._initialize_colors()

        self.modes = [
            self._mode_full_random,
            self._mode_full_on,
            self._mode_random_flicker
        ]
        self.current_mode_index = 0

    def _initialize_colors(self) -> list:
        """Генерирует последовательность цветов без повторения соседних."""
        colors = [choice(self.palette)]
        for _ in range(self.garland_length - 1):
            # Выбор цвета, отличного от предыдущего
            colors.append(choice([c for c in self.palette if c != colors[-1]]))
        return colors
    
    def switch_mode(self) -> None:
        """Переключает режим анимации."""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
    
    def update_and_get_string(self) -> str:
        """Вызывает текущий метод анимации и возвращает готовую строку гирлянды."""
        current_mode_function = self.modes[self.current_mode_index]
        return current_mode_function()
    
    ############################## Режимы анимации ##############################
    
    def _mode_full_random(self) -> str:
        """Режим 1: Случайное раскрасшивание лампочек всеми цветами."""
        garland_parts = []
        for i in range(self.garland_length):
            if i%2==0:
                garland_parts.append(f"{Style.RESET_ALL}{self.wire}")
            else:
                garland_parts.append(f"{choice(self.palette)}{self.bulb_on}")
        return "".join(garland_parts)
    
    def _mode_full_on(self) -> str:
        """Режим 2: Все лампочки статично горят."""
        garland_parts = []
        for i in range(self.garland_length):
            if i%2==0:
                garland_parts.append(f"{Style.RESET_ALL}{self.wire}")
            else:
                garland_parts.append(f"{self.bulb_colors[i//2]}{self.bulb_on}")
        return "".join(garland_parts)
    
    def _mode_random_flicker(self) -> str:
        """Режим 3: Случайное мерцание лампочек."""
        garland_parts = []
        for i in range(self.garland_length):
            if i%2==0:
                garland_parts.append(f"{Style.RESET_ALL}{self.wire}")
            else:
                # Каждая лампочка решает "зажечься" или нет случайным образом
                if choice([True, False]):
                    garland_parts.append(f"{self.bulb_colors[i//2]}{self.bulb_on}")
                else:
                    garland_parts.append(f"{Style.DIM}{self.bulb_off}")
        return "".join(garland_parts)


def clear_console():
    """Очищает консоль в зависимости от ОС."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Главная функция, которая запускает гирлянду и обрабатывает ввод с клавиатуры."""
    clear_console()
    garland = Garland(num_bulps=30)
    
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
        # Нажатие "Ctrl+C" вызыает исключение, которое прекращает цикл
        print("\nГирлянда выключена!")
        
    finally:
        # Точный сброс цвета консоли
        print(Style.RESET_ALL)


if __name__ == "__main__":
    """Запуск программы."""
    init()
    main()
