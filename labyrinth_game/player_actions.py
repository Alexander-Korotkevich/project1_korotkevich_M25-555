import labyrinth_game.utils as utils
from labyrinth_game.types import GameStateType

def show_inventory(game_state: GameStateType):
  inventory = game_state['player_inventory']
  if inventory:
    print(f'Инвентарь: {', '.join(inventory)}')
  else:
    print('Инвентарь пуст!')  

def get_input(prompt="> "):
  try:
    return input(prompt)
  except (KeyboardInterrupt, EOFError):
    print("\nВыход из игры.")
    return "quit"

def move_player(game_state: GameStateType, direction: str):
  [room_data] = utils.get_room_data(game_state)
  exit = room_data['exits'].get(direction)
  if exit:
    game_state['current_room'] = exit
    game_state['steps_taken'] += 1
    utils.describe_current_room(game_state)
  else:
    print("Нельзя пойти в этом направлении.")  

def take_item(game_state: GameStateType, item_name: str):
  [room_data] = utils.get_room_data(game_state)
  items = room_data['items']

  if item_name in items:
    game_state['player_inventory'].append(item_name)
    room_data['items'].remove(item_name)
    print(f'Вы подняли: {item_name}.')
  else:
    print("Такого предмета здесь нет.")

def use_item(game_state: GameStateType, item_name: str):
  items = game_state['player_inventory']

  if item_name in items:
    match item_name:
      case 'torch':
        print("Пламя факела вспыхивает, отбрасывая танцующие тени на стены лабиринта.")
      case 'sword':
        print("Вес меча в руке придает вам уверенности. Теперь вы готовы к встрече с опасностью.")
      case 'bronze_box':
        if 'rusty_key' in items:
          print("Вы открываете шкатулку, но она пуста. Похоже, вы уже забрали ключ.")
        else:
          items.append('rusty_key')
          print("Вы открываете бронзовую шкатулку. Внутри лежит ржавый ключ!")
          print("Ржавый ключ добавлен в инвентарь.")  
      case _:
        print(f'Вы не знаете как использовать {item_name}')  
  else:
    print('У вас нет такого предмета.')
