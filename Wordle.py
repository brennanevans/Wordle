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

        if self.letter == "ENTER":
            textSize = 15
        else:
            textSize = boxWidth

        font = pygame.font.SysFont('arial',textSize,True)
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

    def _setUp(self,keyboardStartY:int):
        """
        Creates the box grid on screen.

        Args:
            keyboardStartY: The The y coordinate of the top of the keyboard.
        """
        PADDING = 5
        SIDE_PADDING = 25

        # Calculates horizontal space given 25 padding from each side and
        # PADDING between each box. This ensures boxes are centered 
        # horizontally.
        xSpaceLeft = gameScreen.width - (SIDE_PADDING*2) - (PADDING*(self.cols-1))
        potentialWidth = xSpaceLeft/self.cols

        # Calculates vertical space given 25 padding from the top of the
        # screen and the top of the keyboard and PADDING between each box.
        # This ensures boxes are centered vertically between top of screen
        # and top of keyboard.
        ySpaceLeft = keyboardStartY - (SIDE_PADDING*2) - (PADDING*(self.rows-1))
        potentialHeight = ySpaceLeft/self.rows

        BOX_SIZE = math.floor(min(potentialWidth,potentialHeight))

        xSpaceLeft -= BOX_SIZE*self.cols
        ySpaceLeft -= BOX_SIZE*self.rows

        y = math.floor(ySpaceLeft/2 + SIDE_PADDING)
        for row in self.gridArray:
            x = xSpaceLeft/2 + SIDE_PADDING

            for box in row:
                box.rect = pygame.Rect(x,y,BOX_SIZE,BOX_SIZE)
                box.display(gameScreen.surface)

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
                       "F","G","H","J","K","L","ENTER","Z","X","C","V","B","N","M","<--"]
        
        self.gridArray = []
        self.letterDictionary = {}
        rowLengths = [10,9,9]
        
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

    def _setUp(self):
        """
        Creates the keyboard on screen.
        Returns:
            int: The y coordinate of the top of the keyboard.
        """
        numOfCols = len(self.gridArray[0])
        numOfRows = 3

        PADDING = 5
        SIDE_PADDING = 25

        # Calculates horizontal space given 25 padding from each side and
        # PADDING between each box. This ensures boxes are centered 
        # horizontally.
        initalXSpaceLeft = gameScreen.width - (SIDE_PADDING*2) - (PADDING*(numOfCols-1))
        potentialWidth = initalXSpaceLeft/numOfCols

        BOX_SIZE = min(math.floor(potentialWidth),50)
        
        # Calculates top y value given 25 padding from bottom, size 
        # of the boxes and padding between each box.
        initalY = gameScreen.height - SIDE_PADDING - (numOfRows * BOX_SIZE) - ((numOfRows-1) * PADDING)
        y= initalY
        
        for row in self.gridArray:
            numOfCols = len(row)
            # x position has to be calculated here as number of columns is 
            # different in each row.
            x = (initalXSpaceLeft - BOX_SIZE*numOfCols)/2 + SIDE_PADDING

            for box in row:
                box.rect = pygame.Rect(x,y,BOX_SIZE,BOX_SIZE)
                box.display(gameScreen.surface)

                x += BOX_SIZE + PADDING
            y += BOX_SIZE + PADDING

        return initalY
    
    def clicked(self,mousePosX:int,mousePosY:int):
        """
        Calls the required method for the keyboard button clicked.

        Args:
            mousePosX: Mouse's x coordinate.
            mousePosY: Mouse's y coordinate.
        """
        for row in self.gridArray:
            for box in row:
                if box.rect.collidepoint(mousePosX,mousePosY):
                    if box.letter == "ENTER":
                        KeyFunctions.enter()
                    elif box.letter == "<--":
                        KeyFunctions.backspace()
                    else:
                        KeyFunctions.letterPressed(box.letter)


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

    def setUp(self):
        """
        Displays the box grid and keyboard.
        """
        keyboardStartY = gameKeyboard._setUp()
        gameGrid._setUp(keyboardStartY)

    def updateScreen(self):
        """
        Updates the box grid and keyboard grid boxes.
        """
        for row in gameGrid.gridArray:
            for box in row:
                self.surface.blit(box._surface,box.rect)
        gameGrid.updateLetters()
        
        for row in gameKeyboard.gridArray:
            for box in row:
                self.surface.blit(box._surface,box.rect)
        gameKeyboard.updateLetters()

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
    def __init__(self,lifespan:int,text:str,textColour="#000000",bgColour="#FFFFFF"):
        font = pygame.font.SysFont('arial',20,True)
        self.text = text
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
        at either the top, or bottom of the screen. This is considered
        the creation of the notification so creationTime is set to the time at
        which the method is called. The notification is then added to the class
        variable notificationList and the value of rect is updated.

        Attributes:
            screen: The screen on which the notification should be displayed.
            verticalAlignment: A value of top/bottom which describes the
              notifications vertical position.
        """
        for notification in Notification.notificationList:
            if notification.text == self.text:
                notification.creationTime = time.time()
                return
            else:
                notification.screenSurface.fill("Black",notification.rect)
                Notification.notificationList.remove(notification)

        if verticalAlignment == "top":
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self._width)/2,0))
        elif verticalAlignment == "bottom":
            self.rect = screen.surface.blit(self.textSurface,((screen.width-self._width)/2,(screen.height-self._height)))
        else:
            # Default to top for invalid alignment values
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

class KeyFunctions():
    """
    A container for the functions of keyboard buttons.
    """
    def backspace():
        """
        Deletes letter from most right, non-empty box in gameGrid.
        """
        for box in reversed(gameGrid.gridArray[currentRowIndex]):
            if box.letter == "":
                continue
            else:
                box.letter = ""
                break
    def enter():
        """
        Handles the user pressing enter at any time.

        If enter pressed when not all boxes are full, creates notification.
        If enter pressed when boxes spell a non-real word, creates 
        notification.
        If enter pressed when boxes spell a real word, calls required methods.
        """
        # Needed as if change global variable anywhere in function, python assumes is local variable
        global currentRowIndex

        currentRow = gameGrid.gridArray[currentRowIndex]
        guess = ""
        for box in currentRow:
            guess += box.letter.lower()

        # Not all boxes filled
        if len(guess) < len(WORD_TO_GUESS):
            tooShortNotification = Notification(1,"Not all boxes filled.","Black","White")
            tooShortNotification.displayNotification(gameScreen)
        
        # Win
        elif guess == WORD_TO_GUESS:
            calculateColours(guess,WORD_TO_GUESS)
            winNotification = Notification(3,f"Congrats!!! You guessed the word in {currentRowIndex+1} tries.","Black","White")
            winNotification.displayNotification(gameScreen)
        
        # Loss or incorrect guess
        elif isRealWord(guess):
            calculateColours(guess,WORD_TO_GUESS)

            currentRowIndex += 1
            #Loss
            if currentRowIndex >= gameGrid.rows:
                lossNotification = Notification(3,f"Unlucky, the word was {WORD_TO_GUESS.upper()}.","Black","White")
                lossNotification.displayNotification(gameScreen)

                currentRowIndex = 0

        # Not a real word
        else:
            notRealNotification = Notification(1,"Word not in word list.","Black","White")
            notRealNotification.displayNotification(gameScreen)
            
    def letterPressed(letter:str):
        """
        Adds letter to right most box unless all boxes full.

        Args:
            letter: The letter that was pressed.
        """
        for box in gameGrid.gridArray[currentRowIndex]:
            if box.letter == "":
                box.letter = letter.upper()
                break

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

def calculateColours(guess:str,answer:str):
    """
    Updates the colours of the keyboard and the current row's boxes.

    The colour of each box is set to #787C7E if its letter is not
    in answer,#C9B458 if it is but it is in the wrong spot and #6AAA64 if its
    in the right spot.

    Args:
        guess: The word guessed.
        answer: The correct word.
    """
    currentRow = gameGrid.gridArray[currentRowIndex]

    # Used to determine if letter has already been seen for #C9B458 
    # determinations.
    lettersLeft = [*answer]

    # First loops checks if letters are in the right place.
    for index in range(len(guess)):
        letter = guess[index]
        if letter == answer[index]:
            currentRow[index].colour = "#6AAA64"
            gameKeyboard.letterDictionary.get(letter.upper()).colour = "#6AAA64"
            lettersLeft.remove(letter)

    #Second loop checks if remaining letters are anywhere in the word.
    for index in range(len(guess)):
        letter = guess[index]
        if letter in lettersLeft and currentRow[index].colour != "#6AAA64":
            currentRow[index].colour = "#C9B458"
            if gameKeyboard.letterDictionary.get(letter.upper()).colour != "#6AAA64":
                gameKeyboard.letterDictionary.get(letter.upper()).colour = "#C9B458"

            lettersLeft.remove(letter)
        elif currentRow[index].colour != "#6AAA64":
            currentRow[index].colour = "#787C7E"
            if gameKeyboard.letterDictionary.get(letter.upper()).colour != "#6AAA64":
                gameKeyboard.letterDictionary.get(letter.upper()).colour = "#787C7E"
            
def generateWord(wordLength:int,difficulty:int):
    """
    Generates a random word.

    Args:
        wordLength: The required length of the word.
        difficulty: A value which filters words by how common it is using 
          Wikipedia word frequency data. 1 = Easy, 5 = Hard.
    
    Returns:
        str: The generated word, if the API refuses to connect this will be
          a placeholder word for the value of wordLength.
    """
    # Get 10 words incase some not accepted by isRealWord()
    URL = f"https://random-word-api.herokuapp.com/word?number=10&length={wordLength}&diff={difficulty}"
    while True:
        try:
            resp = urllib3.request("GET", URL,retries=None,timeout=1)
            wordList = resp.json()
            for word in wordList:
                if isRealWord(word):
                    return(word)
        except (urllib3.exceptions.MaxRetryError):
            print("API refused to connect, selecting appropriate" \
            " placeholder word.")
            wordDict = {3:"and",4:"goal",5:"hello",6:"change",7:"framing"
                        ,8:"abandons",9:"labelling",10:"eastwardly"}
            return wordDict.get(wordLength)

def main(rowAmount=6,columnAmount=5,wordDifficulty=3,
         screenWidth=pygame.display.get_desktop_sizes()[0][0]-50,
         screenHeight=pygame.display.get_desktop_sizes()[0][1]-100):
    """
    Creates the game window and handles the main game loop.

    This is the only method which should be called from external files as it
    will handle the calls to all other methods where necessary.

    Args:
        rowAmount: The number of rows in the game grid (between 3 and 12).
        columnAmount: The number of columns in the game grid (and therefore
          the length of the word to be guessed) (between 3 and 10).
        wordDifficulty: How commonly the word is used in the English Language. 
          (1=Common,5=Rare).
        screenWidth: The width of the game window. If any value is passed is
          below 300 or no value passed, window width is set to width of 
          monitor - 50.
        screenHeight: The height of the game window. Any value passed which is
          below 500 will cause the width and height to be scaled, keeping their
          original ratio, to make height 500. If no value passed, window width
          is set to height of monitor - 100.

    Raises:
        ValueError: If rowAmount or columnAmount or wordDifficulty not in their
          respective exepected ranges.
    """
    global WORD_TO_GUESS,currentRowIndex,gameScreen,gameGrid,gameKeyboard


    if rowAmount > 12 or columnAmount > 10:
        raise ValueError("Max amount of rows or columns exceeded.")
    elif rowAmount < 4 or columnAmount < 3:
        raise ValueError("Min amount of rows or columns not reached.")
    elif wordDifficulty < 1 or wordDifficulty > 5:
        raise ValueError("wordDifficulty must be a value between 1 and 5.")
    elif screenWidth < 300:
        screenWidth = pygame.display.get_desktop_sizes()[0][0]-50

    gameScreen = Screen(screenWidth,screenHeight)
    gameGrid = BoxGrid(rowAmount,columnAmount)
    gameKeyboard = KeyboardGrid()
    gameScreen.setUp()

    WORD_TO_GUESS = generateWord(gameGrid.cols,wordDifficulty)

    currentRowIndex = 0
    running = True
    while running:
        x,y = pygame.mouse.get_pos()
        currentRow = gameGrid.gridArray[currentRowIndex]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                gameKeyboard.clicked(x,y)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    KeyFunctions.backspace()
                elif event.key == pygame.K_RETURN:
                    KeyFunctions.enter()
                elif event.unicode.isalpha():
                    KeyFunctions.letterPressed(event.unicode)
        
        for notification in Notification.notificationList:
            notification.checkLifespan()

        gameScreen.updateScreen()
        pygame.display.update()
        clock.tick(20)

    pygame.quit()

if __name__ == "__main__":
    main()
