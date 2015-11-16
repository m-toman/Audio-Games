#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

import random

size = {
    'small'  : 7,
    'medium' : 15,
    'large'  : 50,
    'huge'   : 100,
}
dead_ends = {
    'small'  : 2,
    'medium' : 4,
    'large'  : 10,
    'huge'   : 20,
}
#myseed = 1337
#random.seed(myseed)
random.seed()
seeds = {
    'small'  : [ random.random() for i in range(1000) ],
    'medium' : [ random.random() for i in range(1000) ],
    'large'  : [ random.random() for i in range(1000) ],
    'huge'   : [ random.random() for i in range(1000) ],
}

displaysize = (400,300)
