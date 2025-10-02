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
    ROOMS,
    RUSTY_KEY,
    TREASURE_CHEST,
    TREASURE_KEY,
)
from labyrinth_game.player_actions import get_input
from labyrinth_game.types import GameStateType, RoomData


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
        room_data["items"].remove(TREASURE_CHEST)

        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        # Предлагаем ввести код для сундука, если нет ключа
        print("Сундук заперт. ... Ввести код? (да/нет)")
        input = get_input()

        if input == "да":
            right_code = room_data.get("puzzle")[1]
            code = get_input("Введите код: ")

            if code == right_code:
                print("Вы вводите код, и замок щёлкает. Сундук открыт!")
                room_data["items"].remove(TREASURE_CHEST)

                print("В сундуке сокровище! Вы победили!")
                game_state["game_over"] = True
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
