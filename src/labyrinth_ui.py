#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

# library imports
import pygame
import pygame.locals
import random

# imports from this project
import labyrinth_config
import labyrinth_text
import liblog

# ==============================================================================
# labyrinth_ui.UI
# ==============================================================================
class UI(object):

    def __init__(self, audio):
        self.audio = audio
        pygame.init()
        icon = pygame.image.load('data/graphics/window_icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Audio-Labyrinth')
        self.screen = pygame.display.set_mode(labyrinth_config.displaysize)
        self.rooms = None
        self.txtsurf = None
        
        self.audio.start_music('data/audio/effects/cave.wav')


    def get_next_event(self):

        pygame.time.wait(50)
        
        self.audio.do_play()

        # get next pygame event in queue
        event = pygame.event.poll()

        if event.type == pygame.locals.QUIT:
            return 'terminate'

        if event.type == pygame.locals.KEYDOWN:

            # log key press
            keyname = pygame.key.name(event.key)
            liblog.log('key pressed: {}'.format(keyname))

            # any key press stops audio
            self.audio.stop_playback()
            self.audio.clear_queue()

            # arrow keys for moving through the labyrinth
            if event.key == pygame.locals.K_LEFT:
                return 'left'
            if event.key == pygame.locals.K_RIGHT:
                return 'right'
            if event.key == pygame.locals.K_UP:
                return 'forward'
            if event.key == pygame.locals.K_DOWN:
                return 'back'

            # space bar for repeating current position and options
            if event.key == pygame.locals.K_SPACE:
                self.tell_position(self.last_curpos)
                self.tell_options(self.last_options)
                return ''

            # escape for terminating
            if event.key == pygame.locals.K_ESCAPE:
                return 'terminate'

            # F2 and F3 to change speaking rate
            if event.key == pygame.locals.K_F2:
                self.audio.change_speed('faster', labyrinth_text.speed_changed)
                return ''
            if event.key == pygame.locals.K_F3:
                self.audio.change_speed('slower', labyrinth_text.speed_changed)
                return ''

            # F4 for aborting current labyrinth
            if event.key == pygame.locals.K_F4:
                self.audio.synthesize_and_play(labyrinth_text.abort)
                liblog.log('labyrinth aborted')
                return 'pre_game'

            # F1 for help
            if event.key == pygame.locals.K_F1:
                self.help()
                return ''


            # invalid key, play short sound
            self.audio.clear_queue()
            self.audio.priority_play('data/audio/effects/blop.wav')

        return ''



    def choose_size(self):
        """
        After interaction with the player, this method will return the
        selected labyrinth size. This method uses its own UI loop.
        """

        pygame.time.wait(500)
        toplay_orig = [
            labyrinth_text.choose_size_begin,
            labyrinth_text.choose_size.format(
                labyrinth_text.sizes['small'][0],
                labyrinth_text.sizes['small'][1],
                labyrinth_config.size['small']
            ),
            labyrinth_text.choose_size.format(
                labyrinth_text.sizes['medium'][0],
                labyrinth_text.sizes['medium'][1],
                labyrinth_config.size['medium']
            ),
            labyrinth_text.choose_size.format(
                labyrinth_text.sizes['large'][0],
                labyrinth_text.sizes['large'][1],
                labyrinth_config.size['large']
            ),
            labyrinth_text.choose_size.format(
                labyrinth_text.sizes['huge'][0],
                labyrinth_text.sizes['huge'][1],
                labyrinth_config.size['huge']
            ),
        ]
        toplay = toplay_orig[:]

        while True:
            self.audio.do_play()

            # get next pygame event in queue
            event = pygame.event.poll()

            if len(toplay) > 0:
                self.audio.synthesize_and_play(toplay.pop(0))

            if event.type == pygame.locals.QUIT:
                return 'terminate'
        
            if event.type == pygame.locals.KEYDOWN:
                # log key press
                keyname = pygame.key.name(event.key)
                liblog.log('key pressed: {}'.format(keyname))
                
                # any key press stops audio
                self.audio.stop_playback()
                self.audio.clear_queue()
                
                # arrow keys to select size
                if event.key == pygame.locals.K_LEFT:
                    self.audio.synthesize_and_play(
                        labyrinth_text.selected_size.format(
                                labyrinth_text.sizes['small'][1]))
                    return 'small'
                if event.key == pygame.locals.K_UP:
                    self.audio.synthesize_and_play(
                        labyrinth_text.selected_size.format(
                                labyrinth_text.sizes['medium'][1]))
                    return 'medium'
                if event.key == pygame.locals.K_RIGHT:
                    self.audio.synthesize_and_play(
                        labyrinth_text.selected_size.format(
                                labyrinth_text.sizes['large'][1]))
                    return 'large'
                if event.key == pygame.locals.K_DOWN:
                    self.audio.synthesize_and_play(
                        labyrinth_text.selected_size.format(
                                labyrinth_text.sizes['huge'][1]))
                    return 'huge'

                # space bar to repeat options
                if event.key == pygame.locals.K_SPACE:
                    toplay = toplay_orig[:]
                
                # escape to terminate
                if event.key == pygame.locals.K_ESCAPE:
                    return 'terminate'

                # F2 and F3 to change speaking rate
                if event.key == pygame.locals.K_F2:
                    self.audio.change_speed('slower', labyrinth_text.speed_changed)
                    continue
                if event.key == pygame.locals.K_F3:
                    self.audio.change_speed('faster', labyrinth_text.speed_changed)
                    continue

                # F1 for help
                if event.key == pygame.locals.K_F1:
                    self.help()
                    continue


    def play_again(self):
        """
        After completing one game, asks the player if she wants to play again.
        If yes, go to choose size. If no, terminate.
        Like choose_size, this uses its own UI loop
        """
        
        toplay_orig = [
            labyrinth_text.left_play_again,
            labyrinth_text.right_play_same_again,
            labyrinth_text.escape_terminate
        ]
        toplay = toplay_orig[:]
        
        while True:
            self.audio.do_play()

            if len(toplay) > 0:
                self.audio.synthesize_and_play(toplay.pop(0))

            # get next pygame event in queue
            event = pygame.event.poll()

            if event.type == pygame.locals.QUIT:
                return 'terminate'
        
            if event.type == pygame.locals.KEYDOWN:
                # log key press
                keyname = pygame.key.name(event.key)
                liblog.log('key pressed: {}'.format(keyname))
                
                # any key press stops audio
                self.audio.stop_playback()
                self.audio.clear_queue()
                
                # arrow keys to select new game, same game or quit
                if event.key == pygame.locals.K_LEFT:
                    return 'new'
                if event.key == pygame.locals.K_RIGHT:
                    liblog.log('restarting same labyrinth')
                    return 'same'

                # space bar to repeat options
                if event.key == pygame.locals.K_SPACE:
                    toplay = toplay_orig[:]
                    continue
                
                # escape to terminate
                if event.key == pygame.locals.K_ESCAPE:
                    return 'terminate'

                # F2 and F3 to change speaking rate
                if event.key == pygame.locals.K_F2:
                    self.audio.change_speed('slower', labyrinth_text.speed_changed)
                    continue
                if event.key == pygame.locals.K_F3:
                    self.audio.change_speed('faster', labyrinth_text.speed_changed)
                    continue

                # F1 for help
                if event.key == pygame.locals.K_F1:
                    self.help()
                    continue
                    
                # unknown key    
                self.audio.play_sound_file('data/audio/effects/blop.wav')



    def welcome(self):
        #print labyrinth_text.welcome
        self.audio.play_sound_file('data/audio/effects/gong.wav')
        #~ self.audio.play_sound_file(self.sounds_welcome)
        self.audio.synthesize_and_play(labyrinth_text.welcome)
        #~ self.help()


    def tell_position(self, curpos):
        """Given a room index (curpos), tells the player her position."""
        
        # store, in case we need to repeat
        self.last_curpos = curpos

        # fetch room strings
        room_name, room_loc, room_dir = self.rooms[curpos]
        
        # build utterance text
        txt = labyrinth_text.youare.format(room_loc, room_name)

        #~ print '-' * 70
        #~ print txt
        
        #self.audio.play_presynthesized(curpos * 5)
        #~ self.audio.play_sound_file(self.sounds_location[curpos])
        self.audio.synthesize_and_play(txt)


    def tell_options(self, options):
        """
        Given a dictionary containing the possible next moves (as returned by
        the get_options function in labyrinth_logic), tell them to the player. 
        """

        # store, in case we need to repeat
        self.last_options = options

        i = 0
        for d in ('left', 'forward', 'right', 'back'):
            i += 1
            if d in options:
                d_string = labyrinth_text.directions[d]
                nextpos = options[d]
                room_name, room_loc, room_dir = self.rooms[nextpos]

                if d == 'back':
                    # dead ens are special
                    if len(options) == 1:
                        txt = labyrinth_text.deadend
                    else:
                        txt = labyrinth_text.youcangoback
                else:
                    txt = labyrinth_text.youcango

                txt = txt.format(d_string, room_dir, room_name)
                #~ print txt
                
                #self.audio.play_presynthesized(nextpos * 5 + i)
                #~ self.audio.play_sound_file(self.sounds_direction[nextpos][d])
                self.audio.synthesize_and_play(txt)


    def tell_goal(self, numsteps):
        #print labyrinth_text.goal
        #~ self.audio.play_sound_file(self.sounds_goal)
        self.audio.synthesize_and_play(labyrinth_text.goal.format(numsteps))
        self.audio.play_sound_file('data/audio/effects/tada.wav')

    def walk(self):
        self.audio.play_sound_file('data/audio/effects/steps.wav')


    def invalid(self):
        self.audio.priority_play('data/audio/effects/blop.wav')


    #~ def presynthesize_utterances(self, outpath):
        #~ utts = []
        #~ for room_name, room_loc, room_dir in self.rooms[0:self.labyrinth_size]:
        #~ for room_name, room_loc, room_dir in self.rooms:
            #~ 
            #~ # "you are now in x" strings
            #~ txt = labyrinth_text.youare.format(room_loc, room_name)
            #~ utts.append(txt)
            #~ 
            #~ # "if you go y, you get to z" strings
            #~ for d in ('left', 'forward', 'right', 'back'):
                #~ if d == 'back':
                    #~ txt = labyrinth_text.youcangoback
                #~ else:
                    #~ txt = labyrinth_text.youcango
                #~ 
                #~ d_string = labyrinth_text.directions[d]
#~ 
                #~ txt = txt.format(d_string, room_dir, room_name)
                #~ utts.append(txt)
        #~ 
        #~ # welcome string
        #~ utts.append(labyrinth_text.welcome)
        #~ 
        #~ # goal reached string
        #~ utts.append(labyrinth_text.goal)
#~ 
        #~ # synthesize them
        #~ soundfiles = self.audio.pre_synthesize(utts, outpath)
#~ 
        #~ # store the soundfiles appropriately
        #~ self.sounds_location = []
        #~ self.sounds_direction = []
        #~ 
        #~ for i in range(len(self.rooms)):
            #~ self.sounds_location.append(soundfiles.pop(0))
            #~ self.sounds_direction.append({
                #~ 'left' : soundfiles.pop(0),
                #~ 'forward' : soundfiles.pop(0),
                #~ 'right' : soundfiles.pop(0),
                #~ 'back' : soundfiles.pop(0),
            #~ })
        #~ self.sounds_welcome = soundfiles.pop(0)
        #~ self.sounds_goal = soundfiles.pop(0)
            

    def shuffle_rooms(self):
        self.rooms = labyrinth_text.rooms[:]
        random.shuffle(self.rooms)
        #~ indices = random.sample(range(len(self.rooms)), size)
        #~ self.sounds_location = [ self.sounds_location[i] for i in indices ]
        #~ self.sounds_direction = [ self.sounds_direction[i] for i in indices ]


    def update_display(self):
        if self.txtsurf is None:
            col = pygame.Color(255,255,255)
            f = pygame.font.Font('data/graphics/DroidSans.ttf', 32)
            #f = pygame.font.Font(pygame.font.get_default_font(), 32)
            self.txtsurf = f.render('Audio-Labyrinth', True, col)
        
        w, h = self.txtsurf.get_size()
        x = (pygame.display.Info().current_w - w) / 2 
        y = (pygame.display.Info().current_h - h) / 2
        self.screen.blit(self.txtsurf, (x, y))
        pygame.display.update()


    def help(self):
        for utt in labyrinth_text.help_utts:
            self.audio.synthesize_and_play(utt)
