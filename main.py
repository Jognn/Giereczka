import pygame

#Screen parameters:
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Frame parameters
FRAME_RATE = 30
FRAMES_PER_IMAGE = 3

#Info parameters
SHOW_FPS = True
FPS_FONT_SIZE = 22
SHOW_DEBUG = True
DEBUG_FONT_SIZE = 24

#Level 1 parameters:
LEVEL1_WIDTH = 1280*2
LEVEL1_HEIGHT = 720

#Floor:
FLOOR = 575

#Moving backgrounds parameters
BG1_STARTING_X = 0
BG1_STARTING_Y = 0
BG2_STARTING_X = 2560
BG2_STARTING_Y = 0


class Mob:
    def __init__(self, **kwargs):  # name = None, starting_position = (0,FLOOR), velocity = 1, health = 100, scene = None
        self.images_stoi_prawo = kwargs.get('images_stoi_prawo', ['Resources/Mobs/default.png'])
        self.images_stoi_lewo = kwargs.get('images_stoi_lewo', ['Resources/Mobs/default.png'])
        self.images_idzie_prawo = kwargs.get('images_idzie_prawo', ['Resources/Mobs/default.png'])
        self.images_idzie_lewo = kwargs.get('images_idzie_lewo', ['Resources/Mobs/default.png'])
        self.current_image = pygame.image.load(self.images_stoi_prawo[0]).convert_alpha()

        self.name = kwargs.get('name', None)
        self.scene = kwargs.get('scene', None)  # Scena w jakiej sie znajduje
        self.width = self.current_image.get_width()
        self.height = self.current_image.get_height()
        self.x = kwargs.get('starting_position', 0)[0]
        y = kwargs.get('starting_position', FLOOR)[1]
        self.y = y - self.height
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.velocity = kwargs.get('velocity', 3)
        self.health = kwargs.get('health', 100)

        self.moving_left = False
        self.moving_right = False
        self.turned_right = True
        self.turned_left = False
        self.moving_background_left = False
        self.moving_background_right = True

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
        self.moving_background_left = False
        self.moving_background_right = False

        if keys[pygame.K_LEFT]: self.move_left()
        if keys[pygame.K_RIGHT]: self.move_right()
        self.change_hitbox()

    def move_left(self):
        self.turned_right = False
        self.turned_left = True
        self.moving_left = True
        if self.scene.background1_position[0] == 0 or (self.scene.background2_position[0] == 0 and self.x > Game.width/2):
            if self.x > self.velocity:
                self.x -= self.velocity
        else:
            self.moving_background_left = True
            self.scene.background1_position[0] += self.velocity
            self.scene.background2_position[0] += self.velocity

    def move_right(self):
        self.turned_left = False
        self.moving_right = True
        self.turned_right = True
        if self.scene.background2_position[0] == 0 or self.x < Game.width/2:
            if self.x + self.velocity < 1220: #1220 - blad ze zdjeciem! (zostawic na razie), powinno byc zwiazane z Game.width
                self.x += self.velocity
        else:
            self.moving_background_right = True
            self.scene.background1_position[0] -= self.velocity
            self.scene.background2_position[0] -= self.velocity

    def show(self):
        if self.moving_left:
            self.current_image = self.images_idzie_lewo[(Game.frame//FRAMES_PER_IMAGE) % 3]
        elif self.moving_right:
            self.current_image = self.images_idzie_prawo[(Game.frame//FRAMES_PER_IMAGE) % 3]
        else:
            if self.turned_left:
                self.current_image = self.images_stoi_lewo[(Game.frame//(FRAMES_PER_IMAGE*2)) % 4] # FRAMES_PER_IMAGE*2 - experimenting       3 czy 4 klatki?
            elif self.turned_right:
                self.current_image = self.images_stoi_prawo[(Game.frame//(FRAMES_PER_IMAGE*2)) % 4] # FRAMES_PER_IMAGE*2 - experimenting       3 czy 4 klatki?

        self.current_image = pygame.image.load(self.current_image)
        Game.screen.blit(self.current_image, (self.x, self.y))
        pygame.draw.rect(Game.screen, (240, 0, 0), self.hitbox, 2)


class Goblin(Mob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.images = kwargs.get('images')
        self.hitbox.width = 192
        self.hitbox.height = 192

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
        if Game.player.moving_background_left:
            self.x += Game.player.velocity
        if Game.player.moving_background_right:
            self.x -= Game.player.velocity
        self.change_hitbox() # Zmienia pozycje hitboxa


class Game:  # Wszystkie zmienne gry
    pygame.init()
    pygame.display.set_caption('Giereczka')  # Ustawia nazwe okienka
    clock = pygame.time.Clock()
    frame = 0

    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    level1_width = LEVEL1_WIDTH
    level1_height = LEVEL1_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tworzy okienko

    player = Player(images_stoi_prawo=['Resources/Mobs/Player/player_stoi_prawo1.png', 'Resources/Mobs/Player/player_stoi_prawo2.png', 'Resources/Mobs/Player/player_stoi_prawo3.png', 'Resources/Mobs/Player/player_stoi_prawo2.png'],
                    images_stoi_lewo= ['Resources/Mobs/Player/player_stoi_lewo1.png', 'Resources/Mobs/Player/player_stoi_lewo2.png', 'Resources/Mobs/Player/player_stoi_lewo3.png', 'Resources/Mobs/Player/player_stoi_lewo2.png'],
                    images_idzie_prawo = ['Resources/Mobs/Player/player_idzie_prawo1.png', 'Resources/Mobs/Player/player_idzie_prawo2.png', 'Resources/Mobs/Player/player_idzie_prawo3.png'],
                    images_idzie_lewo = ['Resources/Mobs/Player/player_idzie_lewo1.png', 'Resources/Mobs/Player/player_idzie_lewo2.png', 'Resources/Mobs/Player/player_idzie_lewo3.png'],
                    name='Tomek', velocity=10, starting_position=(SCREEN_WIDTH/2, FLOOR))

class Info:
    show_fps = SHOW_FPS
    show_debug = SHOW_DEBUG

    font_fps = pygame.font.Font(None, FPS_FONT_SIZE)
    font_debug = pygame.font.Font(None, DEBUG_FONT_SIZE)

    #heights = [0, font_fps.get_height()+2, font_debug.get_height()*2+2]
    h = [0, 0, FPS_FONT_SIZE, DEBUG_FONT_SIZE, DEBUG_FONT_SIZE]
    heights = []

    @classmethod
    def fps(cls):
        fps_content = str(int(Game.clock.get_fps()) + 1) + f" fps   frame: {Game.frame+1}"

        fps = cls.font_fps.render(fps_content, True, (0, 240, 0), None).convert_alpha()
        Game.screen.blit(fps, (0, cls.heights[0]))

    @classmethod
    def debug(cls):
        backgrounds_content = f"Turned_left: {Game.player.turned_left}    Turned_right: {Game.player.turned_right}    " +\
                              f"Moving_left: {Game.player.moving_left}    Moving_right: {Game.player.moving_right}"

        moving_content = f"Moving bg left: {Game.player.moving_background_left}    Moving bg right: {Game.player.moving_right}"

        backgrounds = cls.font_debug.render(backgrounds_content, True, (0, 0, 0), None).convert_alpha()
        moving = cls.font_debug.render(moving_content, True, (0, 0, 0), None).convert_alpha()

        Game.screen.blit(backgrounds, (0, cls.heights[1]))
        Game.screen.blit(moving, (0, cls.heights[2]))

    @classmethod
    def show(cls):
        cls.heights = []
        for i in range(1, len(cls.h)): # Trzeba upiekszyc
            cls.heights.append(cls.h[i-1] + cls.h[i])
        if cls.show_fps:
            cls.fps()
        if cls.show_debug:
            cls.debug()

class Level1:
    def __init__(self):
        self.running = True
        self.background1 = pygame.image.load('Resources/b.jpg').convert() # .convert() - bardzo wazna rzecz!
        self.background1_position = [0,0]
        self.background2 = pygame.image.load('Resources/b.jpg').convert()  # .convert() - bardzo wazna rzecz!
        self.background2_position = [self.background1.get_width(), self.background1_position[1]]
        self.mobs = [Game.player,
                     Goblin(images=['Resources/Mobs/boss1.png', 'Resources/Mobs/boss2.png'], images_stoi_prawo=['Resources/Mobs/boss1.png'],
                            name='Boss', starting_position=(200, FLOOR), scene=self)]

        Game.player.scene = self  # Setting player's scene
        self.floor = pygame.Rect((0, LEVEL1_HEIGHT-500), (LEVEL1_WIDTH, FLOOR))

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

        Info.show()
        Game.clock.tick(FRAME_RATE) # Ograniczna klatki

        pygame.display.update()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
            Game.frame = (Game.frame+1) % FRAME_RATE


if __name__ == "__main__":
    leve1 = Level1()
    leve1.start()