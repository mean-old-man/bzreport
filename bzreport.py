#!/usr/bin/env python3

import argparse
import csv
import datetime
import locale
import os
import platform
import sys

print("Aufruf: " + sys.argv)

# 1
# @TODO: Anzahl der übergebenen Argumente prüfen

# 2
# @TODO: Prüfen, ob eines der Argumente ein '-i' ist und wenn ja, dann prüfen,
# @TODO:    - ob das darauf folgende Argument ein String ist und wenn ja,
# @TODO:    - ob diese Datei gelesen werden kann.
# @TODO: Wenn nicht, dann das Programm mit einer Fehlermeldung beenden.

# 3
# @TODO: Prüfen, ob eines der Argumente ein '-o' ist und wenn ja, dann prüfen,
# @TODO:    - ob das darauf folgende Argument ein String ist und wenn ja.
# @TODO:    - ob die Datei geschrieben werden kann.
# @TODO: Wenn nicht, dann das Programm mit einer Fehlermeldung beenden.

# 4
# @TODO: Prüfen, ob eines der Argumente ein '-d' ist und wenn ja, dann prüfen,
# @TODO:    - ob das darauf folgende Argument ein String ist, der einem der folgenden Muster entspricht:
# @TODO:        - YYYY-MM-DD
# @TODO:        - D[D].M[M].YY[YY]
# @TODO:    - Wenn ja, handelt es sich um ein gültiges Datum?
# @TODO: Wenn nicht, dann das Programm mit einer Fehlermeldung beenden.

# 5
# @TODO: Eingabe-Datei als CSV-Datei öffnen/einlesen.

# 6
# @TODO: Wenn ein Datum übergeben wurde, dann müssen wir nach diesem Tag suchen.
# @TODO: Dazu müssen wir das angegebene Datum in das Format
# @TODO:    'DD-[Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]-YYYY' umwandeln.
# @TODO: Wenn es keinen Datensatz zu diesem Tag gibt, dann wird der nächstfolgende Tag als neuer Startpunkt verwendet.
# @TODO: Und zwar solange, bis das Dateiende der Eingabe-Datei erreicht ist.
# @TODO: Finden wir keinen Startpunkt, dann brechen wir das Programm mit einer Fehlermeldung ab.

# 7
# @TODO: Ausgabe-Datei als CSV Datei öffnen/schreiben.

# 8
# @TODO: Haben wir einen Datensatz gefunden, dann
# @TODO:    - holen wir uns den Inhalt der ersten und dritten Spalte und übergeben ihn an die Variablen
# @TODO:        - importZeitstempel und wertBlutzucker.
# @TODO:    - Trennen Datum und Uhrzeit (dd-???-yyyy hh:mm) aus der Variablen importZeitstempel.
# @TODO:    - Wandeln das Datum in das Format DD.MM.YYYY und weisen es der Variablen exportDatum zu.
# @TODO:    - Weisen die Uhrzeit der Variablen exportUhrzeit zu.

# 9
# @TODO: Werte der Variablen exportDatum, exportUhrzeit und wertBlutzucker in gültige CSV-Zeile wandeln und
# @TODO: in die Ausgabe-Datei schreiben.

#10
# @TODO: Schritte 8 bis 9 solange wiederholen, bis Ende der Eingabe-Datei erreicht worden ist.
# @TODO: Tritt währenddessen ein Fehler auf, brechen wir das Programm mit einer Fehlermeldung ab.
# @TODO: Bei Erfolg beenden wir das Programm und geben dem Anwender ein positives Feedback
