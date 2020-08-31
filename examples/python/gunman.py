#!/usr/bin/env python3

from __future__ import print_function

from random import choice
import vizdoom as vzd
import numpy as np
from argparse import ArgumentParser

import cv2

DEFAULT_CONFIG = "../scenarios/basic.cfg"
if __name__ =="__main__":
    parser = ArgumentParser("ViZDoom example showing how to use labels and labels buffer.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../scenarios/*cfg for more scenarios.")

    args = parser.parse_args()

    game = vzd.DoomGame()

    # Use other config file if you wish.
    game.load_config(args.config)
    game.set_render_hud(False)

    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)

    # Set cv2 friendly format.
    game.set_screen_format(vzd.ScreenFormat.BGR24)

    # Enables labeling of the in game objects.
    game.set_labels_buffer_enabled(True)

    game.clear_available_game_variables()
    game.add_available_game_variable(vzd.GameVariable.POSITION_X)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Z)

    game.init()

    actions = [[True, False, False], [False, True, False], [False, False, True]]

    episodes = 30

    # Sleep time between actions in ms
    sleep_time = 28


    # Prepare some colors and drawing function
    # Colors in in BGR order
    doom_red_color = [0, 0, 203]
    doom_blue_color = [203, 0, 0]

    def draw_bounding_box(buffer, x, y, width, height, color):
        for i in range(width):
            buffer[y, x + i, :] = color
            buffer[y + height, x + i, :] = color

        for i in range(height):
            buffer[y + i, x, :] = color
            buffer[y + i, x + width, :] = color

    def get_centerx(x, w):
        return (x+w/2)

    def get_dx(cx): # distance from center
        return (320 - cx)

    def get_action(dx):
        if abs(dx)<20:
            return actions[2] #shoot
        if dx<0:
            return actions[1] #right
        return actions[0] #left

    def color_labels(labels):
        """
        Walls are blue, floor/ceiling are red (OpenCV uses BGR).
        """
        tmp = np.stack([labels] * 3, -1)
        tmp[labels == 0] = [255, 0, 0]
        tmp[labels == 1] = [0, 0, 255]
        return tmp

    for i in range(episodes):
        print("Episode #" + str(i + 1))
        seen_in_this_episode = set()

        game.new_episode()
        while not game.is_episode_finished():
            state = game.get_state()
            screen = state.screen_buffer
            for l in state.labels:
                if l.object_name in ["Medikit", "GreenArmor"]:
                    draw_bounding_box(screen, l.x, l.y, l.width, l.height, doom_blue_color)
                else:
                    draw_bounding_box(screen, l.x, l.y, l.width, l.height, doom_red_color)
            cv2.imshow('ViZDoom Screen Buffer', screen)

            cv2.waitKey(sleep_time)

            #game.make_action(choice(actions))

            print("State #" + str(state.number))
            print("Player position: x:", state.game_variables[0], ", y:", state.game_variables[1], ", z:", state.game_variables[2])
            print("Labels:")

            # Print information about objects visible on the screen.
            # object_id identifies specific in game object.
            # object_name contains name of object.
            # value tells which value represents object in labels_buffer.
            for l in state.labels:
                seen_in_this_episode.add(l.object_name)
                # print("---------------------")
                print("Label:", l.value, ", object id:", l.object_id, ", object name:", l.object_name)
                print("Object position: x:", l.object_position_x, ", y:", l.object_position_y, ", z:", l.object_position_z)

                # Other available fields:
                #print("Object rotation angle", l.object_angle, "pitch:", l.object_pitch, "roll:", l.object_roll)
                #print("Object velocity x:", l.object_velocity_x, "y:", l.object_velocity_y, "z:", l.object_velocity_z)
                print("Bounding box: x:", l.x, ", y:", l.y, ", width:", l.width, ", height:", l.height)
                cx = get_centerx(l.x, l.width)
                dx = get_dx(cx)
                print("Center position: x:", cx)
                print("dx: ", dx)
                if l.object_id == 0:
                    dx = get_dx(cx)
                    game.make_action(get_action(dx))


            print("=====================")

        print("Episode finished!")

        print("=====================")

        print("Seen in this episode:")
        for l in seen_in_this_episode:
            print(l)

        print("************************")

    cv2.destroyAllWindows()