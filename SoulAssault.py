import pygame,os,sys,time,random
from pygame.locals import *

#Set Window on Center
os.environ['SDL_VIDEO_CENTERED'] = '1'

#Init
pygame.init()

#Screen Resolution
width = 16
height = 10
Tile_Size = 50
w_t = width*Tile_Size
h_t = height*Tile_Size+100
res = (w_t, h_t) #800*600

#Interface
clock = pygame.time.Clock()
screen = pygame.display.set_mode((res))
pygame.display.set_caption("SoulAssault")
FPS = 30

#Character Setup
chara_x = 100  #Player Position
chara_y = 100  #Player Position
fired = 0
chara_pos = (chara_x,chara_y)
c_width = 100  #Player Size
c_height = 100 #Player Size
vel = 8
karma = 0
velar = 20
repos = 770

# Texture/Image Pre-Cached Loading Optimisation
IMAGES = {}
def precacheImage(texture):
    if not texture in IMAGES:
        IMAGES[texture] = pygame.image.load(texture)
    return IMAGES[texture]

col = 0
row = 0

#Define Tile Texture
Black = ((0,0,0))
White = ((255,255,255))
Grey = ((188,188,188))
Wall    = precacheImage('images/wall.png')
Floor   = precacheImage('images/floor.png')
fontSize = 25
myFont = pygame.font.SysFont("Arial", fontSize)
fontColor = (170,170,170)
fontBack = (45,36,63)

#Intro

pos = (50,510)
text = "Приветствую, странник!"
fontImage = myFont.render(text,0,(fontColor))
screen.blit(fontImage,pos)
pygame.display.update()
time.sleep(2)
fontImage = myFont.render(text,0,(0,0,0))
screen.blit(fontImage,pos)
pygame.display.update()
text = "Позволь объяснить, как здесь заведено..."
fontImage = myFont.render(text,0,(fontColor))
screen.blit(fontImage,pos)
pygame.display.update()
time.sleep(2)
fontImage = myFont.render(text,0,(0,0,0))
screen.blit(fontImage,pos)
pygame.display.update()
text = "Стрелки позволят тебе перемещаться,"
fontImage = myFont.render(text,0,(fontColor))
screen.blit(fontImage,pos)
pygame.display.update()
time.sleep(2)
fontImage = myFont.render(text,0,(0,0,0))
screen.blit(fontImage,pos)
pygame.display.update()
text = "Shift - выбраться, если ты зацепишься за стену."
fontImage = myFont.render(text,0,(fontColor))
screen.blit(fontImage,pos)
pygame.display.update()
time.sleep(2)
fontImage = myFont.render(text,0,(0,0,0))
screen.blit(fontImage,pos)
pygame.display.update()
text = "Нажмите F, чтобы закричать"
fontImage = myFont.render(text,0,(fontColor))
screen.blit(fontImage,pos)
pygame.display.update()
time.sleep(2)
fontImage = myFont.render(text,0,(0,0,0))
screen.blit(fontImage,pos)
pygame.display.update()
text = "или поговорить с другим персонажем)"
fontImage = myFont.render(text,0,(fontColor))
screen.blit(fontImage,pos)
pygame.display.update()
time.sleep(2)
fontImage = myFont.render(text,0,(0,0,0))
screen.blit(fontImage,pos)
pygame.display.update()
text = "А теперь... Пора просыпаться и на работу!"
fontImage = myFont.render(text,0,(fontColor))
screen.blit(fontImage,pos)
pygame.display.update()
time.sleep(2)
fontImage = myFont.render(text,0,(0,0,0))
screen.blit(fontImage,pos)
pygame.display.update()

#Tile Variable Predefine
W = 0
B = 1
P = 2
T = 6
V = 7
O = 8
D = 9

#Player Animation
Move_Right = [
    precacheImage('images/walk6-1-right.png'),
    precacheImage('images/walk6-2-right.png'),
    precacheImage('images/walk6-3-right.png'),
    precacheImage('images/walk6-2-right.png'),
    precacheImage('images/walk6-1-right.png'),
    precacheImage('images/walk6-4-right.png'),
    precacheImage('images/walk6-5-right.png'),
    precacheImage('images/walk6-4-right.png')
]
Move_Left = [
    precacheImage('images/walk6-1-left.png'),
    precacheImage('images/walk6-2-left.png'),
    precacheImage('images/walk6-3-left.png'),
    precacheImage('images/walk6-2-left.png'),
    precacheImage('images/walk6-1-left.png'),
    precacheImage('images/walk6-4-left.png'),
    precacheImage('images/walk6-5-left.png'),
    precacheImage('images/walk6-4-left.png')
]
Move_Up = [
    precacheImage('images/walk6-1-up.png'),
    precacheImage('images/walk6-2-up.png'),
    precacheImage('images/walk6-3-up.png'),
    precacheImage('images/walk6-2-up.png'),
    precacheImage('images/walk6-1-up.png'),
    precacheImage('images/walk6-4-up.png'),
    precacheImage('images/walk6-5-up.png'),
    precacheImage('images/walk6-4-up.png')
]
Move_Down = [
    precacheImage('images/walk6-1-down.png'),
    precacheImage('images/walk6-2-down.png'),
    precacheImage('images/walk6-3-down.png'),
    precacheImage('images/walk6-2-down.png'),
    precacheImage('images/walk6-1-down.png'),
    precacheImage('images/walk6-4-down.png'),
    precacheImage('images/walk6-5-down.png'),
    precacheImage('images/walk6-4-down.png')
]

isLeft  = False
isRight = False
isUp    = False
isDown  = False

# init Character Properties and Movement, etc etc
char = pygame.sprite.Sprite()
char.rect = pygame.Rect(chara_x,chara_y,c_width,c_height)
char.image = precacheImage('images/walk6-1-up.png')
char.last_walk_anim = Move_Down[0]
char.last_char_rect = Move_Down[0].get_rect()
char.walk_count = 0

# Begin Pos
def DefaultSpawn(x=350,y=200):
    global chara_x,chara_y, n
    chara_x = x
    chara_y = y
    char.rect.x = chara_x
    char.rect.y = chara_y
    n = random.randint(6,15)

DefaultSpawn()

# Collipsions
C_GROUP_WALL = pygame.sprite.Group()
C_GROUP_STAIRS = pygame.sprite.Group()
C_PLAYER = pygame.sprite.Group()

# Changelevel Brush
TRIGGER_CHANGELEVEL_T = pygame.sprite.Group()
TRIGGER_CHANGELEVEL_V = pygame.sprite.Group()
TRIGGER_CHANGELEVEL_RETURN = pygame.sprite.Group()
TRIGGER_CHANGELEVEL_V_RETURN = pygame.sprite.Group()

map_default = [
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W],
    [O, B, B, B, B, B, B, B, B, B, B, B, B, B, B, W],
    [O, B, B, B, B, B, B, B, B, B, B, B, B, B, B, W],
    [W, B, B, W, B, B, W, B, B, W, W, W, W, B, B, W],
    [W, B, B, B, B, B, B, B, B, B, B, B, B, B, B, W],
    [W, B, B, B, B, B, B, B, B, B, B, B, B, B, B, T],
    [W, B, B, W, B, B, W, B, B, W, W, W, W, B, B, T],
    [W, B, B, B, B, B, B, B, B, B, B, B, B, B, B, W],
    [W, B, B, B, B, B, B, B, B, B, B, B, B, B, B, W],
    [W, W, W, W, W, W, W, W, W, W, W, W, W, W, W, W]
]

PRECACHED_MAP = {}
def precacheMap(file):
    if not file in PRECACHED_MAP:
        fo = open(file, "r+")
        data = fo.readlines()
        fo.close()
        PRECACHED_MAP[file] = data
    return PRECACHED_MAP[file]

def loadMapfromFile(file):
    if not file:
        return False
    #fo = open("Stage2.txt","r+") #todo: This is a Reference original to load a file.
    lines = precacheMap(file)
    map = []
    mxLines = len(lines)
    for r in range(mxLines):
        line = lines[r]
        lineMap = []
        mxCol = len(line)
        for c in range(mxCol):
            if line[c] == "\n":
                continue
            # W, P, T, V, B
            elif line[c] == "W":
                lineMap.append(W)
            elif line[c] == "B":
                lineMap.append(B)
            elif line[c] == "P":
                lineMap.append(P)
            elif line[c] == "T":
                lineMap.append(T)
            elif line[c] == "V":
                lineMap.append(V)
            elif line[c] == "O":
                lineMap.append(O)
            elif line[c] == "D":
                lineMap.append(D)
        map.append(lineMap)
    return map

def loadMap(map):
    global NPos
    NPos = (800,600)
    if not map:
        Map_1 = map_default
    else:
        Map_1 = loadMapfromFile(map)

    #Optimisation: Empty on Every Frame Ticks for Wall & Stairs.
    C_GROUP_WALL.empty()
    C_GROUP_STAIRS.empty()

    #Optimisation: Empty on Every Mape Tricks for Trigger Changelevels
    TRIGGER_CHANGELEVEL_T.empty()
    TRIGGER_CHANGELEVEL_V.empty()
    TRIGGER_CHANGELEVEL_RETURN.empty()
    TRIGGER_CHANGELEVEL_V_RETURN.empty()

    
    #Begin Create the Map.
    for row in range(height):
        for col in range(width):
            tile = Map_1[row][col]
            pos = (col * Tile_Size, row * Tile_Size)
            if tile == W:
                w = pygame.sprite.Sprite()
                w.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, Tile_Size, Tile_Size)
                w.image = Wall
                #if (row == 19 and col == 24):
                #    screen.blit(Floor, w.rect)
                #elif (row == 19 and col == 0):
                #    screen.blit(Floor, w.rect)
                #else:
                screen.blit(w.image,w.rect)
                C_GROUP_WALL.add(w)
            if tile == B:
                 b = pygame.sprite.Sprite()
                 b.image = Floor
                 screen.blit(b.image,pos)
            #Trigger Changelevels
            if tile == T:
                t = pygame.sprite.Sprite()
                t.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, Tile_Size, Tile_Size)
                t.image = precacheImage('images/door.png')
                screen.blit(t.image,pos)
                TRIGGER_CHANGELEVEL_T.add(t)
            if tile == V:
                v = pygame.sprite.Sprite()
                v.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, Tile_Size, Tile_Size)
                v.image = Floor
                #v.image.fill((40,40,180))
                screen.blit(v.image,pos)
                NPos = pos
                TRIGGER_CHANGELEVEL_V.add(v)
            if tile == O:
                o = pygame.sprite.Sprite()
                o.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, Tile_Size, Tile_Size)
                o.image = precacheImage('images/door2.png')
                screen.blit(o.image, pos)
                TRIGGER_CHANGELEVEL_RETURN.add(o)
            if tile == D:
                d = pygame.sprite.Sprite()
                d.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, Tile_Size, Tile_Size)
                d.image = pygame.Surface((Tile_Size, Tile_Size))
                d.image.fill((160, 40, 160))
                screen.blit(d.image, pos)
                TRIGGER_CHANGELEVEL_V_RETURN.add(d)

        NPC = pygame.sprite.Sprite()
        NPC.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, Tile_Size, Tile_Size)
        NPC.image = precacheImage('images/walk'+str(n)+'-1-down.png')
        screen.blit(NPC.image,NPos)
            

        #UI
        pos = (0,500)
        UI = pygame.sprite.Sprite()
        UI.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, 800, 600)
        UI.image = precacheImage('images/UIdown.png')
        screen.blit(UI.image, pos)
        

        #timer
        tim = pygame.sprite.Sprite()
        tim.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, 30, 40)
        tim.image = precacheImage('images/time-40.png')
        pos_x = repos-pygame.time.get_ticks()/360
        if pos_x < 610:
            pos_x = 610
            #fired += 1
        pos = (pos_x, 505)
        screen.blit(tim.image, pos)

            

        #lives
        #if fired == 0:
        pos = (650,0)
        life = pygame.sprite.Sprite()
        life.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, Tile_Size, Tile_Size)
        life.image = precacheImage('images/face-50-8.png')
        screen.blit(life.image, pos)
        #elif fired < 2:
        pos = (700,0)
        screen.blit(life.image, pos)
        #elif fired < 3:
        pos = (750,0)
        screen.blit(life.image, pos)
            
                
LEVEL_T = 0
LEVEL_V = 0
LEVEL_TYPE = "T"
def Level():
    curMapT = {
        0 : "Stage0.txt",
        1 : "Stage1.txt",
        2 : "Stage2.txt",
        3 : "Stage3.txt",
        4 : "Stage4.txt"
    }
    curMapV = {
        0 : "Stage3.txt",
        1 : "StageV1.txt",
        2 : "StageV2.txt"
    }
    current = ""
    if LEVEL_TYPE == "T":
        current = curMapT[LEVEL_T]
    elif LEVEL_TYPE == "V":
        current = curMapV[LEVEL_V]

    loadMap(current)

def walk_anim():
    if char.walk_count == 18:
        char.walk_count = 1

    def SetWalkanim(imgseq,imgstill,x,y):
        char.image = imgseq
        screen.blit(char.image,char.rect)
        # Control Movement and Rect
        char.rect = pygame.Rect(imgstill.get_rect())
        char.last_walk_anim = imgstill
        char.last_char_rect = imgstill.get_rect()

    if isLeft:
        SetWalkanim(Move_Left[char.walk_count//3], Move_Left[0], chara_x, chara_y)
    elif isRight:
        SetWalkanim(Move_Right[char.walk_count // 3], Move_Right[0], chara_x, chara_y)
    elif isUp:
        SetWalkanim(Move_Up[char.walk_count // 3], Move_Up[0], chara_x, chara_y)
    elif isDown:
        SetWalkanim(Move_Down[char.walk_count // 3], Move_Down[0], chara_x, chara_y)
    else:
        screen.blit(char.last_walk_anim, (chara_x, chara_y))
        char.rect = pygame.Rect(char.last_char_rect)

    char.rect.x = chara_x
    char.rect.y = chara_y
    char.walk_count += 1

def TriggerChangeMap(player,x,y):
    global LEVEL_T
    global LEVEL_V
    global LEVEL_TYPE
    global NPCol, repos
    
    # Change Levels
    if pygame.sprite.spritecollideany(player, TRIGGER_CHANGELEVEL_T):
        n = random.randint(6,15)
        repos += velar
        LEVEL_TYPE = "T"
        LEVEL_T += 1
        if LEVEL_T == 2:
            DefaultSpawn(50, 250)
        elif LEVEL_T == 0:
            DefaultSpawn(350,200)
        elif LEVEL_T == 1:
            DefaultSpawn(50, 50)
        elif LEVEL_T == 3:
            DefaultSpawn(650, 50)
        elif LEVEL_T == 4:
            DefaultSpawn(650, 100)
        elif LEVEL_T == 5:
            LEVEL_T = 0
            CurMapT = 0
            DefaultSpawn(350,200)
        else:
            DefaultSpawn()

    if pygame.sprite.spritecollideany(player, TRIGGER_CHANGELEVEL_V):
        NPCol = 1
    else:
        NPCol = 0
        

    # Return Maps
    if pygame.sprite.spritecollideany(player, TRIGGER_CHANGELEVEL_RETURN):
        n = random.randint(6,15)
        repos -= velar
        pos = (50,510)
        text = "Зря ты это... Зря-зря-зря-зря-зря..."
        fontImage = myFont.render(text,0,(fontColor))
        screen.blit(fontImage,pos)
        pygame.display.update()
        time.sleep(2)
        if LEVEL_TYPE == "T":
            LEVEL_T -= 1
            if LEVEL_T == 2:
                DefaultSpawn(60, 60)
            elif LEVEL_T == 1:
                DefaultSpawn(670, 250)
            elif LEVEL_T == 0:
                DefaultSpawn(350, 50)
            elif LEVEL_T == 3:
                DefaultSpawn(60, 100)
            else:
                DefaultSpawn()

    if pygame.sprite.spritecollideany(player, TRIGGER_CHANGELEVEL_V_RETURN):
        if LEVEL_TYPE == "V":
            LEVEL_V -= 1
            if LEVEL_V == 1:
                DefaultSpawn(212, 212)
            elif LEVEL_V == 0:
                LEVEL_TYPE = "T"
                DefaultSpawn(594, 108)
            else:
                DefaultSpawn()

def movement(press):
    global isLeft,isDown,isUp,isRight
    global chara_x, chara_y, karma
    press = pygame.key.get_pressed()

    # set Collision group
    C_PLAYER.empty()
    C_PLAYER.add(char)

    TriggerChangeMap(char,chara_x,chara_y)

    hasCol= pygame.sprite.spritecollideany(char,C_GROUP_WALL)

    # Walk
    if press[pygame.K_LEFT]:
        if hasCol:
            chara_x = chara_x
        else:
            chara_x -= vel
        isLeft = True
        isRight = False
        isUp = False
        isDown = False
    elif press[pygame.K_RIGHT]:
        if hasCol:
            chara_x = chara_x
        else:
            chara_x += vel
        isRight = True
        isLeft = False
        isUp = False
        isDown = False
    elif press[pygame.K_UP]:
        if hasCol:
            chara_y = chara_y
        else:
            chara_y -= vel
        isUp = True
        isDown = False
        isLeft = False
        isRight = False
    elif press[pygame.K_DOWN]:
        if hasCol:
            chara_y = chara_y
        else:
            chara_y += vel
        isUp = False
        isDown = True
        isLeft = False
        isRight = False
    else :
        isLeft = False
        isRight = False
        isUp = False
        isDown = False
        char.walk_count = 0

    # Sprint
    if press[pygame.K_LSHIFT] and press[pygame.K_LEFT]:
        if hasCol:
            chara_x = chara_y
        else:
            chara_x -= (vel/2)
    elif press[pygame.K_LSHIFT] and press[pygame.K_RIGHT]:# and chara_x < w_t - c_width - vel:
        chara_x += (vel/2)
    elif press[pygame.K_LSHIFT] and press[pygame.K_UP]:
        chara_y -= (vel/2)
    elif press[pygame.K_LSHIFT] and press[pygame.K_DOWN]:# and chara_y < h_t - c_height - vel:
        chara_y += (vel/2)

    walk_anim()

            #Karma
    kar = pygame.sprite.Sprite()
    kar.rect = pygame.Rect(col * Tile_Size, row * Tile_Size, 30, 40)
    kar.image = precacheImage('images/soul-40.png')
    pos_kar = 610+karma
    if pos_kar < 610:
        pos_kar = 610
    elif pos_kar > 770:
        pos_kar = 770
        #fired += 1
    pos = (pos_kar, 555)
    screen.blit(kar.image, pos)
    pygame.display.update()
    
    #Shout
    if press[pygame.K_f]:
        if NPCol == 1:
            pos = (50,510)
            text = "Oh, hey!"
            fontImage = myFont.render(text,0,(fontColor))
            screen.blit(fontImage,pos)
            pygame.display.update()
            time.sleep(1)
            fontImage = myFont.render(text,0,(fontBack))
            screen.blit(fontImage,pos)
            pygame.display.update()
            text = ["Ah! Who are you?! What do you want?!","Ah, salut... Do you have some spare time? *winking*","Oh... Is someone there?.. Am I dead?..","О, дарова) Чокак?)","..."]
            i = random.randint(0,4)
            fontImage = myFont.render(text[i],0,(fontColor))
            screen.blit(fontImage,pos)
            pygame.display.update()
            time.sleep(2)
            fontImage = myFont.render(text[i],0,(fontBack))
            screen.blit(fontImage,pos)
            pygame.display.update()
            text = ["Don't worry, I was just passing by.. Why are you here? Are you lost?","Sorry, not much... Do you need any help?","Nah, you're still in that awful place... Are you injured?","О, земляк! Да так себе, если честно, но жить можно) Ты как?","He-ey! Are you okay?"]
            fontImage = myFont.render(text[i],0,(fontColor))
            screen.blit(fontImage,pos)
            pygame.display.update()
            time.sleep(2)
            fontImage = myFont.render(text[i],0,(fontBack))
            screen.blit(fontImage,pos)
            pygame.display.update()
            text = ["No... M-m-m... I was going to aphotecary, but met some... bad guys...","Yeah, over there...","Ah... Damn, that thing didn't work aswell... BUTIWANNADIIIE!1!!","Понимаю, бро... Нам только пахать и пахать, чтоб выжить...","Ah! A-ah... Sorry, I was..."]
            fontImage = myFont.render(text[i],0,(fontColor))
            screen.blit(fontImage,pos)
            pygame.display.update()
            time.sleep(2)
            fontImage = myFont.render(text[i],0,(fontBack))
            screen.blit(fontImage,pos)
            pygame.display.update()
            text = ["AH?! Were you robbed?!","*leaving*","Hey-hey, calm down!","Да... Ну ладно, я как раз пахать и бегу... Увидимся!","What's up?"]
            fontImage = myFont.render(text[i],0,(fontColor))
            screen.blit(fontImage,pos)
            pygame.display.update()
            time.sleep(2)
            fontImage = myFont.render(text[i],0,(fontBack))
            screen.blit(fontImage,pos)
            pygame.display.update()
            text = ["Hm-m-m... I 'm in a hurry, but I can't see you crying... Take this and be careful next time..."," ","Ah, sorry! Sorry... I'll leave now... Trying to die even more silent...","Увидимся... Надеюсь...","Firetrucks are actually watertrucks..."]
            fontImage = myFont.render(text[i],0,(fontColor))
            screen.blit(fontImage,pos)
            pygame.display.update()
            time.sleep(2)
            fontImage = myFont.render(text[i],0,(fontBack))
            screen.blit(fontImage,pos)
            pygame.display.update()
            text = ["Ah? Thank you! Thank you very much! I'm leaving now!"," ","*leaving*"," ","OH FIRETRUCK!1!! 0.0"]
            fontImage = myFont.render(text[i],0,(fontColor))
            screen.blit(fontImage,pos)
            pygame.display.update()
            time.sleep(1)
            karma += velar
        else:
            pos = (50,510)
            text = ["Hey! Is anyone there?!","AAAAAAAAAAAAAAAAAAAA"]
            i = random.randint(0,1)
            fontImage = myFont.render(text[i],0,(fontColor))
            screen.blit(fontImage,pos)
            pygame.display.update()
            time.sleep(1)





def game_run():
    run = True
    while run:
        press = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or press[pygame.K_ESCAPE]:
                pygame.quit()
                quit()

        screen.fill((Black))
        Level()
        movement(press)

        pygame.display.update()
        clock.tick(FPS)

game_run()
