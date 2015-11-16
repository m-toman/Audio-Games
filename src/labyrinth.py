#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

# library imports
import argparse
import pygame
import random
import sys

# imports from this project
import fix_unicode_on_windows
import labyrinth_config
import labyrinth_ui
import labyrinth_logic
import libaudio
import liblog

# ==============================================================================
# LayrinthGame
# ==============================================================================
class LabyrinthGame(object):

    def __init__(self, seed_indices, voice):

        # seed indices per labyrinth size
        self.seed_indices = {
            'small'  : seed_indices[0],
            'medium' : seed_indices[1],
            'large'  : seed_indices[2],
            'huge'   : seed_indices[3],
        }

        # set up logging
        liblog.init_logging('labyrinth')
        self.log_seed_vector()

        # create audio processing object
        self.audio = libaudio.Audio(voice, 'labyrinth')
        
        # create user interface object
        self.ui = labyrinth_ui.UI(self.audio)
        


    def init_game(self, size):
        """
        Initializes a new game of the specified size (number of rooms).
        """

        liblog.log('initializing new game ({})'.format(size))
        
        i = self.seed_indices[size]
        nextseed = labyrinth_config.seeds[size][i]
        random.seed(nextseed)
        liblog.log('seed number {} for {} size is {}'.format(i, size, nextseed))
        self.seed_indices[size] += 1
        
        # initialize game logic, including creation of a random labyrinth
        self.logic = labyrinth_logic.GameLogic(size)

        # assign random names to rooms for player interaction
        self.ui.shuffle_rooms()
        self.logic.rooms = self.ui.rooms

        liblog.log('game initialization complete')


    def run(self):
        self.ui.update_display()
        self.ui.welcome()
        self.ui.help()

        status = 'pre_game'

        while True:

            if status == 'pre_game':
                size = self.ui.choose_size()
                if size == 'terminate':
                    liblog.log('early termination during choose_size')
                    break

                self.init_game(size)
                status = self.logic.handle_event('begin')
                continue

            elif status == 'update':
                self.ui.walk()
                self.ui.tell_position(self.logic.curpos)
                self.ui.tell_options(self.logic.get_options())

            elif status == 'goal':
                self.ui.walk()
                self.ui.tell_position(self.logic.curpos)
                self.ui.tell_goal(self.logic.numsteps)
                self.log_seed_vector()
                again = self.ui.play_again()
                if again == 'new':
                    status = 'pre_game'
                    continue
                elif again == 'same':
                    status = self.logic.handle_event('begin')
                    continue
                elif again == 'terminate':
                    break

            elif status == 'invalid':
				self.ui.invalid()

            eventstring = self.ui.get_next_event()
            if eventstring == 'terminate':
                break
            elif eventstring == 'pre_game':
                status = eventstring
                continue
            else:
                status = self.logic.handle_event(eventstring)
        
        liblog.log('terminating')


    def log_seed_vector(self):
        liblog.log('-' * 54)
        msg = 'seed index vector (small,medium,large,huge) is '
        msg += '{},{},{},{}'.format(
            self.seed_indices['small'],
            self.seed_indices['medium'],
            self.seed_indices['large'],
            self.seed_indices['huge'],
        )
        liblog.log(msg)
        liblog.log('-' * 54)


# ==============================================================================
# main
# ==============================================================================
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seedvector', type=str, default='0,0,0,0')
    parser.add_argument('-v', '--voice', type=str, default='leo')
    args = parser.parse_args()
    
    sv = [ int(s) for s in args.seedvector.split(',') ]
    
    lg = LabyrinthGame(sv, args.voice)
    lg.run()
    
