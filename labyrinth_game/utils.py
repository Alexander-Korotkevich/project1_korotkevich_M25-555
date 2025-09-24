from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
  separator = ', '
  current_room = game_state['current_room'];
  room = ROOMS[current_room]

  print(f'== {current_room.upper()} ==')

  print(room['description'])

  if (room['items']):
    print('Заметные предметы: ' + separator.join(room['items']) )
  
  print('Выходы: ' + separator.join([f'{exit}: {room['exits'][exit]}' for exit in room['exits'].keys()]))

  if (room['puzzle']):
    print("Кажется, здесь есть загадка (используйте команду solve).")
