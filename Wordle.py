import pygame,urllib3,math,time

pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

class Box():
    """
    The boxes which make up the guessing grid and keyboard.

    Attributes:
        row: The row on which the box is found.
        col: The column in which the box is found.
        letter: The letter the box contains.
        colour: The hex colour of the box which indicates its letter's
          correctness.
        rect (pygame.Rect): The coordinates, width and height of the box
    """
    def __init__(self,row:int,col:int,letter="",colour="#D3D6DA"):
        self.row = row
        self.col = col
        self.letter = letter
        self.colour = colour

        self._surface = pygame.Surface((0,0))
        self.rect = pygame.Rect(0,0,0,0)

    def __repr__(self):
        return f"Row:{self.row},Col:{self.col},Letter:{self.letter}"
    
    def updateLetter(self):
        """
        Updates the letter displayed in this box.
        
        Changes the letters displayed to reflect the current value of each 
        box's letter attribute. The letter's colour will change to white for
        any box whose colour isn't default (#D3D6DA).
        """
        if self.colour == "#D3D6DA":
            letterColour = "Black"
        else:
            letterColour = "White"

        boxWidth = self.rect.width
        boxHeight = self.rect.height

        font = pygame.font.SysFont('arial',boxWidth,True)
        textSurface = font.render(self.letter,0,letterColour)
        textWidth = textSurface.get_rect().width
        textHeight = textSurface.get_rect().height

        self._surface.fill(self.colour)
        self._surface.blit(textSurface,((boxWidth-textWidth)/2,((boxHeight-textHeight)/2)))
    
    def display(self,screenSurface:pygame.Surface):
        """
        Updates the box's surface and displays it on screen.
        
        Args:
            screenSurface: The surface on which to add the box.
        """
        self._surface = pygame.Surface((self.rect.width,self.rect.height))
        self._surface.fill(self.colour)
        screenSurface.blit(self._surface,self.rect)

class BoxGrid():
    """
    The grid of boxes which display player guesses.

    Attributes:
        rows: The amount of rows in the grid.
        cols: The amount of columns in the grid.
        gridArray (list): A grid of box objects.
    """
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
        """
        Updates the letters displayed in the boxes in the grid.
        """
        for row in self.gridArray:
            for box in row:
                box.updateLetter() 

    def _setUp(self,screenSurface:pygame.Surface,keyboardStartY:int):
        """
        Creates the box grid on screen.

        Args:
            screenSurface: The surface on which the keyboard should be added.
            keyboardStartY: The The y coordinate of the top of the keyboard.
        """
        PADDING = 5

        #Min of 25 padding each side
        xSpaceLeft = screenSurface.get_width() - 50 - (PADDING*(self.cols-1))
        potentialWidth = xSpaceLeft/self.cols

        #Min of 25 padding from each side
        ySpaceLeft = keyboardStartY - 50 - (PADDING*(self.rows-1))
        potentialHeight = ySpaceLeft/self.rows

        BOX_SIZE = math.floor(min(potentialWidth,potentialHeight))

        xSpaceLeft -= BOX_SIZE*self.cols
        ySpaceLeft -= BOX_SIZE*self.rows

        y = math.floor(ySpaceLeft/2 + 25) # Add half minimum padding = padding from top
        for row in self.gridArray:
            x = xSpaceLeft/2 + 25 # Add half minimum padding = padding from left

            for box in row:
                box.rect = pygame.Rect(x,y,BOX_SIZE,BOX_SIZE)
                box.display(screenSurface)

                x += BOX_SIZE + PADDING
            y += BOX_SIZE + PADDING 

class KeyboardGrid():
    """
    The grid of boxes which make up a keyboard.

    Attributes:
        gridArray (list): A grid of box objects.
        letterDictionary (dict): A mapping of each letter in the alphabet to
          the box object in the keyboard which contains it.
    """
    def __init__(self):
        self._surface = pygame.Surface((0,0))

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
        """
        Updates the letters displayed in the boxes in the keyboard.
        """
        for row in self.gridArray:
            for box in row:
                box.updateLetter()

    def _setUp(self,screenSurface:pygame.Surface):
        """
        Creates the keyboard on screen.

        Args:
            screenSurface: The surface on which the keyboard should be added.

        Returns:
            int: The y coordinate of the top of the keyboard.
        """
        numOfCols = len(self.gridArray[0])
        numOfRows = 3

        PADDING = 5

        #Min of 25 padding each side
        initalXSpaceLeft = screenSurface.get_width() - 50 - (PADDING*(numOfCols-1))
        potentialWidth = initalXSpaceLeft/numOfCols

        BOX_SIZE = min(math.floor(potentialWidth),50)

        y = screenSurface.get_height() - 25 - (numOfRows * BOX_SIZE) - ((numOfRows-1) * PADDING)
        
        for row in self.gridArray:
            numOfCols = len(row)
            x = (initalXSpaceLeft - BOX_SIZE*numOfCols)/2 + 25 # Add half minimum padding = padding from left

            for box in row:
                box.rect = pygame.Rect(x,y,BOX_SIZE,BOX_SIZE)
                box.display(screenSurface)

                x += BOX_SIZE + PADDING
            y += BOX_SIZE + PADDING

        return screenSurface.get_height() - 25 - (numOfRows * BOX_SIZE) - ((numOfRows-1) * PADDING)

class Screen():
    """
    The window on which the game is played.

    Attributes:
        width: The width of the window. 
        height: The height of the window. It has a minimum value of 500, any
          value passed below this will cause the width and height to be scaled,
          keeping their original ratio, to make height 500.
        surface: The background of the window onto which other surfaces are
          added.
    """

    def __init__(self,width:int,height:int):
        min_height = 500
        min_width = width / height * 500

        self.width = max(min_width,width)
        self.height = max(min_height,height)

        self.surface = pygame.display.set_mode((self.width,self.height))
        self.surface.fill("black")

    def setUp(self,grid:BoxGrid,keyboard:KeyboardGrid):
        """
        Displays the box grid and keyboard.

        Args:
            grid: The grid of box objects making up the guessing grid to be
              displayed.
            keyboard: The grid of box objects making up the keyboard to be 
              displayed.
            
              
        """
        keyboardStartY = keyboard._setUp(self.surface)
        grid._setUp(self.surface,keyboardStartY)

    def updateScreen(self,grid:BoxGrid,keyboard:KeyboardGrid):
        """
        Updates the box grid and keyboard grid boxes.

        Args:
            grid: The grid of box objects making up the guessing grid to be
              updated.
            keyboard: The grid of box objects making up the keyboard to be 
              updated.
        """
        for row in grid.gridArray:
            for box in row:
                self.surface.blit(box._surface,box.rect)
        grid.updateLetters()
        
        for row in keyboard.gridArray:
            for box in row:
                self.surface.blit(box._surface,box.rect)
        keyboard.updateLetters()

class Notification():
    """
    A pop-up notification which appears on the screen.

    Provides information about the game which needs to be displayed to the
    player for a short period of time. Examples: Informing them they have
    won/lost/entered an invalid word.

    Attributes:
        lifespan: The amount of time in seconds the notification should be 
          visible for.
        text: The message to be displayed.
        fontSize: The font size of the message.
        textColour: The hexcode of the colour of the message.
        bgColour: The hexcode of the colour of the background.
        creationTime: The time in seconds from the Epoch at which the
          notification was first displayed.
        screenSurface: The surface on which the notification is placed.
        rect (pygame.Rect): The coordinates, width and height of the 
          notification.
    """

    notificationList = []
    def __init__(self,lifespan:int,text:str,fontSize:int,textColour="#000000",bgColour="#FFFFFF"):
        font = pygame.font.SysFont('arial',fontSize,True)
        self.textSurface = font.render(text,0,textColour,bgColour)

        self._width = self.textSurface.get_rect().width
        self._height = self.textSurface.get_rect().height

        self.creationTime = -1
        self.lifespan = lifespan
        self.screenSurface = pygame.surface.Surface((0,0))

    def displayNotification(self,screen:Screen,verticalAlignment="top"):
        """
        Displays the notification on the screen.

        This will place the notification on the screen centered horizontally
        at either the top, middle or bottom of the screen. This is considered
        the creation of the notification so creationTime is set to the time at
        which the method is called. The notification is then added to the class
        variable notificationList and the value of rect is updated.

        Attributes:
            screen: The screen on which the notification should be displayed.
            verticalAlignment: A value of top/center/bottom which describes the
              notifications vertical position.
        """
        if verticalAlignment == "top":
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self._width)/2,0))
        elif verticalAlignment == "center":
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self._width)/2,(screen.height-self._height)/2))
        elif verticalAlignment == "bottom":
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self._width)/2,(screen.height-self._height)))
        else:
            # Default to top 
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self._width)/2,0))
        
        self.creationTime = time.time()
        self.screenSurface = screen.surface
        Notification.notificationList.append(self)
        
    def checkLifespan(self):
        """
        Removes the notification if its lifespan has been exceeded.
        """
        if self.creationTime + (self.lifespan) <= time.time():
            self.screenSurface.fill("Black",self.rect)
            Notification.notificationList.remove(self)

def isRealWord(word:str):
    """
    Returns whether the passed word is in the english dictionary.

    Only words found at https://api.dictionaryapi.dev/api/v2/entries/en/ + word
    will be considered real.

    Args:
        word: The potential word which the player has entered.
    
    Returns:
        boolean: True if word is in english dictionary, else False.
    """
    URL = "https://api.dictionaryapi.dev/api/v2/entries/en/" + word.lower()

    resp = urllib3.request("GET", URL)
    if type(resp.json()) == list:
        return True
    else:
        return False

def calculateColours(currentRow:list,keyboard:KeyboardGrid,guess:str,answer:str):
    """
    Updates the colours of the keyboard and the current row's boxes.

    The colour of each box is set to #787C7E if its letter is not
    in answer,#C9B458 if it is but it is in the wrong spot and #6AAA64 if its
    in the right spot.

    Args:
        currentRow: The row of boxes which contain the most recent guess.
        keyboard: The grid of boxes representing the keyboard.
        guess: The word guessed.
        answer: The correct word.
    """
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
            
def generateWord(wordLength:int,difficulty:int):
    """
    Generates a random word.

    Args:
        wordLength: The required length of the word.
        difficulty: A value which filters words by how common it is using 
          Wikipedia word frequency data. 1 = Easy, 5 = Hard.
    """
    # Get 10 words incase some not accepted by real word tester
    URL = f"https://random-word-api.herokuapp.com/word?number=10&length={wordLength}&diff={difficulty}"
    while True:
        resp = urllib3.request("GET", URL)
        wordList = resp.json()
        for word in wordList:
            if isRealWord(word):
                return(word)

def main(screenWidth:int,screenHeight:int,rowAmount:int,columnAmount:int,wordDifficulty:int):
    """
    Creates the game window and handles the main game loop.

    This is the only method which should be called from external files as it
    will handle the calls to all other methods where necessary.

    Args:
        screenWidth: The width of the game window.
        screenHeight: The height of the game window.
        rowAmount: The number of rows in the game grid.
        columnAmount: The number of columns in the game grid (and therefore
          the length of the word to be guessed)
        wordDifficulty: How commonly the word is used in the English Language. 
          (1=Common,5=Rare)
    """
    gameScreen = Screen(screenWidth,screenHeight)
    gameGrid = BoxGrid(rowAmount,columnAmount)
    gameKeyboard = KeyboardGrid()
    gameScreen.setUp(gameGrid,gameKeyboard)

    WORD_TO_GUESS = generateWord(gameGrid.cols,wordDifficulty)

    currentRowIndex = 0
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
                        
                    elif isRealWord(guess):
                        calculateColours(currentRow,gameKeyboard,guess,WORD_TO_GUESS)

                        currentRowIndex += 1
                        if currentRowIndex >= gameGrid.rows:
                            #Loss
                            lossNotification = Notification(3,f"Unlucky, the word was {WORD_TO_GUESS.upper()}.",20,"Black","White")
                            lossNotification.displayNotification(gameScreen)

                            currentRowIndex = 0

                    else:
                        notRealNotification = Notification(1,"Word not in word list.",20,"Black","White")
                        notRealNotification.displayNotification(gameScreen)

                elif event.unicode.isalpha():
                    for box in currentRow:
                        if box.letter == "":
                            box.letter = event.unicode.upper()  
                            break
        
        for notification in Notification.notificationList:
            notification.checkLifespan()

        gameScreen.updateScreen(gameGrid,gameKeyboard)
        pygame.display.update()
        clock.tick(20)

    pygame.quit()

if __name__ == "__main__":
    monitorWidth,monitorHeight = pygame.display.get_desktop_sizes()[0]
    screenWidth = monitorWidth - 50
    screenHeight = monitorHeight - 100
    
    rowAmount = 6
    columnAmount = 5
    WORD_DIFFICULTY = 3

    main(screenWidth,screenHeight,rowAmount,columnAmount,WORD_DIFFICULTY)

# Commit to repository - gameLibrary

# Add some inline/block comments to explain confusing sections