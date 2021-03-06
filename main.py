import pygame

#Screen parameters:
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Frame parameters
FRAME_RATE = 60
FRAMES_PER_IMAGE = 10

#Meter
PIXELS_PER_METER = 8

#Info parameters
SHOW_INFO = True
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

#Player parameters
JUMP_HEIGHT = 0.25


class Mob:
    def __init__(self, **kwargs):  # name = None, starting_position = (0,FLOOR), velocity = 3, health = 100, scene = None
        self.images_stoi_prawo = kwargs.get('images_stoi_prawo', ['Resources/Mobs/default.png'])
        self.images_stoi_lewo = kwargs.get('images_stoi_lewo', ['Resources/Mobs/default.png'])
        self.images_idzie_prawo = kwargs.get('images_idzie_prawo', ['Resources/Mobs/default.png'])
        self.images_idzie_lewo = kwargs.get('images_idzie_lewo', ['Resources/Mobs/default.png'])
        self.images_skacze_prawo = kwargs.get('images_skacze_prawo', ['Resources/Mobs/default.png'])
        self.images_skacze_lewo = kwargs.get('images_skacze_lewo', ['Resources/Mobs/default.png'])
        self.current_image = pygame.image.load(self.images_stoi_prawo[0]).convert_alpha()

        self.name = kwargs.get('name', None)
        self.scene = kwargs.get('scene', None)  # Scena w jakiej sie znajduje
        self.width = self.current_image.get_width()
        self.height = self.current_image.get_height()
        self.starting_x = kwargs.get('starting_position', 0)[0] - self.width
        self.x = self.starting_x
        self.starting_y = kwargs.get('starting_position', FLOOR)[1] - self.height
        self.y = self.starting_y
        self.hitbox = pygame.Rect(int(self.x), int(self.y), self.width, self.height)

        self.velocity = kwargs.get('velocity', 3)
        self.health = kwargs.get('health', 100)

        self.moving_left = False
        self.moving_right = False
        self.turned_right = True
        self.turned_left = False
        self.jumping = False
        self.jumpCount = 10

    def show(self):
        Game.screen.blit(self.current_image, (self.x, self.y))
        pygame.draw.rect(Game.screen, (240, 0, 0), self.hitbox, 2)

    def change_hitbox(self):
        self.hitbox = pygame.Rect(int(self.x), int(self.y), self.width, self.height)


class Player(Mob):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def movement(self):
        keys = pygame.key.get_pressed()
        self.moving_left = False
        self.moving_right = False
        Camera.update()

        if keys[pygame.K_LEFT]: self.move_left()
        if keys[pygame.K_RIGHT]: self.move_right()
        self.change_hitbox()

    def move_left(self):
        self.turned_right = False
        self.turned_left = True
        self.moving_left = True
        if Camera.backgrounds[0][1][0] in range(-2, 2) or self.hitbox.centerx > self.starting_x + self.width + self.velocity:
            #Warunek nie wyjsca poza mape
            if self.x - self.velocity > 0:
                self.x -= self.velocity
        else:
            Camera.move_backgrounds_left()

    def move_right(self):
        self.turned_left = False
        self.moving_right = True
        self.turned_right = True
        if Camera.backgrounds[1][1][0] in range(-2, 2) or self.hitbox.centerx < self.starting_x + self.width:
            # Warunek nie wyjsca poza mape
            if self.hitbox.right + self.velocity < Game.width:
                self.x += self.velocity
        else:
            Camera.move_backgrounds_right()

    def show(self):
        if self.moving_left:
            self.current_image = self.images_idzie_lewo[(Game.frame//FRAMES_PER_IMAGE) % 4]
        elif self.moving_right:
            self.current_image = self.images_idzie_prawo[(Game.frame//FRAMES_PER_IMAGE) % 4]
        else:
            if self.turned_left:
                self.current_image = self.images_stoi_lewo[(Game.frame//(FRAMES_PER_IMAGE*2)) % 4] # FRAMES_PER_IMAGE*2 - experimenting
            elif self.turned_right:
                self.current_image = self.images_stoi_prawo[(Game.frame//(FRAMES_PER_IMAGE*2)) % 4] # FRAMES_PER_IMAGE*2 - experimenting

        if self.jumping and self.turned_left:
            self.current_image = self.images_skacze_lewo[(Game.frame//FRAMES_PER_IMAGE) % 1]
        elif self.jumping and self.turned_right:
            self.current_image= self.images_skacze_prawo[(Game.frame//FRAMES_PER_IMAGE) % 1]


        self.current_image = pygame.image.load(self.current_image).convert_alpha()
        Game.screen.blit(self.current_image, (int(self.x), int(self.y)))
        pygame.draw.rect(Game.screen, (240, 0, 0), self.hitbox, 2)

    def jump(self):
        if self.jumping:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= (self.jumpCount ** 2) * JUMP_HEIGHT * neg
                self.jumpCount -= 1
            else:
                self.jumping = False
                self.jumpCount = 10


class Ziemniak(Mob):
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
            self.moving_right = False
            self.moving_left = True
            self.turned_left = True
            self.turned_right = False
            if self.hitbox.left - self.velocity <= pozycja_gracza_p:
                self.moving_left = False
            else:
                self.x -= self.velocity
        #Ruch w prawo
        elif self.hitbox.right < pozycja_gracza_l:
            self.moving_left = False
            self.turned_right = True
            self.moving_right = True
            self.turned_left = False
            if self.hitbox.right + self.velocity >= pozycja_gracza_l:
                self.moving_right = False
            else:
                self.x += self.velocity
        #Ruch wzgledny
        if Camera.moving_left:
            self.x += Camera.focus.velocity
        if Camera.moving_right:
            self.x -= Camera.focus.velocity
        self.change_hitbox() # Zmienia pozycje hitboxa

    def show(self):
        if self.moving_left:
            self.current_image = self.images_idzie_lewo[(Game.frame // FRAMES_PER_IMAGE) % 3]
        elif self.moving_right:
            self.current_image = self.images_idzie_prawo[(Game.frame // FRAMES_PER_IMAGE) % 3]
        else:
            if self.turned_left:
                self.current_image = self.images_stoi_lewo[
                    (Game.frame // (FRAMES_PER_IMAGE * 2)) % 4]  # FRAMES_PER_IMAGE*2 - experimenting
            elif self.turned_right:
                self.current_image = self.images_stoi_prawo[
                    (Game.frame // (FRAMES_PER_IMAGE * 2)) % 4]  # FRAMES_PER_IMAGE*2 - experimenting

        self.current_image = pygame.image.load(self.current_image).convert_alpha()
        Game.screen.blit(self.current_image, (self.x, self.y))
        pygame.draw.rect(Game.screen, (240, 0, 0), self.hitbox, 2)

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
                    images_idzie_prawo = ['Resources/Mobs/Player/player_idzie_prawo1.png', 'Resources/Mobs/Player/player_idzie_prawo2.png', 'Resources/Mobs/Player/player_idzie_prawo3.png', 'Resources/Mobs/Player/player_idzie_prawo2.png'],
                    images_idzie_lewo = ['Resources/Mobs/Player/player_idzie_lewo1.png', 'Resources/Mobs/Player/player_idzie_lewo2.png', 'Resources/Mobs/Player/player_idzie_lewo3.png', 'Resources/Mobs/Player/player_idzie_lewo2.png'],
                    images_skacze_prawo = ['Resources/Mobs/Player/player_skacze_prawo1.png'],
                    images_skacze_lewo = ['Resources/Mobs/Player/player_skacze_lewo1.png'],
                    name='Tomek', velocity=4, starting_position=(SCREEN_WIDTH/2, FLOOR))

    ziemniak = Ziemniak(images_stoi_prawo=['Resources/Mobs/Enemy1/ziemniak_stoi_prawo1.png', 'Resources/Mobs/Enemy1/ziemniak_stoi_prawo2.png', 'Resources/Mobs/Enemy1/ziemniak_stoi_prawo3.png', 'Resources/Mobs/Enemy1/ziemniak_stoi_prawo2.png'],
                    images_stoi_lewo=['Resources/Mobs/Enemy1/ziemniak_stoi_lewo1.png', 'Resources/Mobs/Enemy1/ziemniak_stoi_lewo2.png', 'Resources/Mobs/Enemy1/ziemniak_stoi_lewo3.png', 'Resources/Mobs/Enemy1/ziemniak_stoi_lewo2.png'],
                    images_idzie_prawo=['Resources/Mobs/Enemy1/ziemniak_idzie_prawo1.png', 'Resources/Mobs/Enemy1/ziemniak_idzie_prawo2.png', 'Resources/Mobs/Enemy1/ziemniak_idzie_prawo3.png'],
                    images_idzie_lewo=['Resources/Mobs/Enemy1/ziemniak_idzie_lewo1.png', 'Resources/Mobs/Enemy1/ziemniak_idzie_lewo2.png', 'Resources/Mobs/Enemy1/ziemniak_idzie_lewo3.png'],
                    name='Ziemniak', velocity=3, starting_position=(300, FLOOR))

class Tile:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image).convert_alpha()
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()


class WorldGenerator:
    def __init__(self, level_tilemap):
        with open(level_tilemap, 'r') as file:
            self.tilemap = list()
            lines = file.readlines()
            for y in range(len(lines)):
                for x in range(len(lines[y])):
                    position = lines[y][x]
                    if position == ".":
                        continue
                    elif position == "@":
                        self.tilemap.append(Tile('Resources/block.jpg', 32 * x, 32 * y))
                    elif position == "&":
                        self.tilemap.append(Tile('Resources/trawa.png', 32 * x, 32 * y))

    def show_blocks(self):
        self.current_tiles = list()
        for tile in self.tilemap:
            if Camera.x - 32 <= tile.x <= Camera.right and Camera.y <= tile.y <= Camera.down:
                self.current_tiles.append(tile)
                Game.screen.blit(tile.image, (tile.x - Camera.x, tile.y))


class Camera:
    focus = Game.player # Obecny target kamery
    moving_left = False
    moving_right = False
    x = 0
    y = 0
    width = Game.screen.get_width()
    height = Game.screen.get_height()
    right = x + width
    down = y + height

    backgrounds = [[pygame.image.load('Resources/b.jpg').convert(), (2560*i, 0)] for i in range (2)]# [*Surface*, (x,y)]

    @classmethod
    def move_backgrounds_left(cls):
        cls.x -= cls.focus.velocity
        cls.right -= cls.focus.velocity
        cls.moving_left = True
        cls.backgrounds= [[background[0], (background[1][0] + cls.focus.velocity, background[1][1])] for background in cls.backgrounds]

    @classmethod
    def move_backgrounds_right(cls):
        cls.x += cls.focus.velocity
        cls.right += cls.focus.velocity
        cls.moving_right = True
        cls.backgrounds= [[background[0], (background[1][0] - cls.focus.velocity, background[1][1])] for background in cls.backgrounds]

    @classmethod
    def update(cls):
        cls.moving_left = False
        cls.moving_right = False


class Info:
    show_fps = SHOW_FPS
    show_debug = SHOW_DEBUG

    font_fps = pygame.font.Font(None, FPS_FONT_SIZE)
    font_debug = pygame.font.Font(None, DEBUG_FONT_SIZE)

    fonts = [0, 0, FPS_FONT_SIZE, DEBUG_FONT_SIZE, DEBUG_FONT_SIZE]
    text_offset_y = []

    for i in range(1, len(fonts)):
        text_offset_y.append(fonts[i] + fonts[i-1])

    @classmethod
    def fps(cls):
        fps_content = str(int(Game.clock.get_fps()) + 1) + f" fps   frame: {Game.frame+1}"
        fps = cls.font_fps.render(fps_content, True, (0, 240, 0), None).convert_alpha()
        Game.screen.blit(fps, (0, cls.text_offset_y[0]))

    @classmethod
    def debug(cls):
        debug_1 = f"Background_positions: {list(background[1] for background in Camera.backgrounds)}    " +\
                  f"Ziemniak.turned_left: {level1.mobs[1].turned_left}    Ziemniak.turned_right: {level1.mobs[1].turned_right}    Showed tiles: {len(level1.map.current_tiles)}"
        debug_2 = f"Zomniak.moving_left: {level1.mobs[1].moving_left}    Ziemniak.moving_right: {level1.mobs[1].moving_right}"



        backgrounds = cls.font_debug.render(debug_1, True, (0, 0, 0), None).convert_alpha()
        moving = cls.font_debug.render(debug_2, True, (0, 0, 0), None).convert_alpha()

        Game.screen.blit(backgrounds, (0, cls.text_offset_y[1]))
        Game.screen.blit(moving, (0, cls.text_offset_y[2]))

    @classmethod
    def show_info(cls):
        if SHOW_INFO:
            if cls.show_fps:
                cls.fps()
            if cls.show_debug:
                cls.debug()

    @staticmethod
    def show_height(target):
        n = PIXELS_PER_METER
        for i in range(int(target.height / n)):
            pygame.draw.rect(Game.screen, (0, 0, 0), (target.x - n - 2, target.y + n * i, n, n), 1)


class Level1:
    def __init__(self):
        self.running = True
        self.mobs = [Game.player, Game.ziemniak]

        Game.player.scene = self  # Setting player's scene
        self.floor = pygame.Rect((0, LEVEL1_HEIGHT-FLOOR), (LEVEL1_WIDTH, LEVEL1_HEIGHT-FLOOR))
        self.map = WorldGenerator('Resources/tilemap.txt')

    def on_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # ESC - wyjsc z gry
            self.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                Game.player.jumping = True

    def on_loop(self):  # Wszystkie movementy i inne ify
        for mob in self.mobs:
            mob.movement()

        Game.player.jump()

    def on_render(self): # Wszelkie renderowanie obrazow
        for background in Camera.backgrounds:
            Game.screen.blit(background[0], background[1])

        self.map.show_blocks()

        for mob in self.mobs:
            mob.show()
            #Info.show_height(mob)

        Info.show_info()
        Game.clock.tick(FRAME_RATE)# Ograniczna klatki

        pygame.display.update()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()
            Game.frame = (Game.frame+1) % FRAME_RATE


if __name__ == "__main__":
    level1 = Level1()
    level1.start()