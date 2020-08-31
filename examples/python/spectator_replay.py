#!/usr/bin/env python3

#####################################################################
# This script presents SPECTATOR mode. In SPECTATOR mode you play and
# your agent can learn from it.
# Configuration is loaded from "../../scenarios/<SCENARIO_NAME>.cfg" file.
# 
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from __future__ import print_function

from time import sleep
import vizdoom as vzd
from argparse import ArgumentParser
import csv

DEFAULT_CONFIG = "../scenarios/deathmatch.cfg"

if __name__ == "__main__":
    parser = ArgumentParser("ViZDoom example showing how to use SPECTATOR mode.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")
    args = parser.parse_args()
    game = vzd.DoomGame()

    # Choose scenario config file you wish to watch.
    # Don't load two configs cause the second will overrite the first one.
    # Multiple config files are ok but combining these ones doesn't make much sense.

    game.load_config(args.config)

    # Enables freelook in engine
    game.add_game_args("+freelook 1")
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)

    game.add_available_button(vzd.Button.MOVE_LEFT)
    game.add_available_button(vzd.Button.MOVE_RIGHT)
    game.add_available_button(vzd.Button.ATTACK)

    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    game.set_mode(vzd.Mode.PLAYER)

    game.add_game_args("+vid_forcesurface 1")

    game.init()

    episodes = 10

    for i in range(episodes):
        #print("Episode #" + str(i + 1))
        with open("./log.csv") as f:
            actions = []
            for action in csv.reader(f, quoting=csv.QUOTE_NONNUMERIC):
                actions.append(action)
        game.new_episode()
        j=0
        while not game.is_episode_finished():
            state = game.get_state()
            game.make_action(actions[j],1)
            if j < len(actions)-1:
                j=j+1
            else:
                j=0
        sleep(2.0)

    game.close()
