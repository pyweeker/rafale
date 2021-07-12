"""
Platformer Game
"""
import arcade
import random
import math
import os

#from custom_named_sprite import SpriteWithHealth, Dog, MyCustomNamedSprite, MyBirdySprite, BouncingSprite, Explosion

#from arcade.experimental.camera import Camera2D

from arcade import Point, Vector
from arcade.utils import _Vec2

import time

import pyglet


print("\n\n\n     * * *   https://www.kenney.nl/    FREE ASSETS   * * *")

TILE_SPRITE_SCALING = 0.5

# Constants
SCREEN_WIDTH = 1800 #1000
SCREEN_HEIGHT = 1000 #650
SCREEN_TITLE = "Gendarmerie"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SCALE = 0.5

SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH // 2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH // 2
BOTTOM_VIEWPORT_MARGIN = SCREEN_HEIGHT // 2
TOP_VIEWPORT_MARGIN = SCREEN_HEIGHT // 2


MOVEMENT_SPEED = PLAYER_MOVEMENT_SPEED
MOVEMENT_SPEED_AMPHET = MOVEMENT_SPEED * 3


AMPHET_TIME_MAX = 60 * 10




HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -30
LIFEBAR_Yoffset = 30

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25

ENEMY_MAX_HEALTH = 20

PLAYER_MAX_HEALTH = 141

LASER_DAMMAGE = 15
GRENADE_DAMMAGE = 150


MAX_DISTANCE_DOG_DETECTION = SCREEN_HEIGHT


LIVES_AT_START = 3


AMMO_MAX = 50
AMMO_GLOCK_START = 30

AMMO_GRENADE_START = 10

AMMO_GLOCK_PACK = 20
AMMO_GRENADE_PACK = 3

MEDIKIT_HEALTH_BOOST = PLAYER_MAX_HEALTH // 2

LEFT_MOUSE_BTN = 1
RIGHT_MOUSE_BTN = 4

SPRITE_SCALING_LASER = 0.8


ROCKET_SMOKE_TEXTURE = arcade.make_soft_circle_texture(15, arcade.color.GRAY)

CLOUD_TEXTURES = [
    arcade.make_soft_circle_texture(250, arcade.color.WHITE),
    arcade.make_soft_circle_texture(250, arcade.color.LIGHT_GRAY),
    arcade.make_soft_circle_texture(250, arcade.color.LIGHT_BLUE),
]



MUSIC_INTRO = "resources/sounds/jet_sound.ogg"

MUSIC_GAMEOVER = "resources/sounds/jet_sound.ogg"

MUSIC_INGAME = "resources/sounds/jet_sound.ogg"


DISPLAY_YOFFSET_SCORE = 150
DISPLAY_YOFFSET_AMMO = 175
DISPLAY_YOFFSET_GRENADE = 200










# *************************************************************

HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -30
LIFEBAR_Yoffset = 30

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25


CROSSHAIR__RELATIVE_XOFFSET_SETUP = 0
CROSSHAIR__RELATIVE_YOFFSET_SETUP = 100

XRESPAWN = SCREEN_WIDTH // 2
YRESPAWN = SCREEN_HEIGHT // 2


RADAR_RADIUS_DETECTION = 512

ECLOSION_TIME_INTERVAL = 15.0
ECLOSION_MAX_WAVES = 3



class SpriteWithHealth(arcade.Sprite):
    """ Sprite with hit points """

    def __init__(self, image, scale, max_health):
        super().__init__(image, scale)

        # Add extra attributes for health
        self.max_health = max_health
        self.cur_health = max_health

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound("resources/sounds/jet_sound.ogg")
        self.hit_sound = arcade.load_sound("resources/sounds/jet_sound.ogg")
        self.death_sound = arcade.load_sound("resources/sounds/jet_sound.ogg")

        self.respawning = 0


    def respawn(self, xrespawn, yrespawn):
        """
        Called when we die and need to make a new ship.
        'respawning' is an invulnerability timer.
        """
        # If we are in the middle of respawning, this is non-zero.
        self.respawning = 1
        #self.center_x = SCREEN_WIDTH / 2
        #self.center_y = SCREEN_HEIGHT / 2

        self.center_x = xrespawn
        self.center_y = yrespawn

        self.angle = 0

        self.cur_health = self.max_health


    def draw_health_number(self):
        """ Draw how many hit points we have """

        health_string = f"{self.cur_health}/{self.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        """ Draw the health bar """

        # Draw the 'unhealthy' background
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - LIFEBAR_Yoffset,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)







class Dog(SpriteWithHealth):


    def __init__(self, image, scale, max_health):
        super().__init__(image, scale, max_health)

        # Add extra attributes for health
        self.max_health = max_health
        self.cur_health = max_health

        self.path = None
        




    @property
    def distance_player(self, target_sprite): #target will be player in this game , property instead of attribute for fresh values

        dist = math.hypot(self.center_x - target_sprite.center_x, self.center_y - target_sprite.center_y)

        return dist




class Explosion(arcade.Sprite):
    

    def __init__(self, texture_list,x,y):
        
        super().__init__()

        self.center_x = x
        self.center_y = y
        
        self.current_texture = 0      
        self.textures = texture_list  
        self.set_texture(self.current_texture)

    def update(self):

        
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.kill()






# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def make_star_field(star_count):

   pass



# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////





class InstructionView(arcade.View):

    def __init__(self):
        
        super().__init__()
        
        self.music_intro = arcade.load_sound(MUSIC_INTRO)

        self.looping_music = True



        print("type(self.music_intro)   : ", type(self.music_intro))


        self.player_music_intro = None


        # ////
        self.stars = make_star_field(150)
        #self.skyline1 = make_skyline(SCREEN_WIDTH * 5, 250, (80, 80, 80))
        #self.skyline2 = make_skyline(SCREEN_WIDTH * 5, 150, (50, 50, 50))




    
    
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        
        

        #self.player_music_intro.EOS_LOOP = 'loop'
        self.player_music_intro = arcade.play_sound(self.music_intro)
        

        print("type(self.player_music_intro)   : ", type(self.player_music_intro))


    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


        


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup(level=1)
        arcade.set_background_color(arcade.csscolor.BLACK)


        try:
            self.music_intro.stop(self.player_music_intro)
        except ValueError:
            print("music already finished")  # ValueError: list.remove(x): x not in list   media.Source._players.remove(player)

        self.window.show_view(game_view)


    def on_update(self, delta_time):
        """ Movement and game logic """
        pass



#--------------------------------------------------------




class GameOverView(arcade.View):
    """ View to show when game is over """

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()


        #self.texture = arcade.load_texture("game_over.png")


        #self.background = arcade.load_texture("./resources/images/backgrounds/game_over.jpg")
        

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.

        





        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.texture = arcade.load_texture("./resources/images/backgrounds/game_over.jpg")


        self.music_gameover = arcade.load_sound(MUSIC_GAMEOVER)
        #print("type(self.music_intro)   : ", type(self.music_gameover))
        self.player_music_gameover = None


    def on_show(self):

        self.player_music_gameover = arcade.play_sound(self.music_gameover)



    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)


        #self.texture.draw_sized(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT)


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, re-start the game. """
        game_view = GameView()
        #game_view.setup()
        game_view.setup(level=1)

        #self.music_gameover.stop(self.player_music_gameover)


        try:
            self.music_gameover.stop(self.player_music_gameover)
        except ValueError:
            print("music already finished")

        self.window.show_view(game_view)






#class MyGame(arcade.Window):
class GameView(arcade.View):



    

    def __init__(self):
    

        # Call the parent class and set up the window
        #super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
        super().__init__()

        self.tile_map = None

        self.window.set_mouse_visible(False)

        self.topleft_corner = None

        # Cameras
        self.camera = None
        self.gui_camera = None

        self.shake_offset_1 = 0
        self.shake_offset_2 = 0
        self.shake_vel_1 = 0
        self.shake_vel_2 = 0




        self.datamusic = arcade.load_sound(MUSIC_INGAME)

        self.datamusic.get_length()

        self.player_music_ingame = None

        self.explosion_images = []


        #self.set_exclusive_mouse(True) # capture mouse ; not in view ?

        #self.set_vsync(True)

        #self.camera = Camera2D(
        #    viewport=(0, 0, self.width, self.height),
        #    projection=(0, self.width, 0, self.height),
        #)


        #self.camera = Camera2D(
        #    viewport=(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT),
        #    projection=(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT),
        #)

        self.mouse_pos = 0, 0

        self.crosshair_relative_xoffset = 0
        self.crosshair_relative_yoffset = 0



        

        
        #self.set_mouse_visible(True)
        self.window.set_mouse_visible(False)

       
        self.frame_count = 0


        self.coin_list = None
        self.wall_list = None

        self.startposition_list = None
        
        
        
        #self.dont_touch_list = None
        self.player_list = None
        self.life_list = None

        self.enemy_list = None

        
        

        self.crosshair_sprite = None

        # Our physics engine
        self.physics_engine_walls = None

        #.....................................................
        self.water_list = None
        

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None
        #----------------------------------------
        

        


        self.stairs_list = None

        
        #..................

        
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0
        self.lives = 0


        self.ammo = 0
        self.ammo_text = None # ????????????????????

        

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.sound.load_sound("resources/sounds/jet_sound.ogg")
        self.hit_sound = arcade.sound.load_sound("resources/sounds/jet_sound.ogg")
        self.death_sound = arcade.load_sound("resources/sounds/jet_sound.ogg")

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 1

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("resources/sounds/jet_sound.ogg")
        self.jump_sound = arcade.load_sound("resources/sounds/jet_sound.ogg")
        self.game_over = arcade.load_sound("resources/sounds/jet_sound.ogg")




    def load_level(self, level):
        # Read in the tiled map
        #my_map = arcade.tilemap.read_tmx(f":resources:tmx_maps/level_{level}.tmx")

        map_name = f"./resources/maps/level_{level}.json"

        #layer_options = {"Topleft_corner_layer": {"use_spatial_hash": True}}
        #layer_options = {"Startposition_layer": {"use_spatial_hash": True}}
        #layer_options = {"Cloud_thunder_layer": {"use_spatial_hash": True}}
        #layer_options = {"Mi35_layer": {"use_spatial_hash": True}}

        layer_options = {"Topleft_corner_layer": {"use_spatial_hash": True},"Startposition_layer": {"use_spatial_hash": True}, "Cloud_thunder_layer": {"use_spatial_hash": True}, "Mi35_layer": {"use_spatial_hash": True}}

        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SPRITE_SCALING,layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # --- Walls ---

        # Calculate the right edge of the my_map in pixels
        #self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # Grab the layer of items we can't move through
        #self.wall_list = arcade.tilemap.process_layer(my_map,
        #                                              'Platforms',
        #                                              TILE_SPRITE_SCALING,
        #                                              use_spatial_hash=True)

        #self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
        #                                                     self.wall_list,
        #                                                     gravity_constant=GRAVITY)

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Set the view port boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0



    def on_resize(self, width, height):
        """Resize window"""
        self.camera.resize(width, height)
        self.gui_camera.resize(width, height)



        

        



    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        #self.eclosion_remaining_waves = ECLOSION_MAX_WAVES

        #arcade.schedule(self.krontab, ECLOSION_TIME_INTERVAL)


        

        # Keep track of the score
        self.score = 0

        if self.level == 1:
            self.lives = LIVES_AT_START
        

        self.ammo = AMMO_GLOCK_START

        self.startposition_list = arcade.SpriteList()
        
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list =  arcade.SpriteList()


        
        #self.pitbulls_paths = [] # list of list in fact        https://docs.python.org/fr/3/library/typing.html

        self.life_list = arcade.SpriteList()

        #self.is_smoked = False # native from bool()
        #self.is_smoked = True #test

        


        



        for i in range(32):  
        
                        
            texture_name = f"resources/images/explosion/explosion{i:04d}.png"
            self.explosion_images.append(arcade.load_texture(texture_name))

        self.explosion_list = arcade.SpriteList()


        


        self.wall_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=128)

        self.coin_list = arcade.SpriteList()

        
        self.macadam_list = arcade.SpriteList()
        self.pave_list = arcade.SpriteList()

        #......................................................................

        

        #.................................
        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        startposition_layer_name = 'Startposition'

        


        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        #coins_layer_name = 'Coins'
        # Name of the layer that has items for foreground
        #foreground_layer_name = 'Foreground'
        # Name of the layer that has items for background
        #background_layer_name = 'Background'
        # Name of the layer that has items we shouldn't touch
        #dont_touch_layer_name = "Don't Touch"

        

        stairs_layer_name = "Stairs"

        # Map name
  
        #map_name = f"resources/tmx_maps/easymap1_level_{level}.tmx"

        map_name = f"./resources/maps/level_{level}.json"

        # Read in the tiled map
        #my_map = arcade.tilemap.read_tmx(map_name)  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #self.tile_map = arcade.load_tilemap(
            
        #    f"./resources/maps/level_{level}.json", scaling=TILE_SPRITE_SCALING,layer_options=layer_options
        #)

        self.load_level(self.level)

        

        # Calculate the right edge of the my_map in pixels
        #self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        

        

        # -- startposition ------------------------------------------------------------------------------------------------------------------------------------------------
        #self.startposition_list = arcade.tilemap.process_layer(map_object=my_map,
        #                                              layer_name=startposition_layer_name,
        #                                              scaling=TILE_SCALING,
        #                                              use_spatial_hash=True)

        #print("---> ", self.startposition_list[0])
        #print(" X ", self.startposition_list[0].center_x)
        #print(" Y ", self.startposition_list[0].center_y)

        #start_XY = tuple((self.startposition_list[0].center_x,self.startposition_list[0].center_y))
        start_XY = tuple((666,666))




        #image_source = "resources/images/animated_characters/policeboy_gun_128.png"
        image_source = "resources/00/rafale_logo.png"

        
        #self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite = SpriteWithHealth(image_source, CHARACTER_SCALING, max_health = PLAYER_MAX_HEALTH)


        self.player_sprite.center_x = start_XY[0]
        self.player_sprite.center_y = start_XY[1]


        #self.player_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite)

        # *******************************************************************************************
        #self.life_list.append(life)

        for i in range(self.lives):
                life = arcade.Sprite("resources/images/HUD/head_128.png", SCALE)
                self.life_list.append(life)



        #----------------------------------------------------------------------------------------

        

        self.crosshair_list = arcade.SpriteList()

        self.crosshair_sprite = arcade.Sprite("resources/images/HUD/crosshair061.png", 0.4)


        self.crosshair_relative_xoffset = CROSSHAIR__RELATIVE_XOFFSET_SETUP
        self.crosshair_relative_yoffset = CROSSHAIR__RELATIVE_YOFFSET_SETUP
      


        self.crosshair_sprite.center_x = self.player_sprite.center_x + CROSSHAIR__RELATIVE_XOFFSET_SETUP
        self.crosshair_sprite.center_y = self.player_sprite.center_y + CROSSHAIR__RELATIVE_YOFFSET_SETUP

        self.crosshair_list.append(self.crosshair_sprite)
        # ///////////



        

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        self.camera = arcade.Camera(self.window, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.gui_camera = arcade.Camera(self.window, SCREEN_WIDTH, SCREEN_HEIGHT)

        # Center camera on user
        self.pan_camera_to_user()
        #self.window.pan_camera_to_user()

        

        #self.mouse_pos = self.crosshair_sprite.center_x, self.crosshair_sprite.center_y

        # ///////////
        # ----------------------------------------------------------------------------------------------------------------------------------

        

        


        # -- Don't Touch Layer
        #self.dont_touch_list = arcade.tilemap.process_layer(my_map,
                                                            #dont_touch_layer_name,
                                                            #TILE_SCALING,
                                                            #use_spatial_hash=True)

        # --- Other stuff
        # Set the background color
        #if my_map.background_color:
        #    arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        #self.physics_engine_walls = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)


        #if self.level == 1:
            #self.background = arcade.load_texture("./resources/images/backgrounds/abstract_1.jpg")

        #    self.background = arcade.load_texture("./resources/images/backgrounds/jaune_uni.jpg")

            

        




    def krontab(self, delta_time):

        #chrono_spawn_image_source = "./resources/images/tiles/foetus128.png"
        yellowvest_image_source = "./resources/images/enemies/yellowboy_128.png"

        if self.eclosion_remaining_waves > 0:

            for chrono_spawn in self.chrono_spawn_list:

                #new_enemy = SpriteWithHealth(chrono_spawn_image_source, 1, max_health = ENEMY_MAX_HEALTH)
                new_enemy = SpriteWithHealth(yellowvest_image_source, 1, max_health = ENEMY_MAX_HEALTH)
                new_enemy.center_x = chrono_spawn.center_x
                new_enemy.center_y = chrono_spawn.center_y
                new_enemy.angle = 0


                #self.chrono_list.append(new_enemy)
                self.yellowvest_list.append(new_enemy)

            self.eclosion_remaining_waves -= 1

        else:

            arcade.unschedule(krontab)




    def on_show(self):

        self.player_music_ingame = arcade.play_sound(self.datamusic)


    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color

        self.camera.use()
        #self.clear()
        self.window.clear()


        arcade.start_render()

        self.scene.draw()


        self.center_on_player()

        self.gui_camera.use()

        try:

            arcade.set_background_color(arcade.csscolor.BLACK)

                
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background)
        except AttributeError: # level 2 background is None , it gives 'NoneType' object has no attribute 'draw_sized'

            arcade.set_background_color(arcade.csscolor.RED)

        #self.camera.use()
        #self.clear()

        #world_pos = self.camera.mouse_coordinates_to_world(*self.mouse_pos)  # AttributeError: 'Camera' object has no attribute 'mouse_coordinates_to_world'

        #arcade.draw_circle_filled(*world_pos, 10, arcade.color.BLUE)

        # Draw our sprites

        

       
        


        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, DISPLAY_YOFFSET_SCORE + self.view_bottom,
                         arcade.csscolor.WHITE, 18)



        output_ammo = f"Ammo: {self.ammo}"
        #arcade.draw_text(output_ammo, 100, 400, arcade.color.RED, 20)

        arcade.draw_text(output_ammo, 10 + self.view_left, DISPLAY_YOFFSET_AMMO + self.view_bottom,
                         arcade.csscolor.YELLOW, 18)


        


        



    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        #if self.player_sprite.amphet_excited is False:
        

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED


        elif key == arcade.key.ESCAPE:
            raise Exception("\n\n      See You soon, fork it share it !")



 

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """
        Manage Scrolling
        :param panning_fraction: Number from 0 to 1. Higher the number, faster we
                                 pan the camera to the user.
        """

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)



    @property
    def distance_crosshair_player(self):

        dist = math.hypot(self.crosshair_sprite.center_x - self.player_sprite.center_x, self.crosshair_sprite.center_y - self.player_sprite.center_y)

        return dist

    
    def manage_crosshair(self):

        #if self.distance_crosshair_player > SCREEN_HEIGHT / 2:
        if self.distance_crosshair_player > SCREEN_WIDTH:

            self.crosshair_sprite.center_x = self.player_sprite.center_x
            self.crosshair_sprite.center_y = self.player_sprite.center_y



    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves. """

        print(x)
        print(y)
        print(delta_x)
        print(delta_y)


        #self.manage_crosshair()
        
        

        #self.crosshair_sprite.center_x += delta_x
        #self.crosshair_sprite.center_y += delta_y


        self.crosshair_relative_xoffset += delta_x
        self.crosshair_relative_yoffset += delta_y



    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        print(button)
        print(type(button))
        print(modifiers)

        if button == LEFT_MOUSE_BTN and self.ammo > 0:

            # Create a bullet
            bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", SPRITE_SCALING_LASER)

            # Position the bullet at the player's current location
            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            bullet.center_x = start_x
            bullet.center_y = start_y

            # Get from the mouse the destination location for the bullet
            # IMPORTANT! If you have a scrolling screen, you will also need
            # to add in self.view_bottom and self.view_left.
            

            dest_x = self.crosshair_sprite.center_x
            dest_y = self.crosshair_sprite.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Angle the bullet sprite so it doesn't look like it is flying
            # sideways.
            bullet.angle = math.degrees(angle)
            print(f"Bullet angle: {bullet.angle:.2f}")

            # Taking into account the angle, calculate our change_x
            # and change_y. Velocity is how fast the bullet travels.
            bullet.change_x = math.cos(angle) * BULLET_SPEED
            bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the appropriate lists
            
            self.police_bullet_list.append(bullet)

            self.ammo -= 1


        if button == RIGHT_MOUSE_BTN and self.grenade > 0:


            grenade = arcade.Sprite("./resources/images/items/grenade_128_128.png", 0.4)

            start_x = self.player_sprite.center_x
            start_y = self.player_sprite.center_y
            grenade.center_x = start_x
            grenade.center_y = start_y


            dest_x = self.crosshair_sprite.center_x
            dest_y = self.crosshair_sprite.center_y
   
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)


            grenade.angle = math.degrees(angle)
            print(f"grenade angle: {grenade.angle:.2f}")


            grenade.change_x = math.cos(angle) * GRENADE_SPEED
            grenade.change_y = math.sin(angle) * GRENADE_SPEED


            self.police_grenade_list.append(grenade)

            self.grenade -= 1




    


    def update(self, delta_time):
    
        """ Movement and game logic """

        scene_dico = self.scene.__dict__

        print("\n\n *******")

        for k, v in scene_dico.items():
            print(k,"     ",v)
            print("------------")
        

        #self.scene[sprite_lists].update()

        print(type(self.scene))
        #self.scene.sprite_lists.update()

        for spl in self.scene.sprite_lists:
            spl.update()

        

        self.frame_count += 1
        self.player_list.update()

        for i in range (self.lives):
            


            self.life_list[i].center_x = (self.player_sprite.center_x - SCREEN_WIDTH // 2) + i * self.life_list[i].width
            self.life_list[i].center_y = (self.player_sprite.center_y - SCREEN_HEIGHT // 2) 


        self.crosshair_sprite.center_x = self.player_sprite.center_x + self.crosshair_relative_xoffset
        self.crosshair_sprite.center_y = self.player_sprite.center_y + self.crosshair_relative_yoffset

        



        

        

        self.enemy_list.update()
        

        # Move the player with the physics engine
        #self.physics_engine_walls.update()
        #self.stairs_list.update()



   





        #for medikit in ammo_medikit_hit_list:
        #    medikit.remove_from_sprite_lists()
            
        #    self.player_sprite.cur_health += MEDIKIT_HEALTH_BOOST





        # Generate a list of all sprites that collided with the player.
        #stairs_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
        #                                                      self.stairs_list)

        #for stairs in stairs_hit_list:
        #    self.level += 1
        #    self.is_smoked = False
            # Load the next level
        #    self.setup(self.level) #  .............?????????.........

            # Set the camera to the start
        #    self.view_left = 0
        #    self.view_bottom = 0
        #    changed_viewport = True



        


        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            
            start_x = enemy.center_x
            start_y = enemy.center_y

            
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y
            
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)-90

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")                
                
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                #self.bullet_list.append(bullet) -------------------------
                self.terro_bullet_list.append(bullet)


            



        # --- Manage Scrolling ---

        # Scroll left

        """
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

        """


        if self.player_sprite.right >= self.end_of_map:
            if self.level < self.max_level:
                self.level += 1
                self.load_level(self.level)
                self.player_sprite.center_x = 128
                self.player_sprite.center_y = 64
                self.player_sprite.change_x = 0
                self.player_sprite.change_y = 0
            else:
                self.game_over = True




        self.pan_camera_to_user()


    

    def center_on_player(self):
        w_width, w_height = self.window.get_size()
        arcade.set_viewport(
        self.player_sprite.center_x - w_width // 2,
        self.player_sprite.center_x + w_width // 2,
        self.player_sprite.center_y - w_height // 2,
        self.player_sprite.center_y + w_height // 2,
    )



    def go_to_gameover_view(self):

        view = GameOverView()
        self.window.show_view(view)



def main():

    #window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)

    

    #start_view = GameView()
    #window.show_view(start_view)
    
    #start_view.setup()
    #start_view.setup(level=1)

    start_view = InstructionView()
    window.show_view(start_view)

    
    arcade.run()


if __name__ == "__main__":
    main()
