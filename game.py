from enum import Enum
import random
from tile import Tile


# Enum to exporting game state
class DisplayTileTypes(Enum):
    NotRevealed = 0
    Bomb = 1
    Flag = 2
    Revealed = 3


# Class to store game state when exporting
class DisplayTile:
    def __init__(self, type: DisplayTileTypes, adjacentBombs: int = 0):
        self.type: DisplayTileTypes = type
        self._adjacentBombs: int = adjacentBombs

    def getAdjacentCount(self) -> int:
        return self._adjacentBombs

    def getType(self) -> DisplayTileTypes:
        return self.type


# Main game class
class Game:
    def __init__(self, rows: int, cols: int, numBombs: int) -> None:
        self._numTiles: int = rows * cols
        self._rows: int = rows
        self._cols: int = cols
        self._numBombs: int = numBombs
        self._board: list[Tile] = [Tile() for _ in range(self._numTiles)]
        self._firstClick: bool = True
        self._gameOver: bool = False

    # Method to handle a left click on a tile
    def leftClick(self, index: int) -> None:
        # If its the first click then place bombs
        if self._firstClick:
            self._placeBombs(index)
            self._firstClick = False

        # If its a flag then remove the flag and return
        if self._board[index].isFlagged():
            self._board[index].removeFlag()
            return

        # If the tile is already revealed return early
        if self._board[index].isRevealed():
            return

        # At this point the tile clicked is hidden and not a flag so reveal it
        self._board[index].reveal()

        # If its a bomb set game over to true
        if self._board[index].isBomb():
            self._gameOver = True

        # If there are no connected bombs then reveal the connecting tiles
        if self._board[index].getNumAdjacentBombs() == 0:
            self._revealConnectedTiles(index)

    # Method to handle a right click on a tile
    def rightClick(self, index: int) -> None:
        # If the tile is already revealed return early
        if self._board[index].isRevealed():
            return
        # If its a flag, remove it else add a flag
        self._board[index].toggleFlag()

    # Method to export the game state for decoupling user interface from game logic
    def getBoard(self) -> list[DisplayTile]:
        # Loop over every tile and store it as an enum
        board: list[DisplayTile] = []
        for tile in self._board:
            if tile.isFlagged():
                board.append(DisplayTile(DisplayTileTypes.Flag))
            elif not tile.isRevealed():
                board.append(DisplayTile(DisplayTileTypes.NotRevealed))
            elif tile.isBomb():
                board.append(DisplayTile(DisplayTileTypes.Bomb))
            elif tile.isRevealed() and not tile.isBomb():
                board.append(
                    DisplayTile(DisplayTileTypes.Revealed, tile.getNumAdjacentBombs())
                )
        return board

    # Method to place bombs at start of game
    def _placeBombs(self, startIndex: int) -> None:
        tilesToCheck: list[int] = self._getAdjacentTiles(startIndex)
        tilesToCheck.append(startIndex)
        while self._numBombs > 0:
            index: int = random.randrange(0, self._numTiles)
            while self._board[index].isBomb() or index in tilesToCheck:
                index: int = random.randrange(0, self._numTiles)
            self._board[index].placeBomb()
            self._numBombs -= 1
        self._updateNeighbours()

    # Method to update non-bomb tiles to contain the count of adjacent bombs
    def _updateNeighbours(self) -> None:
        for x in range(self._numTiles):
            if self._board[x].isBomb():
                tilesToCheck: list[int] = self._getAdjacentTiles(x)
                for tile in tilesToCheck:
                    self._board[tile].numAdjacentBombs += 1

    # Method to flood reveal connected, non-bomb tiles
    def _revealConnectedTiles(self, index: int) -> None:
        tilesToCheck: list[int] = self._getAdjacentTiles(index)
        for tile in tilesToCheck:
            if (
                not self._board[tile].isBomb()
                and not self._board[tile].revealed
                and self._board[index].numAdjacentBombs == 0
            ):
                self._board[tile].revealed = True
                self._revealConnectedTiles(tile)

    # Helper method to constuct a list of valid adjacent tile indexes
    def _getAdjacentTiles(self, index: int) -> list[int]:
        tilesToCheck: list = []
        row: int = index // self._cols
        col: int = index % self._cols
        if row != 0:
            tilesToCheck.append(index - self._cols)
        if row != self._rows - 1:
            tilesToCheck.append(index + self._cols)
        if col != 0:
            tilesToCheck.append(index - 1)
        if col != self._cols - 1:
            tilesToCheck.append(index + 1)
        if row != 0 and col != 0:
            tilesToCheck.append(index - self._cols - 1)
        if row != 0 and col != self._cols - 1:
            tilesToCheck.append(index - self._cols + 1)
        if row != self._rows - 1 and col != 0:
            tilesToCheck.append(index + self._cols - 1)
        if row != self._rows - 1 and col != self._cols - 1:
            tilesToCheck.append(index + self._cols + 1)
        return tilesToCheck

    # Method to calculate if the player has won
    def isWon(self) -> bool:
        for x in range(self._numTiles):
            if self._board[x].isBomb():
                if not self._board[x].isFlagged():
                    return False
            else:
                if not self._board[x].isRevealed():
                    return False
        return True

    # Method to check if game is over
    def isGameOver(self) -> bool:
        return self._gameOver
