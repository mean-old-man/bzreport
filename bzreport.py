#!/usr/bin/env python3

import argparse
import csv
import datetime as zeit
import locale
import os
import platform
import re as regex
import sys
import time

quelldatei = None
zieldatei = None

# Meine persönlichen Messdaten werden seit 12.10.2015 aufgezeichnet.
# Die folgenden Datumsangaben müssen also individuell angepasst werden.
abJahr = 2015
abMonat = 10
abTag = 12

# 'abDatum' ist ist nur ein Platzhalter und **muss** entweder durch den mittels '--datum' übergebenen
# Wert oder durch das Datum des ersten Datensatzes aus der Quelldatei geändert werden!
abDatum = zeit.date(abJahr, abMonat, abTag).isoformat()

# 'bisDatum' ist ebenfalls nur ein Platzhalter und **muss** durch das Datum des
# letzten Datensatzes aus der Quelldatei geändert werden!
bisDatum = zeit.date.today().isoformat()


# Meine Funktionen

def datum_entspricht_iso8601(eingegebenes_datum=abDatum):
    """
    Prüft, ob das übergebene Datum der ISO 8601:2004 entspricht.
    Zeitpunkte vor 2000-01-01 werden ignoriert!
    Siehe auch https://de.wikipedia.org/wiki/Datumsformat#ISO_8601_und_EN_28601

    :param eingegebenes_datum: String
    :return: Boolian
    """
    iso8601_regex = r"(20[0-9]{2})(-?)(1[0-2]|0[1-9])\2(3[01]|0[1-9]|[12][0-9])\Z"
    iso8601_muster = regex.compile(iso8601_regex)

    if iso8601_muster.fullmatch(eingegebenes_datum):
        return True
    else:
        return False


def datum_entspricht_din5008(eingegebenes_datum=abDatum):
    """
    Prüft ob das übergebene Datum der DIN 5008 entspricht.
    Zeitpunkte vor 2000-01-01 werden ignoriert!
    Siehe auch https://de.wikipedia.org/wiki/Datumsformat#DIN_5008.

    :param eingegebenes_datum: String
    :return: Boolian
    """
    din5008_regex = r"(3[0-1]|2[0-9]|1[0-9]|0[1-9])\.(1[0-2]|0[1-9])\.20([0-9]{2})\Z"
    din5008_muster = regex.compile(din5008_regex)

    if din5008_muster.fullmatch(eingegebenes_datum):
        return True
    else:
        return False


def ist_datum_valide(eingegebenes_datum=abDatum):
    """
    Prüft, ob das übergebene Datum auch gültig ist.
    Dabei wird zwischen den Datumsformaten ISO 8601:2004 und DIN 5008 unterschieden.
    Wird kein Datumsformat übergeben, wird das Format ISO 8601:2004 verwendet.

    :param eingegebenes_datum: String
    :return: Boolian
    """

    datumsformat = None
    tag = None
    monat = None
    jahr = None

    if datum_entspricht_iso8601(eingegebenes_datum):
        datumsformat = 'iso8601'

    if datum_entspricht_din5008(eingegebenes_datum):
        datumsformat = 'din5008'

    if datumsformat == 'iso8601':
        liste = eingegebenes_datum.split('-')

        for _ in liste:
            tag = int(liste.pop())
            monat = int(liste.pop())
            jahr = int(liste.pop())


    elif datumsformat == 'din5008':
        liste = eingegebenes_datum.split('.')

        for _ in liste:
            jahr = int(liste.pop())
            monat = int(liste.pop())
            tag = int(liste.pop())
    else:
        tag = 0
        monat = 0
        jahr = 0

    # Prüfen, ob Schaltjahr oder nicht
    tage_im_monat = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    if monat == 2 and jahr % 4 == 0 and (jahr % 100 != 0 or jahr % 400 == 0):
        if 1 <= tag <= 29:
            return True
        else:
            return False
    elif monat >= 1 and tag <= tage_im_monat[monat - 1]:
        return True
    else:
        return False


def ab_datum_nach_applehealth_datum(eingegebenes_datum=abDatum):
    """
    Konvertiert das übergebene Datum in das AppleHealth-Format '%d-%b-%Y'.

    :param eingegebenes_datum: String
    :return: iso_datum.strftime('%d-%b-%Y')
    """

    tag = None
    monat = None
    jahr = None
    ah_datum = None
    datumsformat = None

    if datum_entspricht_iso8601(eingegebenes_datum):
        datumsformat = 'iso8601'

    if datum_entspricht_din5008(eingegebenes_datum):
        datumsformat = 'din5008'

    if datumsformat == 'iso8601':
        liste = eingegebenes_datum.split('-')

        for _ in liste:
            tag = int(liste.pop())
            monat = int(liste.pop())
            jahr = int(liste.pop())

    elif datumsformat == 'din5008':
        liste = eingegebenes_datum.split('.')

        for _ in liste:
            jahr = int(liste.pop())
            monat = int(liste.pop())
            tag = int(liste.pop())

    else:
        print("Fehler: kein ah_datum")
        return ah_datum

    ah_datum = zeit.datetime(jahr, monat, tag).strftime('%d-%b-%Y')
    return ah_datum


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
    neues_abDatum = argumente.datum

    if ist_datum_valide(neues_abDatum):
        print("\033[0;33mEs werden nur Datensätze ab dem Datum {0} verarbeitet.\033[0m".format(argumente.datum))
        abDatum = neues_abDatum
    else:
        print("\n\033[0;31mDas übergebene Datum {0} ist ungültig!\033[0m".format(argumente.datum))
        print("Das Datum muss der ISO 8601:2004 oder der DIN 5008 (4stellige Jahreszahl) entsprechen.")
        print("\033[0;33mHINWEIS:\033[0m Ein Datum vor dem 01.01.2000 wird ignoriert!")
        print("\n\033[1;37mBeispiele:\033[1;32m")
        print("    - 01.01.2000")
        print("    - 2000-12-31")
        print("    - 2001-01-01")
        print("    - 11.11.2001")
        print("\033[0m")
        exit(1)

# 3. Eingabe-Datei als CSV-Datei öffnen/einlesen.
print("\n\nDatei einlesen …")
csvQuelle = open(quelldatei)
csvQuelldatenLeser = csv.reader(csvQuelle)

# 4. Ziel-Datei öffnen
print("\nDaten schreiben …")
csvZiel = open(zieldatei, 'w')

# 5. Kopfzeilen schreiben
print('Blutzuckerwerte von {0} bis {1}'.format(abDatum, bisDatum))
csvFeldnamen = ['Datum', 'Uhrzeit', 'Blutzuckerwert (md/dL)']
csvZieldatenSchreiber = csv.DictWriter(csvZiel, fieldnames=csvFeldnamen)
csvZieldatenSchreiber.writeheader()

# 7. Solange Daten aus der Quell-Datei lesen, bis das Dateiende erreicht ist.
# @TODO: Tritt währenddessen ein Fehler auf, brechen wir das Programm mit einer Fehlermeldung ab.

for zeile in csvQuelldatenLeser:
    # 8. Wurde ein Datum übergeben, müssen wir prüfen, ob der eingelesen Datensatz dazu passt.
    # @TODO: Dazu müssen wir das angegebene Datum in das Format
    # @TODO:    'DD-[Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]-YYYY' umwandeln.

    applehealthDatum = ab_datum_nach_applehealth_datum(abDatum)


    # @TODO: Wenn es zu diesem Tag keinen Datensatz gibt, wird das nächstfolgende Datum als neuer Startpunkt verwendet.
    # @TODO: Und zwar solange, bis das Dateiende der Eingabe-Datei erreicht ist.
    # @TODO: Finden wir keinen Startpunkt, dann brechen wir das Programm mit einer Fehlermeldung ab.
    #
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
print("\033[1;32m")
print("Konvertierung abgeschlossen.")
print("Die Datei {0} kann nun an den Diabetologen gesendet werden.".format(zieldatei))
print("\033[0m")
