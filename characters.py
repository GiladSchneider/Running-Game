import pygame
import config
import random

# Create a bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = [68, 9]
        self.speedx = config.bullet_speed
        self.image_phases = 60
        self.image_phase = 0
        self.next_image_phase = 0
        
        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def update(self, freeze=False):
        self.rect.x += self.speedx
        if self.rect.right > config.width:
            self.kill()
    
    def draw(self, screen):
        screen.blit(self.get_image(), self.rect)

    def get_image(self):
        row = self.image_phase//10
        col = self.image_phase%10
        bullets = pygame.image.load("images/bullets.png").convert_alpha()
        bul_img = pygame.surface.Surface(self.size)
        bul_img.blit(bullets, (0, 0), (col*self.size[0], row*self.size[1], self.size[0], self.size[1]))
        bul_img.set_colorkey(config.black)
        bul_img = pygame.transform.flip(bul_img, True, False)
        bul_img = pygame.transform.scale(bul_img, (config.bullet_width, config.bullet_height))
        
        if self.next_image_phase == 1:
            self.image_phase += 1
            self.next_image_phase = -1
        if self.image_phase == self.image_phases:
            self.kill()
        self.next_image_phase += 1
        return bul_img

# Create a class for the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.y_vel = 0
        self.jump_count = 0
        self.jump_count_max = 2
        self.jump_vel = config.jump_vel
        self.piercing_shots = False
        
        self.run_sheet = pygame.image.load("images/player.png").convert_alpha()
        self.jump_sheet = pygame.image.load("images/player_jump.png").convert_alpha()
        self.sprite_state = 0
        self.next_sprite_state = 0
        self.image = self.get_image(32 + (self.sprite_state*120), 40, 40, 40)
        
        self.rect = self.image.get_rect()
        self.rect.x = config.width/4
        self.rect.y = config.height/2

        self.upgrades = ['jump_count_upgrade', 'jump_height_upgrade', 'peircing_upgrade',
                         'bullet_speed_upgrade']
        
    def update(self, freeze=False):
        self.rect.y -= self.y_vel
        self.y_vel -= config.gravity

        if self.y_vel < -config.velocity_max:
            self.y_vel = -config.velocity_max

    def draw(self, screen):
        screen.blit(self.get_image(32 + (self.sprite_state*120), 40, 40, 40), self.rect)
    
    def jump(self):
        if self.jump_count != self.jump_count_max:
            self.y_vel = self.jump_vel
            self.jump_count += 1
    
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert_alpha()
        
        if self.jump_count == 0:
            image.blit(self.run_sheet, (0, 0), (x, y, width, height))
            if self.next_sprite_state == 3:
                if self.sprite_state == 9:
                    self.sprite_state = 0
                else:
                    self.sprite_state += 1
                self.next_sprite_state = -1
            self.next_sprite_state += 1
        else:
            if self.y_vel < 0:                
                image.blit(self.jump_sheet, (0, 0), (32, 40, width, height))
            else:
                image.blit(self.jump_sheet, (0, 0), (152, 40, width, height))    
                
        image = pygame.transform.scale(image, config.player_size)
        image.set_colorkey(config.black)
    
        return image

    def attack(self):
        bullet = Bullet(self.rect.x + 40, self.rect.y + 45)
        return bullet

    def random_upgrade(self):
        upgrade = random.choice(self.upgrades)
        upgrade = getattr(self, upgrade)
        return upgrade()

    def jump_count_upgrade(self):
        self.jump_count_max += 1
        text = "Jump Count Upgraded to " + str(self.jump_count_max) + "!"
        return text
    
    def jump_height_upgrade(self):
        self.jump_vel += 1
        text = "Jump Heigh Upgraded!"
        return text
    
    def peircing_upgrade(self):
        self.piercing_shots = True
        self.upgrades.remove("peircing_upgrade")
        text = "Your Shots Now Pierce Wood!"
        return text
    
    def bullet_speed_upgrade(self):
        config.bullet_speed += 1
        text = "Bullet Speed Upgraded!"
        return text

# Create an enemy class
class Enemy(pygame.sprite.Sprite):
    """
    PARAMS:
        speedx: int -> x speed of the enemy, make negative to move left
        speedy: int -> y speed of the enemy
        run_sheet: filename -> the image of the enemy when running
        run_sheet_states: int -> the number of states the enemy has when running
        run_sheet_starting_point: [x, y] -> the starting pixel of the enemy on the run sheet
        run_sheet_sprite_size: [width, height] -> the size of the enemy's sprite
        run_sheet_pixel_distance: [x, y] -> the distance in pixels between each sprite
        SAME is true for attack attributes
        attack_interval: int -> the number of frames between each attack, if the enemy has an attack sheet
    """
    def __init__(self, speedx, speedy,                                                             
                run_sheet, run_sheet_states, run_sheet_starting_point, run_sheet_sprite_size, run_sheet_pixel_distance,   
                flying=False, starting_y=0, reversed=False):                                             
        
        super().__init__()
        self.speedx = speedx if not reversed else -speedx
        self.speedy = speedy
        self.flying = flying
        
        self.run_sheet = pygame.image.load(f"{run_sheet}").convert_alpha()        
        self.run_sheet_starting_point = run_sheet_starting_point
        self.run_sheet_pixel_distance = run_sheet_pixel_distance
        self.run_sheet_sprite_size = run_sheet_sprite_size
        self.run_sheet_states = run_sheet_states
        self.run_sheet_state = 0
        self.run_sheet_next_state = 0

        self.reversed = reversed
        self.image = self.get_image()
        
        self.rect = self.image.get_rect()
        self.rect.x = config.width if not reversed else 0 - self.rect.width
        self.rect.y = starting_y
        
    def update(self, freeze=False):
        if not freeze:
            self.rect.x -= self.speedx
            self.rect.y += self.speedy
        
        if self.rect.right < 0:
            self.kill()
        
        if self.rect.top > config.floor_height:
            self.kill()
        
        if self.speedy < config.velocity_max and self.flying == False:
            self.speedy += 1
    
    def draw(self, screen):
        screen.blit(self.get_image(), self.rect)
    
    def get_image(self):
        image = pygame.Surface([self.run_sheet_sprite_size[0], self.run_sheet_sprite_size[1]]).convert_alpha()
        image.blit(self.run_sheet, (0, 0), (self.run_sheet_starting_point[0] + self.run_sheet_state*self.run_sheet_pixel_distance[0], 
                                            self.run_sheet_starting_point[1] + self.run_sheet_state*self.run_sheet_pixel_distance[1], 
                                            self.run_sheet_sprite_size[0], self.run_sheet_sprite_size[1]))
        image = pygame.transform.scale(image, (self.run_sheet_sprite_size[0]*3, self.run_sheet_sprite_size[1]*3))
        image.set_colorkey(config.black)
        if self.reversed:
            image = pygame.transform.flip(image, True, False)

        self.run_sheet_next_state += 1
        if self.run_sheet_next_state == 3:
            self.run_sheet_state += 1
            self.run_sheet_next_state = 0
        if self.run_sheet_state == self.run_sheet_states:
            self.run_sheet_state = 0
        
        return image

# Chicken class
def Chicken(reversed=False):
    return Enemy(config.chicken_speed, 0, 
                "images/chicken_run.png", 14, [0, 0], [32, 34], [32, 0], reversed=reversed)

def Rhino(reversed=False, y=config.height/2):
    return Enemy(config.rhino_speed, 0,
                "images/rhino_run.png", 6, [0, 0], [52, 34], [52, 0],
                starting_y=y, flying=True, reversed=reversed)