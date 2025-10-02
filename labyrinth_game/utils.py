import math
from typing import Union

import labyrinth_game.constants as const
from labyrinth_game.player_actions import get_input
from labyrinth_game.types import GameStateType, RoomData


def game_over(game_state: GameStateType):
    """Заканчивает игру"""

    game_state["game_over"] = True


def get_current_room_data(game_state: GameStateType):
    """Возвращает данные текущей комнаты и ее название"""

    current_room = game_state.get("current_room")
    room_data = const.ROOMS.get(current_room)

    return room_data, current_room


def describe_current_room(game_state: GameStateType):
    """Описать текущую комнату"""

    room_data, current_room = get_current_room_data(game_state)
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


def get_reward(game_state: GameStateType, room: str):
    inventory = game_state.get("player_inventory")
    reward_item = None

    match (room):
        case const.HALL:
            reward_item = const.ITEMS_TREASURE_KEY
        case const.LIBRARY:
            reward_item = const.ITEMS_RUSTY_KEY
        case _:
            reward_item = const.ITEMS_COIN

    inventory.append(reward_item)
    print(f"В инвентарь добавлен предмет: {reward_item}")


def solve_puzzle(game_state: GameStateType):
    """Попытаться решить загадку"""

    room_data, current_room = get_current_room_data(game_state)
    puzzle = room_data.get("puzzle")

    if not puzzle:
        print("Загадок здесь нет.")
        return

    question = puzzle[0]
    answer = puzzle[1]

    # Выводит загадку
    print(question)

    input = get_input("Ваш ответ: ")

    if input == answer or input in const.PUZZLE_ANSWER:
        print("Правильно! Даже древние хранители были бы впечатлены.")
        const.ROOMS[current_room]["puzzle"] = None
        get_reward(game_state, current_room)
    else:
        print("Неверно. Попробуйте снова.")

        if current_room == const.TRAP_ROOM:
            trigger_trap(game_state)


def win_game(game_state: GameStateType, room_data: RoomData):
    """Заканчивает игру при победе"""

    room_data["items"].remove(const.TREASURE_CHEST)
    game_over(game_state)
    print("В сундуке сокровище! Вы победили!")


def attempt_open_treasure(game_state: GameStateType):
    """Попытаться открыть сундук с сокровищами"""

    room_data, _ = get_current_room_data(game_state)
    items = room_data.get("items")

    # Проверяем есть ли сундук в комнате
    if const.TREASURE_CHEST not in items:
        print("Сундук уже открыт или отсутствует.")
        return

    # Если есть нужный ключ, открываем сундук и завершаем игру
    if any(key in game_state.get("player_inventory") for key in const.KEYS):
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


def show_help(commands: dict[str, str]):
    command_width = 28

    print("\nДоступные команды:")
    for command in commands:
        print(f"  {command.ljust(command_width)}- {commands.get(command)}")


def pseudo_random(seed: int, modulo: int) -> int:
    """Возвращает псевдослучайное целое число в диапазоне [0, modulo]"""

    salted_seed_sin = math.sin(seed * const.SALT_NUMBER_1)
    salted_seed_sin *= const.SALT_NUMBER_2

    fract = salted_seed_sin - math.floor(salted_seed_sin)

    return math.floor(fract * modulo)


def trigger_trap(game_state: GameStateType):
    """Срабатывание ловушки"""

    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state.get("player_inventory")
    inventory_len = len(inventory)
    steps = game_state.get("steps_taken")

    if inventory_len:
        random_index = pseudo_random(steps, inventory_len)
        item_to_remove = inventory[random_index]

        inventory.remove(item_to_remove)
        print(f"Ловушка сработала! Вы потеряли {item_to_remove}.")
    else:
        end = 9
        random_int = pseudo_random(steps, end)

        if random_int < const.DAMAGE_LIMIT:
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

    room_data, _ = get_current_room_data(game_state)
    room_data["items"].append(const.ITEMS_COIN)
    print("Вы заметили монетку, сверкающую на полу.")


def fear_event(game_state: GameStateType):
    """Событие Испуг"""

    items = game_state.get("player_inventory")

    print("Тишину нарушает едва слышный шорох. Кажется, вы не одни.")

    if const.ITEMS_SWORD in items:
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

    if current_room == const.TRAP_ROOM and const.ITEMS_TORCH not in items:
        print("Чувство опасности охватывает вас! Будьте готовы ко всему.")

        trigger_trap(game_state)


def random_event(game_state: GameStateType):
    """Запускает случайное событие"""
    steps = game_state.get('steps_taken')
    end = 10
    random_int = pseudo_random(steps, end)

    if random_int == const.EVENT_HAPPENED:
        start = 0
        event_code = pseudo_random(start, len(const.EVENTS))
        event = const.EVENTS.get(event_code)
        handler = event.get("handler")

        if handler:
            handler(game_state)


def check_room(game_state: GameStateType, next_room: str) -> bool:
    """Проверяет является ли следующая комната Сокровищницей"""

    if next_room != const.TREASURE_ROOM:
        return True

    inventory = game_state.get("player_inventory")
    have_key = any(key in inventory for key in const.KEYS)

    if have_key:
        print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
        return True
    else:
        print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
        return False
