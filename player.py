import pygame
import constants
import math
import os
from spritesheet_functions import SpriteSheet

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, char_type, height=32, width=32):
        super().__init__()
        
        ## load sprite sheets
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = []
        self.standing_frames = []

        self.walk_counter = 0
        self.sprite_index = 0
        self.char_type = char_type

        sprite_sheet = SpriteSheet(os.path.join('art', char_type, 'sprite_sheet.png'))
        
        for n in range(0, 5):
            # get right images
            image = sprite_sheet.get_image(n * 32, 2 * 32, 32, 32)
            self.walking_frames_r.append(image)
            # flip right images to get left images
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
      
        for n in range(0, 5):
            down_image = sprite_sheet.get_image(n * 32, 3 * 32, 32, 32)
            self.walking_frames_d.append(down_image)

            up_image = sprite_sheet.get_image(n * 32, 4 * 32, 32, 32)
            self.walking_frames_u.append(up_image)
        
            stand_image = sprite_sheet.get_image(0 * 32, n * 32, 32, 32)
            self.standing_frames.append(stand_image)

        # Player rect and image
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Speed and Movement Values
        self.move_speed = 6
        self.change_x = 0
        self.change_y = 0

        # environment objects player can bump into
        self.block_list = []
        self.max_hit_count = 30
        self.hit_count = 30
        self.counted = False

    def move(self, direction):
        if direction == "up":
            self.change_y = -1 * self.move_speed
            self.get_next_sprite(self.walking_frames_u)
        elif direction == "down":
            self.change_y = self.move_speed
            self.get_next_sprite(self.walking_frames_d)
        elif direction == "left":
            self.change_x = -1 * self.move_speed
            self.get_next_sprite(self.walking_frames_l)
        elif direction == "right":
            self.change_x = self.move_speed
            self.get_next_sprite(self.walking_frames_r)
        elif direction == "stop_x":
            self.change_x = 0
        elif direction == "stop_y":
            self.change_y = 0

    def get_next_sprite(self, spritelist):
        if self.walk_counter % 6 == 0:
            if self.sprite_index >= len(spritelist):
                self.sprite_index = 0
            self.image = spritelist[self.sprite_index]
            self.sprite_index += 1
        if self.walk_counter >= constants.FPS:
            self.walk_counter = 0

    def decrease_hit_count(self, n=1):
        if self.hit_count > 0:
            self.hit_count -= 1
        else:
            self.hit_count = self.max_hit_count

    def stay_inbounds(self):
        # will the move put us out of the left or right side of the board? 
        is_inbounds_x = is_inbounds_y = True
        target_x = self.rect.x + self.change_x
        target_y = self.rect.y + self.change_y

        # Check right side
        if target_x + self.rect.width >= constants.WINDOW_WIDTH:
            self.move("stop_x") # don't move any further
            self.rect.x = constants.WINDOW_WIDTH - self.rect.width # nudge right up against the edge
            is_inbounds_x = False
        # Check left side
        elif target_x <= 0:
            self.move("stop_x")
            self.rect.x = 0
            is_inbounds_x = False

        # Check bottom side
        if target_y + self.rect.height >= constants.WINDOW_HEIGHT:
            self.move("stop_y") # don't move any further
            self.rect.y = constants.WINDOW_HEIGHT - self.rect.height # nudge right up against the edge
            is_inbounds_y = False
        # Check top side
        elif target_y <= 0:
            self.move("stop_y")
            self.rect.y = 0
            is_inbounds_y = False

        return is_inbounds_x, is_inbounds_y

    def calc_collisions(self, direction):
        block_hit_list = pygame.sprite.spritecollide(self, self.block_list, False)
        if direction == "x":
            for block in block_hit_list:
                block.is_hit()
                # If we are moving right,
                # set our right side to the left side of the item we hit
                if self.change_x > 0:
                    self.rect.right = block.rect.left
                elif self.change_x < 0:
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                self.move("stop_x")
        if direction == "y":
            for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
                block.is_hit()
                if self.change_y > 0:
                    self.rect.bottom = block.rect.top
                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom
                self.move("stop_y")

    def update(self):
        # keep the player on the board
        self.stay_inbounds()

        # CHECK FOR COLLISIONS
        # Move left or right, then see if we bump into anything
        self.rect.x += self.change_x
        self.calc_collisions("x")
        
        # move up or down and see if we hit anything
        self.rect.y += self.change_y
        self.calc_collisions("y")
        
class NonPlayer(Player):
    def __init__(self, x, y, char_type, height=32, width=32):
        super().__init__(x, y, char_type, height, width)

        ## load sprite sheets
        self.walking_frames_l = []
        self.walking_frames_r = []
        self.alerted_frames_l = []
        self.alerted_frames_r = []
        self.walking_frames_u = []
        self.walking_frames_d = []
        self.standing_frames = []
        self.dying_frames = []

        self.walk_counter = 0
        self.sprite_index = 0
        self.char_type = str(char_type)

        self.is_dead = False
        self.dead_counter = 0
        self.destroyed = False

        sprite_sheet = SpriteSheet(os.path.join('art', self.char_type, 'sprite_sheet.png'))
        
        for n in range(0, 5):
            # get right images
            image = sprite_sheet.get_image(n * 32, 2 * 32, 32, 32)
            self.walking_frames_r.append(image)
            # flip right images to get left images
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_l.append(image)
      
        for n in range(0,5):
            # get right alert images
            image = sprite_sheet.get_image(n * 32, 1 * 32, 32, 32)
            self.alerted_frames_r.append(image)
            # flip right images to get left images
            image = pygame.transform.flip(image, True, False)
            self.alerted_frames_l.append(image)

        for n in range(0, 5):
            down_image = sprite_sheet.get_image(n * 32, 3 * 32, 32, 32)
            self.walking_frames_d.append(down_image)

            up_image = sprite_sheet.get_image(n * 32, 4 * 32, 32, 32)
            self.walking_frames_u.append(up_image)
        
            stand_image = sprite_sheet.get_image(0 * 32, 2 * 32, 32, 32)
            self.standing_frames.append(stand_image)
            
            die_image = sprite_sheet.get_image(n * 32, 0 * 32, 32, 32)
            self.dying_frames.append(die_image)

        # Player rect and image
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        
        self.move_speed = 3
        self.rect.x = x
        self.rect.y = y
    
    def check_distance(self):
        if self.player_character is None: 
            pass
        else:
            x1, y1 = self.rect.center
            x2, y2, = self.player_character.rect.center
            self.distance_from_player = calc_distance(x1, y1, x2, y2)
    
    def check_radians(self):
        if self.player_character is None:
            pass
        else:
            x1, y1 = self.rect.center
            x2, y2, = self.player_character.rect.center
            self.radians = calc_radians(x1, y1, x2, y2)

    def danger_close(self, threshold=150):
        self.check_distance()
        if self.distance_from_player >= threshold:
            return False
        if self.distance_from_player < threshold:
            return True

    def is_hit(self):
        self.is_dead = True
        self.sprite_index = 0
        self.walk_counter =0

    def destroy(self):
        self.change_x = 0
        self.change_y = 0
        self.destroyed = True
        print("Destroyed the object.")

    def update(self):
        ## Trigger an alert if player character gets closer than a certain number of pixels
        if self.is_dead:
            self.get_next_sprite(self.dying_frames)
            self.dead_counter += 1
            if self.dead_counter >= 30:
                self.change_x = 0
                self.change_y = 0
            if self.dead_counter >= 90:
                self.image = self.dying_frames[4]
            if self.dead_counter >= 150:
                self.destroy()

        elif self.danger_close():
            self.check_radians()
            self.change_x = self.move_speed * math.cos(self.radians)
            self.change_y = self.move_speed * math.sin(self.radians)
            ## run panicked in the correct direction
            if self.change_x > 0:
                self.get_next_sprite(self.alerted_frames_r)
            else:
                self.get_next_sprite(self.alerted_frames_l)
        else:  
            self.get_next_sprite(self.standing_frames)
            self.change_x = 0
            self.change_y = 0

        # keep the player on the board
        self.stay_inbounds()

        # CHECK FOR COLLISIONS
        # Move left or right, then see if we bump into anything
        self.rect.x += self.change_x
        self.calc_collisions("x")
        
        # move up or down and see if we hit anything
        self.rect.y += self.change_y
        self.calc_collisions("y")
        

def calc_distance(x1, y1, x2, y2):
    # distance formula = √(x2−x1)^2+(y2−y1)^2
    dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    return dist

def calc_radians(x1, y1, x2, y2):
    # slope formula
    radians = math.atan2((y1-y2), (x1 - x2))
    return radians


def calc_angle(x1, y1, x2, y2):
    pass