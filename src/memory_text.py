#!/usr/bin/env python
# -*- coding: utf-8 -*-

# FTW Telecommunications Research Center Vienna (www.ftw.at)
# Dietmar Schabus (schabus@ftw.at)
# July 2014

#alphabeta = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'

select = [
    'Wähle erstes Feld.', 'Wähle zweites Feld.'
]

memory_themes = [ 'lebensmittel', 'tiere', 'musikinstrumente', 'fortbewegungsmittel', 'schule', 'pflanzen', 'länder', 'kleidung' ]
memory_things = [
  [ 'kartoffel', 'tomate', 'gurke', 'banane', 'apfel', 'karotte', 'nektarine', 'kiwi', 'sellerie', 'maiskolben', 'salz', 'pfeffer', 'reiskorn', 'nudel', 'brot', 'wurst', 'kuchen', 'zucker', 'zimt', 'spargel', 'erdbeere', 'traube', 'zitrone' ],
 [ 'katze', 'faultier', 'krokodil', 'maus', 'affe', 'bär', 'gorilla', 'schlange', 'leguan', 'schnecke', 'elch', 'hirsch', 'elefant', 'löwe', 'tiger', 'gazelle', 'hase', 'nilpferd', 'esel', 'ente' ],
 [ 'klavier', 'gitarre', 'flöte', 'saxophon', 'klarinette', 'orgel', 'triangel', 'trommel', 'pauke', 'trompete', 'tuba', 'posaune', 'harfe', 'horn', 'geige' ],  
 [ 'auto', 'flugzeug', 'schiff', 'segelboot', 'traktor', 'mähdrescher', 'bagger', 'moped', 'motorrad', 'fahrrad', 'frachter', 'hubschrauber', 'u-bahn', 'bus', 'eisenbahn' ],
 [ 'schere', 'bleistift', 'papier', 'radiergummi', 'lineal', 'büroklammer', 'heft-maschine', 'kugelschreiber', 'filzstift', 'taschenrechner', 'notiz-heft', 'kalender'  ], 
 [ 'löwenzahn', 'tanne', 'fichte', 'esche', 'ahorn', 'distel', 'maiglöckchen', 'sonnenblume', 'gänseblümchen', 'fliegenpilz', 'trauerweide', 'kastanie' ],
 [ 'frankreich', 'österreich', 'deutschland', 'norwegen', 'holland', 'spanien', 'italien', 'ungarn', 'kanada', 'england', 'schweiz', 'portugal', 'slowakei' ],
 [ 'hemd', 'hose', 'krawatte', 'socken', 'schuhe', 'hut', 'kapuze', 'pullover', 'unterhemd', 'mantel', 'jacke', 'kleid' ]
 ]

help_text1 = "Finde je zwei gleiche Gegenstände. Für ein kleines Feld verwende die Tasten A S D F, J K L Ö. Für ein großes Feld zusätzlich Q, W, E, R, U, I, O, P."
help_text2 = "F zwei und F drei zur Änderung der Sprechgeschwindigkeit, Leer taste zum wiederholen der letzten Nachricht."


allow_quit = "Du hast alle Runden erfolgreich abgeschlossen. Du kannst weiterspielen wenn du möchtest, ansonsten kannst du jederzeit Eskäp drücken um zu beenden."

round_info = "Runde {}"
theme_chosen = "Thema, {}."
size_info_small = "Ein kleines Feld, du benötigst nur eine Tastenreihe."
size_info_large = "Ein großes Feld, du benötigst beide Tastenreihen."

correct = 'Richtig.'
notcorrect = 'Leider falsch.'
goal = 'gratulation, du hast alle paare nach {} zügen gefunden!'

speed_slower = speed_faster = 'Sprechgeschwindigkeit geändert.'
welcome = 'willkommen beim audio memory. drücke F eins für Hilfe, Leer-Taste um die letzte Nachricht zu wiederholen.'

choose_begin = 'wähle die größe des spielfelds.'
choose_small = 'pfeil links für ein kleines spielfeld mit {} tasten.'
choose_medium = 'pfeil oben für ein mittleres spielfeld mit {} karten.'
choose_large = 'pfeil rechts für ein großes spielfeld mit {} tasten.'
choose_huge = 'pfeil unten für ein riesiges spielfeld mit {} karten.'

left_play_again = 'drücke links für noch einmal spielen.'
forward_play_same_again = 'drücke gerade aus, um genau das selbe labyrinth noch einmal zu spielen.'
right_terminate = 'drücke rechts für beenden.'
