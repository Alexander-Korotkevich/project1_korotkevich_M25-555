from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
  separator = ', '
  current_room = game_state['current_room'];
  room_data = ROOMS[current_room]

  print(f'== {current_room.upper()} ==')

  print(room_data['description'])

  if room_data['items']:
    print('Заметные предметы: ' + separator.join(room_data['items']))
  
  print('Выходы: ' + separator.join([f'{exit}: {room_data['exits'][exit]}' for exit in room_data['exits'].keys()]))

  if room_data['puzzle']:
    print("Кажется, здесь есть загадка (используйте команду solve).")
