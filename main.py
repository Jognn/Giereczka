import pygame

class Mob:
    def __init__(self, name, health, damage): # TO DO
        self.name = name
        self.health = health
        self.damage = damage

class Player(Mob):
    def __init__(self, name, image):
        Mob.__init__(self, name, 100, 10)

        self.image = pygame.image.load(image)
        self.x = 300
        self.y = 200
        self.speed = 0.5
    
    def show(self):
        self.scene.screen.blit(self.image, (self.x, self.y))

    def changeX(self, value):
        self.x += self.speed * value

    def changeY(self, value):
        self.y += self.speed * value

class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.running = True
        self.screen = pygame.display.set_mode((self.width, self.height)) # Tworzy okienko
        pygame.display.set_caption('Giereczka') # Ustawia nazwe okienka

    player = Player('Tomek', 'Resources/player.png') # Tworzenie gracza
        

class Scene(Game):
    def __init__(self, name, width, height):
        super().__init__(width, height)
        self.name = name

    def on_init(self):
        pygame.init()
        Game.player.scene = self

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def on_render(self):
        self.screen.fill((123, 255, 231))
        self.player.show()
        pygame.display.update()

    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] : Game.player.changeX(-1)
        if keys[pygame.K_RIGHT] : Game.player.changeX(1)
        if keys[pygame.K_UP] : Game.player.changeY(-1)
        if keys[pygame.K_DOWN] : Game.player.changeY(1)

    def start(self):
        self.on_init()
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            
            self.movement()
            self.on_render()



if __name__ == "__main__":
    scena_1 = Scene('Level 1', 800, 600)
    scena_1.start()
