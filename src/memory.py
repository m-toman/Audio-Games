#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Markus Toman (toman@ftw.at)
# July 2014

# library imports
import argparse
import pygame
import random
import sys

# imports from this project
import fix_unicode_on_windows
import memory_config
import memory_ui
import memory_text
import memory_logic
import libaudio
import liblog

# ==============================================================================
# MemoryGame
# ==============================================================================
class MemoryGame(object):

    def __init__(self, gamenum, voice):
        
        if gamenum is not None:
            self.gamenum = gamenum
        else:
            # try to load game
            self.load_game()
        
        print "Beginne mit " + str(self.gamenum)
        
        # set up logging
        liblog.init_logging('memory')
        
        liblog.log('game starting with game number {}'.format(self.gamenum))

        # create audio processing object
        self.audio = libaudio.Audio(voice, 'memory')

        # create user interface object
        self.ui = memory_ui.UI(self.audio)


    def init_theme(self, size):
        """ Select a random theme and size/2 things from this theme. """
        self.themeidx = random.randint(0, len(memory_text.memory_things)-1) #self.gamenum % len(memory_text.memory_things)        
        all_things = memory_text.memory_things[self.themeidx] 
        self.things = random.sample( all_things, size / 2 )


    def init_game(self, size):
        """
        Initializes a new game of the specified size.
        """

        liblog.log('initializing new game ({}) with number {}'.format(size, self.gamenum))
            
        nextseed = memory_config.seeds[self.gamenum]
        random.seed(nextseed)

        # initialize game logic, including creation of a random board
        self.logic = memory_logic.GameLogic(size)
        
        # now select game theme and random objects from theme for each board field
        self.init_theme(self.logic.board.size)
        self.ui.set_num_fields(self.logic.board.size)       
        self.logic.things = self.things 

        liblog.log('board = {}'.format(self.logic.board.fields))
        liblog.log('things = {}'.format(self.things))
        liblog.log('game initialization complete')
        
    def save_game(self):
        sg = open( 'data/savegame.txt', 'wt' )
        sg.write( str(self.gamenum) )
        sg.close()

    def load_game(self):
        try:
            sg = open( 'data/savegame.txt', 'rt' )
            self.gamenum = int(sg.readline())
            sg.close()
        except IOError:            
            self.gamenum = 0

    def choose_size(self):
        # we let the people choose their 9th game+
        #if self.gamenum < 5:
        #    size = 'small'
        #elif self.gamenum < 8:
        #    size = 'large'
        #else:
        size = self.ui.choose_size()
        return size

    def run(self):
        self.ui.update_display()
        self.ui.welcome()

        self.ui.tell_round(self.gamenum+1)
        size = self.choose_size()
        if size == 'terminate':
            liblog.log('early termination during choose_size')
            return

        self.init_game(size)                   
        self.ui.tell_size(size)        
        self.ui.tell_theme(self.themeidx)

        laststatus = status = self.logic.handle_event('begin')

        while not self.logic.terminate:
                        
            # user has to select field 1
            if status == 'select1':
                # tell user which field she selected as #2
                if self.logic.current_thing  is not None:
                    self.ui.tell_thing_selected( self.things[ self.logic.current_thing - 1 ] )
                # tell user if both fields matched
                if self.logic.last_correct  is not None:
                    self.ui.tell_correct( self.logic.last_correct )
                # tell user to selected a #1 field                
                self.ui.tell_select_field( 1 )
                
            # user has to select field 2
            elif status == 'select2':                
                # tell user the field #1 she selected
                if self.logic.current_thing is not None:
                    self.ui.tell_thing_selected( self.things[ self.logic.current_thing - 1 ] )
                # sell user to select field #2                
                self.ui.tell_select_field( 2 )
                
            elif status == 'wrongfield':
                self.ui.tell_wrongfield()
                                
            elif status == 'finished':
                self.ui.tell_thing_selected( self.things[ self.logic.current_thing - 1 ] )
                                
                # all games done?                
                #if self.gamenum == 7: self.ui.tell_goal_all8(self.logic.numsteps)
                self.ui.tell_goal(self.logic.numsteps)
                
                self.gamenum += 1
                self.save_game()
                self.ui.tell_round(self.gamenum+1)                
                size = self.choose_size()
                if size == 'terminate':
                    break
                else:                                        
                    self.init_game(size)          
                    self.ui.tell_size(size)
                    self.ui.tell_theme( self.themeidx )                    
                    status = self.logic.handle_event('begin')
                    pygame.event.clear()
                    continue

            eventstring = self.ui.get_next_event()
            # repeat last status
            if eventstring == 'repeat':    
                status = laststatus                            
                continue
            # don't allow quitting too early ;)
            #if eventstring == 'terminate' and self.gamenum < 8:
            #    eventstring = ''
            status = self.logic.handle_event(eventstring)
            # save last status message
            if status is not None and status is not "wrongfield": laststatus = status

        liblog.log('terminating')

# ==============================================================================
# main
# ==============================================================================
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--gamenum', type=str, default=None)
    parser.add_argument('-v', '--voice', type=str, default='leo')    
    args = parser.parse_args()

    if args.gamenum is None:
        sv = None
    else:
        sv = int(args.gamenum) #[ int(s) for s in args.seedvector.split(',') ]

    lg = MemoryGame(sv, args.voice)
    lg.run()


