#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

# library imports
import datetime
import random

# imports from this project
import memory_config
import liblog

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# ==============================================================================
# memory_logic.Logic
# ==============================================================================
class GameLogic(object):

    class Board(object):
        def __init__(self, size):
            self.size = size
            self.fields = [0] * size
            self.init_fields()
            
        def init_fields(self):
            # loop size / 2 memory objects and choose 2 fields for each
            for memoryobject in range( 1, self.size / 2 + 1):
                idx = random.choice( [ ele for ele in range(len(self.fields)) if self.fields[ele] == 0 ] )
                self.fields[idx] = memoryobject
                idx = random.choice( [ ele for ele in range(len(self.fields)) if self.fields[ele] == 0 ] )
                self.fields[idx] = memoryobject                

            print self.fields
                  
            

    def __init__(self, sizename):

        self.things = None
        self.States = enum( 'SELECT_1', 'SELECT_2', 'FINISH' )
        self.current_state = None
        self.current_thing = None
        self.size = memory_config.size[sizename]        

        # when the game logic changes this to True, the game should terminate
        self.terminate = False
        
        # create the board
        self.board = self.Board( self.size )
        


    def handle_event(self, eventstring):
        
        if eventstring == '':
            return None
        
        #print 'eventstring: {}'.format(eventstring)
        
        if eventstring == 'terminate':
            self.terminate = True
            return None
        
        if eventstring == 'hardterminate':
            self.terminate = True
            return None        
        
        # get started
        if eventstring == 'begin':
            self.current_state = self.States.SELECT_1
            self.field1 = None
            self.field2 = None
            self.current_thing = None
            self.last_correct = None
            self.starttime = datetime.datetime.now()
            self.numsteps = 0
            return 'select1'
        
        # user selected a field
        if eventstring.startswith( "field_" ):
            fieldsel = int(eventstring[6:])
            
            if self.board.fields[fieldsel] < 1 or fieldsel == self.field1:
                liblog.log('user selected field {} which is already finished.'.format(fieldsel))
                return 'wrongfield' 
            
            # user selected the first field
            if self.current_state == self.States.SELECT_1:
                liblog.log('user selected field1: {} ({}).'.format(fieldsel, self.things[self.board.fields[ fieldsel ]-1]))
                self.field1 = fieldsel
                self.current_thing = self.board.fields[fieldsel]                
                self.current_state = self.States.SELECT_2
                return 'select2'
            
            # user selected the second field
            if self.current_state == self.States.SELECT_2:
                liblog.log('user selected field2: {} ({}).'.format(fieldsel, self.things[self.board.fields[ fieldsel ]-1]))
                self.field2 = fieldsel
                self.current_thing = self.board.fields[fieldsel]
                
                self.numsteps += 1
                
                # see if fields match
                if self.board.fields[ self.field1 ] == self.board.fields[ self.field2 ]:
                    liblog.log('user was correct with field1: {} ({}) and field2: {} ({}).'.format(
                            self.field1, self.things[self.board.fields[ self.field1 ]-1], self.field2, self.things[self.board.fields[ self.field2 ]-1]))
                    self.board.fields[ self.field1 ] = self.board.fields[ self.field2 ] = 0
                    self.last_correct = True
                    
                    if sum(self.board.fields) == 0:
                        elapsedtime = datetime.datetime.now() - self.starttime
                        liblog.log('goal reached after {} steps and {} seconds'.format(
                                                            self.numsteps, elapsedtime.total_seconds()))                        
                        self.current_state = self.States.FINISH
                        return 'finished'
                    
                else:
                    liblog.log('user was wrong with field1: {} ({}) and field2: {} ({}).'.format(
                            self.field1, self.things[self.board.fields[ self.field1 ]-1], self.field2, self.things[self.board.fields[ self.field2 ]-1]))
                    self.last_correct = False
                    
                self.field1 = None
                self.field2 = None                                                                       
                self.current_state = self.States.SELECT_1
                return 'select1'
                        

        return None            



            
