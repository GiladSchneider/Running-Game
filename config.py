import pygame
pygame.init()

# Screen
infoObject = pygame.display.Info()
x, y = (infoObject.current_w, infoObject.current_h)
width = x - 200
height = y - 200
floor_height = height - 70

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
pearl = (255, 255, 200)
deep_blue = (0, 0, 128)

# object sizes
bullet_width = 136
bullet_height = 18
player_size = [120, 120]

# object speeds
bullet_speed = 1
map_scroll_speed = 2
chicken_speed = 10
rhino_speed = 20
platform_speed = 4

chicken_timer_max = 200
box_timer_max = 60
rhino_timer_max = 250

fps = 60

upgrade_threshold = 1
upgrade_text_linger_time = 100

jump_vel = 16
gravity = 1
velocity_max = 20