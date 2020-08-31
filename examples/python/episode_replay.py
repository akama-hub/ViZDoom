#!/usr/bin/env python3

#####################################################################
# This script presents how to use Doom's native demo mechanism to
# replay episodes with perfect accuracy.
#####################################################################

from __future__ import print_function

import os
from random import choice
from vizdoom import *

game = DoomGame()

# Use other config file if you wish.
game.load_config("../scenarios/basic.cfg")
game.set_episode_timeout(100)

# Record episodes while playing in 320x240 resolution without HUD
game.set_screen_resolution(ScreenResolution.RES_800X600)
game.set_render_hud(True)

# Episodes can be recorder in any available mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR)
game.set_mode(Mode.SPECTATOR)

game.init()

actions = [[True, False, False], [False, True, False], [False, False, True]]

# Replay can be played in any mode.

print("\nREPLAY OF EPISODE")
print("************************\n")

episodes = 5

for i in range(episodes):

    # Replays episodes stored in given file. Sending game command will interrupt playback.
    game.replay_episode("./recorded_episodes/episode" + str(i) + "_rec.lmp")

    while not game.is_episode_finished():
        s = game.get_state()

        # Use advance_action instead of make_action.
        game.advance_action()

        r = game.get_last_reward()
        # game.get_last_action is not episodes = 5supported and don't work for replay at the moment.

game.close()