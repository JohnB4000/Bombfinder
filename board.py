import pygame, square, math, random
from typing import List


class Board:
    tile: pygame.Surface = pygame.transform.scale(pygame.image.load('assets/tile.png'), (40, 40))
    mine: pygame.Surface = pygame.transform.scale(pygame.image.load('assets/mine.png'), (40, 40))
    flag: pygame.Surface = pygame.transform.scale(pygame.image.load('assets/flag.png'), (40, 40))
    numbers: List[pygame.Surface] = [pygame.transform.scale(pygame.image.load('assets/blank.png'), (40, 40)),
                pygame.transform.scale(pygame.image.load('assets/1.png'), (40, 40)),
                pygame.transform.scale(pygame.image.load('assets/2.png'), (40, 40)),
                pygame.transform.scale(pygame.image.load('assets/3.png'), (40, 40)),
                pygame.transform.scale(pygame.image.load('assets/4.png'), (40, 40)),
                pygame.transform.scale(pygame.image.load('assets/5.png'), (40, 40)),
                pygame.transform.scale(pygame.image.load('assets/6.png'), (40, 40)),
                pygame.transform.scale(pygame.image.load('assets/7.png'), (40, 40)),
                pygame.transform.scale(pygame.image.load('assets/8.png'), (40, 40)) ]
    rows: int = 16
    cols: int = 30
    cells: int = rows * cols
    firstClick: bool = True

    imageScale: int = 40

    minesToPlace: int = cells / 10

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.board: List[square.Square] = [square.Square(screen) for _ in range(self.cells)]

    def display(self) -> None:
        for x in range(self.cells):
            self.board[x].display(((x % self.cols) * self.imageScale, (x // self.cols) * self.imageScale))

    def leftClickedSquare(self) -> bool:
        index: int = self.getIndexFromClick(pygame.mouse.get_pos())
        if self.firstClick:
            self.placeMines(index)
            self.firstClick = False
        if self.board[index].revealed:
            return False
        if self.board[index].isFlag:
            self.board[index].isFlag = False
            return False
        wasMine = self.board[index].reveal()
        if wasMine:
            return True
        if self.board[index].numAdjacentMines == 0:
            self.revealConnectedSquares(index)
        return False

    def rightClickedSquare(self) -> None:
        index: int = self.getIndexFromClick(pygame.mouse.get_pos())
        if self.board[index].revealed:
            return
        if self.board[index].isFlag:
            self.board[index].isFlag = False
        else:
            self.board[index].isFlag = True
        
    def getIndexFromClick(self, position: int) -> int:
        x: int = position[0]
        y: int = position[1]
        return math.floor(x/self.imageScale) + math.floor(y/self.imageScale) * self.cols

    def placeMines(self, startIndex: int) -> None:
        squaresToCheck: List[int] = self.getAdjacentSquares(startIndex)
        squaresToCheck.append(startIndex)
        while self.minesToPlace > 0:
            index: int = random.randrange(0, self.cells)
            while self.board[index].isMine or index in squaresToCheck:
                index: int = random.randrange(0, self.cells)
            self.board[index].isMine = True
            self.minesToPlace -= 1
        self.updateNeighbours()

    def updateNeighbours(self) -> None:
        for x in range(self.cells):
            if self.board[x].isMine:
                squaresToCheck: List[int] = self.getAdjacentSquares(x)
                for square in squaresToCheck:
                    self.board[square].numAdjacentMines += 1

    def revealConnectedSquares(self, index: int) -> None:
        squaresToCheck: List[int] = self.getAdjacentSquares(index)
        for square in squaresToCheck:
            if not self.board[square].isMine and not self.board[square].revealed and self.board[index].numAdjacentMines == 0:
                self.board[square].revealed = True
                self.revealConnectedSquares(square)

    def getAdjacentSquares(self, index: int) -> List[int]:
        squaresToCheck: List = []
        row: int = index // self.cols
        col: int = index % self.cols
        if row != 0:
            squaresToCheck.append(index-self.cols)
        if row != self.rows-1:
            squaresToCheck.append(index+self.cols)
        if col != 0:
            squaresToCheck.append(index-1)
        if col != self.cols-1:
            squaresToCheck.append(index+1)
        if row != 0 and col != 0:
            squaresToCheck.append(index-self.cols-1)
        if row != 0 and col != self.cols-1:
            squaresToCheck.append(index-self.cols+1)
        if row != self.rows-1 and col != 0:
            squaresToCheck.append(index+self.cols-1)
        if row != self.rows-1 and col != self.cols-1:
            squaresToCheck.append(index+self.cols+1)
        return squaresToCheck
    
    def checkForGameFinished(self) -> bool:
        for x in range(self.cells):
            if self.board[x].isMine:
                if not self.board[x].isFlag:
                    return False
            else:
                if not self.board[x].revealed:
                    return False
        return True