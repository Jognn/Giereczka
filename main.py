import pygame

# Screen parameters:
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#Level 1 parameters:
LEVEL1_WIDTH = 2000
LEVEL1_HEIGHT = 800


class Mob:
    def __init__(self, image, **kwargs):  # name = None, starting_position = (0,0), velocity = 1, health = 100, surface = None,  scene = None
        self.image = pygame.image.load(image)
        self.name = kwargs.get('name', None)
        self.x = kwargs.get('starting_position', 0)[0]
        self.y = kwargs.get('starting_position', 500)[1]
        self.velocity = kwargs.get('velocity', 1)
        self.health = kwargs.get('health', 100)
        self.surface = kwargs.get('surface', None)
        self.scene = kwargs.get('scene', None)  # Scena w jakiej sie znajduje

    def show(self):
        Game.screen.blit(self.image, (self.x, self.y))


class Player(Mob):
    def __init__(self, image, **kwargs):
        super().__init__(image, **kwargs)

        self.width = 64  # Piksele
        self.height = 64  # Piksele

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: self.move_left()
        if keys[pygame.K_RIGHT]: self.move_right()

    def move_left(self):
        if self.x > self.velocity:
            self.x -= self.velocity

    def move_right(self):
        if self.x + self.width < Game.width:
            self.x += self.velocity


class Game:  # Wszystkie zmienne gry
    pygame.init()
    pygame.display.set_caption('Giereczka')  # Ustawia nazwe okienka
    pygame.time.delay(30)

    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Tworzy okienko
    player = Player('Resources/Mobs/player.png', name='Tomek', velocity=5, starting_position=(0, 500))

    # @classmethod
    # def load_image(cls, file):
    #     try:
    #         surface = pygame.image.load(file)
    #     except pygame.error:
    #         raise SystemExit(f'Could not load the image "{image}" {pygame.get_error()}')
    #     return surface.convert()


class Scene:
    def __init__(self, name):
        self.name = name
        self.running = True
        self.background = pygame.image.load('Resources/background.jpg')
        self.mobs = [Mob('Resources/Mobs/goblin_prawo.png', name='Goblin1', starting_position=(200, 500), scene=self),
                     Mob('Resources/Mobs/goblin_lewo.png', name='Goblin2', starting_position=(600, 500), scene=self)]

        Game.player.scene = self  # Setting player's scene
        self.floor = pygame.Rect((0, LEVEL1_HEIGHT-500), (LEVEL1_WIDTH, 500))

    def on_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): # ESC - wyjsc z gry
            self.running = False

    def on_loop(self):  # Wszystkie movementy i inne ify
        Game.player.movement()

    def on_render(self):
        Game.screen.blit(self.background, (0, 0))
        Game.player.show()
        for mob in self.mobs:  # Pokazuje wszystkie moby
            mob.show()

        pygame.display.update()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()


if __name__ == "__main__":
    scena_1 = Scene('Level 1')
    scena_1.start()
