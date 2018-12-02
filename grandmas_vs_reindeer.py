
# imports
import pygame
import os
from pygame.locals import * # local constants

# initialization
pygame.init()
pygame.display.set_caption('Grandmas vs. Reindeer')

WIDTH, HEIGHT = 900, 550
game_surface = pygame.display.set_mode((WIDTH, HEIGHT))

fps_clock = pygame.time.Clock()
FPS = 30

# class Circle():
#     def __init__(self, background, x=WIDTH//2, y=HEIGHT//2, radius = 20):
#         game_surface.blit(background, (0,0))
#         pygame.draw.circle(game_surface, (255,0,0), (x,y), radius)

class Player():
    def __init__(self):
        self.player_width = width = 32
        self.player_height = height = 32


        spritesheet = pygame.image.load(os.path.join('art', 'reindeer.png')).convert()

        self.sprite_dict = {
            "stand" : [],
            "graze" : [],
            "right" : [],
            "down" : [],
            "up" : [],
        }
        
        ## skip left for now
        row=0
        for key, value in self.sprite_dict.items():
            for col in range(5):
                sprite_rect = pygame.Rect(col*width, row*height, width, height)
                image = pygame.Surface(sprite_rect.size).convert()
                image.blit(spritesheet, (0,0), sprite_rect)
                alpha = image.get_at((0,0))
                image.set_colorkey(alpha)
                value.append(image)
            row += 1

        self.sprite_dict["left"] = []
        for sprite in self.sprite_dict["right"]:
            image = pygame.transform.flip(sprite, True, False)
            self.sprite_dict["left"].append(image)

        self.player_img = self.sprite_dict["stand"][0]
        self.player_img_rect = self.player_img.get_rect()

# game logic
def run_game():
    bg_image = pygame.image.load(os.path.join('art', 'snowy_village.png'))
    background = game_surface.blit(bg_image, (0,0))
    
    # background = pygame.Surface(game_surface.get_size())
    # background = background.convert()
    # background.fill((0,0,250))

    # game_surface.blit(background, (0,0))
    game_surface.blit(bg_image, (0,0))

    # circle_rf = Circle(background)
    player = Player()
    print(player)
    print(player.player_img)
    print(player.player_img_rect)

    

    # game loop
    x_pos, y_pos = WIDTH//2, HEIGHT//2
    speed = 5
    run_game = True
    
    player.player_img_rect.center = x_pos, y_pos
    pygame.display.update()
    player_img_idx = 0

    while run_game:
        fps_clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT: 
                run_game = False 

            if event.type == KEYDOWN and event.key == K_RIGHT:
                pass

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_SPACE]:
            player.player_img_rect.center = x_pos, y_pos
            player_img_idx += 1
            if player_img_idx >= 5:
                player_img_idx = 0
            player.player_img = player.sprite_dict["graze"][player_img_idx]
        if pressed_keys[K_UP]:
            player_img_idx += 1
            if player_img_idx >= 5:
                player_img_idx = 0
            player.player_img = player.sprite_dict["up"][player_img_idx]
            player.player_img_rect.y -= speed
        if pressed_keys[K_DOWN]:
            player.player_img_rect.y += speed
            player_img_idx += 1
            if player_img_idx >= 5:
                player_img_idx = 0
            player.player_img = player.sprite_dict["down"][player_img_idx]
        if pressed_keys[K_RIGHT]:
            player_img_idx += 1
            if player_img_idx >= 5:
                player_img_idx = 0
            player.player_img = player.sprite_dict["right"][player_img_idx]
            player.player_img_rect.x += speed
        if pressed_keys[K_LEFT]:
            player_img_idx += 1
            if player_img_idx >= 5:
                player_img_idx = 0
            player.player_img = player.sprite_dict["left"][player_img_idx]
            player.player_img_rect.x -= speed

        # game_surface.blit(background, (0,0))
        game_surface.blit(bg_image, (0,0))
        game_surface.blit(player.player_img, player.player_img_rect)
        pygame.display.update()
    
    # exit game
    pygame.quit()

if __name__ == '__main__':
    run_game()