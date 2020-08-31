#!/usr/bin/env python3

#####################################################################
# This script presents how to use the most basic features of the environment.
# It configures the engine, and makes the agent perform random actions.
# It also gets current state and reward earned with the action.
# <episodes> number of episodes are played. 
# Random combination of buttons is chosen for every action.
# Game variables from state and last reward are printed.
#
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from __future__ import print_function
import vizdoom as vzd

from random import choice
from time import sleep
import numpy as np
from argparse import ArgumentParser
import cv2

import csv
import datetime
import os

DEFAULT_CONFIG = "../../scenarios/basic.cfg"
if __name__ == "__main__":
    parser = ArgumentParser("ViZDoom example showing how to use labels and labels buffer.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")
    # Create DoomGame instance. It will run the game and communicate with you.
    game = vzd.DoomGame()

    args = parser.parse_args()

    # Now it's time for configuration!
    # load_config could be used to load configuration instead of doing it here with code.
    # If load_config is used in-code configuration will also work - most recent changes will add to previous ones.
    game.load_config(args.config)
    game.set_render_hud(False)

    # Sets path to additional resources wad file which is basically your scenario wad.
    # If not specified default maps will be used and it's pretty much useless... unless you want to play good old Doom.
    game.set_doom_scenario_path("../../scenarios/basic.wad")

    # Sets map to start (scenario .wad files can contain many maps).
    game.set_doom_map("map01")

    # Sets resolution. Default is 320X240
    game.set_screen_resolution(vzd.ScreenResolution.RES_1280X720)

    # Sets the screen buffer format. Not used here but now you can change it. Default is CRCGCB.
    game.set_screen_format(vzd.ScreenFormat.RGB24)

    # Enables depth buffer.
    game.set_depth_buffer_enabled(True)

    # Enables labeling of in game objects labeling.
    game.set_labels_buffer_enabled(True)

    game.clear_available_game_variables()
    game.add_available_game_variable(vzd.GameVariable.POSITION_X)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Z)

    # Enables buffer with top down map of the current episode/level.
    game.set_automap_buffer_enabled(True)

    # Enables information about all objects present in the current episode/level.
    game.set_objects_info_enabled(True)

    # Enables information about all sectors (map layout).
    game.set_sectors_info_enabled(True)

    # Sets other rendering options (all of these options except crosshair are enabled (set to True) by default)
    game.set_render_hud(False)
    game.set_render_minimal_hud(False)  # If hud is enabled
    game.set_render_crosshair(False)
    game.set_render_weapon(True)
    game.set_render_decals(False)  # Bullet holes and blood on the walls
    game.set_render_particles(False)
    game.set_render_effects_sprites(False)  # Smoke and blood
    game.set_render_messages(False)  # In-game messages
    game.set_render_corpses(False)
    game.set_render_screen_flashes(True)  # Effect upon taking damage or picking up items

    # Adds buttons that will be allowed.
    game.add_available_button(vzd.Button.MOVE_LEFT)
    game.add_available_button(vzd.Button.MOVE_RIGHT)
    game.add_available_button(vzd.Button.ATTACK)
    #game.add_available_button(vzd.Button.MOVE_BACKWARD)
    #game.add_available_button(vzd.Button.MOVE_FORWARD)
    #game.add_available_button(vzd.Button.TURN_RIGHT)
    #game.add_available_button(vzd.Button.TURN_LEFT)
    #game.add_available_button(vzd.Button.)

    # Adds game variables that will be included in state.
    game.add_available_game_variable(vzd.GameVariable.AMMO2)

    # Causes episodes to finish after 200 tics (actions)
    game.set_episode_timeout(200)

    # Makes episodes start after 10 tics (~after raising the pweapon)
    game.set_episode_start_time(10)

    # Makes the window appear (turned on by default)
    game.set_window_visible(True)

    # Turns on the sound. (turned off by default)
    game.set_sound_enabled(True)

    # Sets the living reward (for each move) to -1
    game.set_living_reward(-1)

    # Sets ViZDoom mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR, PLAYER mode is default)
    game.set_mode(vzd.Mode.PLAYER)
    # game.set_mode(vzd.Mode.SPECTATOR)

    # Enables engine output to console.
    #game.set_console_enabled(True)

    # Initialize the game. Further configuration won't take any effect from now on.
    game.init()

    # Define some actions. Each list entry corresponds to declared buttons:
    # MOVE_LEFT, MOVE_RIGHT, ATTACK
    # game.get_available_buttons_size() can be used to check the number of available buttons.
    # 5 more combinations are naturally possible but only 3 are included for transparency when watching.
    #actions = [[True, False, False, False, False, False, False], [False, True, False, False, False, False, False], [False, False, True, False, False, False, False], [False, False, False, True, False, False, False], [False, False, False, False, True, False, False], [False, False, False, False, False, True, False], [False, False, False, False, False, False, True]]
    actions = [[True, False, False], [False, True, False], [False, False, True]]

    # Run this many episodes
    episodes = 10

    # Sets time that will pause the engine after each action (in seconds)
    # Without this everything would go too fast for you to keep track of what's happening.
    sleep_time = 1.0 / vzd.DEFAULT_TICRATE  # = 0.028

    now = datetime.datetime.now()
    f = open('./log/log_{0:%Y%m%d_%H%M}'.format(now) + '.csv', 'w')
    writer = csv.writer(f, lineterminator = '\n')

    for i in range(episodes):
        print("Episode #" + str(i + 1))
        seen_in_this_episode = set()

        # Starts a new episode. It is not needed right after init() but it doesn't cost much. At least the loop is nicer.
        game.new_episode()

        while not game.is_episode_finished():

            # Gets the state
            state = game.get_state()

            # Which consists of:
            n = state.number
            #writer.writerow([n])
            vars = state.game_variables
            #writer.writerow([vars])
            #screen_buf = state.screen_buffer
            screen = state.screen_buffer
            #writer.writerow([screen])
            depth_buf = state.depth_buffer
            #writer.writerow([depth_buf])
            labels_buf = state.labels_buffer
            #writer.writerow([labels_buf])
            automap_buf = state.automap_buffer
            #writer.writerow([automap_buf])
            labels = state.labels
            #writer.writerow([labels])
            objects = state.objects
            #writer.writerow([objects])
            sectors = state.sectors
            #writer.writerow([sectors])

            # Games variables can be also accessed via:
            #game.get_game_variable(GameVariable.AMMO2)

            # Makes a random action and get remember reward.
            r = game.make_action(choice(actions))

            # Makes a "prolonged" action and skip frames:
            # skiprate = 4
            # r = game.make_action(choice(actions), skiprate)

            # The same could be achieved with:
            # game.set_action(choice(actions))
            # game.advance_action(skiprate)
            # r = game.get_last_reward()

            # Prints state's game variables and reward.
            print("State #" + str(state.number))
            #writer.writerow(["State #" + str(state.number)])
            print("Player position: x:", state.game_variables[0], ", y:", state.game_variables[1], ", z:", state.game_variables[2])
            #writer.writerow([state.game_variables[0], state.game_variables[1], state.game_variables[2]])
            last_action = game.get_last_action()
            print("Action:", last_action)
            writer.writerow(last_action)
            print("Labels:")

            # Print information about objects visible on the screen.
            # object_id identifies specific in game object.
            # object_name contains name of object.
            # value tells which value represents object in labels_buffer.
            for l in state.labels:
                seen_in_this_episode.add(l.object_name)
                # print("---------------------")
                print("Label:", l.value, ", object id:", l.object_id, ", object name:", l.object_name)
                #writer.writerow([l.value, l.object_id, l.object_name])
                print("Object position: x:", l.object_position_x, ", y:", l.object_position_y, ", z:", l.object_position_z)
                #writer.writerow([l.object_position_x, l.object_position_y, l.object_position_z])

                # Other available fields:
                print("Object rotation angle", l.object_angle, "pitch:", l.object_pitch, "roll:", l.object_roll)
                #writer.writerow([l.object_angle, l.object_pitch, l.object_roll])
                print("Object velocity x:", l.object_velocity_x, "y:", l.object_velocity_y, "z:", l.object_velocity_z)
                #writer.writerow([l.object_velocity_x, l.object_velocity_y, l.object_velocity_z])
                #print("Bounding box: x:", l.x, ", y:", l.y, ", width:", l.width, ", height:", l.height)

            print("=====================")
            print("Reward:", r)
            #writer.writerow([r])
            print("=====================")

            if sleep_time > 0:
                sleep(sleep_time)

        # Check how the episode went.
        print("Episode finished.")
        writer.writerow(["Episode finished."])
        print("Total reward:", game.get_total_reward())
        #writer.writerow([game.get_total_reward()])
        print("************************")

    # It will be done automatically anyway but sometimes you need to do it in the middle of the program...
    game.close()
