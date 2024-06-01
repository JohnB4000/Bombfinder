from enum import Enum
import random
from tile import Tile


class DisplayTileTypes(Enum):
    NotRevealed = 0
    Bomb = 1
    Flag = 2
    Revealed = 3


class DisplayTile:
    def __init__(self, type: DisplayTileTypes, adjacentBombs: int = 0):
        self.type: DisplayTileTypes = type
        self._adjacentBombs: int = adjacentBombs

    def getAdjacentCount(self) -> int:
        return self._adjacentBombs

    def getType(self) -> DisplayTileTypes:
        return self.type


class Game:
    def __init__(self, rows: int, cols: int, numBombs: int) -> None:
        self.numTiles: int = rows * cols
        self.rows: int = rows
        self.cols: int = cols
        self.numBombs: int = numBombs
        self.board: list[Tile] = [Tile() for _ in range(self.numTiles)]
        self.firstClick: bool = True
        self.gameOver: bool = False

    def getBoard(self) -> list[DisplayTile]:
        board: list[DisplayTile] = []
        for tile in self.board:
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

    def leftClick(self, index: int) -> None:
        # If its the first click then place bombs
        if self.firstClick:
            self.placeBombs(index)
            self.firstClick = False

        # If its a flag then remove the flag and return
        if self.board[index].isFlagged():
            self.board[index].removeFlag()
            return

        if self.board[index].isRevealed():
            return

        # At this point the tile clicked is hidden and not a flag so reveal it
        self.board[index].reveal()

        # If its a bomb set game over to true
        if self.board[index].isBomb():
            self.gameOver = True

        # If there are no connected bombs then reveal the connecting tiles
        if self.board[index].getNumAdjacentBombs() == 0:
            self.revealConnectedTiles(index)

    def rightClick(self, index: int) -> None:
        if self.board[index].isRevealed():
            return
        # If its a flag, remove it else add a flag
        self.board[index].toggleFlag()

    def placeBombs(self, startIndex: int) -> None:
        tilesToCheck: list[int] = self.getAdjacentTiles(startIndex)
        tilesToCheck.append(startIndex)
        while self.numBombs > 0:
            index: int = random.randrange(0, self.numTiles)
            while self.board[index].isBomb() or index in tilesToCheck:
                index: int = random.randrange(0, self.numTiles)
            self.board[index].placeBomb()
            self.numBombs -= 1
        self.updateNeighbours()

    def updateNeighbours(self) -> None:
        for x in range(self.numTiles):
            if self.board[x].isBomb():
                tilesToCheck: list[int] = self.getAdjacentTiles(x)
                for tile in tilesToCheck:
                    self.board[tile].numAdjacentBombs += 1

    def revealConnectedTiles(self, index: int) -> None:
        tilesToCheck: list[int] = self.getAdjacentTiles(index)
        for tile in tilesToCheck:
            if (
                not self.board[tile].isBomb()
                and not self.board[tile].revealed
                and self.board[index].numAdjacentBombs == 0
            ):
                self.board[tile].revealed = True
                self.revealConnectedTiles(tile)

    def getAdjacentTiles(self, index: int) -> list[int]:
        tilesToCheck: list = []
        row: int = index // self.cols
        col: int = index % self.cols
        if row != 0:
            tilesToCheck.append(index - self.cols)
        if row != self.rows - 1:
            tilesToCheck.append(index + self.cols)
        if col != 0:
            tilesToCheck.append(index - 1)
        if col != self.cols - 1:
            tilesToCheck.append(index + 1)
        if row != 0 and col != 0:
            tilesToCheck.append(index - self.cols - 1)
        if row != 0 and col != self.cols - 1:
            tilesToCheck.append(index - self.cols + 1)
        if row != self.rows - 1 and col != 0:
            tilesToCheck.append(index + self.cols - 1)
        if row != self.rows - 1 and col != self.cols - 1:
            tilesToCheck.append(index + self.cols + 1)
        return tilesToCheck

    def isWon(self) -> bool:
        for x in range(self.numTiles):
            if self.board[x].isBomb():
                if not self.board[x].isFlagged():
                    return False
            else:
                if not self.board[x].isRevealed():
                    return False
        return True

    def isGameOver(self) -> bool:
        return self.gameOver
