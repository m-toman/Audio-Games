#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

# library imports
import datetime
import networkx
import numpy
import random

# imports from this project
import labyrinth_config
import liblog

# ==============================================================================
# labyrinth_logic.Logic
# ==============================================================================
class GameLogic(object):

    def __init__(self, sizename):

        self.size = labyrinth_config.size[sizename]
        self.dead_ends = labyrinth_config.dead_ends[sizename]
        
        # create the labyrinth graph
        self.graph = self.create_graph()

        # select goal node
        self.goal = self.select_goal()
        
        self.curpos = None
        self.prevpos = None
        self.numsteps = None
        self.starttime = None


    def handle_event(self, eventstring):
        
        if eventstring == '':
            return None
        
        #~ print 'eventstring: {}'.format(eventstring)

        if eventstring == 'begin':
            # put player in start node
            self.curpos = 0
            self.prevpos = None
            self.numsteps = 0
            self.starttime = datetime.datetime.now()
            return 'update'

        if eventstring in ('left', 'right', 'forward', 'back'):

            opts = self.get_options()

            # selected option might be invalid at current node
            if eventstring not in opts.keys():
                return 'invalid'

            # otherwise, update current and position
            self.prevpos = self.curpos
            self.curpos = opts[eventstring]

            # increment number of taken steps
            self.numsteps += 1

            # log player move
            liblog.log('player moved {:7s}: {}->{} ({} -> {})'.format(
                eventstring,
                self.prevpos,
                self.curpos,
                self.rooms[self.prevpos][0],
                self.rooms[self.curpos][0],
            ))

            # we might have reached the goal
            if self.curpos == self.goal:
                elapsedtime = datetime.datetime.now() - self.starttime
                liblog.log('goal reached after {} steps and {} seconds'.format(
                    self.numsteps, elapsedtime.total_seconds()))
                return 'goal'
            else:
                return 'update'
            


    def create_graph(self):
        """Creates a random undirected graph, the actual labyrinth
        
        The graph is represented by a (symmetrical, because the graph is
        undirected) incidence matrix (a numpy.ndarray), which this function
        returns.
        """

        n = self.size

        # create empty incidence matrix
        graph = numpy.zeros((n, n), dtype=numpy.int8)

        # set a number of rooms aside, they will be added as dead ends at the
        # end
        m = n - self.dead_ends

        # create random tree by attaching each node to a randomly selected
        # earlier node which doesn't have too many neighbors yet
        for i in range(1, m):

            # potential neighbors
            nodes = [ x for x in range(i) if sum(graph[x]) < 3 ]

            j = random.choice(nodes)
            graph[i,j] = 1
            graph[j,i] = 1
        
        #print graph

        blacklist = []

        # add dead ends
        # all nodes whose degree is less than 4
        nodes = [ x for x in range(m) if sum(graph[x]) < 4 and x != 0]
        random.shuffle(nodes)
        for i in range(m, n):

            j = nodes.pop(0)
            graph[i,j] = 1
            graph[j,i] = 1
            blacklist.append(i)

        # randomly add edges, as long as no node's degree gets too large
        #~ blacklist = []
        while True:
            
            # all nodes whose degree is less than 3
            nodes = [ x for x in range(m) if sum(graph[x]) < 3 and x not in blacklist ]

            if len(nodes) == 0:
                #print 'I couldn\'t find a node with degree less than 3'
                break
            
            i = random.choice(nodes)
            
            #print 'I\'ll try to add an edge to node {}'.format(i)
            
            # all nodes
            #  - except the start node
            #  - and i itself
            #  - whose degree is less than 4
            #  - and which are not already connected to i
            nodes = [ x for x in range(1,m) if x != i and sum(graph[x]) < 4 and graph[i,x] == 0 ]
            if len(nodes) == 0:
                #print 'I couldn\'t find one, blacklisting node {}'.format(i)
                blacklist.append(i)
                continue
            
            j = random.choice(nodes)
            
            #print 'adding edge ({},{})'.format(i, j)
            graph[i,j] = 1
            graph[j,i] = 1
            #print graph

        #self.draw_graph(graph)
        #print graph
        
        # write labyrinth info to log
        numedges = graph.sum() / 2
        liblog.log('labyrinth generated. number of nodes: {} number of edges: {}'.format(n, numedges))
        msg = 'labyrinth node adjacency matrix:\n'
        opts = numpy.get_printoptions()
        numpy.set_printoptions(threshold='nan')
        msg += numpy.array_str(graph, max_line_width=500)
        numpy.set_printoptions(**opts)
        liblog.log(msg)

        return graph


    #~ def draw_graph(self, A):
        #~ import networkx
        #~ import pylab
        #~ g = networkx.Graph(A)
        #~ #pos = networkx.graphviz_layout(g, prog='fdp')
        #~ pos = networkx.spectral_layout(g)
        #~ #pos = networkx.circular_layout(g)
        #~ networkx.draw(g, pos)
        #~ #pylab.show()
        #~ pylab.savefig("graph.png")


    def select_goal(self):
        """Determines the node furthest away from the start and returns it"""

        # compute length of shortest path for each node, store maximum
        maxlen = 0
        maxnode = None
        for i in range(1, self.size):
            path = networkx.shortest_path(networkx.Graph(self.graph), 0, i)
            #print path
            #print 'there is a path of length {} from 0 to {}'.format(len(path)-1, i)
            if len(path) > maxlen:
                maxlen = len(path)
                maxnode = i
        
        #~ print 'The goal node is {} with a shortest path of length {}'.format(maxnode, maxlen-1)
        return maxnode


    def get_options(self):
        """Returns the options from the current position"""

        # build dictionary of possible directions to go
        d = {}
        
        # get neighbor nodes of current node
        # indices of non-zero entries of the row corresponding to the current
        # node
        neighbors = list(numpy.nonzero(self.graph[self.curpos])[0])

        # reverse neighbors, such that dead ends are named first
        neighbors.reverse()

        #print neighbors

        # if previous position is available (then it will be a neighbor), set
        # 'back' option to lead there
        if self.prevpos in neighbors:
            d['back'] = self.prevpos
            neighbors.remove(self.prevpos)

        #print neighbors

        # this should not happen, but if there is only one option it will be
        # to go straight
        if len(neighbors) == 1:
            d['forward'] = neighbors[0]
        # if there are only two other options, they will be left and right
        elif len(neighbors) == 2:
            d['left'] = neighbors[0]
            d['right'] = neighbors[1]
        # else we have three options, left, forward, right
        elif len(neighbors) == 3:
            d['left'] = neighbors[0]
            d['forward'] = neighbors[1]
            d['right'] = neighbors[2]

        # there might also be no neighbors, in this case it's a dead end and the
        # player has no other option than going back

        return d
