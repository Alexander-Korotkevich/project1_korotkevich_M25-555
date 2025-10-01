from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input

def get_room_data(game_state):
  """Возвращает название текущей комнаты и ее данные"""

  current_room = game_state['current_room'];
  room_data = ROOMS.get(current_room)

  return [current_room, room_data]

def describe_current_room(game_state):
  """Описать текущую комнату"""

  separator = ', '
  [current_room, room_data] = get_room_data(game_state)

  print(f'== {current_room.upper()} ==')

  print(room_data['description'])

  if room_data['items']:
    print('Заметные предметы: ' + separator.join(room_data['items']))
  
  print('Выходы: ' + separator.join([f'{exit}: {room_data['exits'][exit]}' for exit in room_data['exits'].keys()]))

  if room_data['puzzle']:
    print("Кажется, здесь есть загадка (используйте команду solve).")

def solve_puzzle(game_state):
  """Попытаться решить загадку"""

  [current_room, room_data] = get_room_data(game_state)
  puzzle = room_data['puzzle']

  if not puzzle:
    print("Загадок здесь нет.")
    return

  question = puzzle[0]
  answer = puzzle[1]

  # Выводит загадку
  print(question)

  input = get_input("Ваш ответ: ")

  if input == answer:
    print("Правильно! Даже древние хранители были бы впечатлены.")
    ROOMS[current_room]['puzzle'] = None
    #TODO: добавить награду
  else:
    print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
  """Попытаться открыть сундук с сокровищами"""

  [current_room, room_data] = get_room_data(game_state)
  items = room_data['items']

  # Проверяем есть ли сундук в комнате
  if 'treasure_chest' not in items:
    print("Сундук уже открыт или отсутствует.")
    return
    
  # Если есть нужный ключ, открываем сундук и завершаем игру
  if any(key in game_state['player_inventory'] for key in ['treasure_key', 'rusty_key']):
    print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
    room_data['items'].remove('treasure_chest')

    print("В сундуке сокровище! Вы победили!")
    game_state['game_over'] = True
  else:
    # Предлагаем ввести код для сундука, если нет ключа
    print("Сундук заперт. ... Ввести код? (да/нет)")
    input = get_input()

    if input == 'да':
      right_code = room_data['puzzle'][1]
      code = get_input('Введите код: ')

      if code == right_code:
        print("Вы вводите код, и замок щёлкает. Сундук открыт!")
        room_data['items'].remove('treasure_chest')

        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
      else:
        print("Вы вводите код и ничего не происходит...")

    else:
      # При отказе от ввода кода
      print("Вы отступаете от сундука.")    
