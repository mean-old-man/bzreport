#!/usr/bin/env python3

import argparse
import csv
import datetime as zeit
import locale
import os
import platform
import sys
import time

quelldatei = ''
zieldatei = ''
# 'abDatum' ist ist nur ein Platzhalter und **muss** entweder durch den mittels '--datum' übergebenen
# Wert oder durch das Datum des ersten Datensatzes aus der Quelldatei geändert werden!
abDatum = '1970-01-01'

# 'bisDatum' ist ebenfalls nur ein Platzhalter und **muss** durch das Datum des
# letzten Datensatzes aus der Quelldatei geändert werden!
bisDatum = zeit.date.today().isoformat()

# 1. Aufruf und übergebene Parameter prüfen
parser = argparse.ArgumentParser(
    description="Das Programm bzreport wandelt die aus Apple Health exportierten Blutzucker-Datensätze im Format " +
                "(strftime(%d-%b-%Y %H:%M),strftime(%d-%b-%Y %H:%M), float) in das Format (strftime(%d.%m.%Y), " +
                "strftime(%H:%M), uint16_t) und erstellt daraus eine neue CSV-Datei.")

parser.add_argument("quelldatei",
                    type=argparse.FileType('r', -1, encoding='ASCII'),
                    help='Die von QS-Access bereitgestellte Datei.')

parser.add_argument("zieldatei",
                    type=argparse.FileType('w', -1, encoding='ASCII'),
                    help='Ziel-Datei für den Diabetologen.')

parser.add_argument("-d", "--datum", help='Nur Daten ab diesem Datum verarbeiten.')

argumente = parser.parse_args()

# 2. Argumente auswerten
if argumente.quelldatei:
    quelldatei = argumente.quelldatei.name
    print("Quell-Datei: {0}".format(quelldatei))

if argumente.zieldatei:
    zieldatei = argumente.zieldatei.name
    print("Ziel-Datei: {0}".format(zieldatei))

if argumente.datum:
    # @TODO: Prüfen, ob das darauf folgende Argument ein String ist, der einem der folgenden Muster entspricht:
    # @TODO:     - YYYY-MM-DD
    # @TODO:     - D[D].M[M].YY[YY]
    # @TODO: Wenn ja, handelt es sich um ein gültiges Datum?
    # @TODO: Wenn nicht, dann das Programm mit einer entsprechenden Fehlermeldung abbrechen.
    print("Es werden nur Datensätze ab dem Datum {0} verarbeitet.".format(argumente.datum))


# 3. Eingabe-Datei als CSV-Datei öffnen/einlesen.
print("\n\nDatei einlesen …")
csvQuelle = open(quelldatei)
csvQuelldatenLeser = csv.reader(csvQuelle)


# 4. Übergebenes Datum verarbeiten.
# @TODO: Wenn ein Datum übergeben wurde, dann müssen wir nach diesem Tag suchen.
# @TODO: Dazu müssen wir das angegebene Datum in das Format
# @TODO:    'DD-[Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]-YYYY' umwandeln.
# @TODO: Wenn es keinen Datensatz zu diesem Tag gibt, dann wird der nächstfolgende Tag als neuer Startpunkt verwendet.
# @TODO: Und zwar solange, bis das Dateiende der Eingabe-Datei erreicht ist.
# @TODO: Finden wir keinen Startpunkt, dann brechen wir das Programm mit einer Fehlermeldung ab.


# 5. Ziel-Datei öffnen
print("\nDaten schreiben …")
csvZiel = open(zieldatei, 'w')

# 6. Kopfzeilen schreiben
print('Blutzuckerwerte vom {0} bis zum {1}'.format(abDatum, bisDatum))
csvFeldnamen = ['Datum', 'Uhrzeit', 'Blutzuckerwert (md/dL)']
csvZieldatenSchreiber = csv.DictWriter(csvZiel, fieldnames=csvFeldnamen)
csvZieldatenSchreiber.writeheader()

# 7. Solange Daten aus der Quell-Datei lesen, bis das Dateiende erreicht ist.
# @TODO: Tritt währenddessen ein Fehler auf, brechen wir das Programm mit einer Fehlermeldung ab.

for zeile in csvQuelldatenLeser:
    # 8. Wurde ein Datum übergeben, müssen wir prüfen, ob der eingelesen Datensatz dazu passt.
    # @TODO: Haben wir einen Datensatz gefunden, dann
    # @TODO:    - holen wir uns den Inhalt der ersten und dritten Spalte und übergeben ihn an die Variablen
    # @TODO:        - importZeitstempel und wertBlutzucker.
    # @TODO:    - Trennen Datum und Uhrzeit (dd-???-yyyy hh:mm) aus der Variablen importZeitstempel.
    # @TODO:    - Wandeln das Datum in das Format DD.MM.YYYY und weisen es der Variablen exportDatum zu.
    # @TODO:    - Weisen die Uhrzeit der Variablen exportUhrzeit zu.

    # 9. Eingelesene Datensätze verarbeiten.
    # @TODO: Werte der Variablen exportDatum, exportUhrzeit und wertBlutzucker in gültige CSV-Zeile wandeln und
    zeitstempel = zeit.datetime.today()
    datum = zeitstempel.strftime('%d.%m.%Y')
    uhrzeit = zeitstempel.strftime('%H:%M')
    blutzuckerwert = 100

    # 10. Datensatz in Ziel-Datei schreiben
    csvZieldatenSchreiber.writerow({'Datum': datum, 'Uhrzeit': uhrzeit, 'Blutzuckerwert (md/dL)': blutzuckerwert})

# 11. Quell- und Zieldatei schliesen.
csvZiel.close()
csvQuelle.close()

# 12. Rückmeldung an den Benutzer geben.
print("Konvertierung abgeschlossen.")
print("Die Datei {0} kann nun an den Diabetologen gesendet werden.".format(zieldatei))




