#!/usr/bin/env python3

#####################################################################
# This script presents how to use Doom's native demo mechanism to
# replay episodes with perfect accuracy.
#####################################################################

from __future__ import print_function

import os
from random import choice
from vizdoom import *
import time

game = DoomGame()

# Use other config file if you wish.
game.load_config("../scenarios/basic.cfg")
game.set_episode_timeout(100)

# Record episodes while playing in 320x240 resolution without HUD
game.set_screen_resolution(ScreenResolution.RES_320X240)
game.set_render_hud(False)

# Episodes can be recorder in any available mode (PLAYER, ASYNC_PLAYER, SPECTATOR, ASYNC_SPECTATOR)
game.set_mode(Mode.PLAYER)

game.init()

actions = [[True, False, False], [False, True, False], [False, False, True]]

# Run and record this many episodes
episodes = 5

# Recording
print("\nRECORDING EPISODES")
print("************************\n")

for i in range(episodes):

    # new_episode can record the episode using Doom's demo recording functionality to given file.
    # Recorded episodes can be reconstructed with perfect accuracy using different rendering settings.
    # This can not be used to record episodes in multiplayer mode.
    game.new_episode("./recorded_episodes/episode" + str(i) + "_rec.lmp")

    while not game.is_episode_finished():
        s = game.get_state()
        r = game.make_action(choice(actions))

# 理由はわからないけど何故か最終エピソードが保存されないのでひとまず新規ゲームだけ作って終わってる
game.new_episode("./recorded_episodes/episodetmp_rec.lmp")

game.close()