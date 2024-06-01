import pygame, square, random

class MouseClickTypes:
    LeftClick: int = 0
    RightClick: int = 1

class Board:
    tile: pygame.Surface = pygame.transform.scale(pygame.image.load('assets/tile.png'), (40, 40))
    mine: pygame.Surface = pygame.transform.scale(pygame.image.load('assets/mine.png'), (40, 40))
    flag: pygame.Surface = pygame.transform.scale(pygame.image.load('assets/flag.png'), (40, 40))
    numbers: list[pygame.Surface] = [pygame.transform.scale(pygame.image.load('assets/' + str(x) + '.png'), (40, 40)) for x in range(0, 9)]
    # TODO Mode to configuration file
    rows: int = 16
    cols: int = 30
    cells: int = rows * cols
    firstClick: bool = True

    imageScale: int = 40

    minesToPlace: int = cells // 10

    gameOver: bool = False

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.board: list[square.Square] = [square.Square(screen) for _ in range(self.cells)]

    def display(self) -> None:
        for x in range(self.cells):
            self.board[x].display(((x % self.cols) * self.imageScale, (x // self.cols) * self.imageScale))

    def leftClickedSquare(self, index: int) -> None:
        # If its the first click then place mines
        if self.firstClick:
            self.placeMines(index)
            self.firstClick = False
        
        # If its a flag then remove the flag and return
        if self.board[index].isFlagged():
            self.board[index].removeFlag()
            return

        # At this point the square clicked is hidden and not a flag so reveal it
        self.board[index].reveal()

        # If its a mine set game over to true
        if self.board[index].isMine():
            self.gameOver = True
        
        # If there are no connected mines then reveal the connecting squares
        if self.board[index].numAdjacentMines == 0:
            self.revealConnectedSquares(index)

    def placeMines(self, startIndex: int) -> None:
        squaresToCheck: list[int] = self.getAdjacentSquares(startIndex)
        squaresToCheck.append(startIndex)
        while self.minesToPlace > 0:
            index: int = random.randrange(0, self.cells)
            while self.board[index].isMine() or index in squaresToCheck:
                index: int = random.randrange(0, self.cells)
            self.board[index].placeMine()
            self.minesToPlace -= 1
        self.updateNeighbours()

    def updateNeighbours(self) -> None:
        for x in range(self.cells):
            if self.board[x].isMine():
                squaresToCheck: list[int] = self.getAdjacentSquares(x)
                for square in squaresToCheck:
                    self.board[square].numAdjacentMines += 1

    def revealConnectedSquares(self, index: int) -> None:
        squaresToCheck: list[int] = self.getAdjacentSquares(index)
        for square in squaresToCheck:
            if not self.board[square].isMine() and not self.board[square].revealed and self.board[index].numAdjacentMines == 0:
                self.board[square].revealed = True
                self.revealConnectedSquares(square)

    def getAdjacentSquares(self, index: int) -> list[int]:
        squaresToCheck: list = []
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
    
    def isWon(self) -> bool:
        for x in range(self.cells):
            if self.board[x].isMine():
                if not self.board[x].isFlagged():
                    return False
            else:
                if not self.board[x].isRevealed():
                    return False
        return True
    
    def handleMouseClick(self, mouseButton: int, index: int) -> None:
        # If its already revealed then return
        if self.board[index].isRevealed():
            return

        if mouseButton == MouseClickTypes.LeftClick:
            self.leftClickedSquare(index)
        elif mouseButton == MouseClickTypes.RightClick:
            # If its a flag, remove it else add a flag
            self.board[index].toggleFlag()

    def isGameOver(self) -> bool:
        return self.gameOver