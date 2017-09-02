#!/usr/bin/env python3

import argparse
import csv
import datetime as zeit
import re as regex

# Meine Variablen
quelldatei = None
zieldatei = None
datumsformat_zieldatei = 'din5008'
kopfzeile_geschrieben = False

# 'abDatum' ist ist nur ein Platzhalter und **muss** entweder durch den mittels '--datum' übergebenen
# Wert oder durch das Datum des ersten Datensatzes aus der Quelldatei geändert werden!
abDatum = None

# 'bisDatum' wird initial auf das aktuelle Datum im Datumsformat ISO 8601:2004 gesetzt.
# Wird der Schalter --datum verwendet, richtet sich das Datumsformat an das übergebene abDatum.
bisDatum = zeit.date.today().strftime('%Y-%m-%d')

# 'applehealth_Datum' enhält ein Datum im Datumsformat '%d-%b-%Y' und hat anfangs keinen Wert zugewiesen.
applehealthDatum = None


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

        ah_datum = zeit.datetime(jahr, monat, tag).strftime('%d-%b-%Y')

    if datumsformat == 'din5008':
        liste = eingegebenes_datum.split('.')

        for _ in liste:
            jahr = int(liste.pop())
            monat = int(liste.pop())
            tag = int(liste.pop())

        ah_datum = zeit.datetime(jahr, monat, tag).strftime('%d-%b-%Y')

    return ah_datum


def ah_datum_nach_ab_datum(eingegebenes_datum, datumsformat):
    """
    Konvertiert das im AppleHealth-Format übergebene Datum in das in gefordert Datumsformat.

    :param eingegebenes_datum: iso_datum.strftime('%d-%b-%Y')
    :param datumsformat: iso8601 || din5008
    :return: String mit Datum nach ISO 8601:2004- oder DIN 5008-Format
    """

    monate = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    tag = None
    abk_monat = None
    jahr = None
    ab_datum = None
    liste = eingegebenes_datum.split('-')

    for _ in liste:
        jahr = int(liste.pop())
        abk_monat = str(liste.pop())
        tag = int(liste.pop())

    if abk_monat in monate:
        monat = monate[abk_monat]

        if datumsformat == 'iso8601':
            ab_datum = zeit.datetime(jahr, monat, tag).strftime('%Y-%m-%d')

        if datumsformat == 'din5008':
            ab_datum = zeit.datetime(jahr, monat, tag).strftime('%d.%m.%Y')

    return ab_datum


def erzeuge_date_objekt(eingelesenes_datum):
    """
    Prüft das Datumsformat des Strings datum,
    zerlegt es in Jahr, Monat und Tag
    und erzeugt daraus ein Objekt vom Typ datetime.date()
    :param eingelesenes_datum:
    :return: datetime.date(datum.jahr, datum.monat, datum.tag)
    """
    tag = None
    monat = None
    jahr = None
    datumsformat = None
    date_objekt = None

    if datum_entspricht_iso8601(eingelesenes_datum):
        datumsformat = 'iso8601'

    if datum_entspricht_din5008(eingelesenes_datum):
        datumsformat = 'din5008'

    if datumsformat == 'iso8601':
        liste = eingelesenes_datum.split('-')

        for _ in liste:
            tag = int(liste.pop())
            monat = int(liste.pop())
            jahr = int(liste.pop())

        date_objekt = zeit.date(jahr, monat, tag)

    if datumsformat == 'din5008':
        liste = eingelesenes_datum.split('.')

        for _ in liste:
            jahr = int(liste.pop())
            monat = int(liste.pop())
            tag = int(liste.pop())

        date_objekt = zeit.date(jahr, monat, tag)

    return date_objekt


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
        if datum_entspricht_din5008(abDatum):
            bisDatum = zeit.date.today().strftime('%d.%m.%Y')
        if datum_entspricht_iso8601(abDatum):
            bisDatum = zeit.date.today().strftime('%Y-%m-%d')
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
print("Daten schreiben …\n")
csvZiel = open(zieldatei, 'w', newline='')
csvFeldnamen = ['Datum', 'Uhrzeit', 'Blutzuckerwert (md/dL)']
csvZieldatenSchreiber = csv.DictWriter(csvZiel, fieldnames=csvFeldnamen)

# 5. Solange Daten aus der Quell-Datei lesen, bis das Dateiende erreicht ist.
input_regex = r"\[\'\d{2}-\D{3}-\d{4}\s+\d{2}:\d{2}\',\s+\'\d{2}-\D{3}-\d{4}\s+\d{2}:\d{2}\',\s+\'\d+\.\d+\'\]\Z"
input_muster = regex.compile(input_regex)

for zeile in csvQuelldatenLeser:
    if input_muster.fullmatch(str(zeile)):
        # @TODO: Ausgabeformat beim Aufruf des Programm festlegen
        # 6.1 Wurde ein Datum mit --datum übergeben?
        if abDatum:
            if kopfzeile_geschrieben:
                applehealthDatum = ab_datum_nach_applehealth_datum(abDatum)
                zeitstempel = str(zeile[0])
                datum = ah_datum_nach_ab_datum(zeitstempel.split(' ')[0], datumsformat_zieldatei)

                # Dann müssen wir prüfen, ob der eingelesen Datensatz dazu passt.
                tmp_datum = erzeuge_date_objekt(datum)
                tmp_abDatum = erzeuge_date_objekt(abDatum)

                if tmp_datum < tmp_abDatum:
                    continue
                else:
                    uhrzeit = str(zeitstempel.split(' ')[1])
                    blutzuckerwert = int(str(zeile[2]).split('.')[0])
                    csvZieldatenSchreiber.writerow(
                        {
                            'Uhrzeit'               : uhrzeit,
                            'Datum'                 : datum,
                            'Blutzuckerwert (md/dL)': blutzuckerwert
                        }
                    )
            else:
                print('Blutzuckerwerte von {0} bis {1}'.format(abDatum, bisDatum))
                csvZiel.write('Blutzuckerwerte von {0} bis {1}\r\n'.format(abDatum, bisDatum))
                csvZieldatenSchreiber.writeheader()
                kopfzeile_geschrieben = True
        # 6.2 Ansonsten wandeln wir alle Datensätze um
        else:
            if kopfzeile_geschrieben:
                zeitstempel = str(zeile[0])
                datum = ah_datum_nach_ab_datum(zeitstempel.split(' ')[0], datumsformat_zieldatei)
                uhrzeit = str(zeitstempel.split(' ')[1])
                blutzuckerwert = int(str(zeile[2]).split('.')[0])
                csvZieldatenSchreiber.writerow(
                    {
                        'Uhrzeit'               : uhrzeit,
                        'Datum'                 : datum,
                        'Blutzuckerwert (md/dL)': blutzuckerwert
                    }
                )
            else:
                ausgelesenes_abDatum = str(zeile[0]).split(' ')[0]
                print('Blutzuckerwerte von {0} bis {1}'.
                      format(ah_datum_nach_ab_datum(ausgelesenes_abDatum, 'iso8601'), bisDatum))
                csvZiel.write(str('Blutzuckerwerte von {0} bis {1}\r\n'.
                                  format(ah_datum_nach_ab_datum(ausgelesenes_abDatum, 'iso8601'), bisDatum)))
                csvZieldatenSchreiber.writeheader()
                kopfzeile_geschrieben = True
    else:
        continue

# 7. Quell- und Zieldatei schliesen.
csvZiel.close()
csvQuelle.close()

# 8. Rückmeldung an den Benutzer geben.
print("\033[1;32m")
print("Konvertierung abgeschlossen.")
print("Die Datei {0} kann nun an den Diabetologen gesendet werden.".format(zieldatei))
print("\033[0m")
