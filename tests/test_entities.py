import pytest
from src.server.model.Entities import Shelf, Bag, Board, Tile, PersonalGoal, CommonGoal


class TestTile:
    def test_str(self):
        assert str(Tile.CATS) == "cats"
        assert str(Tile.BOOKS) == "books"
        assert str(Tile.GAMES) == "games"
        assert str(Tile.FRAMES) == "frames"
        assert str(Tile.THROPHIES) == "throphies"
        assert str(Tile.PLANTS) == "plants"

    def test_count(self):
        assert len(Tile) == 6


class TestBag:
    @pytest.fixture(autouse=True)
    def init(self):
        self.bag = Bag()

    def test_str(self):
        assert str(self.bag) == str(self.bag.tiles)

    def test_init(self):
        assert len(self.bag.tiles) == 22 * 6
        assert self.bag.tiles.count(Tile.CATS) == 22
        assert self.bag.tiles.count(Tile.BOOKS) == 22
        assert self.bag.tiles.count(Tile.GAMES) == 22
        assert self.bag.tiles.count(Tile.FRAMES) == 22
        assert self.bag.tiles.count(Tile.THROPHIES) == 22
        assert self.bag.tiles.count(Tile.PLANTS) == 22

    def test_draw(self):
        tile = self.bag.draw()
        assert tile in Tile
        assert len(self.bag.tiles) == 22 * 6 - 1
        for kind in Tile:
            if kind != tile:
                assert self.bag.tiles.count(kind) == 22


class TestShelf:
    @pytest.fixture(autouse=True)
    def init(self):
        self.shelf = Shelf()
        self.bag = Bag()

    def draw_tile(self):
        return self.bag.draw()

    @pytest.fixture(name="tile")
    def drawn_tile(self):
        return self.draw_tile()

    def test_init(self):
        assert self.shelf.height == 9
        assert self.shelf.width == 5
        assert self.shelf.shelf == [
            [None for _ in range(self.shelf.height)] for _ in range(self.shelf.width)
        ]

    def test_str(self):
        assert str(self.shelf) == str(self.shelf.shelf)

    @pytest.mark.parametrize("column", [0, 1, 2, 3, 4])
    def test_add(self, tile, column: int):
        self.shelf.add(tile, column)
        assert self.shelf.shelf[column][0] == tile

    @pytest.mark.parametrize("column", [0, 1, 2, 3, 4])
    def test_add_full_column(self, column: int):
        for _ in range(self.shelf.height):
            self.shelf.add(self.draw_tile(), column)
        with pytest.raises(Exception) as excinfo:
            self.shelf.add(self.draw_tile(), column)
        assert str(excinfo.value) == "Column is full"

    @pytest.mark.parametrize("column", [-1, 5])
    def test_add_column_out_of_range(self, column: int):
        with pytest.raises(Exception) as excinfo:
            self.shelf.add(self.draw_tile(), column)
        assert str(excinfo.value) == "Column out of bounds"

    @pytest.mark.parametrize("column", [0, 1, 2, 3, 4])
    def test_is_column_full(self, column: int):
        for _ in range(self.shelf.height):
            self.shelf.add(self.draw_tile(), column)
        assert self.shelf.is_column_full(column)

    def test_is_full(self):
        for column in range(self.shelf.width):
            for _ in range(self.shelf.height):
                self.shelf.add(self.draw_tile(), column)
        assert self.shelf.is_full()

    def test_is_not_full(self):
        assert not self.shelf.is_full()

    def test_get_available_spaces(self):
        spaces = [self.shelf.height for _ in range(self.shelf.width)]
        assert self.shelf.get_available_spaces() == spaces
        for column in range(self.shelf.width):
            for i in range(self.shelf.height):
                self.shelf.add(self.draw_tile(), column)
                assert (
                    self.shelf.get_available_spaces()[column] == spaces[column] - i - 1
                )

    def test_get_available_spaces_full(self):
        for column in range(self.shelf.width):
            for _ in range(self.shelf.height):
                self.shelf.add(self.draw_tile(), column)
        assert self.shelf.get_available_spaces() == [0 for _ in range(self.shelf.width)]


class TestBoard:
    @pytest.fixture(autouse=True)
    def init(self):
        self.board = Board()
        self.bag = Bag()

    def test_init(self):
        assert self.board.rows == 9
        assert self.board.cols == 9
        assert self.board.board == [
            [None for _ in range(self.board.rows)] for _ in range(self.board.cols)
        ]
        assert self.board.number_of_players == 0
        assert isinstance(self.board.bag, Bag)
        assert self.board.common_goals == []


class TestPersonalGoal:
    @pytest.fixture(autouse=True)
    def init(self):
        self.personal_goal = PersonalGoal("test", "test", 1)

    def test_init(self):
        assert self.personal_goal.name == "test"
        assert self.personal_goal.description == "test"
        assert self.personal_goal.points == 1

    def test_str(self):
        assert str(self.personal_goal) == "test: test (1 points)"


class TestCommonGoal:
    @pytest.fixture(autouse=True)
    def init(self):
        self.common_goal = CommonGoal("test", "test", 1)

    def test_init(self):
        assert self.common_goal.name == "test"
        assert self.common_goal.description == "test"
        assert self.common_goal.points == 1

    def test_str(self):
        assert str(self.common_goal) == "test: test (1 points)"
