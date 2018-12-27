import pygame
from player import *
import constants
import random

## SET UP GAME BOARD
pygame.init()
screen = pygame.display.set_mode([constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT])
pygame.display.set_caption("Grandmas vs. Reindeer")

## If true, show player location on teh screen
display_location = True
pygame.font.init()
myfont = pygame.font.SysFont('Arial', 20)


def create_grannies(granny_list, player, x = None, y = None):
    ## see how many grannies there are in play
    ## if there are fewer grannies than the granny count, create more grannies
    num_grannies_to_create = constants.GRANNY_COUNT - len(granny_list)
    
    ## create the grannies
    for n in range(num_grannies_to_create):
        if x is None: 
            x = random.randint(0, constants.WINDOW_WIDTH - 32)
        if y is None: 
            y = random.randint(0, constants.WINDOW_HEIGHT - 32)
        
        granny = NonPlayer(x, y, 'grandma')
        granny.player_character = player
        granny_list.add(granny)

def score_finished_screen(screen, score):
    # clear the screen
    screen.fill((0, 0, 0)) ## TODO: replace with background

    # show the score centered on the screen
    score_font = pygame.font.SysFont('Arial', 40)
    textsurface = myfont.render(f"You hit {score:.0f} grannies. Nice work.", False, (255, 255, 255))
    screen.blit(textsurface, ((constants.WINDOW_WIDTH - textsurface.get_width()) / 2, constants.WINDOW_HEIGHT / 2))
    pygame.display.flip()
    # put reindeer and a grandma on either part of the screen

    pygame.time.wait(3000)
    pygame.event.clear()
    textsurface = myfont.render(f"Press any key to play again.", False, (255, 255, 255))
    screen.blit(textsurface, ((constants.WINDOW_WIDTH - textsurface.get_width()) / 2, (constants.WINDOW_HEIGHT / 2) + textsurface.get_height()))
    pygame.display.flip()
    any_key = False

    while not(any_key):
        for event in pygame.event.get():
            # Exit main loop on quit event
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                any_key = True
    
    ready_to_play_screen()

def ready_to_play_screen():
    screen.fill((0,0,0))
    pygame.display.flip()
 
    pygame.time.wait(2000)

    constants.GRANNY_COUNT = 1
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join('sound','grandma_got_runover_by_a_reindeer.mp3'))
    pygame.mixer.music.play(-1)
    
    pygame.event.clear()
    textsurface = myfont.render(f"Ready, Player One!", False, (255, 255, 255))
    screen.blit(textsurface, ((constants.WINDOW_WIDTH - textsurface.get_width()) / 2, (constants.WINDOW_HEIGHT / 2) - textsurface.get_height()))
    pygame.display.flip()

    pygame.time.wait(2000)
    textsurface = myfont.render(f"Press any key to start.", False, (255, 255, 255))
    screen.blit(textsurface, ((constants.WINDOW_WIDTH - textsurface.get_width()) / 2, (constants.WINDOW_HEIGHT / 2) + textsurface.get_height()))
    pygame.display.flip()
    
    any_key = False

    while not(any_key):
        for event in pygame.event.get():
            # Exit main loop on quit event
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                any_key = True

    run_game()


def run_game():
    ## SETUP
    score = 0

    ## SETUP BOARD OBJECTS AND PLAYERS  
    player_list = pygame.sprite.Group()
    granny_list = pygame.sprite.Group()
    
    player = Player(constants.WINDOW_WIDTH * .33, constants.WINDOW_HEIGHT / 2, 'deer')

    ## Create the number of grannies needed:
    create_grannies(granny_list, player, constants.WINDOW_WIDTH * .66, constants.WINDOW_HEIGHT /2)
    player_list.add(player)
    player.block_list = granny_list

    ## MAIN GAME LOOP
    clock = pygame.time.Clock()
    start_tick = pygame.time.get_ticks()
    done = False

    granny_hit_sound = pygame.mixer.Sound(os.path.join('sound', 'granny_hit.wav'))

    while not done:
        ## Calculate time remaining: 
        seconds = constants.ROUND_LENGTH - round((pygame.time.get_ticks() - start_tick)/1000, 0)

        if seconds <= 0:
            done = True
            score_finished_screen(screen, score)

        ## GET USER INPUTS
        for event in pygame.event.get():
            # Exit main loop on quit event
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player.move("stop_x")
                if event.key  in [pygame.K_UP, pygame.K_DOWN]:
                    player.move("stop_y")
                            
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.move("left")
        if keys[pygame.K_RIGHT]:
            player.move("right")
        if keys[pygame.K_UP]:
            player.move("up")
        if keys[pygame.K_DOWN]:
            player.move("down")

        ## PROCESS GAME EVENTS
        
        # remove any destroyed sprites
        destroy_list = []
        dead_list = []
        for granny in granny_list:
            if granny.destroyed:
                destroy_list.append(granny)
            if granny.is_dead:
                dead_list.append(granny)
                if not(granny.counted):
                    granny.counted = True
                    score += 1
                    pygame.mixer.Sound.play(granny_hit_sound)

        granny_list.remove(destroy_list)
        
        # Increase the number of grandas if they're all dead
        if len(dead_list) >= constants.GRANNY_COUNT:
            constants.GRANNY_COUNT += 1


        # create any needed grannies
        create_grannies(granny_list, player)

        # update characters
        granny_list.update()
        player_list.update()

        ## PROCESS GAME VISUALS
        screen.fill((0, 0, 0))
        granny_list.draw(screen)
        player_list.draw(screen)

   
        textsurface = myfont.render(f"Time Remaining: {seconds:.0f} - Grannies Hit: {score}", False, (255, 255, 255))
        screen.blit(textsurface, (0, 0))

        pygame.display.flip()

        ## PROGRESS TO NEXT FRAME
        clock.tick(constants.FPS)
    pygame.quit()

if __name__ == "__main__":
    ready_to_play_screen()

