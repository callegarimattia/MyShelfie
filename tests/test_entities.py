import pytest
from src.server.model.Entities import Tile, Shelf, Bag


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

    @pytest.mark.parametrize("column", [0, 1, 2, 3, 4])
    def test_add(self, tile, column: int):
        self.shelf.add(tile, column)
        assert self.shelf.shelf[column][0] == tile

    @pytest.mark.parametrize("column", [0, 1, 2, 3, 4])
    def test_add_full_column(self, column: int):
        for _ in range(self.shelf.height):
            self.shelf.add(self.draw_tile(), column)
        with pytest.raises(Exception):
            self.shelf.add(Tile(), column)

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
