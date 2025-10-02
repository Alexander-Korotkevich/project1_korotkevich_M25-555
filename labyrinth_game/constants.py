

from labyrinth_game.types import RoomData

# Комната с сундуком
TREASURE_ROOM = "treasure_room"

# Сундук с сокровищами
TREASURE_CHEST = 'treasure_chest'

# Ключи
RUSTY_KEY = 'rusty_key'
TREASURE_KEY = 'treasure_key'

ROOMS: dict[str, RoomData] = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта...',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': ('На пьедестале надпись: "Назовите число, которое идет после девяти". Введите ответ цифрой или словом.', '10')
    },
    'trap_room': {
          'description': 'Комната с хитрой плиточной поломкой. На стене видна надпись: "Осторожно — ловушка".',
          'exits': {'west': 'entrance'},
          'items': ['rusty key'],
          'puzzle': ('Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд (введите "шаг шаг шаг")', 'шаг шаг шаг')
    },
    'library': {
          'description': 'Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ от сокровищницы.',
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient book'],
          'puzzle': ('В одном свитке загадка: "Что растет, когда его съедают?" (ответ одно слово)', 'резонанс')  # намеренно странная загадка: можно сделать альтернативу
    },
    'armory': {
          'description': 'Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая шкатулка.',
          'exits': {'south': 'library'},
          'items': ['sword', 'bronze box'],
          'puzzle': None
    },
    TREASURE_ROOM: {
          'description': 'Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.',
          'exits': {'south': 'hall'},
          'items': [TREASURE_CHEST],
          'puzzle': ('Дверь защищена кодом. Введите код (подсказка: это число пятикратного шага, 2*5= ? )', '10')
    },
    'garden': {
        'description': 'Тайный сад с волшебными растениями. В центре растет сияющий цветок, а в фонтане что-то блестит.',
        'exits': {'east': 'hall', 'south': 'secret_passage'},
        'items': ['magic flower', 'fountain coin'],
        'puzzle': ('Цветок говорит: "Я живу без тела и дышу без воздуха. Что я?" (ответ в именительном падеже)', 'огонь')
    },
    'secret_passage': {
        'description': 'Узкий потайной проход. Стены покрыты древними символами. Здесь темно и пыльно.',
        'exits': {'north': 'garden', 'east': 'trap_room'},
        'items': ['old map'],
        'puzzle': ('На стене высечена головоломка: "Сколько углов у круга?" (ответ цифрой)', '0')
    }
}

# Основные команды игры
CMD_HELP = 'help'
CMD_LOOK = 'look' 
CMD_USE = 'use'
CMD_GO = 'go'
CMD_TAKE = 'take'
CMD_INVENTORY = 'inventory'
CMD_SOLVE = 'solve'
CMD_QUIT = 'quit'
CMD_EXIT = 'exit'
