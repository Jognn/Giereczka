import pygame

#Screen parameters:
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Mob:
    def __init__(self, name, velocity, health, scene = None):
        self.name = name
        self.velocity = 1
        self.health = health
        self.scene = scene # Scena w jakiej sie znajduje

class Player(Mob):
    def __init__(self, name, image):
        Mob.__init__(self, name, 1, 100, 10)

        self.image = pygame.image.load(image)
        self.x = 300 # Ustalam tutaj startowe polozenie
        self.y = 200 
        self.width = 64 # Piksele
        self.height = 64 # Piksele
    
    def show(self): # TO DO: Przerzucic do klasy Mob
        Game.screen.blit(self.image, (self.x, self.y))
    
    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] : self.moveLeft()
        if keys[pygame.K_RIGHT] : self.moveRight()

    def moveLeft(self):
        if self.x > self.velocity:
            self.x -= self.velocity

    def moveRight(self):
        if self.x + self.width < Game.width:
            self.x += self.velocity

class Game: # Wszystkie zmienne gry
    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Tworzy okienko
    pygame.display.set_caption('Giereczka') # Ustawia nazwe okienka
    player = Player('Tomek', 'Resources/player.png')
        

class Scene:
    def __init__(self, name):
        self.name = name
        self.running = True

    def on_init(self):
        pygame.init()
        Game.player.scene = self # Player's scene

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_loop(self): # Wszystkie movementy i inne ify
        Game.player.movement()

    def on_render(self):
        Game.screen.fill((123, 255, 231))
        Game.player.show()
        pygame.display.update()


    def start(self):
        self.on_init()
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            
            self.on_loop()
            self.on_render()



if __name__ == "__main__":
    scena_1 = Scene('Level 1')
    scena_1.start()
