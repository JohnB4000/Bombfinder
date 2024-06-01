class Tile:
    def __init__(self):
        self.bomb: bool = False
        self.numAdjacentBombs: int = 0
        self.revealed: bool = False
        self.isFlag: bool = False

    def reveal(self) -> bool:
        self.revealed: bool = True
        if self.bomb:
            return True
        return False

    def isFlagged(self) -> bool:
        return self.isFlag

    def removeFlag(self) -> None:
        self.isFlag = False

    def isBomb(self) -> bool:
        return self.bomb

    def placeBomb(self) -> None:
        self.bomb = True

    def isRevealed(self) -> bool:
        return self.revealed

    def toggleFlag(self) -> None:
        self.isFlag = False if self.isFlag else True

    def getNumAdjacentBombs(self) -> int:
        return self.numAdjacentBombs
