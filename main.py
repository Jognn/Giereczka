import pygame

# Screen parameters:
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Level 1 parameters:
LEVEL1_WIDTH = 1280*2
LEVEL1_HEIGHT = 720

#Floor:
FLOOR_Y = 500


class Mob:
    def __init__(self, **kwargs):  # name = None, starting_position = (0,0), velocity = 1, health = 100, surface = None,  scene = None
        self.images = kwargs.get('images', ['Resources/Mobs/default.png'])
        self.current_image = pygame.image.load(self.images[0]).convert_alpha() # .convert_alpha() - any good?
        self.width = kwargs.get('width', 64)
        self.height = kwargs.get('height', 64)
        self.name = kwargs.get('name', None)
        self.scene = kwargs.get('scene', None)  # Scena w jakiej sie znajduje
        self.surface = kwargs.get('surface', None)

        self.x = kwargs.get('starting_position', 0)[0]
        self.y = kwargs.get('starting_position', FLOOR_Y)[1]
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.velocity = kwargs.get('velocity', 1)
        self.health = kwargs.get('health', 100)

        self.moving_left = False
        self.moving_right = False

    def show(self):
        Game.screen.blit(self.current_image, (self.x, self.y))
        pygame.draw.rect(Game.screen, (240, 0, 0), self.hitbox, 2)

    def change_hitbox(self):
        self.hitbox = self.hitbox = (self.x, self.y, self.width, self.height)

class Player(Mob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: self.move_left()
        if keys[pygame.K_RIGHT]: self.move_right()
        self.change_hitbox()

    def move_left(self):
        self.moving_left = True
        if self.x > self.velocity:
            self.x -= self.velocity
            self.moving_left = False

    def move_right(self):
        self.moving_right = True
        if self.x + self.width < Game.width:
            self.x += self.velocity
            self.moving_right = False

class Goblin(Mob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def movement(self):
        pozycja_gracza_l = Game.player.x + Game.player.width
        pozycja_gracza_p = Game.player.x - Game.player.width

        #Ruch w lewo
        if self.x > pozycja_gracza_l:
            self.moving_left = True
            if self.x - self.velocity <= pozycja_gracza_l:
                self.moving_left = False
            else:
                if not self.current_image == self.images[0]: self.current_image = pygame.image.load(self.images[0]).convert_alpha()
                self.x -= self.velocity
        #Ruch w prawo
        elif self.x < pozycja_gracza_p:
            self.moving_right = True
            if self.x + self.velocity >= pozycja_gracza_p:
                self.moving_right = False
            else:
                if not self.current_image == self.images[1]: self.current_image = pygame.image.load(self.images[1]).convert_alpha()
                self.x += self.velocity
        self.change_hitbox() # Zmienia pozycje hitboxa

class Game:  # Wszystkie zmienne gry
    pygame.init()
    pygame.display.set_caption('Giereczka')  # Ustawia nazwe okienka
    clock = pygame.time.Clock()

    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tworzy okienko
    player = Player(images=['Resources/Mobs/player.png'], name='Tomek', velocity=5, starting_position=(0, FLOOR_Y))


class Level1:
    def __init__(self):
        Game.clock.tick(60) # Ilosc klatek
        self.running = True
        self.background = pygame.image.load('Resources/background.jpg').convert() # .convert() - bardzo wazna rzecz!
        self.mobs = [Game.player,
            Goblin(images=['Resources/Mobs/goblin_lewo.png', 'Resources/Mobs/goblin_prawo.png'], name='Goblin1', starting_position=(200, FLOOR_Y), scene=self),
            Goblin(images=['Resources/Mobs/goblin_lewo.png', 'Resources/Mobs/goblin_prawo.png'], name='Goblin2', starting_position=(600, FLOOR_Y), scene=self),
            Goblin(images=['Resources/Mobs/goblin_lewo.png', 'Resources/Mobs/goblin_prawo.png'], name='Goblin3', starting_position=(800, FLOOR_Y), scene=self),
            Goblin(images=['Resources/Mobs/goblin_lewo.png', 'Resources/Mobs/goblin_prawo.png'], name='Goblin4', starting_position=(1000, FLOOR_Y), scene=self)]

        Game.player.scene = self  # Setting player's scene
        self.floor = pygame.Rect((0, LEVEL1_HEIGHT-500), (LEVEL1_WIDTH, FLOOR_Y))

    def on_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # ESC - wyjsc z gry
            self.running = False

    def on_loop(self):  # Wszystkie movementy i inne ify
        for mob in self.mobs:
            mob.movement()

    def on_render(self): # Wszelkie renderowanie obrazow
        Game.screen.blit(self.background, (0, 0))
        for mob in self.mobs:
            mob.show()

        pygame.display.update()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()


if __name__ == "__main__":
    leve1 = Level1()
    leve1.start()
