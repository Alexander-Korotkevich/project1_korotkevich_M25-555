#!/usr/bin/env python3
import labyrinth_game.constants as const
import labyrinth_game.player_actions as actions
import labyrinth_game.utils as utils
from labyrinth_game.types import GameStateType

game_state: GameStateType = {
    "player_inventory": [],  # Инвентарь игрока
    "current_room": "entrance",  # Текущая комната
    "game_over": False,  # Значения окончания игры
    "steps_taken": 0,  # Количество шагов
}


def process_command(game_state: GameStateType, command: str):
    splitted = command.split()
    _command = splitted[0]
    payload: str | None = None
    is_treasure_room = game_state["current_room"] == const.TREASURE_ROOM

    if len(splitted) > 1:
        payload = splitted[1]

    match _command:
        case const.CMD_HELP:
            utils.show_help(const.COMMANDS)
        case const.CMD_LOOK:
            utils.describe_current_room(game_state)
        case const.CMD_USE:
            if is_treasure_room and payload == "treasure_chest":
                utils.attempt_open_treasure(game_state)
            else:
                actions.use_item(game_state, payload)
        case _command if _command == const.CMD_GO or _command in const.DIRECTIONS:
            actions.move_player(game_state, payload or _command)
        case const.CMD_TAKE:
            actions.take_item(game_state, payload)
        case const.CMD_INVENTORY:
            actions.show_inventory(game_state)
        case const.CMD_SOLVE:
            if is_treasure_room:
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)
        case const.CMD_EXIT | const.CMD_QUIT:
            utils.game_over(game_state)
            print("Игра окончена! До новых встреч")
        case _:
            print("Неизвестная команда.")


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    utils.describe_current_room(game_state)

    while not game_state["game_over"]:
        input = actions.get_input()
        process_command(game_state, input)


if __name__ == "__main__":
    main()
