#!/usr/bin/env python

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

import random
import pygame

size = {
    'small'  : 8,
    'medium' : 12,
    'large'  : 16,
    'huge'   : 20,
}

#myseed = 1337
#random.seed(myseed)
random.seed()
seeds = [ random.random() for i in range(1000) ]

displaysize = (400,300)

#field_keys = [ pygame.K_a, pygame.K_b, pygame.K_c, pygame.K_d, pygame.K_e, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_i, pygame.K_j, 
#               pygame.K_k, pygame.K_l, pygame.K_m, pygame.K_n, pygame.K_o, pygame.K_p, pygame.K_q, pygame.K_r, pygame.K_s, pygame.K_t,
#               pygame.K_u, pygame.K_v, pygame.K_w, pygame.K_x, pygame.K_y, pygame.K_z ]

field_keys = [ pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON,  
               pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p ]