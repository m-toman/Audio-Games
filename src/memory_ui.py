#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

# library imports
import pygame
import pygame.locals

# imports from this project
import memory_config
import memory_text
import liblog

# ==============================================================================
# memory_ui.UI
# ==============================================================================
class UI(object):

    def init_all_keys(self):
        self.field_keys = memory_config.field_keys
        

    def __init__(self, audio):
        self.lastkey = None
        self.lasttask = None
        self.lastthing = None
        self.lastcorr = None
                
        self.audio = audio
        pygame.init()
        icon = pygame.image.load('data/graphics/window_icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Audio-Memory')
        self.screen = pygame.display.set_mode(memory_config.displaysize)
        self.init_all_keys()        
        #~ self.presynthesize_utterances('audio/labyrinth')
        self.txtsurf = None        
        #self.audio.start_music('data/audio/effects/cave.wav')
        


    def set_num_fields(self, count):
        self.allowed_field_keys = self.field_keys[0:count] 

    def get_next_event(self):

        pygame.time.wait(10)
        
        self.audio.do_play()

        # get next pygame event in queue
        event = pygame.event.poll()

        if event.type == pygame.locals.QUIT:
            return 'hardterminate'

        if event.type == pygame.locals.KEYDOWN:

            # log key press
            keyname = pygame.key.name(event.key)
            if keyname == ';': keyname = '\xc3\xb6'
            liblog.log('key pressed: {}'.format(keyname))

            # any key press stops audio
            self.audio.stop_playback()
            self.audio.clear_queue()

            if event.key in self.allowed_field_keys:
                self.lastkey = keyname
                return 'field_' + str( self.allowed_field_keys.index(event.key) )
             
            # space bar for repeating current position and options
            if event.key == pygame.locals.K_SPACE:
                return 'repeat'

            # escape for terminating
            if event.key == pygame.locals.K_ESCAPE:
                return 'terminate'
            
            if event.key == pygame.locals.K_F1:
                self.tell_help()
                return ''            
            # F2 and F3 to change speaking rate
            if event.key == pygame.locals.K_F2:
                self.audio.change_speed('slower', memory_text.speed_slower)
                return ''
            if event.key == pygame.locals.K_F3:
                self.audio.change_speed('faster', memory_text.speed_faster)
                return ''
            
            # invalid key, play short sound
            self.audio.clear_queue()
            self.audio.priority_play('data/audio/effects/blop.wav')

        return ''
 
 
    def choose_size(self):
        """
        After interaction with the player, this method will return the
        selected board size. This method uses its own UI loop.
        """
 
        pygame.time.wait(300)
        toplay_orig = [
            #memory_text.choose_begin,
            memory_text.choose_small.format(memory_config.size['small']),
            #memory_text.choose_medium.format(memory_config.size['medium']),
            memory_text.choose_large.format(memory_config.size['large']),
            #memory_text.choose_huge.format(memory_config.size['huge']),
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
                    return 'small'
                #if event.key == pygame.locals.K_UP:
                #    return 'medium'
                elif event.key == pygame.locals.K_RIGHT:
                    return 'large'
                #if event.key == pygame.locals.K_DOWN:
                #    return 'huge'
                
                if event.key == pygame.locals.K_F1:
                    self.tell_help()           
                
                 
                # escape to terminate
                elif event.key == pygame.locals.K_ESCAPE:
                    return 'terminate'
                
                # everything else to repeat
                #event.key == pygame.locals.K_SPACE:
                else:
                    toplay = toplay_orig[:]
                

    def welcome(self):
        self.audio.play_sound_file('data/audio/effects/gong.wav')
        #~ self.audio.play_sound_file(self.sounds_welcome)
        self.audio.synthesize_and_play(memory_text.welcome)

    def tell_help(self):
        self.audio.synthesize_and_play(memory_text.help_text1)
        self.audio.synthesize_and_play(memory_text.help_text2)

    def tell_round(self, num):
        txt = memory_text.round_info.format(num)
        self.audio.synthesize_and_play(txt)

    def tell_wrongfield(self):
        self.audio.play_sound_file('data/audio/effects/blop.wav')
                       
    def tell_size(self, size):
        if size == 'small':
            txt = memory_text.size_info_small
        else:
            txt = memory_text.size_info_large
        self.audio.synthesize_and_play(txt)            
                       
    def tell_theme(self, themeidx ):        
        txt = memory_text.theme_chosen.format( memory_text.memory_themes[themeidx] )
        self.audio.synthesize_and_play(txt)        

    def tell_correct(self, corr):
        """ Tell the user if she matched two fields correctly. """
        if corr: 
            txt = memory_text.correct
        else:
            txt = memory_text.notcorrect
        self.lastcorr = txt
        self.audio.synthesize_and_play(txt)

    def tell_select_field(self, fieldnum):
        """ Tell to user to select the fieldnum-th field. """
        txt = memory_text.select[fieldnum-1]
        self.lasttask = txt
        self.audio.synthesize_and_play(txt)
        
    def tell_thing_selected(self, thingname):
        """ Tell user which thing she selected. """        
        txt = self.lastkey + ". " + thingname + "."
        self.lastthing = txt
        self.audio.priority_play('data/audio/effects/sweep_short.wav')
        self.audio.synthesize_and_play(txt)               
                    
    def tell_goal(self, numsteps):
        self.audio.play_sound_file('data/audio/effects/tada.wav')
        self.audio.synthesize_and_play(memory_text.goal.format(numsteps))
        pygame.time.wait(50)
        while pygame.mixer.get_busy() > 0 or len(self.audio.queue) > 0:
            self.audio.do_play()
            pygame.time.wait(50)            
            
    def tell_goal_all8(self, numsteps):
        self.audio.play_sound_file('data/audio/effects/tada.wav')
        self.audio.play_sound_file('data/audio/effects/tada.wav')
        self.audio.synthesize_and_play(memory_text.goal.format(numsteps))
        self.audio.synthesize_and_play(memory_text.allow_quit)
        pygame.time.wait(50)
        while pygame.mixer.get_busy() > 0 or len(self.audio.queue) > 0:
            self.audio.do_play()
            pygame.time.wait(50)            
        
    def invalid(self):
        self.audio.priority_play('data/audio/effects/blop.wav')

    def update_display(self):
        if self.txtsurf is None:
            col = pygame.Color(255,255,255)
            f = pygame.font.Font('data/graphics/DroidSans.ttf', 32)
            self.txtsurf = f.render('Audio-Memory', True, col)
        
        w, h = self.txtsurf.get_size()
        x = (pygame.display.Info().current_w - w) / 2 
        y = (pygame.display.Info().current_h - h) / 2
        self.screen.blit(self.txtsurf, (x, y))
        pygame.display.update()
        

# 
#     def play_again(self):
#         """
#         After completing one game, asks the player if she wants to play again.
#         If yes, go to choose size. If no, terminate.
#         Like choose_size, this uses its own UI loop
#         """
#         
#         toplay_orig = [
#             labyrinth_text.left_play_again,
#             labyrinth_text.forward_play_same_again,
#             labyrinth_text.right_terminate,
#         ]
#         toplay = toplay_orig[:]
#         
#         while True:
#             self.audio.do_play()
# 
#             if len(toplay) > 0:
#                 self.audio.synthesize_and_play(toplay.pop(0))
# 
#             # get next pygame event in queue
#             event = pygame.event.poll()
# 
#             if event.type == pygame.locals.QUIT:
#                 return 'terminate'
#         
#             if event.type == pygame.locals.KEYDOWN:
#                 # log key press
#                 keyname = pygame.key.name(event.key)
#                 liblog.log('key pressed: {}'.format(keyname))
#                 
#                 # any key press stops audio
#                 self.audio.stop_playback()
#                 self.audio.clear_queue()
#                 
#                 # arrow keys to select new game, same game or quit
#                 if event.key == pygame.locals.K_LEFT:
#                     return 'new'
#                 if event.key == pygame.locals.K_UP:
#                     liblog.log('restarting same labyrinth')
#                     return 'same'
#                 if event.key == pygame.locals.K_RIGHT:
#                     return 'terminate'
# 
#                 # space bar to repeat options
#                 if event.key == pygame.locals.K_SPACE:
#                     toplay = toplay_orig[:]
#                 
#                 # escape to terminate
#                 if event.key == pygame.locals.K_ESCAPE:
#                     return 'terminate'
        
