import pygame
import random

pygame.init()
pygame.display.set_caption("Petals Around the Rose")
screen = pygame.display.set_mode((800,600))

font = pygame.font.SysFont(None, 30)

COLORS = {
    "pastelPink": (255,203,203),
    "red": (255,0,0)
}

# Cool helper functions
centerVertically = lambda surface: (screen.get_width() / 2) - (surface.get_width() / 2)
centerHorizontally = lambda surface: (screen.get_height() / 2) - (surface.get_height() / 2)

# Classes to handle screens below:
class ScreenManager():
    def __init__(self) -> None:
        self.screens = {}
        self.currentScreen = None

    def registerScreen(self, name, screenObject):
        self.screens[name] = screenObject

    def navigate(self, screenName):
        if screenName not in self.screens:
            return Exception("Invalid screenName")
        
        self.currentScreen = screenName

    def draw(self, screen):
        # If no screens are registered, don't crash, just don't draw anything.
        if len(self.screens) == 0: return 
        # If no currentScreen, set the currentScreen to the first one that is registered.
        if self.currentScreen == None:
            self.currentScreen = list(self.screens.keys())[0]

        self.screens[self.currentScreen].draw(screen)
    
class WelcomeScreen():
    def __init__(self) -> None:
        self.titleFont = pygame.font.Font(None, 50)

    def draw(self, screen):
        titleText = self.titleFont.render("Petals Around the Rose", True, COLORS["red"])
        subText = font.render("the worst thing i have ever played", True, COLORS["red"])
        spaceToPlayText = font.render("Press space to play.", True, COLORS["red"])

        screen.blit(titleText, (centerVertically(titleText), 200))
        screen.blit(subText, (centerVertically(subText), 250))
        screen.blit(spaceToPlayText, (centerVertically(spaceToPlayText), 300))

class GameScreen():
    def __init__(self) -> None:
        self.gameLogic = PetalsGame()
        self.gameLogic.rollDice()
        self.inputText = ""

    def handleKeyDown(self, e):
        if e.key == pygame.K_BACKSPACE: 
            self.inputText = self.inputText[:-1]
            return
        
        elif e.key == pygame.K_RETURN:
            if len(self.inputText) == 0: return
            inputInt = int(self.inputText)
            isCorrect = self.gameLogic.checkAnswer(inputInt)

            if not isCorrect: self.gameLogic.new()
            
            self.gameLogic.rollDice()
            self.inputText = ""
            return
            
        if not e.unicode.isdigit(): return
        self.inputText += e.unicode

    def draw(self, screen):
        streakText = font.render(f"Streak: {self.gameLogic.currentStreak}", False, COLORS["red"])
        screen.blit(streakText, (
            screen.get_width() - streakText.get_width() - 25,
            25)
        )

        for diceIndex, dice in enumerate(self.gameLogic.dice):
            diceImage = pygame.image.load(f"./dice/{dice}.png").convert_alpha()
            screen.blit(diceImage, (180 + (1 + diceIndex * 75), 250))

        instructionsText = font.render("Enter your answer using your keyboard. Press enter to submit.", False, COLORS["red"])
        screen.blit(
            instructionsText,
            (centerVertically(instructionsText), 320)
        )

        inputText = font.render(self.inputText, False, (0,0,0))
        screen.blit(inputText, (centerVertically(inputText), 350))

class GameOverScreen():
    def __init__(self) -> None:
        pass

    def draw(self):
        pass

        

# Game logic classes
class PetalsGame():
    def __init__(self) -> None:
        self.currentStreak = 0
        self.dice = []
        self.correctAnswer = 0
        self.correctSound = pygame.mixer.Sound("correct.mp3")
        self.wrongSound = pygame.mixer.Sound("wrong.mp3")

    def new(self):
        self.currentStreak = 0

    def rollDice(self):
        # Make sure these are reset.
        self.dice = []
        self.correctAnswer = 0
        for _ in range(6):
            diceNumber = random.randint(1,6)
            if diceNumber == 3:
                self.correctAnswer += 2
            if diceNumber == 5:
                self.correctAnswer += 4

            self.dice.append(diceNumber)
        return self.dice

    def checkAnswer(self, answer) -> bool:
        if answer == self.correctAnswer:
            self.currentStreak += 1
            pygame.mixer.Sound.play(self.correctSound)
            return True
        else:
            self.currentStreak = 0
            pygame.mixer.Sound.play(self.wrongSound)
            return False
        

gameRunning = True

screenManager = ScreenManager()
screenManager.registerScreen("Welcome", WelcomeScreen())
screenManager.registerScreen("Game", GameScreen())

while gameRunning:
    # Using this to handle navigation and inputs.
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            gameRunning = False
        
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and screenManager.currentScreen == "Welcome":
                screenManager.navigate("Game")

            elif screenManager.currentScreen == "Game": screenManager.screens[screenManager.currentScreen].handleKeyDown(e)

    screen.fill(COLORS["pastelPink"])

    # Anything UI from this point will be handled by the ScreenManager.

    screenManager.draw(screen)

    pygame.display.flip()