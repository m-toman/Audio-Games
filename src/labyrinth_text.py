#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

# 3-tuple:
#  rooms[i][0] name of the room, e.g. "Wohnzimmer"
#
#  rooms[i][1] preposition and article for stating where the player is, e.g.
#              "im" for building a sentence like
#              "Du bis jetzt " + "im" + " " + "Wohnzimmer"
#
#  rooms[[i][2] preposition and article for stating options for the next move,
#               e.g. "ins" for building a sentence like
#               "Links" + " führt eine Tür " + "ins" + " " + "Wohnzimmer"
rooms = [
    [ 'küche', 'in der', 'in die' ],
    [ 'schlafzimmer', 'im', 'ins' ],
    [ 'wohnzimmer', 'im', 'ins' ],
    [ 'badezimmer', 'im', 'ins' ],
    [ 'keller', 'im', 'in den' ],
    [ 'dachboden', 'auf dem', 'auf den' ],
    [ 'balkon', 'auf dem', 'auf den' ],
    [ 'garage', 'in der', 'in die' ],
    [ 'waschküche', 'in der', 'in die' ],
    [ 'besenkammerl', 'im', 'in das' ],
    [ 'garten', 'im', 'in den' ],
    [ 'vorratskammer', 'in der', 'in die' ],
    [ 'aula', 'in der', 'in die' ],
    [ 'turnsaal', 'im', 'in den' ],
    [ 'bibliothek', 'in der', 'in die' ],
    [ 'dachterrasse', 'auf der', 'auf die' ],
    [ 'maschinenraum', 'im', 'in den' ],
    [ 'labor', 'im', 'in das' ],
    [ 'hühnerstall', 'im', 'in den' ],
    [ 'pferdestall', 'im', 'in den' ],
    [ 'hundehütte', 'in der', 'in die' ],
    [ 'konzertsaal', 'im', 'in den' ],
    [ 'büro des chefs', 'im', 'ins' ],
    [ 'höhle', 'in der', 'in die' ],
    [ 'kommandozentrale', 'in der', 'in die' ],
    [ 'geräteschuppen', 'im', 'in den' ],
    [ 'werkstatt', 'in der', 'in die' ],
    [ 'lagerhalle', 'in der', 'in die' ],
    [ 'cockpit', 'im', 'ins' ],
    [ 'frachtraum', 'im', 'in den' ],
    [ 'speisesaal', 'im', 'in den' ],
    [ 'kühlraum', 'im', 'in den' ],
    [ 'thronsaal', 'im', 'in den' ],
    [ 'rittersaal', 'im', 'in den' ],
    [ 'schatzkammer', 'in der', 'in die' ],
    [ 'löwengrube', 'in der', 'in die' ],
    [ 'empfangshalle', 'in der', 'in die' ],
    [ 'sauna', 'in der', 'in die' ],
    [ 'wellness-bereich', 'im', 'in den' ],
    [ 'schwimmbad', 'im', 'ins' ],
    [ 'tresorraum', 'im', 'in den' ],
    [ 'computerraum', 'im', 'in den' ],
    [ 'tonstudio', 'im', 'ins' ],
    [ 'würstchenbude', 'in der', 'in die' ],
    [ 'zimmer mit den undichten fenstern', 'in dem', 'in das' ],
    [ 'zimmer wo es von der decke tropft', 'in dem', 'in das' ],
    [ 'zimmer mit dem eigenartigen geruch', 'in dem', 'in das' ],
    [ 'raum aus dem man komische geräusche hört', 'in dem', 'in den' ],
    [ 'raum voller tickender uhren', 'in dem', 'in den' ],
    [ 'raum wo laute musik läuft', 'in dem', 'in den' ],
    [ 'kammer voller gerümpel', 'in der', 'in die' ],
    [ 'kammer mit den leckereien', 'in der', 'in die' ],
    [ 'kammer ohne fenster', 'in der', 'in die' ],
    [ 'vogelnest', 'im', 'ins' ],
    [ 'affengehege', 'im', 'ins' ],
    [ 'hüpfburg', 'in der', 'in die' ],
    [ 'eisdiele', 'in der', 'in die' ],
    [ 'gewächshaus', 'im', 'ins' ],
    [ 'tanzfläche', 'auf der', 'auf die' ],
    [ 'bar', 'an der', 'an die' ],
    [ 'heizraum', 'im', 'in den' ],
    [ 'weinkeller', 'im', 'in den' ],
    [ 'produktionshalle', 'in der', 'in die' ],
    [ 'wartezimmer', 'im', 'in das' ],
    [ 'zirkuszelt', 'im', 'ins' ],
    [ 'wohnwagen', 'im', 'in den' ],
    [ 'proberaum', 'im', 'in den' ],
    [ 'schlafgemach der prinzessin', 'im', 'ins' ],
    [ 'wirts-stüberl', 'im', 'ins' ],
    [ 'meeting-raum', 'im', 'in den' ],
    [ 'telefonzelle', 'in der', 'in die' ],
    [ 'zisterne', 'in der', 'in die' ],
    [ 'glockenturm', 'im', 'in den' ],
    [ 'partyzelt', 'im', 'ins' ],
    [ 'forschungszentrum', 'im', 'ins' ],
    [ 'b b i', 'im', 'ins' ],
    [ 'sitzungssaal', 'im', 'in den' ],
    [ 'druckerei', 'in der', 'in die' ],
    [ 'teeküche', 'in der', 'in die' ],
    [ 'fahrrad-abstellraum', 'im', 'in den' ],
    [ 'müll-raum', 'im', 'in den' ],
    [ 'lehrerzimmer', 'im', 'ins' ],
    [ 'konferenzzimmer', 'im', 'ins' ],
    [ 'direktion', 'in der', 'in die' ],
    [ 'sekretariat', 'im', 'ins' ],
    [ 'buchhaltung', 'in der', 'in die' ],
    [ 'flugzeughangar', 'im', 'in den' ],
    [ 'treibstoff-lagerraum', 'im', 'in den' ],
    [ 'fitnessraum', 'im', 'in den' ],
    [ 'krankenstation', 'auf der', 'auf die' ],
    [ 'operationssaal', 'im', 'in den' ],
    [ 'intensivstation', 'auf der', 'auf die' ],
    [ 'leuchtturm', 'auf dem', 'auf den' ],
    [ 'begehbaren kleiderschrank', 'im', 'in den' ],
    [ 'solarium', 'im', 'ins' ],
    [ 'scheune', 'in der', 'in die' ],
    [ 'hörsaal', 'im', 'in den' ],
    [ 'klassenzimmer', 'im', 'ins' ],
    [ 'getreidesilo', 'im', 'ins' ],
    [ 'goldmine', 'in der', 'in die' ],
]

directions = {
    'left'    : 'links',
    'right'   : 'rechts',
    'forward' : 'gerade aus',
    'back'    : 'zurück',
}

welcome = 'willkommen im audio-labyrinth'
youare = 'du bist jetzt {} {}.'
youcango = '{} geht es {} {}.'
youcangoback = 'du kannst auch {} {} {} gehen.'
deadend = 'hier ist eine sackgasse. du kannst nur {} {} {} gehen.'
goal = 'hier ist der ausgang aus dem labyrinth. gratulation, du hast das ziel nach {} zügen erreicht!'

sizes = {
    'small'  : ('links', 'kleines'),
    'medium' : ('oben', 'mittleres'),
    'large'  : ('rechts', 'großes'),
    'huge'   : ('unten', 'riesiges'),
}

choose_size_begin = 'wähle die größe des labyrinths.'
choose_size = 'pfeil {}, {} labyrinth mit {} räumen.'
selected_size = 'du hast ein {} labyrinth gewählt. finde den ausgang.'

left_play_again = 'drücke links für ein neues labyrinth.'
right_play_same_again = 'drücke rechts, um genau das selbe labyrinth noch einmal zu spielen.'
escape_terminate = 'drücke escape, um das spiel zu beenden.'

speed_changed = 'Sprechgeschwindigkeit geändert.'

abort = 'labyrinth abgebrochen.'

help_utts = [
    'beim audio-labyrinth bewegt man sich mit den pfeil-tasten durch die räume, und versucht den ausgang zu finden.',
    'es handelt sich um kein raster-förmiges labyrinth, sondern jeder raum kann beliebig mit anderen räumen verbunden sein.',
    'leer-taste, letzte nachricht wiederholen.',
    'f zwei, stimme schneller machen',
    'f drei, stimme langsamer machen.',
    'f vier, das derzeitige labyrinth abbrechen.'
    'f eins, diese hilfe hören.',
]

alphabet = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
