import math
import sys
import pygame
from typing import Protocol
from game import Game, DisplayTile, DisplayTileTypes


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


class Screen(Protocol):
    def __init__(self, *args) -> None: ...
    def update(self, screen: pygame.Surface) -> None: ...
    def handleEvent(self, event: pygame.event.Event) -> None: ...


class UserInterface:
    def __init__(self, imageScale: int, fps: int) -> None:
        self.game: GameScreen | None = None
        self.imageScale: int = imageScale
        self.fps = fps
        width: int = 400
        height: int = 400
        self.screen: pygame.Surface = pygame.display.set_mode((width, height))

    def newGame(self, rows: int, cols: int, numBombs: int):
        self.game = GameScreen(rows, cols, numBombs, self.imageScale)
        self.rows = rows
        self.cols = cols
        width: int = cols * self.imageScale
        height: int = rows * self.imageScale
        self.screen = pygame.display.set_mode((width, height))

    def update(self) -> None:
        if self.game:
            self.game.update(self.screen)
        pygame.display.flip()

    def runGame(self):
        gameOver = False
        while True:
            while not gameOver:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if self.handleEvent(event):
                        gameOver = True
                    self.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def handleEvent(self, event: pygame.event.Event):
        if self.game:
            self.game.handleEvent(event)


def initInterface() -> UserInterface:
    pygame.init()
    pygame.display.set_caption("Bombfinder")
    ui = UserInterface(40, 60)
    return ui


class GameScreen(Screen):
    def __init__(self, rows: int, cols: int, numBombs: int, imageScale: int):
        self._rows: int = rows
        self._cols: int = cols
        self._numBombs: int = numBombs
        self._imageScale: int = imageScale
        self._game: Game = Game(rows, cols, numBombs)

    def update(self, screen: pygame.Surface) -> None:
        self._displayGame(screen, self._game.getBoard())

    def handleEvent(self, event: pygame.event.Event):
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

    def _displayGame(
        self,
        screen: pygame.Surface,
        board: list[DisplayTile],
    ) -> None:
        for index, tile in enumerate(board):
            self._displayTile(
                screen,
                tile,
                (
                    (index % self._cols) * self._imageScale,
                    (index // self._cols) * self._imageScale,
                ),
            )

    def _displayTile(
        self, screen: pygame.Surface, tile: DisplayTile, coordinates: tuple[int, int]
    ) -> None:
        match tile.getType():
            case DisplayTileTypes.NotRevealed:
                screen.blit(Assets.tileAsset, coordinates)
            case DisplayTileTypes.Bomb:
                screen.blit(Assets.bombAsset, coordinates)
            case DisplayTileTypes.Flag:
                screen.blit(Assets.flagAsset, coordinates)
            case DisplayTileTypes.Revealed:
                screen.blit(Assets.numbersAsset[tile.getAdjacentCount()], coordinates)

    def _getIndexFromClick(self, position: tuple[int, int]) -> int:
        return (
            math.floor(position[0] / self._imageScale)
            + math.floor(position[1] / self._imageScale) * self._cols
        )
