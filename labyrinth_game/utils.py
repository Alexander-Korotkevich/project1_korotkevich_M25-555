import math
from typing import Union

from labyrinth_game.constants import (
    CMD_GO,
    CMD_HELP,
    CMD_INVENTORY,
    CMD_LOOK,
    CMD_QUIT,
    CMD_SOLVE,
    CMD_TAKE,
    CMD_USE,
    DAMAGE_LIMIT,
    EVENT_HAPPENED,
    EVENTS,
    ROOMS,
    RUSTY_KEY,
    SALT_NUMBER_1,
    SALT_NUMBER_2,
    TREASURE_CHEST,
    TREASURE_KEY,
)
from labyrinth_game.player_actions import get_input
from labyrinth_game.types import GameStateType, RoomData


def game_over(game_state: GameStateType):
    """Заканчивает игру"""

    game_state["game_over"] = True


def get_room_data(game_state: GameStateType) -> list[Union[RoomData, str]]:
    """Возвращает данные комнаты и ее название"""

    current_room = game_state.get("current_room")
    room_data = ROOMS.get(current_room)

    return [room_data, current_room]


def describe_current_room(game_state: GameStateType):
    """Описать текущую комнату"""

    [room_data, current_room] = get_room_data(game_state)
    room_items = room_data.get("items")
    room_exits = room_data.get("exits")
    separator = ", "

    print(f"== {current_room.upper()} ==")

    print(room_data.get("description"))

    if room_items:
        print("Заметные предметы: " + separator.join(room_items))

    print(
        "Выходы: "
        + separator.join(
            [f"{exit}: {room_exits.get(exit)}" for exit in room_exits.keys()]
        )
    )

    if room_data.get("puzzle"):
        print("Кажется, здесь есть загадка (используйте команду solve).")


def solve_puzzle(game_state: GameStateType):
    """Попытаться решить загадку"""

    [room_data, current_room] = get_room_data(game_state)
    puzzle = room_data.get("puzzle")

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question = puzzle[0]
    answer = puzzle[1]

    # Выводит загадку
    print(question)

    input = get_input("Ваш ответ: ")

    if input == answer:
        print("Правильно! Даже древние хранители были бы впечатлены.")
        ROOMS[current_room]["puzzle"] = None
        # TODO: добавить награду
    else:
        print("Неверно. Попробуйте снова.")


def win_game(game_state: GameStateType, room_data: RoomData):
    """Заканчивает игру при победе"""

    room_data["items"].remove(TREASURE_CHEST)
    game_over(game_state)
    print("В сундуке сокровище! Вы победили!")


def attempt_open_treasure(game_state: GameStateType):
    """Попытаться открыть сундук с сокровищами"""

    [room_data] = get_room_data(game_state)
    items = room_data.get("items")

    # Проверяем есть ли сундук в комнате
    if TREASURE_CHEST not in items:
        print("Сундук уже открыт или отсутствует.")
        return

    # Если есть нужный ключ, открываем сундук и завершаем игру
    if any(
        key in game_state.get("player_inventory") for key in [TREASURE_KEY, RUSTY_KEY]
    ):
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        win_game(game_state, room_data)
    else:
        # Предлагаем ввести код для сундука, если нет ключа
        print("Сундук заперт. ... Ввести код? (да/нет)")
        input = get_input()

        if input == "да":
            right_code = room_data.get("puzzle")[1]
            code = get_input("Введите код: ")

            if code == right_code:
                print("Вы вводите код, и замок щёлкает. Сундук открыт!")
                win_game(game_state, room_data)
            else:
                print("Вы вводите код и ничего не происходит...")

        else:
            # При отказе от ввода кода
            print("Вы отступаете от сундука.")


def show_help():
    print("\nДоступные команды:")
    print(f"  {CMD_GO} <direction>  - перейти в направлении (north/south/east/west)")
    print(f"  {CMD_LOOK}            - осмотреть текущую комнату")
    print(f"  {CMD_TAKE} <item>     - поднять предмет")
    print(f"  {CMD_USE} <item>      - использовать предмет из инвентаря")
    print(f"  {CMD_INVENTORY}       - показать инвентарь")
    print(f"  {CMD_SOLVE}           - попытаться решить загадку в комнате")
    print(f"  {CMD_QUIT}            - выйти из игры")
    print(f"  {CMD_HELP}            - показать это сообщение")


def pseudo_random(seed: int, modulo: int) -> int:
    """Возвращает псевдослучайное целое число в диапазоне [0, modulo]"""

    salted_seed_sin = math.sin(seed * SALT_NUMBER_1)
    salted_seed_sin *= SALT_NUMBER_2

    fract = salted_seed_sin - math.floor(salted_seed_sin)

    return math.floor(fract * modulo)


def trigger_trap(game_state: GameStateType):
    """Срабатывание ловушки"""

    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state.get("player_inventory")
    inventory_len = len(inventory)

    if inventory_len:
        random_index = pseudo_random(game_state.get("steps_taken"), inventory_len)
        item_to_remove = inventory[random_index]

        inventory.remove(item_to_remove)
        print(f"Ловушка сработала! Вы потеряли {item_to_remove}.")
    else:
        start = 0
        end = 9
        random_int = pseudo_random(start, end)

        if random_int < DAMAGE_LIMIT:
            game_over(game_state)
            print(
                (
                    "Эхо вашего последнего вздоха затихает в каменных коридорах."
                    "\nИгра окончена."
                )
            )
        else:
            print("Похоже, у ловушки был выходной. Вам повезло!")


def find_event(game_state: GameStateType):
    """Событие Находка"""

    [room_data] = get_room_data(game_state)
    room_data["items"].append("coin")
    print("Вы заметили монетку, сверкающую на полу.")


def fear_event(game_state: GameStateType):
    """Событие Испуг"""

    items = game_state.get("player_inventory")

    print("Тишину нарушает едва слышный шорох. Кажется, вы не одни.")

    if "sword" in items:
        print(
            (
                "Шорох обрывается на полуслове."
                " Присутствие отступает перед холодной сталью."
            )
        )


def trap_event(game_state: GameStateType):
    """Событие Срабатывание ловушки"""

    current_room = game_state.get("current_room")
    items = game_state.get("player_inventory")

    if current_room == "trap_room" and "torch" not in items:
        print("Чувство опасности охватывает вас! Будьте готовы ко всему.")

        trigger_trap(game_state)


def random_event(game_state: GameStateType):
    """Запускает случайное событие"""

    start = 0
    end = 10
    random_int = pseudo_random(start, end)

    if random_int == EVENT_HAPPENED:
        event_code = pseudo_random(start, len(EVENTS))
        event = EVENTS.get(event_code)
        handler = event.get("handler")

        if handler:
            handler(game_state)
