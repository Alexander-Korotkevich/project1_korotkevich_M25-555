from typing import Dict

from labyrinth_game.types import EventData, RoomData
from labyrinth_game.utils import fear_event, find_event, trap_event

# Комната с сундуком
TREASURE_ROOM = "treasure_room"

# Другие комнаты
TRAP_ROOM = 'trap_room'

# Сундук с сокровищами
TREASURE_CHEST = "treasure_chest"

# Предметы
ITEMS_TORCH = "torch"
ITEMS_SWORD = "sword"
ITEMS_BRONZE_BOX = "bronze_box"
ITEMS_COIN = "coin"
ITEMS_RUSTY_KEY = "rusty_key"
ITEMS_TREASURE_KEY = "treasure_key"

KEYS = [ITEMS_RUSTY_KEY, ITEMS_TREASURE_KEY]

ROOMS: dict[str, RoomData] = {
    "entrance": {
        "description": "Вы в темном входе лабиринта...",
        "exits": {"north": "hall", "east": TRAP_ROOM},
        "items": [ITEMS_TORCH],
        "puzzle": None,
    },
    "hall": {
        "description": (
            "Большой зал с эхом." "По центру стоит пьедестал с запечатанным сундуком."
        ),
        "exits": {"south": "entrance", "west": "library", "north": "treasure_room"},
        "items": [],
        "puzzle": (
            (
                'На пьедестале надпись: "Назовите число, которое идет после девяти".'
                " Введите ответ цифрой или словом."
            ),
            "10",
        ),
    },
    TRAP_ROOM: {
        "description": (
            "Комната с хитрой плиточной поломкой."
            ' На стене видна надпись: "Осторожно — ловушка".'
        ),
        "exits": {"west": "entrance"},
        "items": [ITEMS_RUSTY_KEY],
        "puzzle": (
            (
                "Система плит активна. "
                'Чтобы пройти, назовите слово "шаг" '
                'три раза подряд (введите "шаг шаг шаг")'
            ),
            "шаг шаг шаг",
        ),
    },
    "library": {
        "description": (
            "Пыльная библиотека. На полках старые свитки."
            " Где-то здесь может быть ключ от сокровищницы."
        ),
        "exits": {"east": "hall", "north": "armory"},
        "items": ["ancient book"],
        "puzzle": (
            "В одном свитке загадка: "
            '"Что растет, когда его съедают?" (ответ одно слово)',
            "резонанс",
        ),  # намеренно странная загадка: можно сделать альтернативу
    },
    "armory": {
        "description": (
            "Старая оружейная комната. "
            "На стене висит меч, рядом — небольшая бронзовая шкатулка."
        ),
        "exits": {"south": "library"},
        "items": [ITEMS_SWORD, ITEMS_BRONZE_BOX],
        "puzzle": None,
    },
    TREASURE_ROOM: {
        "description": (
            "Комната, на столе большой сундук." " Дверь заперта — нужен особый ключ."
        ),
        "exits": {"south": "hall"},
        "items": [TREASURE_CHEST],
        "puzzle": (
            (
                "Дверь защищена кодом. "
                "Введите код (подсказка: это число пятикратного шага, 2*5= ? )"
            ),
            "10",
        ),
    },
    "garden": {
        "description": (
            "Тайный сад с волшебными растениями."
            " В центре растет сияющий цветок, а в фонтане что-то блестит."
        ),
        "exits": {"east": "hall", "south": "secret_passage"},
        "items": ["magic flower", "fountain coin"],
        "puzzle": (
            (
                'Цветок говорит: "Я живу без тела и дышу без воздуха.'
                ' Что я?" (ответ в именительном падеже)'
            ),
            "огонь",
        ),
    },
    "secret_passage": {
        "description": (
            "Узкий потайной проход."
            " Стены покрыты древними символами. Здесь темно и пыльно."
        ),
        "exits": {"north": "garden", "east": "trap_room"},
        "items": ["old map"],
        "puzzle": (
            'На стене высечена головоломка: "Сколько углов у круга?" (ответ цифрой)',
            "0",
        ),
    },
}

# Основные команды игры
CMD_HELP = "help"
CMD_LOOK = "look"
CMD_USE = "use"
CMD_GO = "go"
CMD_TAKE = "take"
CMD_INVENTORY = "inventory"
CMD_SOLVE = "solve"
CMD_QUIT = "quit"
CMD_EXIT = "exit"

SALT_NUMBER_1 = 12.9898
SALT_NUMBER_2 = 43758.5453

DAMAGE_LIMIT = 3

EVENT_HAPPENED = 0

EVENTS: Dict[int, EventData] = {
    0: {"event": "find", "handler": find_event},
    1: {"event": "fear", "handler": fear_event},
    2: {"event": "trap", "handler": trap_event},
}
