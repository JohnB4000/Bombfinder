import pygame, sys, board
from typing import Type


pygame.init()

width: int = board.Board.cols * board.Board.imageScale
height: int = board.Board.rows * board.Board.imageScale
fps: int = 60

gameRunning: bool = True
gameOver: bool = False

screen: pygame.Surface = pygame.display.set_mode((width, height))
pygame.display.set_caption('Minesweeper')

clock: pygame.time.Clock = pygame.time.Clock()

boardObject: board.Board = board.Board(screen)

def refresh() -> None:
    boardObject.display()
    pygame.display.flip()
    clock.tick(fps)

def mouseClick(mouseButton: int) -> bool:
    wasMine: bool = False
    if mouseButton == 1:
        wasMine = boardObject.leftClickedSquare() 
    elif mouseButton== 3:
        boardObject.rightClickedSquare()
    gameFinished = boardObject.checkForGameFinished()
    return wasMine or gameFinished
    
while gameRunning:
    while not gameOver:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                gameEnded = mouseClick(event.button)
                if gameEnded:
                    print("Game Over")
                    gameOver = True
                        
        refresh()
    refresh()
