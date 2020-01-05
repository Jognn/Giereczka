import pygame

# Screen parameters:
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Level 1 parameters:
LEVEL1_WIDTH = 1280*2
LEVEL1_HEIGHT = 720

#Floor:
FLOOR_Y = 500

BG1_STARTING_X = 0
BG1_STARTING_Y = 0

BG2_STARTING_X = 2560
BG2_STARTING_Y = 0


class Mob:
    def __init__(self, **kwargs):  # name = None, starting_position = (0,0), velocity = 1, health = 100, surface = None,  scene = None
        self.images = kwargs.get('images', ['Resources/Mobs/default.png'])
        self.current_image = pygame.image.load(self.images[0]).convert_alpha() # .convert_alpha() - any good?
        self.width = kwargs.get('width', 64)
        self.height = kwargs.get('height', 64)
        self.name = kwargs.get('name', None)
        self.scene = kwargs.get('scene', None)  # Scena w jakiej sie znajduje
        self.surface = kwargs.get('surface', None)
        self.frame = 0

        self.x = kwargs.get('starting_position', 0)[0]
        self.y = kwargs.get('starting_position', FLOOR_Y)[1]
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.velocity = kwargs.get('velocity', 3)
        self.health = kwargs.get('health', 100)

        self.moving_left = False
        self.moving_right = False

    def show(self):
        Game.screen.blit(self.current_image, (self.x, self.y))
        pygame.draw.rect(Game.screen, (240, 0, 0), self.hitbox, 2)

    def change_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

class Player(Mob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movement(self):
        keys = pygame.key.get_pressed()
        self.moving_left = False
        self.moving_right = False

        if keys[pygame.K_LEFT]: self.move_left()
        if keys[pygame.K_RIGHT]: self.move_right()
        self.change_hitbox()

    def move_left(self):
        if self.scene.background1_position[0] == 0 or (self.scene.background2_position[0] == 0 and self.x > Game.width/2):
            if self.x > self.velocity:
                self.x -= self.velocity
        else:
            self.moving_left = True
            self.scene.background1_position[0] += self.velocity
            self.scene.background2_position[0] += self.velocity

    def move_right(self):
        if self.scene.background2_position[0] == 0 or self.x < Game.width/2:
            if self.x + self.velocity < 1220: #1220 - blad ze zdjeciem! (zostawic na razie), powinno byc zwiazane z Game.width
                self.x += self.velocity
        else:
            self.moving_right = True
            self.scene.background1_position[0] -= self.velocity
            self.scene.background2_position[0] -= self.velocity

    def show(self):
        if Game.frame < 10:
            self.current_image = pygame.image.load(self.images[0]).convert_alpha()
        elif Game.frame  < 20:
            self.current_image = pygame.image.load(self.images[1]).convert_alpha()
        elif Game.frame  < 30:
            self.current_image = pygame.image.load(self.images[2]).convert_alpha()

        Game.screen.blit(self.current_image, (self.x, self.y))
        pygame.draw.rect(Game.screen, (240, 0, 0), self.hitbox, 2)


class Goblin(Mob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movement(self):
        pozycja_gracza_l = Game.player.hitbox.left
        pozycja_gracza_p = Game.player.hitbox.right

        #Ruch w lewo
        if self.hitbox.left > pozycja_gracza_p:
            self.moving_left = True
            if self.hitbox.left - self.velocity <= pozycja_gracza_l:
                self.moving_left = False
            else:
                if not self.current_image == self.images[0]: self.current_image = pygame.image.load(self.images[0]).convert_alpha()
                self.x -= self.velocity
        #Ruch w prawo
        elif self.hitbox.right < pozycja_gracza_l:
            self.moving_right = True
            if self.hitbox.right + self.velocity >= pozycja_gracza_l:
                self.moving_right = False
            else:
                if not self.current_image == self.images[1]: self.current_image = pygame.image.load(self.images[1]).convert_alpha()
                self.x += self.velocity
        #Ruch wzgledny
        if Game.player.moving_left:
            self.x += Game.player.velocity
        if Game.player.moving_right:
            self.x -= Game.player.velocity
        self.change_hitbox() # Zmienia pozycje hitboxa


class Game:  # Wszystkie zmienne gry
    pygame.init()
    pygame.display.set_caption('Giereczka')  # Ustawia nazwe okienka
    clock = pygame.time.Clock()
    font_fps = pygame.font.Font(None, 22)
    font_debug = pygame.font.Font(None, 24)
    frame = 0

    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    level1_width = LEVEL1_WIDTH
    level1_height = LEVEL1_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tworzy okienko
    player = Player(images=['Resources/Mobs/player1.png', 'Resources/Mobs/player2.png', 'Resources/Mobs/player3.png'],
                    name='Tomek', velocity=10, starting_position=(SCREEN_WIDTH/2, FLOOR_Y))


class Level1:
    def __init__(self):
        self.running = True
        self.background1 = pygame.image.load('Resources/b.jpg').convert() # .convert() - bardzo wazna rzecz!
        self.background1_position = [0,0]
        self.background2 = pygame.image.load('Resources/b.jpg').convert()  # .convert() - bardzo wazna rzecz!
        self.background2_position = [self.background1.get_width(), self.background1_position[1]]
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
        Game.screen.blit(self.background1, (self.background1_position[0], self.background1_position[1]))
        Game.screen.blit(self.background2, (self.background2_position[0], self.background2_position[1]))
        for mob in self.mobs:
            mob.show()

        fps = Game.font_fps.render(str(int(Game.clock.get_fps())) + " fps", True, (0,240,0), None).convert_alpha()
        backgrounds = Game.font_debug.render(f"Player: {(Game.player.x, Game.player.y)}  Background1: {tuple(self.background1_position)}  Background2: {tuple(self.background2_position)}   Frame", True, (0, 0, 0), None).convert_alpha()
        moving = Game.font_debug.render(f"Moving Left: {Game.player.moving_left}  Moving Right: {Game.player.moving_right}", True, (0, 0, 0), None).convert_alpha()
        Game.screen.blit(fps, (0, 0))
        Game.screen.blit(backgrounds, (0, fps.get_height() + 2))
        Game.screen.blit(moving, (0 , backgrounds.get_height()*2 + 2))
        Game.clock.tick(30) # Ograniczna klatki

        pygame.display.update()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
            Game.frame = (Game.frame+1) % 30


if __name__ == "__main__":
    leve1 = Level1()
    leve1.start()