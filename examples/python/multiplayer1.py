#!/usr/bin/env python3

#####################################################################
# This script presents how to join and play a deathmatch game,
# that can be hosted using cig_multiplayer_host.py script.
#####################################################################

from __future__ import print_function

from vizdoom import *
import sys

from argparse import ArgumentParser
from time import sleep


DEFAULT_CONFIG = "../../scenarios/deathmatch.cfg"

if __name__ == "__main__":
    parser = ArgumentParser("ViZDoom example showing how to use SPECTATOR mode.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")
    
    args = parser.parse_args()
    game = DoomGame()

    # Use CIG example config or your own.
    game.load_config("../../scenarios/deathmatch.cfg")

    game.set_screen_resolution(vizdoom.ScreenResolution.RES_1280X720)

    game.set_doom_map("map01")  # Limited deathmatch.
    #game.set_doom_map("map02")  # Full deathmatch.

    # Join existing game.
    #game.add_game_args("-join 192.168.11.200") # Connect to a host for a multiplayer game.
    game.add_game_args("-netmode 0 "
                        "-host 2 "
                        "-nomonsters"        )


    # Name your agent and select color
    # colors: 0 - green, 1 - gray, 2 - brown, 3 - red, 4 - light gray, 5 - light brown, 6 - light red, 7 - light blue
    game.add_game_args("+name AI +colorset 0")

    # During the competition, async mode will be forced for all agents.
    game.set_window_visible(True)
    game.set_mode(Mode.SPECTATOR)
    #game.set_mode(Mode.ASYNC_PLAYER)

    #game.set_window_visible(False)

    game.init()

    # Get player's number
    player_number = int(game.get_game_variable(GameVariable.PLAYER_NUMBER))
    last_frags = 0

    # Play until the game (episode) is over.
    while not game.is_episode_finished():

        # Get the state.
        s = game.get_state()

        # Analyze the state.

        # Make your action.
        game.advance_action()
        last_action = game.get_last_action()
        reward = game.get_last_reward()
        frags = game.get_game_variable(GameVariable.FRAGCOUNT)

        if frags != last_frags:
            last_frags = frags
            print("Player " + str(player_number) + " has " + str(frags) + " frags.")

        # Check if player is dead
        if game.is_player_dead():
            print("Player " + str(player_number) + " died.")
            # Use this to respawn immediately after death, new state will be available.
            game.respawn_player()

    game.close()
