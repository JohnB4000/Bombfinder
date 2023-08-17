import board, pygame
from typing import Tuple


class Square:
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.isMine: bool = False
        self.numAdjacentMines: int = 0
        self.revealed: bool = False
        self.isFlag: bool = False

    def display(self, coordinate: Tuple[int]) -> None:
        if not self.revealed:
            if self.isFlag:
                self.screen.blit(board.Board.flag, coordinate)
            else:
                self.screen.blit(board.Board.tile, coordinate)
        elif self.isMine:
            self.screen.blit(board.Board.mine, coordinate)
        else:
            self.screen.blit(board.Board.numbers[self.numAdjacentMines], coordinate)

    def reveal(self) -> bool:
        self.revealed: bool = True
        if self.isMine:
            return True
        return False