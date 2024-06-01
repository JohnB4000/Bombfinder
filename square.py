import board, pygame

class Square:
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.mine: bool = False
        self.numAdjacentMines: int = 0
        self.revealed: bool = False
        self.isFlag: bool = False

    def display(self, coordinate: tuple[int, int]) -> None:
        if not self.revealed:
            if self.isFlag:
                self.screen.blit(board.Board.flag, coordinate)
            else:
                self.screen.blit(board.Board.tile, coordinate)
        elif self.mine:
            self.screen.blit(board.Board.mine, coordinate)
        else:
            self.screen.blit(board.Board.numbers[self.numAdjacentMines], coordinate)

    def reveal(self) -> bool:
        self.revealed: bool = True
        if self.mine:
            return True
        return False
    
    def isFlagged(self) -> bool:
        return self.isFlag
    
    def removeFlag(self) -> None:
        self.isFlag = False

    def isMine(self) -> bool:
        return self.mine
    
    def placeMine(self) -> None:
        self.mine = True

    def isRevealed(self) -> bool:
        return self.revealed
    
    def toggleFlag(self) -> None:
        self.isFlag = False if self.isFlag else True