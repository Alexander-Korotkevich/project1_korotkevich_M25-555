from typing import Dict, List, TypedDict, Union


class GameStateType(TypedDict):
    player_inventory: List[str]
    current_room: str
    game_over: bool
    steps_taken: int


class RoomData(TypedDict):
    description: str
    exits: Dict[str, str]
    items: List[str]
    puzzle: Union[tuple, None]
