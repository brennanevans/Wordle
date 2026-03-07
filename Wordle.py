import pygame,urllib3,math,time

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

class Box():
    # Default letter and colour arguments used for empty boxes - before guesses
    def __init__(self,row:int,col:int,letter="",colour="#D3D6DA"):
        self.row = row
        self.col = col
        self.letter = letter
        self.colour = colour

        self.surface = pygame.Surface((0,0))
        self.topLeft = (0,0)
    def __repr__(self):
        return f"Row:{self.row},Col:{self.col},Letter:{self.letter}"
    
    def updateLetter(self):
        if self.colour != "#D3D6DA":
            letterColour = "White"
        else:
            letterColour = "Black"

        boxWidth = self.surface.get_rect().width
        boxHeight = self.surface.get_rect().height

        font = pygame.font.SysFont('arial',boxWidth,True)
        textSurface = font.render(self.letter,0,letterColour)
        textWidth = textSurface.get_rect().width
        textHeight = textSurface.get_rect().height

        self.surface.fill(self.colour)
        self.surface.blit(textSurface,((boxWidth-textWidth)/2,((boxHeight-textHeight)/2)))

class BoxGrid():
    def __init__(self,rows,cols):
        # Max rows = 12
        # Max cols = 10
        self.rows = rows
        self.cols = cols
        self.gridArray = []
    
        for i in range(rows):
            rowList = []
            for j in range(cols):
                rowList.append(Box(i,j))
            self.gridArray.append(rowList)

    def updateLetters(self):
        for row in self.gridArray:
            for box in row:
                box.updateLetter()  

class KeyboardGrid():
    def __init__(self):
        self.surface = pygame.Surface((0,0))

        letterOrder = ["Q","W","E","R","T","Y","U","I","O","P","A","S","D",
                       "F","G","H","J","K","L","Z","X","C","V","B","N","M"]
        self.gridArray = []
        self.letterDictionary = {}
        rowLengths = [10,9,7]
        
        letterIndex = 0
        rowIndex = 0
        for rowLength in rowLengths:
            row = []
            for col in range(rowLength):
                box = Box(row,col,letterOrder[letterIndex],"#D3D6DA")
                row.append(box)
                self.letterDictionary[letterOrder[letterIndex]] = box
                letterIndex += 1
            self.gridArray.append(row)
            rowIndex += 1 
    
    def updateLetters(self):
        for row in self.gridArray:
            for box in row:
                box.updateLetter()

class Screen():
    def __init__(self,width:int,height:int):
        min_height = 500
        min_width = width / height * 500

        self.width = max(min_width,width)
        self.height = max(min_height,height)

        #,pygame.SCALED
        self.surface = pygame.display.set_mode((self.width,self.height))
        self.surface.fill("black")

        self.fullScreen = False

    def setUpKeyboard(self,keyboard:KeyboardGrid):
        numOfCols = len(keyboard.gridArray[0])
        numOfRows = 3

        PADDING = 5

        #Min of 25 padding each side
        xSpaceLeft = self.width - 50 - (PADDING*(numOfCols-1))
        potentialWidth = xSpaceLeft/numOfCols

        BOX_SIZE = min(math.floor(potentialWidth),50)

        xSpaceLeft -= BOX_SIZE*numOfCols
        y = self.height - 25 - (numOfRows * BOX_SIZE) - ((numOfRows-1) * PADDING)
        
        for row in keyboard.gridArray:
            xSpaceLeft = self.width - 50 - (PADDING*(numOfCols-1))
            numOfCols = len(row)
            xSpaceLeft -= BOX_SIZE*numOfCols
            x = xSpaceLeft/2 + 25 # Add half minimum padding = padding from left
            for box in row:
                box.surface = pygame.Surface((BOX_SIZE,BOX_SIZE))
                box.surface.fill(box.colour)
                box.topLeft = (x,y)
                self.surface.blit(box.surface,box.topLeft)
                x += BOX_SIZE + PADDING
            y += BOX_SIZE + PADDING
        return self.height - 25 - (numOfRows * BOX_SIZE) - ((numOfRows-1) * PADDING)

    def setUpBoxes(self,grid:BoxGrid,keyboardStartY:int):
        numOfRows = len(grid.gridArray)
        numOfCols = len(grid.gridArray[0])

        PADDING = 5

        #Min of 25 padding each side
        xSpaceLeft = self.width - 50 - (PADDING*(numOfCols-1))
        potentialWidth = xSpaceLeft/numOfCols

        #Min of 25 padding from each side
        ySpaceLeft = keyboardStartY - 50 - (PADDING*(numOfRows-1))
        potentialHeight = ySpaceLeft/numOfRows

        # Need to decide whether to add a max size (dont actually seem to need one)

        # potentialSize = min(potentialWidth,potentialHeight)
        # BOX_SIZE = min(potentialSize,200)

        BOX_SIZE = min(potentialWidth,potentialHeight)
        BOX_SIZE = math.floor(BOX_SIZE)

        xSpaceLeft -= BOX_SIZE*numOfCols
        ySpaceLeft -= BOX_SIZE*numOfRows

        y = math.floor(ySpaceLeft/2 + 25) # Add half minimum padding = padding from top
        
        for row in grid.gridArray:
            x = xSpaceLeft/2 + 25 # Add half minimum padding = padding from left
            for box in row:
                box.surface = pygame.Surface((BOX_SIZE,BOX_SIZE))
                box.surface.fill(box.colour)
                box.topLeft = (x,y)
                self.surface.blit(box.surface,box.topLeft)
                x += BOX_SIZE + PADDING
            y += BOX_SIZE + PADDING

    def setUp(self,grid,keyboard):
        keyboardStartY = self.setUpKeyboard(keyboard)
        self.setUpBoxes(grid,keyboardStartY)

    def updateScreen(self,grid:BoxGrid,keyboard:KeyboardGrid):
        for row in grid.gridArray:
            for box in row:
                self.surface.blit(box.surface,box.topLeft)
        grid.updateLetters()
        
        for row in keyboard.gridArray:
            for box in row:
                self.surface.blit(box.surface,box.topLeft)
        keyboard.updateLetters()

class Notification():
    notifcationList = []

    def __init__(self,lifespanSeconds:int,text,fontSize,textColour,bgColour):
        font = pygame.font.SysFont('arial',fontSize,True)
        self.textSurface = font.render(text,0,textColour,bgColour)

        self.width = self.textSurface.get_rect().width
        self.height = self.textSurface.get_rect().height

        self.creationTime = -1
        self.lifespan = lifespanSeconds
        self.screenSurface = pygame.surface.Surface((0,0))

    def displayNotification(self,screen:Screen,verticalAllignment="top"):
        if verticalAllignment == "top":
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self.width)/2,0))
        elif verticalAllignment == "center":
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self.width)/2,(screen.height-self.width)/2))
        elif verticalAllignment == "bottom":
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self.width)/2,(screen.height-self.height)))
        else:
            # Default to top 
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self.width)/2,0))
        
        self.creationTime = time.time()
        self.screenSurface = screen.surface
        Notification.notifcationList.append(self)
        
    def checkLifespan(self):
        if self.creationTime + (self.lifespan) <= time.time():
            self.screenSurface.fill("Black",self.rect)
            Notification.notifcationList.remove(self)

def isRealWord(guess):
    URL = "https://api.dictionaryapi.dev/api/v2/entries/en/" + guess.lower()

    resp = urllib3.request("GET", URL)
    if type(resp.json()) == list:
        return True
    else:
        return False

def calculateColours(currentRow,keyboard:KeyboardGrid,guess,answer):
    # #787C7E= Not there, #C9B458= There but wrong place, #6AAA64= Correct
    lettersLeft = [*answer]

    for index in range(len(guess)):
        letter = guess[index]
        if letter == answer[index]:
            currentRow[index].colour = "#6AAA64"
            keyboard.letterDictionary.get(letter.upper()).colour = "#6AAA64"
            lettersLeft.remove(letter)

    for index in range(len(guess)):
        letter = guess[index]
        if letter in lettersLeft and currentRow[index].colour != "#6AAA64":
            currentRow[index].colour = "#C9B458"
            if keyboard.letterDictionary.get(letter.upper()).colour != "#6AAA64":
                keyboard.letterDictionary.get(letter.upper()).colour = "#C9B458"

            lettersLeft.remove(letter)
        elif currentRow[index].colour != "#6AAA64":
            currentRow[index].colour = "#787C7E"
            if keyboard.letterDictionary.get(letter.upper()).colour != "#6AAA64":
                keyboard.letterDictionary.get(letter.upper()).colour = "#787C7E"
            
def generateWord(wordLength,difficulty):
    # Get 10 words incase some not accepted by real word tester
    URL = f"https://random-word-api.herokuapp.com/word?number=10&length={wordLength}&diff={difficulty}"
    while True:
        resp = urllib3.request("GET", URL)
        wordList = resp.json()
        for word in wordList:
            if isRealWord(word):
                return(word)

monitorWidth,monitorHeight = pygame.display.get_desktop_sizes()[0]
gameScreen = Screen(monitorWidth-50,monitorHeight-100)

gameGrid = BoxGrid(10,8)
gameKeyboard = KeyboardGrid()
gameScreen.setUp(gameGrid,gameKeyboard)

GAME_DIFFICULTY = 3 #1 = Easy, 5 = Hard
WORD_TO_GUESS = generateWord(gameGrid.cols,GAME_DIFFICULTY)

currentRowIndex = 0
allowInputs = True
running = True
while running:
    x,y = pygame.mouse.get_pos()
    currentRow = gameGrid.gridArray[currentRowIndex]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                for box in reversed(currentRow):
                    if box.letter == "":
                        continue
                    else:
                        box.letter = ""
                        break
            
            elif event.key == pygame.K_RETURN:
                guess = ""
                for box in currentRow:
                    guess += box.letter.lower()

                if len(guess) < len(WORD_TO_GUESS):
                    tooShortNotification = Notification(1,"Not all boxes filled.",20,"Black","White")
                    tooShortNotification.displayNotification(gameScreen)
                
                elif guess == WORD_TO_GUESS:
                    #Win
                    calculateColours(currentRow,gameKeyboard,guess,WORD_TO_GUESS)
                    winNotification = Notification(3,f"Congrats!!! You guessed the word in {currentRowIndex+1} tries.",20,"Black","White")
                    winNotification.displayNotification(gameScreen)

                    allowInputs = False
                    
                elif isRealWord(guess):
                    calculateColours(currentRow,gameKeyboard,guess,WORD_TO_GUESS)

                    currentRowIndex += 1
                    if currentRowIndex >= gameGrid.rows:
                        #Loss
                        lossNotification = Notification(3,f"Unlucky, the word was {WORD_TO_GUESS.upper()}.",20,"Black","White")
                        lossNotification.displayNotification(gameScreen)

                        currentRowIndex = 0
                        allowInputs = False

                else:
                    notRealNotification = Notification(1,"Word not in word list.",20,"Black","White")
                    notRealNotification.displayNotification(gameScreen)

            elif event.unicode.isalpha():
                for box in currentRow:
                    if box.letter == "":
                        box.letter = event.unicode.upper()  
                        break
    
    for notification in Notification.notifcationList:
        notification.checkLifespan()

    gameScreen.updateScreen(gameGrid,gameKeyboard)
    pygame.display.update()
    clock.tick(20)

pygame.quit()

# Write documentation
# Commit to repository - gameLibrary