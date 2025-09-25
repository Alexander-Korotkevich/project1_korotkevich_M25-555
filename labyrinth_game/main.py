#!/usr/bin/env python3
import labyrinth_game.constants
import labyrinth_game.utils
import labyrinth_game.player_actions
  
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
         labyrinth_game.utils.describe_current_room(game_state)
      case 'use':
         pass
      case 'go':
         labyrinth_game.player_actions.move_player(game_state, payload)   
      case 'take':
         labyrinth_game.player_actions.take_item(game_state, payload)
      case 'inventory':
         labyrinth_game.player_actions.show_inventory(game_state)   
      case 'quit' | 'exit':
         game_state['game_over'] = True
      case _:
         print("Неизвестная команда.")      

def main():
  print("Добро пожаловать в Лабиринт сокровищ!")
  labyrinth_game.utils.describe_current_room(game_state)

  while not game_state['game_over']:
     input = labyrinth_game.player_actions.get_input()
     process_command(game_state, input)


if __name__ == "__main__":
    main()
