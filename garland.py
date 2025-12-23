from argparse import ArgumentParser, Namespace
from colorama import init, Fore, Style
from time import sleep, time
from random import choice
from sys import stdin
import os

# Определение ОС
OS_NAME = os.name

# Подключение библиотек для работы с клавиатурой в зависимости от ОС
if OS_NAME == 'nt':
    from msvcrt import kbhit, getch
else:
    from termios import tcgetattr, tcsetattr, TCSADRAIN
    from select import select
    from tty import setcbreak


# Константы для управления курсором в консоли
CURSOR_UP = "\033[A"
CLEAR_LINE = "\r\033[K"


class Garland:
    """
    Класс Гирлянды с переключаемыми режимами анимации.

    num_bulps - количество лампочек на гирлянде.
    """

    # -------------------------------- КОНСТРУКТОР --------------------------------
    def __init__(self, num_bulbs: int = 20):
        # Составные части гирлянды
        self.num_bulbs = num_bulbs
        self.bulb_on = "●"
        self.bulb_off = "○"
        self.wire = "-"

        # Флаги интерфейса
        self.header_visible = True
        self.auto_switch = False

        # Генерация палитры (исключая тёмные/серые цвета)
        self.palette = [c for i, c in enumerate(Fore.__dict__.values()) if i not in [0, 4, 10, 14, 15]]
        # Статичные цвета для лампочек (чтобы гирлянда была "разноцветной" и неизменной)
        self.bulb_colors = self._initialize_unique_colors()

        # Структура режимов: Функция, Название, Скорость анимации (delay)
        self.modes = [
            {"func": self._mode_full_static,   "name": "Статичный",          "delay": 0.2},
            {"func": self._mode_random_colors, "name": "Дискотека",          "delay": 0.1},
            {"func": self._mode_running,       "name": "Бегущий огонёк",     "delay": 0.05},
            {"func": self._mode_flicker,       "name": "Случайное мерцание", "delay": 0.15},
            {"func": self._mode_blink_all,     "name": "Вспышка",            "delay": 0.4},
            {"func": self._mode_filling,       "name": "Заполнение",         "delay": 0.05},
            {"func": self._mode_odd_even,      "name": "Чётные-нечётные",    "delay": 0.25},
            {"func": self._mode_blinking,      "name": "Мигание",            "delay": 0.25},
            {"func": self._mode_flipping,      "name": "Переброс",           "delay": 0.2}
        ]
        
        self.last_switch_time = time()  # Время последнего переключения режима
        self.current_mode_index = 0     # Текущий режим анимации
        self.tick = 0                   # Счётчик кадров

    # -------------------------------- ФУНКЦИИ --------------------------------
    def _initialize_unique_colors(self) -> list:
        """Генерирует последовательность цветов для лампочек, где соседние не повторяются."""
        colors = [choice(self.palette)]
        for _ in range(self.num_bulbs - 1):
            colors.append(choice([c for c in self.palette if c != colors[-1]]))
        return colors

    def switch_mode(self) -> None:
        """Переключает режим анимации на следующий."""
        self.current_mode_index = (self.current_mode_index + 1) % len(self.modes)
        self.tick = 0                   # Сброс тика для корректного старта новой анимации
        self.last_switch_time = time()  # Обновление времени последнего переключения

    def toggle_header(self) -> None:
        """Включает/выключает отображение заголовка (строки состояния)."""
        self.header_visible = not self.header_visible

    def toggle_auto_switch(self) -> None:
        """Включает/выключает автоматическую смену режимов."""
        self.auto_switch = not self.auto_switch
        # Сброс таймера, чтобы смена режима не произошла мгновенно при включении
        self.last_switch_time = time()

    @property  # Для превращения метода в атрибут (чтобы не писать скобки)
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
        Метод сборки цветной гирлянды.
        1. Получает состояние лампочек от текущего режима
        2. Собирает их в строку с бесцветными проводами.
        """
        mode_func = self.current_mode_info["func"]

        # Получение цветов и состояний лампочек (в виде списка кортежей)
        bulbs_data = mode_func()

        # Сборка строки гирлянды
        parts = []
        for color, is_active in bulbs_data:
            parts.append(self._format_bulb(color, is_active))

        # Соединение проводами (-●-●-●-)
        result = f"{Style.RESET_ALL}{self.wire}" + \
            f"{Style.RESET_ALL}{self.wire}".join(parts) + \
            f"{Style.RESET_ALL}{self.wire}"

        self.tick += 1
        return result

    # -------------------------------- РЕЖИМЫ АНИМАЦИИ --------------------------------
    # Режимы возвращают список настроек для каждой лампочки: (color, is_active)

    def _mode_full_static(self) -> list:
        # Все лампочки горят своими цветами
        return [(color, True) for color in self.bulb_colors]

    def _mode_random_colors(self) -> list:
        # Цвета случайно меняются каждый кадр (эффект дискотеки)
        return [(choice(self.palette), True) for _ in range(self.num_bulbs)]

    def _mode_running(self) -> list:
        # Лампочки загораются по очереди (эффект бегущего огонька)
        active_idx = self.tick % self.num_bulbs
        return [(color, i == active_idx) for i, color in enumerate(self.bulb_colors)]

    def _mode_flicker(self) -> list:
        # Случайное мерцание (горит или нет)
        return [(color, choice([True, False])) for color in self.bulb_colors]

    def _mode_blink_all(self) -> list:
        # Все лампочки мигают одновременно
        is_on = self.tick % 2 == 0
        return [(color, is_on) for color in self.bulb_colors]

    def _mode_filling(self) -> list:
        # Лампочки сначала поочерёдно загораются, затем поочерёдно гаснут
        anim_len = self.num_bulbs * 2
        step = self.tick % anim_len
        result = []
        for i in range(self.num_bulbs):
            if step < self.num_bulbs:  # Фаза зажигания (0 -> N)
                is_on = (i <= step)
            else:                      # Фаза выключения (N -> 2N)
                cutoff = step - self.num_bulbs
                is_on = (i > cutoff)
            result.append((self.bulb_colors[i], is_on))
        return result

    def _mode_odd_even(self) -> list:
        # Загораются поочерёдно то чётные, то нечётные лампочки
        return [(color, (self.tick + i) % 2 == 0) for i, color in enumerate(self.bulb_colors)]

    def _mode_blinking(self) -> list:
        # Мигают чётные два раза, потом нечётные два раза
        if self.tick % 2 == 0:
            return [(color, False) for color in self.bulb_colors]
        return [(color, (self.tick // 4 + i) % 2 == 0) for i, color in enumerate(self.bulb_colors)]

    def _mode_flipping(self) -> list:
        # Лампочки перекидываются с конца в начало
        temp_colors = self.bulb_colors[-(self.tick % self.num_bulbs):] + self.bulb_colors[:-(self.tick % self.num_bulbs)]
        return [(color, True) for color in temp_colors]

# ------------------  Утилиты для терминала  ------------------
def get_key() -> str | None:
    """Считывает нажатие клавиши в зависимости от ОС."""
    if OS_NAME == 'nt':  # Windows
        if kbhit():
            ch = getch()
            try:
                return ch.decode('utf-8').lower()
            except UnicodeDecodeError:
                return None
        return None
    else:  # Linux/Mac
        dr, dw, de = select([stdin], [], [], 0)
        if dr:
            return stdin.read(1).lower()
        return None


def setup_terminal() -> tuple[int, int]:
    """Переводит терминал в raw-режим, чтобы читать клавиши без Enter."""
    if OS_NAME != 'nt':
        fd = stdin.fileno()
        old_settings = tcgetattr(fd)
        setcbreak(fd)  # Чтение посимвольно
        return fd, old_settings
    return None, None


def restore_terminal(fd, old_settings) -> None:
    """Возвращает настройки терминала обратно."""
    if OS_NAME != 'nt' and fd is not None:
        tcsetattr(fd, TCSADRAIN, old_settings)


def clear_console() -> None:
    """Очищает консоль в зависимости от ОС."""
    os.system('cls' if OS_NAME == 'nt' else 'clear')


def arguments_init() -> Namespace:
    """Инициализация и парсинг аргументов командной строки."""
    parser = ArgumentParser(description="🎄 Новогодняя гирлянда в консоли 🎄")
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=40,
        help="Длина гирлянды (кол-во лампочек). По умолчанию: 40"
    )
    return parser.parse_args()

# ------------------  Запуск  ------------------
def main():
    # Получение аргументов командной строки
    args = arguments_init()
    if args.length < 1:
        print("Ошибка: Длина гирлянды должна быть больше 0!")
        return

    clear_console()  # Очистка консоли для выделения гирлянды
    init()           # Инициализация colorama

    fd, old_settings = setup_terminal()       # Настройка терминала
    garland = Garland(num_bulbs=args.length)  # Создание гирлянды

    print("\n")  # Отступ для корректного срабатывания CURSOR_UP на первом кадре

    try:
        while True:
            # --- ОБРАБОТКА ВВОДА ---
            key = get_key()
            match key:
                case '\r' | '\n':   # Enter
                    garland.switch_mode()
                case 'h':           # H
                    garland.toggle_header()
                case 'a':           # A
                    garland.toggle_auto_switch()
                case '\x03':        # Ctrl+C
                    raise KeyboardInterrupt

            # --- ЛОГИКА АВТОМАТИЧЕСКОГО ПЕРЕКЛЮЧЕНИЯ РЕЖИМОВ ---
            if garland.auto_switch:
                if time() - garland.last_switch_time > 5:  # Смена каждые 5 секунд
                    garland.switch_mode()

            # --- ОТРИСОВКА ИНТЕРФЕЙСА ---
            if garland.header_visible:
                mode_name = garland.current_mode_info['name']
                auto_status = f"{Fore.GREEN}Вкл" if garland.auto_switch else f"{Fore.RED}ВЫКЛ"

                header_str = (
                    f"{Fore.GREEN}🎄 garland.py 🌟 "
                    f"{Fore.CYAN}Режим: {mode_name} 🌟 "
                    f"{Fore.BLUE}Авто: {auto_status} 🌟 "
                    f"{Fore.WHITE}hotkeys: ENTER, Ctrl+C, A, H 🎄"
                )
            else:
                # Если заголовок скрыт, то рисуется пустота для сохранения разметки экрана
                header_str = ""

            # Формирование строки гирлянды
            garland_str = garland.get_garland_string()

            # Вывод заголовка и гирлянды, печатая всё с начала
            print(f"{CURSOR_UP}{CLEAR_LINE}{header_str}\n{CLEAR_LINE} {garland_str} ", end="")

            # Задержка конкретного режима (в секундах)
            sleep(garland.current_mode_info['delay'])

    except KeyboardInterrupt:
        # Нажатие "Ctrl+C" вызыает исключение, которое прекращает цикл работы программы
        print(f"\n{Style.RESET_ALL}Гирлянда выключена!")

    finally:
        restore_terminal(fd, old_settings)  # Восстановление настроек терминала
        print(Style.RESET_ALL)              # Точный сброс цвета консоли перед выходом


if __name__ == "__main__":
    main()
