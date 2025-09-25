#!/usr/bin/env python3
import labyrinth_game.constants
import labyrinth_game.utils as utils
import labyrinth_game.player_actions as actions
  
game_state = {
  'player_inventory': [], # Инвентарь игрока
  'current_room': 'entrance', # Текущая комната
  'game_over': False, # Значения окончания игры
  'steps_taken': 0 # Количество шагов
}

def process_command(game_state, command):
   [command, payload] = command.split()

   match command:
      case 'look':
         utils.describe_current_room(game_state)
      case 'use':
         actions.use_item(game_state, payload)
         pass
      case 'go':
         actions.move_player(game_state, payload)   
      case 'take':
         actions.take_item(game_state, payload)
      case 'inventory':
         actions.show_inventory(game_state)   
      case 'quit' | 'exit':
         game_state['game_over'] = True
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
