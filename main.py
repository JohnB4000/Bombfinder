from userInterface import UserInterface, initInterface

NUM_ROWS = 16
NUM_COLS = 30
NUM_BOMBS = 80

IMAGE_SCALE = 40

ui: UserInterface = initInterface(IMAGE_SCALE)
ui.newGame(NUM_ROWS, NUM_COLS, NUM_BOMBS)
ui.runGame()
