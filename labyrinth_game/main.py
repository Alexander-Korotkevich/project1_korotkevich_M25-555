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

def main():
  print("Добро пожаловать в Лабиринт сокровищ!")
  labyrinth_game.utils.describe_current_room(game_state)

  while(not game_state['game_over']):
     prompt = input()
     labyrinth_game.player_actions.get_input(prompt)

if __name__ == "__main__":
    main()
