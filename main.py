import pygame, sys, math
from board import Board, MouseClickTypes

pygame.init()

# TODO Mode constants to config file
width: int = Board.cols * Board.imageScale
height: int = Board.rows * Board.imageScale
fps: int = 60

programActive: bool = True
gameActive: bool = False

screen: pygame.Surface = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bombfinder")

clock: pygame.time.Clock = pygame.time.Clock()

game: Board = Board(screen)


def refreshProgram() -> None:
    game.display()
    pygame.display.flip()
    clock.tick(fps)


def getIndexFromClick(position: tuple[int, int]) -> int:
    x, y = position
    return (
        math.floor(x / Board.imageScale) + math.floor(y / Board.imageScale) * Board.cols
    )


def handleEvent(event):
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            game.handleMouseClick(
                MouseClickTypes.LeftClick, getIndexFromClick(pygame.mouse.get_pos())
            )
        elif event.button == 3:
            game.handleMouseClick(
                MouseClickTypes.RightClick, getIndexFromClick(pygame.mouse.get_pos())
            )
        if game.isGameOver():
            print("Game Over")
            return True
        if game.isWon():
            print("You win")
        return False


while programActive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if handleEvent(event):
            gameOver = True
    refreshProgram()
