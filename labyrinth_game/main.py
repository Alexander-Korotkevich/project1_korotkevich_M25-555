#!/usr/bin/env python3
from typing import List
import labyrinth_game.constants
import labyrinth_game.utils as utils
import labyrinth_game.player_actions as actions
from labyrinth_game.types import GameStateType
  
game_state: GameStateType = {
  'player_inventory': [], # Инвентарь игрока
  'current_room': 'entrance', # Текущая комната
  'game_over': False, # Значения окончания игры
  'steps_taken': 0 # Количество шагов
}

def process_command(game_state: GameStateType, command: str):
   splitted: List[str] = command.split()
   _command: str = splitted[0]
   payload: str | None = None
   is_treasure_room: bool = game_state["current_room"] == "treasure_room"

   if len(splitted) > 1:
     payload = splitted[1]

   match _command:
      case 'help':
        utils.show_help()
      case 'look':
        utils.describe_current_room(game_state)
      case 'use':
        if is_treasure_room and payload == 'treasure_chest':
          utils.attempt_open_treasure(game_state)
        else:  
          actions.use_item(game_state, payload)
      case 'go':
        actions.move_player(game_state, payload)   
      case 'take':
        actions.take_item(game_state, payload)
      case 'inventory':
        actions.show_inventory(game_state)   
      case 'solve':
        if is_treasure_room:
          utils.attempt_open_treasure(game_state)
        else:
          utils.solve_puzzle(game_state)    
      case 'quit' | 'exit':
        game_state['game_over'] = True
        print('Игра окончена! До новых встреч')
      case _:
        print("Неизвестная команда.")

def main():
  print("Добро пожаловать в Лабиринт сокровищ!")
  utils.describe_current_room(game_state)

  while not game_state['game_over']:
     input = actions.get_input()
     process_command(game_state, input)


if __name__ == "__main__":
    main()
