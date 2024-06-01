import math
import sys
import pygame
from game import Game, DisplayTile, DisplayTileTypes


# Class to store the assets
class Assets:
    tileAsset: pygame.Surface = pygame.transform.scale(
        pygame.image.load("assets/tile.png"), (40, 40)
    )
    bombAsset: pygame.Surface = pygame.transform.scale(
        pygame.image.load("assets/mine.png"), (40, 40)
    )
    flagAsset: pygame.Surface = pygame.transform.scale(
        pygame.image.load("assets/flag.png"), (40, 40)
    )
    numbersAsset: list[pygame.Surface] = [
        pygame.transform.scale(pygame.image.load("assets/" + str(x) + ".png"), (40, 40))
        for x in range(0, 9)
    ]


# Main user interface class
class UserInterface:
    def __init__(self, imageScale: int) -> None:
        self._game: GameScreen | None = None
        self._imageScale: int = imageScale
        self._screen: pygame.Surface = pygame.display.set_mode((400, 400))

    def newGame(self, rows: int, cols: int, numBombs: int):
        self._game = GameScreen(self._screen, rows, cols, numBombs, self._imageScale)
        self.rows: int = rows
        self.cols: int = cols
        width: int = cols * self._imageScale
        height: int = rows * self._imageScale
        self._screen = pygame.display.set_mode((width, height))

    def runGame(self):
        if self._game:
            self._game.runGame()


# Game screen class
class GameScreen:
    def __init__(
        self,
        screen: pygame.Surface,
        rows: int,
        cols: int,
        numBombs: int,
        imageScale: int,
    ):
        self._screen: pygame.Surface = screen
        self._rows: int = rows
        self._cols: int = cols
        self._numBombs: int = numBombs
        self._imageScale: int = imageScale
        self._game: Game = Game(rows, cols, numBombs)

    # Main game loop
    def runGame(self):
        gameOver: bool = False
        while True:
            while not gameOver:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if self._handleEvent(event):
                        gameOver = True
                    self._displayGame(self._game.getBoard())
                    pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # Method to handle user input
    def _handleEvent(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._game.leftClick(self._getIndexFromClick(pygame.mouse.get_pos()))
            elif event.button == 3:
                self._game.rightClick(self._getIndexFromClick(pygame.mouse.get_pos()))
            if self._game.isGameOver():
                print("Game Over")
                return True
            if self._game.isWon():
                print("You win")
            return False

    # Method to display the game to the user
    def _displayGame(
        self,
        board: list[DisplayTile],
    ) -> None:
        for index, tile in enumerate(board):
            coordinates: tuple[int, int] = (
                (index % self._cols) * self._imageScale,
                (index // self._cols) * self._imageScale,
            )
            match tile.getType():
                case DisplayTileTypes.NotRevealed:
                    self._screen.blit(Assets.tileAsset, coordinates)
                case DisplayTileTypes.Bomb:
                    self._screen.blit(Assets.bombAsset, coordinates)
                case DisplayTileTypes.Flag:
                    self._screen.blit(Assets.flagAsset, coordinates)
                case DisplayTileTypes.Revealed:
                    self._screen.blit(
                        Assets.numbersAsset[tile.getAdjacentCount()], coordinates
                    )

    # Helper method to convert a mouse position to a index
    def _getIndexFromClick(self, position: tuple[int, int]) -> int:
        return (
            math.floor(position[0] / self._imageScale)
            + math.floor(position[1] / self._imageScale) * self._cols
        )


# Function to create the user interface
def initInterface(imageScale: int) -> UserInterface:
    pygame.init()
    pygame.display.set_caption("Bombfinder")
    ui = UserInterface(imageScale)
    return ui
