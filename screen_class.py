import pygame
import random
import config

# Create a class for the screen
class Screen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode([config.width, config.height])
        self.screen_speed = config.map_scroll_speed

        self.image = pygame.Surface([config.width, config.height])
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        
        self.backround_sheet = pygame.image.load("images/background.png").convert_alpha()
        self.backround_sheet = pygame.transform.scale(self.backround_sheet, (config.width, config.height))
        self.background_x = 0

        self.image.blit(self.backround_sheet, (0,0))
        self.background = self.image
        
    def update(self, sprites, freeze=False):
        self.move_backround(freeze)
        for sprite in sprites:
            sprite.update(freeze)

    def draw(self, sprites, score, upgrade_text):
        self.screen.blit(self.background, (0,0))
        font = pygame.font.SysFont("ariel", 100)
        text = font.render(f"{score}", False, config.pearl)
        self.screen.blit(text, (100,100))

        font = pygame.font.SysFont("ariel", 50)
        text = font.render(upgrade_text, False, config.deep_blue)   
        self.screen.blit(text, (config.width/2 - text.get_width()/2, text.get_height() + 2))

        for sprite in sprites:
            sprite.draw(self.screen)    

    def move_backround(self, freeze=False):
        self.background_x += self.screen_speed if not freeze else 0
        self.background.blit(self.backround_sheet, (0,0), (self.background_x, 0, config.width, config.height))
        if self.background_x <= config.width:
            self.background.blit(self.backround_sheet, (config.width-self.background_x,0), (0, 0, config.width, config.height))
        if self.background_x > config.width:
            self.background_x = 0
            self.background.blit(self.backround_sheet, (0,0), (0, 0, config.width, config.height))

class Platform(pygame.sprite.Sprite):
        def __init__(self, width, height, sheet, scale, x = config.width, y = config.height/2, num_sprites = 1):
            super().__init__()
            self.sprite_state = 0
            self.next_image_phase = 0
            self.num_sprites = num_sprites
            self.scale = scale
            self.width = width
            self.height = height
            self.sprite_sheet = pygame.image.load(sheet).convert_alpha()
            self.image = self.get_image()
            
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
        def draw(self, screen):
            screen.blit(self.get_image(), self.rect)

        def update(self, freeze=False):
            if not freeze:
                self.rect.x -= config.platform_speed
            if self.rect.right < 0:
                self.kill()
        
        def get_image(self):
            image = pygame.Surface([self.width, self.height]).convert_alpha()
            
            image.blit(self.sprite_sheet, (0, 0), (self.sprite_state*self.width, 0, self.width, self.height))
            image = pygame.transform.scale(image, (self.width*self.scale, self.height*self.scale))
            image.set_colorkey(config.black)
            image = pygame.transform.flip(image, True, False)
            
            self.next_image_phase += 1
            if self.next_image_phase == 5:
                self.sprite_state += 1
                self.next_image_phase = 0
            if self.sprite_state == self.num_sprites:
                self.sprite_state = 0
            
            return image

def Box(y=config.height/2, scale=3):
    return Platform(width=22, height=16, sheet="images/box_platform.png", scale=scale, y=y)

def Box_triplet(y=config.height/2, scale=3):
    p1 = Platform(width=22, height=16, sheet="images/box_platform.png", scale=scale, y=y, x=config.width)
    p2 = Platform(width=22, height=16, sheet="images/box_platform.png", scale=scale, y=y, x=config.width + p1.width*p1.scale)
    p3 = Platform(width=22, height=16, sheet="images/box_platform.png", scale=scale, y=y, x=config.width + p1.width*p1.scale + p2.width*p2.scale)
    return p1, p2, p3