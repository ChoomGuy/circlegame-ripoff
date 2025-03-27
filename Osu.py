import pygame # type: ignore
import random
import time

weightedY = [i for i in range(14,761)]
for i in range(5):
    weightedY.append([ j for j in range(239,610)])
pygame.init()
pygame.display.set_caption('Osu Ripoff')
Width = 1920
Height = 1080
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
timer = pygame.event.custom_type()
pygame.time.set_timer(timer, 250)
running = True
#Fonts
font_150 = pygame.font.Font(r"OtherHand.otf", 150)
font_100 = pygame.font.Font(r"OtherHand.otf", 100)
#Cursor
CursorRaw = pygame.image.load(r"OsuRipoffIcon.png")
Cursor = pygame.transform.scale(CursorRaw,(100,100))
CursorCenter = Cursor.get_rect()
pygame.mouse.set_visible(False)
#Colours
Purple = (150, 0, 150)
Red = (255, 0, 0)
Green =(0, 200, 50)

class Button: #button class
    def __init__(self, screen, font, text, colour, x_div, y_div, action):
        self.screen = screen
        self.font = font
        self.text = text
        self.colour = colour
        self.x_div = x_div
        self.y_div = y_div
        self.action = action
        self.rec_pos = None

    def ButtonVar(self): #screen, font variable, text, colour x_div and y_div
        button_text = font_100.render(self.text, True, self.colour, (0, 0, 0)) #sets up rendering for the text
        self.rec_pos = button_text.get_rect(center=(Width // self.x_div, Height // self.y_div)) #centers the text
        screen.blit(button_text, self.rec_pos) #renders the text

    def Button_Pressed(self, mouse_pos):
        if self.rec_pos and self.rec_pos.collidepoint(mouse_pos):
            if self.action:
                self.action()
    
class Player:
    def __init__(self, Name, Score, button):
        self.Name = Name
        self.Score = Score
        self.button = None

class TextBox: #responsible for variables in TextBox
    def __init__(self, screen, font, text, colour, x_div, y_div, rect=None):
        self.screen = screen
        self.font = font
        self.text = text
        self.colour = colour
        self.x_div = x_div
        self.y_div = y_div
        self.rect = rect
    
    def EditText(self, char):
        if event.type == pygame.KEYDOWN:
            if char == "\b":
                self.text = self.text[:-1] #:-1 removes 1 charater from the end of the text
            else:
                self.text += char #gets key that was pressed
                #print(self.text)

    def Box(self):
        text_box = self.font.render(self.text, True, self.colour, (0, 0, 0))
        textcentre = text_box.get_rect(center=(Width // 2, Height // 2))
        self.screen.blit(text_box, textcentre)

def PreGame():
    screen.fill("black")
    NameHeader.ButtonVar()
    Start_Button.ButtonVar()
    Corner_Quit.ButtonVar()
    Back_Menu.ButtonVar()
    PlayerTB.Box()

def Main(Current_Rect, Score):
    screen.fill("black")
    print(PlayerData.Score)
    global Game_State
    global Rand_x, Rand_y
    Rand_x = random.randint(210, 1156)
    Rand_y = weightedY[random.randint(0,len(weightedY))]
    print(f'{Rand_x, Rand_y=}')
    Rand_xy = (Rand_x, Rand_y)
    pygame.draw.circle(screen, "purple", (Rand_x, Rand_y), 64)
    Current_Rect.append(Rand_xy)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    Score.ButtonVar()
    for points in Current_Rect[:]:  # Iterate over a copy to modify safely
        rect_object = pygame.Rect(points[0]-64, points[1]-64, 128,128)
        pygame.draw.rect(screen, "purple", rect_object)
    PointLen = len(Current_Rect)
    if PointLen > 10:
        Game_State = "Menu"

def PrePreGame():
    global Game_State
    Game_State = "PreGame"

def Back():
    global Game_State
    Game_State = "Menu"

def Start():
    global Game_State
    Game_State = "Start"

def Stop():
    global running
    print("stopped")
    running = False

PlayerTB = TextBox(screen, font_150, "", Red, 2, 2)
PlayerData = Player(None, 0, None)

#The button class can be used as general text output
#     def __init__(self, screen, font, text, colour, x_div, y_div, action):

NameHeader = Button(screen, font_150, "Enter your Name", Purple, 2, 4, None)
Start_Button = Button(screen, font_100, "Start", Green, 2, 1.5, Start)
Play_Button = Button(screen, font_100, "Play", Green, 2, 2, PrePreGame) #variables for the buttons
Quit_Button = Button(screen, font_100, "Quit", Red, 2, 1.5, Stop)
Corner_Quit = Button(screen, font_100, "X", Red, 20, 12, Stop)
Back_Menu = Button(screen, font_100, "Back", Red, 14, 1.1, Back)
Score = Button(screen, font_150, str(PlayerData.Score), Green, 2, 2, Start)

def MainMenu(): #x and y div control position of text
    screen.fill("black")
    menu_text = font_150.render("Game", True, (150, 0, 150), (0, 0, 0))
    textcentre = menu_text.get_rect(center=(Width // 2, Height // 4))
    screen.blit(menu_text, textcentre)
    Play_Button.ButtonVar()
    Quit_Button.ButtonVar()

Game_State = "Menu" #current game state
Current_Rect = [] #current nodes on screen

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Game_State == "Menu":
                Quit_Button.Button_Pressed(mouse_pos)
                Play_Button.Button_Pressed(mouse_pos)
            if Game_State == "PreGame":
                Corner_Quit.Button_Pressed(mouse_pos)
                Start_Button.Button_Pressed(mouse_pos)
                Back_Menu.Button_Pressed(mouse_pos)
        elif event.type == pygame.KEYDOWN:
            if Game_State == "PreGame":
                PlayerTB.EditText(event.unicode)
            if event.key in [pygame.K_e, pygame.K_r]:
                for points in Current_Rect:
                    rect_object = pygame.Rect(points[0]-64, points[1]-64, 128,128)
                    if rect_object.collidepoint(mouse_pos[0], mouse_pos[1]):
                        PlayerData.Score += 1
                        Current_Rect.remove(points)
                        Score.text = str(PlayerData.Score)
        elif event.type == timer and Game_State == "Start":
            Main(Current_Rect, Score)  # Trigger rectangle creation on timer event

    CursorCenter.center = mouse_pos

    if Game_State == "Menu":
        MainMenu()
    elif Game_State == "PreGame":
        PreGame()
    elif Game_State == "Start":
        screen.fill("black")
        Score.ButtonVar()
        for points in Current_Rect: #redraw all
            pygame.draw.circle(screen, "purple", (points[0], points[1]), 64)
    screen.blit(Cursor, CursorCenter)
    pygame.display.flip()
    clock.tick(165) # just gonna assume this is the "fps"

pygame.quit()