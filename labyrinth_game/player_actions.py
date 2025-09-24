import labyrinth_game.utils

def show_inventory(game_state):
  inventory = game_state['player_inventory']
  if (inventory):
    print(f'Инвентарь: {', '.join(inventory)}')
  else:
    print('Инвентарь пуст!')  

def get_input(prompt="> "):
  try:
     pass
      # тут ваш код
  except (KeyboardInterrupt, EOFError):
    print("\nВыход из игры.")
    return "quit"

def move_player(game_state, direction):
  exit = game_state['exits'].get(direction)
  if (exit):
    game_state['current_room'] = exit
    game_state['steps_taken'] += 1
    labyrinth_game.utils.describe_current_room(game_state)
  else:
    print("Нельзя пойти в этом направлении.")  
