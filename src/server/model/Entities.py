from enum import Enum
from random import shuffle


class Tile(Enum):
    """Enum for the different types of tiles in the game."""

    CATS = 0
    BOOKS = 1
    GAMES = 2
    FRAMES = 3
    THROPIES = 4
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
        """Draw a random tile from the bag."""
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
        self.board: list[list[Tile | None]] = [
            [None for _ in range(9)] for _ in range(9)
        ]
        self.number_of_players: int = 0
        self.bag = Bag()


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

    def add(self, tile: Tile, column: int):
        """
        Add a tile to the column of the shelf.
        Simulate gravity.
        """
        if self.is_column_full(column):
            raise Exception("Column is full")
        for row in range(self.height):
            if self.shelf[column][row] is None:
                self.shelf[column][row] = tile
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
