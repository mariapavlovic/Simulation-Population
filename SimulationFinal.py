from pygame import *
from random import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (50, 50)
init()
SIZE = (1000, 700)
screen = display.set_mode(SIZE)

# FONTS
controlsFont = font.SysFont("Impact", 25)
optionsFont = font.SysFont("Arial Black", 15)
buttonsFont = font.SysFont("Impact", 15)
warningFont = font.SysFont("Arial",18)

# COLOURS
lightRed = (255, 117, 117)
green = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (107, 137, 235)
pink = (255, 102, 178)
yellow = (252, 214, 2)
grey = (216, 216, 216)
color = (107, 137, 235) #color for man drawing
color2 = (255, 102, 178) #color for woman drawing

# COLOUR CHANGES
##color change for location buttons in control
locationButtonA = white
locationButtonB = white
locationButtonC = white
##color change for speed of spread buttons in control
spreadButtonA = white
spreadButtonB = white
spreadButtonC = white
##color change for cure buttons in control
cureButtonA = white
cureButtonB = white
##color change for immunity percentage in control
immunityButtonA = white
immunityButtonB = white
immunityButtonC = white
immunityButtonD = white
##color change for length of infection in control
infectionActiveA = white
infectionActiveB = white
infectionActiveC = white
##color change for run button
runButton = red
# colour change for two buttons on start up screen
startColoursA = white
startColoursB = white

# FACTORS ON CONTROL PANEL
#booleans to change simulation based on control selections
america = False
europe = False
africa = False
cure = False
cureNo = False
immunity1 = False
immunity2 = False
immunity3 = False
immunity4 = False
months6 = False
year1 = False
year6 = False
fastSpread = False
mediumSpread = False
slowSpread = False
speedInfect = 0
lengthToHealing = 0
startPopulation = True
convertImmuneRun: bool = False

# SIMULATION
girlColour = pink
boyColour = blue
##assigns a number to each condition in the simulation (in the list)
healthy = 1
sick = 2
dead = 3
immune = 4
##sets up counters to healthy , dead , and sick during simulation
sickCount = 0
immunityCount = 0
healthyCount = 225 - immunityCount
deadCount = 0
population = 0
dx = 0  # outbreak year counter
ex = 0 # dead counter
c = 69 #x position for woman drawing
d = 60 #y position for woman drawing
e = 100 #x position for man drawing
f = 100 #y position for man drawing

# draw.rect(screen, white, (0, 0, 1000, 700))  # background

col = []
def assignCol(): #method to initiate list of healthy (everyone starts healthy, immune people converted later)
    global col
    for i in range(0, 15):
        row = []
        for j in range(0, 15):
            row.append(healthy)
        col.append(row)

def findImmune(m: int) -> int: #method to find percent immune based on control selection
    if m == 1: #if first immunity button is clicked
        immunePercent = 0
    elif m == 2: #if second immunity button is clicked
        immunePercent = randint(10,39) #differing ranges of immunity percentage chosen randomly
    elif m == 3: #if third immunity button is clicked
        immunePercent = randint(40,79) #differing ranges of immunity percentage chosen randomly
    else: #if fourth immunity button is clicked
        immunePercent = randint(80,90) #differing ranges of immunity percentage chosen randomly
    return immunePercent


def convertImmune(immunePercent): #method to convert status from healthy to immune based on percentage that is immune
    global immune
    global immunityCount
    if immunePercent>0: # doesn't continue is 0% of population is immune
        #loop to go through entire grid
        for i in range(0, 15):
            for j in range(0, 15):
                immunePopulation = randint(0,100)
                if immunePopulation <= immunePercent: # every person has the chosen amount of percent chance to become immune
                    col[i][j] = immune #adds appropriate number of immune people depending on control selection and randomness
                    immunityCount += 1 #add one to count every time a new immune person is appended to list


def drawWoman(c, d, color2):
    draw.circle(screen, color2, (c, d), 7)  # head
    draw.polygon(screen, color2, [(c, d), (c - 11, d + 20), (c + 11, d + 20)])  # skirt
    draw.rect(screen, color2, (c - 5, d + 20, 5, 7))  # legs
    draw.rect(screen, color2, (c + 2, d + 20, 5, 7))


def drawMan(e, f, color):
    draw.circle(screen, color, (e, f), 7)  # head
    draw.rect(screen, color, (e - 8, f + 6, 16, 22))  # torso
    draw.rect(screen, white, (e - 1, f + 20, 3, 10))
    draw.rect(screen, color, (e - 10, f + 6, 2, 12))  # arms
    draw.rect(screen, color, (e + 8, f + 6, 2, 12))


def popstatus(prevStatus, timeToHealth, timeToDead, infection, deaths): #method to determine status of each person during simulation, and change status based on old one
    newStatus = prevStatus #updates current status every time
    ##uses variables set up outside of the method
    global healthy
    global sick
    global dead
    global immune
    global lengthToHealing
    global healthyCount
    global sickCount
    global deadCount
    global cure
    if cure == True: #if cure yes button is clicked
        if timeToHealth <= lengthToHealing:  # from beginning of simulation to halfway mark
            if prevStatus == healthy and infection < 14:  # if person is healthy and less than 14 persons are infected
                newStatus = sick  # change that person's status to sick
                healthyCount -= 1  # alter count depending on num of healthy and sick
                sickCount += 1
            if prevStatus == sick and timeToDead > 10 and deaths < 14:  # if person is sick and less than 14 people died
                newStatus = dead  # change that person's status to dead
                deadCount += 1  # change counts accordingly
                sickCount -= 1
            if prevStatus == dead:  # if person is dead
                newStatus = dead  # keep him/her dead
            if prevStatus == immune:  # if person is immune
                newStatus = immune  # keep him immune
        if timeToHealth > lengthToHealing:  # if halfway mark is past
            if prevStatus == healthy:  # if person is healthy
                newStatus = healthy  # keep him healthy
            if prevStatus == sick:  # if person is sick
                newStatus = healthy  # cure him
                sickCount -= 1  # change count accordingly
                healthyCount += 1
            if prevStatus == dead:  # if person is dead
                newStatus = dead  # keep him dead
            if prevStatus == immune:  # if person is immune
                newStatus = immune  # keep him immune
    else:  # if cure no button is clicked
        if prevStatus == healthy and infection < 14:  # if person is healthy and less than 14 persons are infected
            newStatus = sick  # change that person's status to sick
            healthyCount -= 1  # change count accordingly
            sickCount += 1
        if prevStatus == sick and timeToDead > 10 and deaths < 14:  # if person is sick and less than 14 persons are dead
            newStatus = dead  # change that person's status to dead
            sickCount -= 1  # change count accordingly
            deadCount += 1
        if prevStatus == dead:  # if person is dead
            newStatus = dead  # keep him dead
        if prevStatus == immune:  # if person is immune
            newStatus = immune  # keep him immune
    return newStatus


def stillsimscreen():
    vertX = 90 #x position for vertical grid lines
    y = 50 #y position for vertical grid lines
    a = 50 #x position for horizontal grid lines
    b = 90 #y position for horizontal grid lines
    draw.rect(screen, black, (50, 50, 600, 600), 2)  # grid outline
    for w in range(15):  # vert lines
        draw.line(screen, black, (vertX, y), (vertX, y + 600), 1)
        vertX += 40
    for z in range(14):  # horiz lines
        draw.line(screen, black, (a, b), (a + 600, b), 1)
        b += 40
    posy = 60 #y position to draw man and woman
    boxy = 52
    boxx = 50
    for i in range(15):  # drawing the icons
        posx = 69 #x position to draw man and woman
        for j in range(15):
            if j % 2 == 0: #if row list index is even
                boyColour = blue
                drawMan(posx, posy, boyColour) #draw a man
            else: #if row list index is odd
                girlColour = pink
                drawWoman(posx, posy, girlColour) #draw a woman
            posx += 40
            boxx += 40
        posy += 40
        boxy += 40


def redrawIcons():  # method to redraw icons if player quits and comes back
    # variables defined globally
    global col
    global healthy
    global sick
    global dead
    global immune
    global girlColour
    global boyColour
    vertX = 90  # x position for vertical grid lines
    y = 50  # y position for vertical grid lines
    a = 50  # x position for horizontal grid lines
    b = 90  # y position for horizontal grid lines
    draw.rect(screen, black, (50, 50, 600, 600), 2)  # grid outline
    for w in range(15):  # vert lines
        draw.line(screen, black, (vertX, y), (vertX, y + 600), 1)
        vertX += 40
    for z in range(14):  # horiz lines
        draw.line(screen, black, (a, b), (a + 600, b), 1)
        b += 40
    posy = 60
    boxy = 52
    boxx = 50
    for i in range(15):  # vertical
        posx = 69
        for j in range(15):  # horizontal
            if j % 2 == 0:  # if num is even - draw boys
                boyStatus = col[i][j]
                if boyStatus == sick:  # color based on status
                    boyColour = red
                elif boyStatus == dead:
                    boyColour = black
                elif boyStatus == immune:
                    boyColour = yellow
                else:
                    boyColour = blue
                drawMan(posx, posy, boyColour)
            else:  # if num is odd - draw girls
                girlStatus = col[i][j]
                if girlStatus == sick:  # color change based on status
                    girlColour = red
                elif girlStatus == dead:
                    girlColour = black
                elif girlStatus == immune:
                    girlColour = yellow
                else:
                    girlColour = pink
                drawWoman(posx, posy, girlColour)
            posx += 40 # increases x and y positions of grid lines and people to draw across and down screen
            boxx += 40
        posy += 40
        boxy += 40


def simscreen(x, c, infectRate):  # method draws the simulation screen
    # uses variables set up globally
    global healthy
    global sick
    global dead
    global col
    global girlColour
    global boyColour
    global immune
    posy = 60
    boxy = 51
    # loop to go through entire grid
    for i in range(15):  # drawing the icons
        posx = 69
        boxx = 50
        for j in range(15):
            print(col[i][j])
            infection = randint(0, infectRate)  # changes infection num based on infection rate
            deaths = randint(0, 14)
            if j % 2 == 0:  # if list index is even
                if infection <= 14:  # if less than 14 persons are infected
                    boyStatus = popstatus(col[i][j], x, c, infection, deaths)  # calls on previous method to decide person status
                    col[i][j] = boyStatus
                    # sets person's color depending on status
                    if boyStatus == sick:
                        boyColour = red
                    elif boyStatus == dead:
                        boyColour = black
                    elif boyStatus == immune:
                        boyColour = yellow
                    else:
                        boyColour = blue
                    drawMan(posx, posy, boyColour)
            else:
                if infection <= 14:  # if less than 14 persons are infected
                    girlStatus = popstatus(col[i][j], x, c, infection, deaths)  # calls on previous method to decide person status
                    col[i][j] = girlStatus
                    # sets person's color depending on status
                    if girlStatus == sick:
                        girlColour = red
                    elif girlStatus == dead:
                        girlColour = black
                    elif girlStatus == immune:
                        girlColour = yellow
                    else:
                        girlColour = pink
                    drawWoman(posx, posy, girlColour)
            posx += 40
            boxx += 40
        posy += 40
        boxy += 40
    time.wait(600)  # prevents simulation from running too fast


def drawstartScreen(): # menu screen, first thing shows
    draw.rect(screen, (224, 236, 255), (0, 0, 1000, 700))  # background
    startFontTitle = font.SysFont("Impact", 100)
    text = startFontTitle.render("Cholera Outbreak", 1, black)  #title
    screen.blit(text, Rect(130, 100, 400, 100))
    draw.rect(screen, startColoursA, (280, 310, 450, 60))
    draw.rect(screen, black, (280, 310, 450, 60), 5)
    startFont = font.SysFont("Arial Black", 30)
    text = startFont.render("Continue From Last Run", 1, black) # button 1
    screen.blit(text, Rect(305, 315, 400, 100))
    draw.rect(screen, startColoursB, (280, 435, 450, 60))
    draw.rect(screen, black, (280, 435, 450, 60), 5)
    text = startFont.render("Start Simulation Over", 1, black)  # button 2
    screen.blit(text, Rect(325, 440, 400, 100))


def drawControls(): # method draws control panel
    text = warningFont.render("Choose from each option before clicking 'run'", 1, black)
    screen.blit(text, Rect(680, 230, 400, 100))
    draw.rect(screen, black, (680, 250, 320, 450))  # background
    text = controlsFont.render("Cholera Outbreak", 1, white)
    screen.blit(text, Rect(690, 255, 400, 100))
    draw.line(screen, white, (880, 270), (980, 270), 5)  # aesthetic line
    if (america == True or europe == True or africa == True) and (slowSpread == True or mediumSpread == True or fastSpread == True) and (cure == True or cure == False) and (immunity1 == True or immunity2 == True or immunity3 == True or immunity4 == True) and (months6 == True or year1 == True or year6 == True):
        draw.rect(screen, runButton, (700, 600, 80, 47))  # run button
        text = controlsFont.render("RUN", 1, white)
        screen.blit(text, Rect(720, 607, 400, 100))
    else:
        draw.rect(screen, lightRed, (700, 600, 80, 47))  # run button
        text = controlsFont.render("RUN", 1, white)
        screen.blit(text, Rect(720, 607, 400, 100))        
    # LOCATON TITLE AND BUTTONS
    controlsText = optionsFont.render("LOCATION", 1, white)
    screen.blit(controlsText, Rect(690, 300, 400, 100))
    draw.rect(screen, locationButtonA, (790, 300, 60, 20))
    contButtons = buttonsFont.render("America", 1, black)
    screen.blit(contButtons, Rect(795, 300, 400, 100))
    draw.rect(screen, locationButtonB, (860, 300, 60, 20))
    contButtons = buttonsFont.render("Europe", 1, black)
    screen.blit(contButtons, Rect(869, 300, 400, 100))
    draw.rect(screen, locationButtonC, (930, 300, 60, 20))
    contButtons = buttonsFont.render("Africa", 1, black)
    screen.blit(contButtons, Rect(940, 300, 400, 100))
    # YEAR TITLE AND BUTTONS
    controlsText = optionsFont.render("SPEED OF SPREADING", 1, white)
    screen.blit(controlsText, Rect(690, 340, 400, 100))
    draw.rect(screen, spreadButtonA, (690, 365, 90, 20))
    contButtons = buttonsFont.render("Fast", 1, black)
    screen.blit(contButtons, Rect(720, 365, 400, 100))
    draw.rect(screen, spreadButtonB, (795, 365, 90, 20))
    contButtons = buttonsFont.render("Medium", 1, black)
    screen.blit(contButtons, Rect(815, 365, 400, 100))
    draw.rect(screen, spreadButtonC, (900, 365, 90, 20))
    contButtons = buttonsFont.render("Slow", 1, black)
    screen.blit(contButtons, Rect(933, 365, 400, 100))
    # CURE TITLE AND BUTTONS
    controlsText = optionsFont.render("IS THERE A CURE?", 1, white)
    screen.blit(controlsText, Rect(690, 410, 400, 100))
    draw.rect(screen, cureButtonA, (860, 411, 30, 20))
    contButtons = buttonsFont.render("YES", 1, black)
    screen.blit(contButtons, Rect(865, 411, 400, 100))
    draw.rect(screen, cureButtonB, (900, 411, 30, 20))
    contButtons = buttonsFont.render("NO", 1, black)
    screen.blit(contButtons, Rect(907, 411, 400, 100))
    # IMMUNITY TITLE AND BUTTONS
    controlsText = optionsFont.render("HOW MANY ARE IMMUNE?", 1, white)
    screen.blit(controlsText, Rect(690, 455, 400, 100))
    draw.rect(screen, immunityButtonA, (690, 480, 30, 20))
    contButtons = buttonsFont.render("0%", 1, black)
    screen.blit(contButtons, Rect(695, 480, 400, 100))
    draw.rect(screen, immunityButtonB, (740, 480, 70, 20))
    contButtons = buttonsFont.render("10% - 30%", 1, black)
    screen.blit(contButtons, Rect(745, 480, 400, 100))
    draw.rect(screen, immunityButtonC, (830, 480, 70, 20))
    contButtons = buttonsFont.render("40% - 70%", 1, black)
    screen.blit(contButtons, Rect(835, 480, 400, 100))
    draw.rect(screen, immunityButtonD, (920, 480, 70, 20))
    contButtons = buttonsFont.render("80% - 90%", 1, black)
    screen.blit(contButtons, Rect(925, 480, 400, 100))
    controlsText = optionsFont.render("INFECTION ACTIVE FOR", 1, white)
    screen.blit(controlsText, Rect(690, 525, 400, 100))
    draw.rect(screen, infectionActiveA, (690, 550, 80, 20))
    contButtons = buttonsFont.render("6 months", 1, black)
    screen.blit(contButtons, Rect(698, 550, 400, 100))
    draw.rect(screen, infectionActiveB, (800, 550, 80, 20))
    contButtons = buttonsFont.render("1 year", 1, black)
    screen.blit(contButtons, Rect(818, 550, 400, 100))
    draw.rect(screen, infectionActiveC, (910, 550, 80, 20))
    contButtons = buttonsFont.render("3 years", 1, black)
    screen.blit(contButtons, Rect(925, 550, 400, 100))
    #KEY
    drawWoman(20, 10, pink)
    drawMan(45,10,blue)
    draw.line(screen, black, (60, 20), (70, 20), 4)
    draw.line(screen, black, (60, 27), (70, 27), 4)
    statusFont = font.SysFont("Arial", 20)
    keyText1 = statusFont.render("HEALTHY", 1, black)
    screen.blit(keyText1, Rect(75, 13, 40, 30))
    drawWoman(180,10,red)
    drawMan(205,10,red)
    draw.line(screen, black, (220, 20), (230, 20), 4)
    draw.line(screen, black, (220, 27), (230, 27), 4)
    statusFont = font.SysFont("Arial", 20)
    keyText2 = statusFont.render("SICK", 1, black)
    screen.blit(keyText2, Rect(235, 13, 40, 30))
    drawWoman(310,10,black)
    drawMan(335,10,black)
    draw.line(screen, black, (350, 20), (360, 20), 4)
    draw.line(screen, black, (350, 27), (360, 27), 4)
    statusFont = font.SysFont("Arial", 20)
    keyText3 = statusFont.render("DEAD", 1, black)
    screen.blit(keyText3, Rect(365, 13, 40, 30))
    drawWoman(440,10,yellow)
    drawMan(465,10,yellow)
    draw.line(screen, black, (480, 20), (490, 20), 4)
    draw.line(screen, black, (480, 27), (490, 27), 4)
    statusFont = font.SysFont("Arial", 20)
    keyText4 = statusFont.render("IMMUNE", 1, black)
    screen.blit(keyText4, Rect(495, 13, 40, 30))


def populationInfo(country):  # method changes population legend and country pictures
    # uses global variables previously set up
    global america
    global europe
    global africa
    global population
    global cure
    global endScreen
    global immunityCount
    global simulationRun
    if country == america:  # if america button is clicked
        draw.rect(screen, white, (700, 10, 300, 220))
        pic = image.load("MariaLanaAmerica.jpg")  # america picture
        screen.blit(pic, Rect(700, 0, 105, 78))
        text = controlsFont.render("1.7M", 1, white)  # legend numbers
        screen.blit(text, Rect(880, 590, 40, 20))
        text = controlsFont.render("1.4M", 1, white)
        screen.blit(text, Rect(880, 630, 40, 20))
        population = 1500000  # changes population to vary count
    elif country == europe:  # if europe is clicked
        draw.rect(screen, white, (700, 0, 300, 220))
        pic = image.load("MariaLanaEurope.jpg")  # europe picture
        screen.blit(pic, Rect(740, 10, 105, 78))
        text = controlsFont.render("3.6M", 1, white)  # legend numbers
        screen.blit(text, Rect(880, 590, 40, 20))
        text = controlsFont.render("2.9M", 1, white)
        screen.blit(text, Rect(880, 630, 40, 20))
        population = 3300000  # changes population to vary count
    elif country == africa:  # if africa is clicked
        draw.rect(screen, white, (700, 0, 300, 220))
        europePic = image.load("MariaLanaAfrica.jpg")  # africa picture
        screen.blit(europePic, Rect(740, 10, 105, 78))
        text = controlsFont.render("4.9M", 1, white)  # legend numbers
        screen.blit(text, Rect(880, 630, 40, 20))
        text = controlsFont.render("4.3M", 1, white)
        screen.blit(text, Rect(880, 590, 40, 20))
        population = 4600000  # changes population to vary count
    # draws legend and key symbols
    drawWoman(850, 595, pink)
    draw.rect(screen, white, (10, 655, 650, 50))
    draw.line(screen, white, (865, 603), (875, 603), 4)
    draw.line(screen, white, (865, 608), (875, 608), 4)
    draw.circle(screen, blue, (850, 630), 7)  # head
    draw.rect(screen, blue, (850 - 8, 630 + 6, 16, 22))  # torso
    draw.rect(screen, black, (850 - 1, 630 + 20, 3, 10))
    draw.rect(screen, blue, (850 - 10, 630 + 6, 2, 12))  # arms
    draw.rect(screen, blue, (850 + 8, 630 + 6, 2, 12))
    draw.line(screen, white, (865, 640), (875, 640), 4)
    draw.line(screen, white, (865, 645), (875, 645), 4)
    # key explanation
    statusFont = font.SysFont("Arial", 20)
    statustext1 = statusFont.render("HEALTHY:", 1, black)
    screen.blit(statustext1, Rect(20, 660, 400, 100))
    statustext1 = statusFont.render(str(int(population * healthyCount)), 1, black)  # count based on healthy count times the country's population
    screen.blit(statustext1, Rect(130, 660, 400, 100))
    statustext1 = statusFont.render("SICK:", 1, black)
    screen.blit(statustext1, Rect(300, 660, 400, 100))
    statustext1 = statusFont.render(str(int(population * sickCount)), 1, black)  # count based on healthy count times the country's population
    screen.blit(statustext1, Rect(355, 660, 400, 100))
    statustext1 = statusFont.render("DEAD:", 1, black)
    screen.blit(statustext1, Rect(500, 660, 400, 100))
    statustext1 = statusFont.render(str(int(population * deadCount)), 1, black)  # count based on healthy count times the country's population
    screen.blit(statustext1, Rect(560, 660, 400, 100))
    if cure == True:
        if sickCount == 0 and healthyCount != 225 and deadCount != 0: #if simulation is over when there is a cure
            time.wait(2000)
            endScreen = True # end of simulation screen
            simulationRun = False
            display.flip()
    else:
        if deadCount + immunityCount == 225 and healthyCount == 0 and sickCount == 0: #if simulation is over when there is no cure
            time.wait(2000)
            endScreen = True
            simulationRun = False
            display.flip()


def writePopulationData(): #write population data from current simulation for future one
    global col
    print("start writing population data")
    populationFile = open("MariaLanaPopulationData.txt", "w") #open file for writing
    for i in range(15): #same grid loop
        for j in range(15):
            populationFile.write(str(col[i][j])) #write status of person (from previous run before closing) into file
            if j < 14:
                populationFile.write(",") # divides up data
        populationFile.write("\n")
    populationFile.close()


def readPopulationData(): #reads population data from the previous simulation
    global col
    populationFile = open("MariaLanaPopulationData.txt", "r") #open file for reading
    for i in range(15):
        row = []
        rowFile = populationFile.readline() #reads line from the previous simulation
        strRow = rowFile.split(',') #splits data at the comma
        for j in range(15): #goes through each row
            row.append(int(strRow[j])) #appends the pop data point into list row
        col.append(row) #creates a list of rows
    populationFile.close()


def writeFactorData():#method to write factor data from previous simulation
    global america     #uses same variables defined globally
    global africa
    global europe
    global slowSpread
    global mediumSpread
    global fastSpread
    global cure
    global immunity1
    global immunity2
    global immunity3
    global immunity4
    global immunityPercent
    global months6
    global year1
    global year6
    global ex
    global dx
    global healthyCount
    global sickCount
    global deadCount
    global immunityCount
    #initializes strings
    location = ''
    rate = ''
    time = ''
    factorFile = open("MariaLanaFactorsData.txt", "w")
    #different file recording depending on button clicked
    if america:
        location = 'america'
    if europe:
        location = 'europe'
    if africa:
        location = 'africa'
    if slowSpread:
        rate = 'slowSpread'
    if mediumSpread:
        rate = 'mediumSpread'
    if fastSpread:
        rate = 'fastSpread'
    if months6:
        time = 'months6'
    if year1:
        time = 'year1'
    if year6:
        time = 'year6'
    # Exact writing into file with organization
    factorFile.write("location=" + location + "\n")
    factorFile.write("rate=" + rate + "\n")
    factorFile.write("cure=" + str(cure) + "\n")
    factorFile.write("immunityPercent=" + str(immunityPercent) + "\n")
    factorFile.write("immunity1=" + str(immunity1) + "\n")
    factorFile.write("immunity2=" + str(immunity2) + "\n")
    factorFile.write("immunity3=" + str(immunity3) + "\n")
    factorFile.write("immunity4=" + str(immunity4) + "\n")
    factorFile.write("time=" + time + "\n")
    factorFile.write("ex=" + str(ex) + "\n")
    factorFile.write("dx=" + str(dx) + "\n")
    factorFile.write("healthyCount=" + str(healthyCount) + "\n")
    factorFile.write("sickCount=" + str(sickCount) + "\n")
    factorFile.write("deadCount=" + str(deadCount) + "\n")
    factorFile.write("immunityCount=" + str(immunityCount) + "\n")
    factorFile.close() # closes file


def readFactorData(): #method to read factor data next simulation
    global america
    global africa
    global europe
    global slowSpread
    global mediumSpread
    global fastSpread
    global cure
    global immunity1
    global immunity2
    global immunity3
    global immunity4
    global immunityPercent
    global months6
    global year1
    global year6
    global ex
    global dx
    global lengthToHealing
    global healthyCount
    global sickCount
    global deadCount
    global immunityCount
    factorFile = open("MariaLanaFactorsData.txt", "r") #opens file for reading
    row = factorFile.readline() #read line from previous written file
    rowSplit = row.split('=') #divide data at the equal sign
    if rowSplit[0] == 'location':  #if first word is location all location buttons will be false to avoid two being True
        america = False
        europe = False
        africa = False
        location = rowSplit[1].rstrip("\n") #change value of location
        #change simulation reaction based on location readings
        if location == 'america':
            america = True
        elif location == 'europe':
            europe = True
        elif location == 'africa':
            africa = True

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'rate': #if first word is rate all rate buttons are false
        fastSpread = False
        slowSpread = False
        mediumSpread = False
        rate = rowSplit[1].rstrip("\n") #reads value of rate
        if rate == 'fastSpread':
            fastSpread = True
        elif rate == 'mediumSpread':
            mediumSpread = True
        elif rate == 'slowSpread':
            slowSpread = True

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'cure': #if first word is cure, check condition
        if rowSplit[1].rstrip("\n") == 'True':
            cure = True #run simulation with a cure
        else:
            cure = False #run simulation without a cure

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'immunityPercent': #read value of the immunity percentage of population
        immunityPercent = int(rowSplit[1].rstrip("\n"))

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'immunity1': # first button chosen, make the variable true
        if rowSplit[1].rstrip("\n") == 'True':
            immunity1 = True
        else:
            immunity1 = False

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'immunity2': # second button chosen, make the variable true
        if rowSplit[1].rstrip("\n") == 'True':
            immunity2 = True
        else:
            immunity2 = False

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'immunity3': # third button chosen, make the variable true
        if rowSplit[1].rstrip("\n") == 'True':
            immunity3 = True
        else:
            immunity3 = False

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'immunity4': # fourth button chosen, make the variable true
        if rowSplit[1].rstrip("\n") == 'True':
            immunity4 = True
        else:
            immunity4 = False

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'time': # reads time that will pass until healing begins
        months6 = False
        year1 = False
        year6 = False
        if rowSplit[1].rstrip("\n") == 'months6':
            months6 = True
            lengthToHealing = 30 # how long until people stop becoming more infected, and start getting healthy again
        elif rowSplit[1].rstrip("\n") == 'year1':
            year1 = True
            lengthToHealing = 60
        elif rowSplit[1].rstrip("\n") == 'year6':
            year6 = True
            lengthToHealing = 100

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'ex': #retrieve numbers for count
        ex = int(rowSplit[1].rstrip("\n"))

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'dx': #retrieve numbers for count
        dx = int(rowSplit[1].rstrip("\n"))

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'healthyCount': #retrieve numbers for count
        healthyCount = int(rowSplit[1])

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'sickCount': #retrieve numbers for count
        sickCount = int(rowSplit[1])

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'deadCount': #retrieve numbers for count
        deadCount = int(rowSplit[1])

    row = factorFile.readline()
    rowSplit = row.split('=')
    if rowSplit[0] == 'immunityCount': #retrieve numbers for count
        immunityCount = int(rowSplit[1])

    factorFile.close()

#initiate starting status' before running
stillScreen = False
startCounter = 0
startScreen = True
simulationRun = False
endScreen = False
running = True
mainscreen = False
immunityPercent=0
# CONTROL PAD
while running: #simulation loop
    if startScreen: # start up screen
        drawstartScreen() # draw buttons and title
        for evnt in event.get():
            if evnt.type == QUIT: #if simulation is exited
                running = False
            if evnt.type == MOUSEBUTTONDOWN:
                mx, my = evnt.pos
                if 280 < mx < 730 and 310 < my < 370: #if "run from previous" button is clicked
                    draw.rect(screen, white, (0, 0, 1000, 700))
                    stillsimscreen() #run method of still screen (draws simulation start position)
                    readPopulationData() #read the file data
                    readFactorData() #read the file data
                    # changing visuals and variables based on location
                    if america:
                        populationInfo(america) #show america pic and legend
                        locationButtonA = red # change colours permanently when clicked (so user knows which options were chosen)
                        locationButtonB = white
                        locationButtonC = white
                    elif europe:
                        populationInfo(europe)
                        locationButtonA = white
                        locationButtonB = red
                        locationButtonC = white
                    elif africa:
                        populationInfo(africa)
                        locationButtonA = white
                        locationButtonB = white
                        locationButtonC = red
                    # changing visuals and variables based on speed of infection
                    if fastSpread:
                        speedInfect = randint(100, 500) #range that effects probability/speed of infection
                        spreadButtonA = red
                        spreadButtonB = white
                        spreadButtonC = white
                        spreadButtonD = white
                    elif mediumSpread:
                        speedInfect = randint(701, 1100)
                        spreadButtonA = white
                        spreadButtonB = red
                        spreadButtonC = white
                        spreadButtonD = white
                    elif slowSpread:
                        speedInfect = randint(1200, 1600)
                        spreadButtonA = white
                        spreadButtonB = white
                        spreadButtonC = red
                        spreadButtonD = white
                    else:
                        speedInfect = 0
                        spreadButtonA = white
                        spreadButtonB = white
                        spreadButtonC = white
                        spreadButtonD = red
                    # changing visuals and variables based on immunity
                    if immunity1:
                        immunityButtonA = red
                        immunityButtonB = white
                        immunityButtonC = white
                        immunityButtonD = white
                    elif immunity2:
                        immunityButtonA = white
                        immunityButtonB = red
                        immunityButtonC = white
                        immunityButtonD = white
                    elif immunity3:
                        immunityButtonA = white
                        immunityButtonB = white
                        immunityButtonC = red
                        immunityButtonD = white
                    elif immunity4:
                        immunityButtonA = white
                        immunityButtonB = white
                        immunityButtonC = white
                        immunityButtonD = red
                    # changing visuals and variables based on cure or not
                    if cure:
                        cureButtonA = red
                        cureButtonB = white
                    else:
                        cureButtonB = red
                        cureButtonA = white
                    # changing visuals and variables based on length of infection active
                    if months6:
                        lengthToHealing = 30
                        infectionActiveA = red
                        infectionActiveB = white
                        infectionActiveC = white
                    elif year1:
                        lengthToHealing = 60
                        infectionActiveA = white
                        infectionActiveB = red
                        infectionActiveC = white
                    elif year6:
                        lengthToHealing = 100
                        infectionActiveA = white
                        infectionActiveB = white
                        infectionActiveC = red
                    drawControls() # draws control panel with buttons clicked
                    redrawIcons() #run method to redraw after quitting
                    display.flip()
                    time.wait(1000) # waits 1 sec before continuing simulation
                    convertImmuneRun = True
                    simulationRun = True
                    startScreen = False
                elif 280 < mx < 730 and 435 < my < 495:
                    assignCol()
                    mainscreen = True
                    startScreen = False
                    simulationRun = False
            if evnt.type == MOUSEMOTION: # hover colour changes on start screen buttons
                mx, my = evnt.pos
                if 280 < mx < 730 and 310 < my < 370:
                    startColoursA = grey
                elif 280 < mx < 730 and 435 < my < 495:
                    startColoursB = grey
                else:
                    startColoursA = white
                    startColoursB = white
    if mainscreen: # when starting simulation from scratch (not reading files), control panel factors are chosen here
        draw.rect(screen, white,(0, 0, 1000 ,700))
        drawControls()
        stillsimscreen() #run still simulation screen (not simulation running, but the starting picture of it)
        for evnt in event.get():
            if evnt.type == QUIT:
                running = False
            if evnt.type == MOUSEMOTION:
                mx, my = evnt.pos #if mouse hovers over certain coordinates
                if 790 < mx < 850 and 300 < my < 320:
                    locationButtonA = red
                elif 860 < mx < 920 and 300 < my < 320:
                    locationButtonB = red
                elif 930 < mx < 990 and 300 < my < 320:
                    locationButtonC = red
                elif 690 < mx < 780 and 365 < my < 385:
                    spreadButtonA = red
                elif 795 < mx < 885 and 365 < my < 385:
                    spreadButtonB = red
                elif 900 < mx < 990 and 365 < my < 385:
                    spreadButtonC = red
                elif 860 < mx < 890 and 411 < my < 431:
                    cureButtonA = red
                elif 900 < mx < 930 and 411 < my < 431:
                    cureButtonB = red
                elif 690 < mx < 720 and 480 < my < 500:
                    immunityButtonA = red
                elif 740 < mx < 810 and 480 < my < 500:
                    immunityButtonB = red
                elif 830 < mx < 900 and 480 < my < 500:
                    immunityButtonC = red
                elif 920 < mx < 990 and 480 < my < 500:
                    immunityButtonD = red
                elif 700 < mx < 780 and 600 < my < 647:
                    runButton = lightRed
                elif 690 < mx < 770 and 550 < my < 570:
                    infectionActiveA = red
                elif 800 < mx < 880 and 550 < my < 570:
                    infectionActiveB = red
                elif 910 < mx < 990 and 550 < my < 570:
                    infectionActiveC = red
                else: # colour constants that occur when not hovering over
                    locationButtonA = white
                    locationButtonB = white
                    locationButtonC = white
                    spreadButtonA = white
                    spreadButtonB = white
                    spreadButtonC = white
                    cureButtonA = white
                    cureButtonB = white
                    immunityButtonA = white
                    immunityButtonB = white
                    immunityButtonC = white
                    immunityButtonD = white
                    infectionActiveA = white
                    infectionActiveB = white
                    infectionActiveC = white
                    runButton = red
            if evnt.type == MOUSEBUTTONDOWN: #if button is clicked
                mx, my = evnt.pos
                if 790 < mx < 850 and 300 < my < 320: # america clicked - change status of variables and button colours
                    america = True
                    europe = False
                    africa = False
                elif 860 < mx < 920 and 300 < my < 320: # europe clicked - change status of variables and button colours
                    europe = True
                    america = False
                    africa = False
                elif 930 < mx < 990 and 300 < my < 320: # africa clicked - change status of variables and button colours
                    africa = True
                    europe = False
                    america = False
                elif 690 < mx < 780 and 365 < my < 385: # fast spreading clicked - change status of variables and button colours
                    fastSpread = True
                    mediumSpread = False
                    slowSpread = False
                elif 795 < mx < 885 and 365 < my < 385: # medium spreading clicked - change status of variables and button colours
                    mediumSpread = True
                    fastSpread = False
                    slowSpread = False
                elif 900 < mx < 990 and 365 < my < 385: # slow clicked - change status of variables and button colours
                    slowSpread = True
                    mediumSpread = False
                    fastSpread = False
                elif 860 < mx < 890 and 411 < my < 431: # yes cure clicked - change status of variables and button colours
                    cure = True
                    cureNo = False
                elif 900 < mx < 930 and 411 < my < 431: # no cure clicked - change status of variables and button colours
                    cure = False
                    cureNo = True # used for colour change later
                elif 690 < mx < 720 and 480 < my < 500: # 0% immune clicked - change status of variables and button colours
                    immunity1 = True
                    immunity2 = False
                    immunity3 = False
                    immunity4 = False
                    immunityPercent = findImmune(1)
                    healthyPercent = 100 - immunityPercent
                elif 740 < mx < 810 and 480 < my < 500: # 10-30% immune clicked - change status of variables and button colours
                    immunity2 = True
                    immunity1 = False
                    immunity3 = False
                    immunity4 = False
                    immunityPercent = findImmune(2)
                    healthyPercent = 100 - immunityPercent
                elif 830 < mx < 900 and 480 < my < 500: # 40-70% immune clicked - change status of variables and button colours
                    immunity3 = True
                    immunity2 = False
                    immunity1 = False
                    immunity4 = False
                    immunityPercent = findImmune(3)
                    healthyPercent = 100 - immunityPercent
                elif 920 < mx < 990 and 480 < my < 500: # 80-90% clicked - change status of variables and button colours
                    immunity4 = True
                    immunity2 = False
                    immunity3 = False
                    immunity1 = False
                    immunityPercent = findImmune(4)
                    healthyPercent = 100 - immunityPercent
                elif 690 < mx < 770 and 550 < my < 570: # 6 months active clicked - change status of variables and button colours
                    months6 = True
                    year1 = False
                    year6 = False
                    lengthToHealing = 30
                elif 800 < mx < 880 and 550 < my < 570: # 1 year active clicked - change status of variables and button colours
                    year1 = True
                    months6 = False
                    year6 = False
                    lengthToHealing = 60
                elif 910 < mx < 990 and 550 < my < 570: # 3 years active clicked - change status of variables and button colours
                    year6 = True
                    year1 = False
                    months6 = False
                    lengthToHealing = 100
                elif 700 < mx < 780 and 600 < my < 647: # can only run simulation if all factors are chosen
                    if (america == True or europe == True or africa == True) and (slowSpread == True or mediumSpread == True or fastSpread == True) and (cure == True or cure == False) and (immunity1 == True or immunity2 == True or immunity3 == True or immunity4 == True) and (months6 == True or year1 == True or year6 == True):
                        simulationRun = True
                        mainscreen = False

        # changing button colours permanently when clicked, changing variables affected
        if america == True: #if america is clicked
            locationButtonA = red #change status of america
            populationInfo(america)
        elif europe == True:  #if europe is clicked
            locationButtonB = red  # change status of europe
            populationInfo(europe)
        elif africa == True: #if africa is clicked
            locationButtonC = red #change status of africa
            populationInfo(africa)

        if fastSpread: #if fast spread is clicked
            speedInfect = randint(100, 500) #change status
            spreadButtonA = red
        elif mediumSpread:
            speedInfect = randint(701, 1100) #change status
            spreadButtonB = red
        elif slowSpread:
            speedInfect = randint(1200, 1600) #change status
            spreadButtonC = red
        else:
            speedInfect = 0

        if cure:
            cureButtonA = red #change status of button colour
        if cureNo:
            cureButtonB = red #change status of button colour

        if immunity1:
            immunityButtonA = red #change status of button colour
        elif immunity2:
            immunityButtonB = red #change status of button colour
        elif immunity3:
            immunityButtonC = red #change status of button colour
        elif immunity4:
            immunityButtonD = red #change status of button colour

        if months6:
            infectionActiveA = red #change status of button colour
        elif year1:
            infectionActiveB = red #change status of button colour
        elif year6:
            infectionActiveC = red #change status of button colour

        drawControls() # draw controls, updates in the loop when different button clicked (colour changes)


    if simulationRun: #if simulation is running (both from scratch and from reading files, same function used)
        for evnt in event.get():
            if evnt.type == QUIT:
                writePopulationData()
                writeFactorData()
                running = False
        if (not convertImmuneRun) and immunityPercent > 0 :
            convertImmune(immunityPercent)
            redrawIcons()
            convertImmuneRun=True
            print("immunityPercent=" + str(immunityPercent))

        simscreen(dx, ex, speedInfect)
        ex += 1
        dx += 1
        if america:
            populationInfo(america)
        if europe:
            populationInfo(europe)
        if africa:
            populationInfo(africa)


    if endScreen: # once simulation ends -- (NO CURE) people all die or (CURE) people who didn't die restore health
        for evnt in event.get(): # mouse events
            if evnt.type == QUIT:
                running = False
        draw.rect(screen, white, (0, 0, 1000, 700)) # redraw
        endText = font.SysFont("Impact", 30)  # done once
        text = endText.render("Simulation Finished", 1, (255, 0, 0))
        screen.blit(text, Rect(200, 200, 400, 100))

    display.flip()
quit()