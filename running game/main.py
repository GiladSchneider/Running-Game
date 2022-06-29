import pygame
import config
import characters
import screen_class
import random

#Create a you lose screen
def you_lose(screen, sprites):
    pygame.time.wait(1500)
    reset_config()
    main()

def reset_config():
    config.bullet_speed = 1

def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()

    screen = screen_class.Screen()
    freeze_screen=False
    player = characters.Player()

    # Create sprites lists
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    player_bullets = pygame.sprite.Group()

    enemies = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    chicken_timer = 0
    box_timer = 0
    rhino_timer = 0

    score = 0
    upgrade_text = None
    upgrade_text_timer = 0

    # Ueful functions
    def create_box():
        y = random.uniform(30, config.height - 200)
        box = screen_class.Box(y)
        platforms.add(box)
        all_sprites.add(box)
    
    def create_box_triplet():
        y = random.uniform(30, config.height - 200)
        b1, b2, b3 = screen_class.Box_triplet(y)
        platforms.add(b1)
        platforms.add(b2)
        platforms.add(b3)
        all_sprites.add(b1)
        all_sprites.add(b2)
        all_sprites.add(b3)
    
    def create_chicken(reversed=False):
        chicken = characters.Chicken(reversed=reversed)
        enemies.add(chicken)
        all_sprites.add(chicken)

    def create_rhino(reversed=False):
        y = random.uniform(30, config.height - 200)
        rhino = characters.Rhino(reversed=reversed, y=y)
        enemies.add(rhino)
        all_sprites.add(rhino)

    # Create floor at start
    for i in range(0, 3*config.width, 22*7):
        box = screen_class.Platform(width=22, height=16, sheet="images/box_platform.png", scale=7, y=config.floor_height, x=i)
        platforms.add(box)
        all_sprites.add(box)

    # Main Loop
    running = True
    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                    bullet = player.attack()
                    all_sprites.add(bullet)
                    player_bullets.add(bullet)

        # Spawn Rates
        chicken_timer += 1
        box_timer += 1
        rhino_timer += 1
        if chicken_timer == config.chicken_timer_max:
            create_chicken(reversed = score > 9)          
            chicken_timer = 0
        if box_timer == config.box_timer_max:
            create_box_triplet()
            create_box()
            box_timer = 0
        if rhino_timer == config.rhino_timer_max:
            if score > 2:
                create_rhino(reversed = score > 19)
            rhino_timer = 0
        
        # Create map floor
        if box_timer == 0:
           create_box_triplet()

        screen.update(all_sprites, freeze_screen)        
        screen.draw(all_sprites, round(score, 2), upgrade_text)
        pygame.display.update()

        if upgrade_text != None:
            upgrade_text_timer += 1
            if upgrade_text_timer == config.upgrade_text_linger_time:
                upgrade_text = None
                upgrade_text_timer = 0

        # Check for collisions
        if pygame.sprite.groupcollide(player_bullets, enemies, True, True):
            score += 1
            if score % config.upgrade_threshold == 0:
                upgrade_text = player.random_upgrade()

        if not player.piercing_shots:
            pygame.sprite.groupcollide(player_bullets, platforms, True, False)
        
        # Check for platform collisions
        for platform in platforms:
            player_midbottom = (player.rect.right + player.rect.left)/2
            if player.rect.bottom >= platform.rect.top and player.rect.bottom <= platform.rect.top + config.velocity_max + 1 and player.y_vel<0:
                if player_midbottom >= platform.rect.left and player_midbottom <= platform.rect.right:
                    player.rect.bottom = platform.rect.top
                    player.jump_count = 0
                    player.y_vel = 0
            
            for enemy in enemies:
                if enemy.rect.bottom >= platform.rect.top and enemy.rect.bottom <= platform.rect.top + config.velocity_max + 1 and enemy.speedy > 0:
                    if enemy.rect.right >= platform.rect.left and enemy.rect.left <= platform.rect.right:
                        enemy.rect.bottom = platform.rect.top
                        enemy.speedy = 0
        
        # Loss conditions
        if player.rect.top > config.height:
            you_lose(screen, all_sprites)
        
        #check if the player collides withthe chicken
        for chicken in enemies:
            old_player_rect = player.rect.copy()
            new_player_rect = pygame.rect.Rect(old_player_rect[0], old_player_rect[1], old_player_rect[2]*(2/3), old_player_rect[3]*(2/3))
    
            old_chicken_rect = chicken.rect.copy()
            new_chicken_rect = pygame.rect.Rect(old_chicken_rect[0], old_chicken_rect[1], old_chicken_rect[2]*(2/3), old_chicken_rect[3]*(2/3))

            if new_player_rect.colliderect(new_chicken_rect):
                you_lose(screen, all_sprites)

        # Delay 
        clock.tick(config.fps)

    # Close Pygame
    pygame.quit()
    quit()

if __name__ == "__main__":
   main()