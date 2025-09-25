from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input

def get_room_data(game_state):
  # Возвращает название текущей комнаты и ее данные

  current_room = game_state['current_room'];
  room_data = ROOMS.get(current_room)

  return [current_room, room_data]

def describe_current_room(game_state):
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
