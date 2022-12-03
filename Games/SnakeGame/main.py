import pygame 
import time 
from collections import deque
from random import randint 
from pygame.locals import *

SIZE = 40

class Apple: 
    def __init__(self, parent_screen) -> None:
        self.image = pygame.image.load("./resources/apple.jpg").convert() 
        self.parent_screen = parent_screen
        
        self.x = SIZE*3 
        self.y = SIZE*3
        
    def draw(self) : 
        self.parent_screen.blit(source=self.image, dest=(self.x, self.y))  
        pygame.display.flip() 
        
    def move(self) :
        self.x = randint(0, 24)*SIZE
        self.y = randint(0, 19)*SIZE

class Snake : 
    def __init__(self, parent_screen, lenght= 10) -> None:
        
        self.parent_screen = parent_screen 
        
        # getting block image 
        self.block = pygame.image.load("./resources/block.jpg").convert()
        self.length = lenght 
        self.x = deque([SIZE]*lenght) 
        self.y = deque([SIZE]*lenght) 
        self.speed = SIZE
        self.dir = 'down'
    
    def increase_length(self) :
        self.length += 1 
        self.x.append(-1)
        self.y.append(-1)
        pass
              
    def walk(self) : 
        if self.dir == 'down' :
            self.move_down()
        elif self.dir == 'up' :
            self.move_up() 
        elif self.dir == 'left' :
            self.move_left() 
        else : 
            self.move_right()
    
    def draw(self) : 
        self.parent_screen.fill(color=(110, 110, 5)) 
        for i in range(self.length) :
            self.parent_screen.blit(source=self.block, dest=(self.x[i], self.y[i]))  
        pygame.display.flip() 
        
    def move_right(self) : 
        self.x.pop()
        self.y.pop()
        self.x.appendleft(self.x[0]+self.speed)
        self.y.appendleft(self.y[0])
        self.draw()
        
    def move_left(self) : 
        self.x.pop()
        self.y.pop()
        self.x.appendleft(self.x[0]-self.speed)
        self.y.appendleft(self.y[0]) 
        self.draw()
        
    def move_up(self) : 
        self.x.pop()
        self.y.pop()
        self.x.appendleft(self.x[0])
        self.y.appendleft(self.y[0]-self.speed) 
        self.draw()
        
    def move_down(self) : 
        self.x.pop()
        self.y.pop()
        self.x.appendleft(self.x[0])
        self.y.appendleft(self.y[0]+self.speed) 
        self.draw()
        

class Game : 
    def __init__(self) -> None:
        pygame.init()  
           
        # setting screen size
        self.surface = pygame.display.set_mode(size=(1000, 800)) 
    
        # choosing color (https://g.co/kgs/ccHb2A)
        self.surface.fill(color=(110, 110, 5))
        
        # making apple object 
        self.apple = Apple(self.surface) 
        
        # making snake object 
        self.snake = Snake(self.surface, 2)
        
        self.play() 
        
        self.run()
        
    def play(self) :
        self.snake.walk() 
        self.apple.draw()
        self.display_score()
        pygame.display.flip()
        
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y) : 
            self.apple.move() 
            self.snake.increase_length()
            
        for i in range(1, self.snake.length) :
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]) :
                pass
        
    def is_collision(self, x1, y1, x2, y2) : 
        if x2 <= x1 < x2 + SIZE and y2 <= y1 < y2 + SIZE : 
            return True 
        else : 
            return False 
    
    def display_score(self) : 
       font = pygame.font.SysFont('arial', 30) 
       score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255)) 
       self.surface.blit(score, (800, 10))  
    
    def run(self) : 
        running = True 
        while running : 
            for event in pygame.event.get():
                if event.type == QUIT : 
                    running = False 
                elif event.type == KEYDOWN : 

                    if event.key == K_ESCAPE :
                        running = False 

                    if event.key == K_UP : 
                        self.snake.dir = 'up'

                    if event.key == K_DOWN : 
                        self.snake.dir = 'down'

                    if event.key == K_LEFT : 
                        self.snake.dir = 'left'

                    if event.key == K_RIGHT : 
                        self.snake.dir = 'right'
            self.play()
            time.sleep(0.3)

if __name__ == "__main__" : 
    Game() 
    
                
                    
                
                 