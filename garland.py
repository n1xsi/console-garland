from colorama import init, Fore, Style
from keyboard import on_press_key
from random import choice
from time import sleep
import os


# Константы для управления курсором в консоли
CURSOR_UP = "\033[A"
CLEAR_LINE = "\r\033[K"


class Garland:
    """
    Класс Гирлянды с переключаемыми режимами анимации.

    num_bulps - количество лампочек на гирлянде.
    """

    def __init__(self, num_bulbs: int = 20):
        # Логические параметры
        self.num_bulbs = num_bulbs
        self.bulb_on = "●"
        self.bulb_off = "○"
        self.wire = "-"

        # Флаг видимости заголовка
        self.header_visible = True

        # Генерация палитры (исключая тёмные и серые цвета)
        self.palette = [c for i, c in enumerate(Fore.__dict__.values()) if i not in [0, 4, 10, 14, 15]]

        # Статичные цвета для лампочек (чтобы гирлянда была "разноцветной" и неизменной)
        self.bulb_colors = self._initialize_unique_colors()

        # Структура режимов: Функция, Название, Скорость (delay)
        self.modes = [
            {"func": self._mode_full_static,    "name": "Статичный",        "delay": 0.2},
            {"func": self._mode_random_colors,  "name": "Дискотека",        "delay": 0.1},
            {"func": self._mode_running,        "name": "Бегущий огонь",    "delay": 0.05},
            {"func": self._mode_flicker,        "name": "Мерцание",         "delay": 0.15},
            {"func": self._mode_blink_all,      "name": "Вспышка",          "delay": 0.4},
            {"func": self._mode_filling,        "name": "Заполнение",       "delay": 0.05},
            {"func": self._mode_odd_even,       "name": "Чётные и нечётные",  "delay": 0.25},
            {"func": self._mode_blinking_odd_even, "name": "Поочерёдное мигание", "delay": 0.25},
            {"func": self._mode_flipping, "name": "Переброс", "delay": 0.2}
        ]
        self.current_mode_index = 0
        self.tick = 0  # Счётчик кадров для анимаций

    def _initialize_unique_colors(self) -> list:
        """Генерирует последовательность цветов, где соседние не повторяются."""
        colors = [choice(self.palette)]
        for _ in range(self.num_bulbs - 1):
            colors.append(choice([c for c in self.palette if c != colors[-1]]))
        return colors

    def switch_mode(self) -> None:
        """Переключает режим анимации на следующий."""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        self.tick = 0  # Сброс тика для красивого старта новой анимации

    def toggle_header(self) -> None:
        """Включает/выключает отображение заголовка."""
        self.header_visible = not self.header_visible

    @property
    def current_mode_info(self) -> dict:
        """Возвращает информацию о текущем режиме."""
        return self.modes[self.current_mode_index]

    def _format_bulb(self, color: str, is_active: bool) -> str:
        """Форматирует лампочку в зависимости от состояния."""
        if is_active:
            return f"{color}{self.bulb_on}"
        else:
            return f"{Style.DIM}{Fore.WHITE}{self.bulb_off}"

    def get_garland_string(self) -> str:
        """
        Главный метод сборки:
        1. Получает состояние лампочек от текущего режима.
        2. Собирает их в строку с бесцветными проводами.
        """
        mode_func = self.current_mode_info["func"]

        # Получение цветов и состояний лампочек в виде списка кортежей: (color, is_active)
        bulbs_data = mode_func()

        # Сборка строки гирлянды
        parts = []
        for color, is_active in bulbs_data:
            parts.append(self._format_bulb(color, is_active))

        # Соединение проводами: -●-●-●-
        result = f"{Style.RESET_ALL}{self.wire}" + \
            f"{Style.RESET_ALL}{self.wire}".join(parts) + \
            f"{Style.RESET_ALL}{self.wire}"

        self.tick += 1
        return result

    ############################## Режимы анимации ##############################
    # Режимы возвращают список настроек для каждой лампочки: (color, is_active)

    def _mode_full_static(self):
        # Все лампочки горят своими цветами
        return [(color, True) for color in self.bulb_colors]

    def _mode_random_colors(self):
        # Цвета случайно меняются каждый кадр (эффект дискотеки)
        return [(choice(self.palette), True) for _ in range(self.num_bulbs)]
    
    def _mode_running(self):
        # Лампочки загораются по очереди (эффект бегущего огонька)
        active_idx = self.tick % self.num_bulbs
        return [(color, i == active_idx) for i, color in enumerate(self.bulb_colors)]

    def _mode_flicker(self):
        # Случайное мерцание (горит или нет)
        return [(color, choice([True, False])) for color in self.bulb_colors]

    def _mode_blink_all(self):
        # Все лампочки мигают одновременно
        is_on = self.tick % 2 == 0
        return [(color, is_on) for color in self.bulb_colors]
    
    def _mode_filling(self):
        # Лампочки загораются по очереди до полного заполнения, затем гаснут также по очереди
        anim_len = self.num_bulbs * 2
        step = self.tick % anim_len
        result = []
        for i in range(self.num_bulbs):
            if step < self.num_bulbs:  # Фаза зажигания (0 -> N)
                is_on = (i <= step)
            else:                      # Фаза гаснения (N -> 2N)
                cutoff = step - self.num_bulbs
                is_on = (i > cutoff)
            result.append((self.bulb_colors[i], is_on))
        return result
    
    def _mode_odd_even(self):
        # Загораются поочерёдно то чётные, то нечётные лампочки
        return [(color, (self.tick + i) % 2 == 0) for i, color in enumerate(self.bulb_colors)]
    
    def _mode_blinking_odd_even(self):
        # Мигают чётные два раза, потом нечётные два раза
        if self.tick % 2 == 0: return [(color, False) for color in self.bulb_colors]
        return [(color, (self.tick // 4 + i) % 2 == 0) for i, color in enumerate(self.bulb_colors)]
    
    def _mode_flipping(self):
        # Лампочки меняются местами с конца в начало
        temp_colors = self.bulb_colors[-(self.tick%self.num_bulbs):] + self.bulb_colors[:-(self.tick%self.num_bulbs)]
        return [(color, True) for color in temp_colors]


def clear_console():
    """Очищает консоль в зависимости от ОС."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    """Главная функция, которая запускает гирлянду и обрабатывает ввод с клавиатуры."""
    # Очистка консоли перед запуском
    clear_console()

    # Создание гирлянды на 20 лампочек
    garland = Garland(num_bulbs=20)

    # Регистрация горячих клавиш
    on_press_key("enter", lambda _: garland.switch_mode())  # Смена анимации гирлянды
    on_press_key("h", lambda _: garland.toggle_header())    # Переключение видимости заголовка

    # Вывод строки с инструкцией
    print("🎄 Гирлянда (ENTER - switch, Ctrl+C - exit)")

    try:
        while True:
            if garland.header_visible:
                mode_name = garland.current_mode_info['name']
                header_str = (
                    f"{Fore.GREEN}🎄 garland.py 🌟 "
                    f"{Fore.CYAN}Режим: {mode_name} 🌟 "
                    f"{Fore.WHITE}ENTER - switch; Ctrl+C - exit; H - hide it 🎄"
                )
            else:
                # Если заголовок скрыт - то он становится пустотой, чтобы сохранить разметку экрана
                header_str = ""

            # Формирование строки гирлянды
            garland_str = garland.get_garland_string()

            # Вывод заголовка и гирлянды, выводя всё с начала

            # Логика: подъём на 1 строку ↑, очистка строки, печать заголовка,
            # спуск на 1 строку ↓, очистка строки, печать гирлянды

            print(f"{CURSOR_UP}{CLEAR_LINE}{header_str}\n{CLEAR_LINE} {garland_str} ", end="")

            # Задержка, специфичная для режима
            sleep(garland.current_mode_info['delay'])

    except KeyboardInterrupt:
        # Нажатие "Ctrl+C" вызыает исключение, которое прекращает цикл
        print("\nГирлянда выключена!")

    finally:
        # Точный сброс цвета консоли перед выходом
        print(Style.RESET_ALL)


if __name__ == "__main__":
    """Запуск программы."""
    init()
    main()
