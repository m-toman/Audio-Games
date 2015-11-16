#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

# library imports
import datetime
import os
import pygame
import shutil
import subprocess
import sys
import tempfile

# imports from this project
import labyrinth_config
import labyrinth_text
import liblog

# ==============================================================================
# libaudio.Audio
# ==============================================================================
class Audio(object):

    def __init__(self, voicename, gamename):
        pygame.mixer.pre_init(frequency=48000)
        self.speed = 1.0
        self.presynthesized = []
        self.cache = {}
        self.queue = []

        # delete old cache directory if present, create new one
        self.cachedir = 'data/audio/cache'
        if os.path.isdir(self.cachedir):
            shutil.rmtree(self.cachedir)
        os.mkdir(self.cachedir)

        self.voicefile = 'data/tts/voices/' + voicename + '.htsvoice'
        if not os.path.exists(self.voicefile):
            sys.exit('Unable to load voice "{}": there is no file "{}".'.format(
                voicename, self.voicefile))
        
        self.rulesfile = 'data/tts/lexicon/' + gamename + '.rules'
        if not os.path.exists(self.rulesfile):
            sys.exit('Unable to load pronunciation rules for game "{}": there is no file "{}".'.format(gamename, self.rulesfile))


    def do_play(self):
        if pygame.mixer.get_busy():
            return

        if len(self.queue) > 0:
            soundfile = self.queue.pop(0)
            liblog.log('playing sound file "{}"'.format(soundfile))
            sound = pygame.mixer.Sound(soundfile)
            sound.play()


    def clear_queue(self):
        self.queue = []


    def play_sound_file(self, filename):
        #print 'playing sound file "{}"'.format(filename)
        #self.channel.queue(pygame.mixer.Sound(filename))
        #pygame.mixer.Sound(filename).play()
        self.queue.append(filename)
        self.do_play()


    def priority_play(self, filename):
        self.queue.insert(0, filename)


    def play_presynthesized(self, i):
        #if self.channel is None:
            #self.channel = pygame.mixer.Channel(0)
        self.play_sound_file(self.presynthesized[i])
        while pygame.mixer.get_busy():
            pygame.time.wait(50)


    def stop_playback(self):
        pygame.mixer.stop()


    def start_music(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(-1)


    def synthesize_and_play(self, utt):
        #~ print utt
        key = (utt, self.speed)
        if key in self.cache:
            filename = self.cache[key]
        else:
            filename = self.synthesize(utt)
            self.cache[key] = filename
        print utt
        self.play_sound_file(filename)


    def change_speed(self, how, msg):
        minspeed = 0.6
        maxspeed = 2.0
        if how == 'faster':
            if self.speed < maxspeed:
                self.speed = min(self.speed + 0.2, maxspeed)
        else:
            if self.speed > minspeed:
                self.speed = max(self.speed - 0.2, minspeed)
        self.synthesize_and_play(msg)
        liblog.log('changed speaking rate to {:.1f}'.format(self.speed))

    def synthesize(self, utt):
        
        # write utt to temporary text file
        handle, filename = tempfile.mkstemp(text=True)
        os.write(handle, utt)

        # open null device for dumping htstts output there
        with open(os.devnull) as fnull:

            # call HTS TTS in subprocess
            # The path of the first argument (the executable) is relative to
            # the calling path, i.e., .../SALB/games
            # The paths of the other arguments are relative to cwd, which is
            # equal to cachedir, such that htstts writes its results there.
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            subprocess.check_output((
                'data/tts/htstts.exe',
                '../../../' + self.voicefile,
                '../../../' + self.rulesfile,
                '-f', filename,
                '{:.1f}'.format(self.speed),
            ), cwd=self.cachedir, stdin=fnull, stderr=fnull, startupinfo=si) #creationflags=0x08000000)

        oldname = self.cachedir + '/output_1.wav'
        newname = self.cachedir + '/cached_{}.wav'.format(len(self.cache) + 1)
        os.rename(oldname, newname)

        # delete temporary textfile
        os.close(handle)
        os.remove(filename)

        return newname


    #~ def pre_synthesize(self, utterances, outpath):
        #~ """
        #~ Given a list (or other iterable) of utterances (sentences), this
        #~ method synthesizes all of them to sound files in outpath and
        #~ returns a list containing the file names of the sound files.
        #~ """
#~ 
        #~ resultfiles = []
#~ 
        #~ # write utterances to temporary text file
        #~ handle, filename = tempfile.mkstemp(text=True)
        #~ os.write(handle, '\n'.join(utterances))
#~ 
        #~ # call HTS TTS in subprocess
        #~ subprocess.check_call((
            #~ 'tts/htstts.exe',
            #~ '../../tts/leo.htsvoice',
            #~ '../../tts/mini.rules',
            #~ '-f', filename,
            #~ '1.4',
        #~ ), cwd=outpath)
#~ 
        #~ for i in range(len(utterances)):
            #~ fname = '{}/output_{}.wav'.format(outpath, i+1)
            #~ resultfiles.append(fname)
#~ 
        #~ # remove temporary text file
        #~ os.close(handle)
        #~ os.remove(filename)
#~ 
        #~ return resultfiles
