def show_inventory(game_state):
  inventory = game_state['player_inventory']
  if (inventory):
    print(f'Инвентарь: {', '.join(inventory)}')
  else:
    print('Инвентарь пуст!')  


