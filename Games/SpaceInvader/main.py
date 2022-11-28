import pygame 
from random import randint, random

# initialize the pygane 
pygame.init() 

# screen Size
x, y = 800, 600

# create the screen 
screen = pygame.display.set_mode(size=(x, y)) 

# Setting title 
pygame.display.set_caption("Space Invader") 

# Setting icon 
icon = pygame.image.load("./images/spaceship.png")
pygame.display.set_icon(icon)

# setting background 
background = pygame.image.load("./images/background.jpg")
background = pygame.transform.scale(surface=background, size=(x, y))

# setting background audio 
pygame.mixer.music.load("./audio/background.wav") 
pygame.mixer.music.play(-1)

# setting Score at left-------------------------
score = 0 
font = pygame.font.Font('freesansbold.ttf', 32)

def scoreWindow(): 
    window = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(source=window, dest=(10, 10))
    
# Player ----------------------------------------
playerImg = pygame.image.load("./images/player.png")
playerX, playerY = 350, 500 
move = 0.2
playerXSpeed, playerYSpeed = 0, 0

def player(x, y):
    screen.blit(source=playerImg, dest=(x, y))
    
# Alien ---------------------------------------------
alienImg = pygame.image.load("./images/alien.png") 
alienMove = 0.1

class Alien() :
    def __init__(self) -> None: 
        self.alienX = randint(0, x-64)
        self.alienY = randint(0, 200) 
        self.alienXSpeed = move*random()
        
    def blit(self) :
        screen.blit(source=alienImg, dest=(self.alienX, self.alienY))
        
alienSet = {Alien()}

    
# bullet -------------------------------------------
bulletImg = pygame.image.load("./images/bullet.png")
bulletX, bulletY = 0, 0 
bulletSpeed = 0.5    #  bullet speed
bulletState = False  # True -> bullet fired  # False -> ready to fire
bulletSound = pygame.mixer.Sound("./audio/laser.wav")

def fireBullet(x, y) :
    global bulletState, bulletX, bulletY
    bulletState = True # bullet fired
    bulletY = y+10 
    bulletX = x+16
    screen.blit(source=bulletImg, dest=(bulletX, bulletY))
    
# collision ------------------------------------------------------ 
collisionSound = pygame.mixer.Sound("./audio/explosion.wav")
def collisionBulletEnemy(alien) : 
    if alien.alienX <= bulletX+16 <= alien.alienX+64 and bulletY <= alien.alienY <= bulletY+32 : 
        return True 
    else : 
        return False 
        
def collisionPlayerAlien(alien) : 
    if alien.alienX <= playerX <= alien.alienX+64 and playerY <= alien.alienY+32 <= playerY+64 : 
        return True 
    else : 
        return False 


#game loop --------------------------------------------
temp = 0
running = True 
while running : 
    
    screen.fill(color=(0, 0, 0))
    # background 
    screen.blit(source=background, dest=(0, 0))
    
    for event in pygame.event.get() :
        if event.type == pygame.QUIT : # to quit
            running = False 
        if event.type == pygame.KEYDOWN : # key is pressed continue
            if event.key == pygame.K_LEFT :  # left key
                playerXSpeed = -move 
            if event.key == pygame.K_RIGHT : # right key
                playerXSpeed = move 
            if event.key == pygame.K_UP : # up key
                playerYSpeed = -move 
            if event.key == pygame.K_DOWN : # down key
                playerYSpeed = move 
            if event.key == pygame.K_SPACE : # space bar key 
                if not bulletState :  
                    bulletSound.play()
                    fireBullet(playerX, playerY)
                
        if event.type == pygame.KEYUP : # key is released 
            playerYSpeed, playerXSpeed = 0, 0 

    #player movement
    playerX += playerXSpeed 
    playerY += playerYSpeed
    
    # to create border or range of free roaming of player 
    playerX = min(max(0, playerX), x-64)
    playerY = min(max(0, playerY), y-64)
    
    # bullet Movement 
    if bulletState == True : # bullet is fired 
        if 0 < bulletY < y : 
            bulletY -= bulletSpeed 
            screen.blit(source=bulletImg, dest=(bulletX, bulletY))
        else : 
            bulletState = False
            
    
    # new alien swan after some interval
    temp += 1 
    if temp % 3000 == 0 : 
        temp = 0 
        alienSet.add(Alien())
        
    # aliens movement    
    collisionBulletAlienlist = []
    for alien in alienSet : 
        alien.alienX += alien.alienXSpeed
        if alien.alienX < 0 : 
            alien.alienY += 32 
            alien.alienXSpeed = -alien.alienXSpeed
        elif alien.alienX > x-64 : 
            alien.alienY += 32 
            alien.alienXSpeed = -alien.alienXSpeed 
        if alien.alienY > y-64 : 
            collisionSound.play() 
            running = False 
        if collisionBulletEnemy(alien) : 
            collisionBulletAlienlist.append(alien)
            collisionSound.play()
        if collisionPlayerAlien(alien) :
            collisionSound.play()
            running = False
        else : 
            alien.blit()
    
    # removing all the aliens that hit by bullet 
    for alien in collisionBulletAlienlist : 
        alienSet.remove(alien)
        bulletState = False 
        score += 1 
    del collisionBulletAlienlist
            
    player(playerX, playerY) 
    scoreWindow()
    pygame.display.update()
    
# setting gameover ------------------------------------------------
gameoverFont = pygame.font.Font('freesansbold.ttf', 64)
gameoverText = gameoverFont.render("Game Over", True, (255, 255, 255))
# game over 
collisionSound.play()
running = True 
while running : 
    screen.fill(color=(0, 0, 0)) 
    screen.blit(background, dest=(0, 0))
    for event in pygame.event.get() : 
        if event.key : 
            running = False  
    screen.blit(gameoverText, (250, 200))
    scoreWindow()
    pygame.display.update()