import math, time
import pygame
pygame.init()

yellow = (255,255,0)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)

class Pacman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for image in ['pacman2.png','pacman1.png','pacman2.png','pacman3.png','pacman4.png','pacman3.png',]:
            self.images.append(pygame.image.load(image).convert_alpha())
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.keys = []
        self.update_time = time.time()
        self.image_update_time = self.update_time
        self.image_index = 0
    def keydown(self, key):
        if key in (pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT, pygame.K_RIGHT):
            self.keys.append(key)
    def keyup(self, key):
        self.keys.remove(key)
    def update(self):
        now = time.time()
        if self.keys:
            pps = 50.0
            move = math.ceil((now - self.update_time) * pps)
            key = self.keys[-1]
            if key == pygame.K_UP:
                transform = lambda x: pygame.transform.rotate(x, 90)
                self.rect = self.rect.move(0,-move)
            elif key == pygame.K_DOWN:
                transform = lambda x: pygame.transform.rotate(x, -90)
                self.rect.move_ip(0,move)
            elif key == pygame.K_RIGHT:
                transform = lambda x: x
                self.rect.move_ip(move,0)
            elif key == pygame.K_LEFT:
                transform = lambda x: pygame.transform.flip(x, True, False)
                self.rect.move_ip(-move,0)
                
            if (now - self.image_update_time) > (1.0/6.0):
                self.image_update_time = now
                self.image_index += 1
                if self.image_index >=len(self.images):
                    self.image_index = 0
                self.image = transform(self.images[self.image_index])
        else:
            self.image_index = 0
            self.image = self.images[0]
        
        self.update_time = now

class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y, color = red):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.move_ip(x,y)

size = (500,500)
screen = pygame.display.set_mode(size)
screen.fill(blue)

background = pygame.Surface(screen.get_size())
background.fill(blue)


all = pygame.sprite.RenderUpdates()
pellets = pygame.sprite.Group()

pacman = Pacman()
all.add(pacman)

for x in range(0,500,20):
    for y in range(0,500,20):
        pellet = Pellet(x,y,red)
        all.add(pellet)
        pellets.add(pellet)

pygame.display.flip()

collide = pygame.sprite.collide_rect_ratio(.30)

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            pacman.keydown(event.key)
        elif event.type == pygame.KEYUP:
            pacman.keyup(event.key)
    all.clear(screen, background)
    all.update()
    for sprite in pellets:
        if collide(pacman, sprite):
            sprite.kill()
    dirty_rects = all.draw(screen)
    screen.blit(pacman.image, pacman.rect)
    pygame.display.update(dirty_rects)
       
pygame.quit()