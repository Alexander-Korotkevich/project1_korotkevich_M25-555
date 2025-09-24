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


