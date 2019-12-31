import pygame

#Screen parameters:
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Mob:
    def __init__(self, image, **kwargs): #, name = None, starting_position = (0,0), velocity = 1, health = 100, scene = None
        self.image = pygame.image.load(image)
        self.name = kwargs.get('name', "Jerry")
        self.x = kwargs.get('starting_position', (0,0))[0]
        self.y = kwargs.get('starting_position', (0,0))[1]
        self.velocity = kwargs.get('velocity', 1) | 1
        self.health = kwargs.get('health', 100)
        self.scene = kwargs.get('scene') # Scena w jakiej sie znajduje

    def show(self):
        Game.screen.blit(self.image, (self.x, self.y))

class Player(Mob):
    def __init__(self, image, name):
        super().__init__(image, name = name, starting_position = (400, 300))

        self.width = 64 # Piksele
        self.height = 64 # Piksele
    
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
    pygame.init()
    pygame.display.set_caption('Giereczka') # Ustawia nazwe okienka

    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Tworzy okienko
    player = Player('Resources/player.png', 'Tomek')
        

class Scene:
    def __init__(self, name):
        self.name = name
        self.running = True
        self.mobs = []

    def on_init(self):
        Game.player.scene = self # Player's scene
        self.mobs.append(Mob('Resources/goblin.png', name = 'Goblin1', starting_position = (200, 300), scene = self))
        self.mobs.append(Mob('Resources/goblin.png', name = 'Goblin2', starting_position = (600, 300), scene = self))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_loop(self): # Wszystkie movementy i inne ify
        Game.player.movement()

    def on_render(self):
        Game.screen.fill((123, 255, 231))
        Game.player.show()
        for mob in self.mobs: # Pokazuje wszystkie moby
            mob.show()

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
