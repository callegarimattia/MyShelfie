from enum import Enum
from random import shuffle


class Tile(Enum):
    """Enum for the different types of tiles in the game."""

    CATS = 0
    BOOKS = 1
    GAMES = 2
    FRAMES = 3
    THROPHIES = 4
    PLANTS = 5

    def __str__(self):
        return self.name.lower()


class Bag:
    """Class for the bag of tiles."""

    def __init__(self):
        """Initialize the bag with the correct number of tiles."""
        self.tiles: Tile = []
        for tile in Tile:
            for _ in range(22):
                self.tiles.append(tile)
        shuffle(self.tiles)

    def __str__(self):
        """Return a string representation of the bag."""
        return str(self.tiles)

    def draw(self):
        """Draw a tile from the bag."""
        return self.tiles.pop()


class PersonalGoal:
    """Class for the personal goals."""

    def __init__(self, name, description, points):
        """Initialize the personal goal."""
        self.name: str = name
        self.description: str = description
        self.points: int = points

    def __str__(self):
        """Return a string representation of the personal goal."""
        return f"{self.name}: {self.description} ({self.points} points)"


class CommonGoal:
    """Class for the common goals."""

    def __init__(self, name, description, points):
        """Initialize the common goal."""
        self.name: str = name
        self.description: str = description
        self.points: int = points

    def __str__(self):
        """Return a string representation of the common goal."""
        return f"{self.name}: {self.description} ({self.points} points)"


class Board:
    """Class for the board."""

    def __init__(self):
        """Initialize the board."""
        self.rows = 9
        self.cols = 9
        self.board: list[list[Tile | None]] = [
            [None for _ in range(self.rows)] for _ in range(self.cols)
        ]
        self.number_of_players: int = 0
        self.bag = Bag()
        self.common_goals: list[CommonGoal] = []

    def __str__(self):
        """Return a string representation of the board."""
        return str(self.board)


class Shelf:
    """Class for the shelf."""

    def __init__(self):
        """Initialize the shelf."""
        self.height: int = 9
        self.width: int = 5
        self.shelf: list[list[Tile | None]] = [
            [None for _ in range(self.height)] for _ in range(self.width)
        ]

    def __str__(self):
        """Return a string representation of the shelf."""
        return str(self.shelf)

    def add(self, tiles: list[Tile], column: int):
        """
        Add the given tiles to the column of the shelf.
        Simulate gravity.
        """
        if self.get_available_spaces()[column] < len(tiles):
            raise Exception("")
        for row in range(self.height):
            if self.shelf[column][row] is None:
                self.shelf[column][row] = tiles
                return

    def is_column_full(self, column: int):
        """Return whether the column is full."""
        if column < 0 or column >= self.width:
            raise Exception("Column out of bounds")
        return all(tile is not None for tile in self.shelf[column])

    def is_full(self):
        """Return whether the shelf is full."""
        return all(self.is_column_full(column) for column in range(self.width))

    def get_available_spaces(self):
        """Return a list of number of available spaces in each column."""
        return [column.count(None) for column in self.shelf]


class Player:
    """Class for the player."""

    def __init__(self, name: str, board: Board):
        """Initialize the player."""
        self.name: str = name
        self.personal_goals: PersonalGoal = None
        self.shelf: Shelf = Shelf()
        self.score: int = 0

    def __str__(self):
        """Return a string representation of the player."""
        return f"{self.name}: {self.personal_goals}"

    def init_personal_goal(self, personal_goal: PersonalGoal):
        """Initialize the personal goal of the player."""
        if self.personal_goals is not None:
            raise Exception("Player already has a personal goal")
        self.personal_goals = personal_goal

    def is_shelf_full(self) -> bool:
        """Return whether the shelf is full."""
        return self.shelf.is_full()

    def get_available_spaces(self) -> list[int]:
        """Return a list of number of available spaces in each column."""
        return self.shelf.get_available_spaces()

    def put_tiles_on_shelf(self, tiles: list[Tile], column: int):
        """Put tiles on the shelf."""
        self.shelf.add(tiles, column)
