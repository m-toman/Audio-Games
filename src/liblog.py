#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

import datetime
import logging
import os
import socket

starttime = datetime.datetime.now()
logdir = 'data/logs'

def init_logging(prefix):

    if not os.path.isdir(logdir):
        os.mkdir(logdir)

    hostname = socket.gethostname()
    tstamp = starttime.strftime('%Y-%m-%d-%H.%M.%S')
    logfilename = '{}/{}_{}_{}.txt'.format(logdir, prefix, hostname, tstamp)
    logging.basicConfig(filename=logfilename,
        format='%(asctime)s %(message)s', level=logging.DEBUG)

def log(message):
    reltime = datetime.datetime.now() - starttime
    reltimestr = '{:9.3f}'.format(reltime.total_seconds())
    logging.info(reltimestr + '   ' + message)
