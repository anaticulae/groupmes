# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import pytest
import utila
import utilatest

import tests.groupme_.figuretable


def merge_required(toc: iamraw.Toc) -> str:
    result = []

    def recursive(item, level):
        result = []
        result.append('    ' * level + item.title)
        assert item.raw_location >= 0, str(item)
        if item.children:
            for child in item.children:
                result.extend(recursive(child, level + 1))
        return result

    for item in toc:
        result.extend(recursive(item, level=0))
    titles = utila.NEWLINE.join(result)
    return titles


FIGURETABLE_BACHELOR90 = """\
Verknüpfung klassisches und AUTOSAR-Steuergerät
linearer Bus und ein Einzelstern nach [WL11]
Pegel bei der NRZ-Datenübertragung
Nominelle Potentiale nach [WR10, Seite 214]
Buszugriff Abitrierungsphase nach [WR10, Seite 216]
CAN-Nachricht nach [WL11, Seite 19]
Generierung für abstrakte Schnittstelle nach [Rum05, Seite 61]
Parametrisierte Codegenerierung nach [Rum05, Seite 62]
Kapselung der Zugriffe nach [JL07, Seite 389]
Handgeschriebenes System
Zusammengesetztes System
Komplett integriertes System
Umsetzung des Treiberkonzepts in Simulink nach [mat12a]
S-Function Builder mit vier Eingangsports und einem Ausgangs- ports sowie ein S-Funktion-Block
Möglichkeiten des Testens nach [JL07, Seite 253]
Testfall durchführen nach [JL07, Seite 258]
Ablauf Regressionstest nach [Lig09, Seite 194]
MiL-Prinzip nach [Plu06, Seite 3]
SiL-Prinzip
Allgemeine Einordnung des Debuggings in den Testprozess nach [AT09, Abschnitt 8.2.3]
Drehgestell Sensorverteilung
Softwareentwicklung Übersicht
Allgemeiner Ablauf der Entwicklung
Allgemeiner Aufbau der Algorithmen
Allgemeiner Ablauf des Algorithmus
Nachrichtenformat
Deserialisierung der Nachrichten
Buffer Funktionsübersicht
Histogramm zur Durchmesserbestimmung
Einlesen vom Speicher
MiL-Test für das Histogramm
Manuelle Integration der Durchmesserberechnung
Integrationstest Einlesen
Manueller Test der Gesamtintegration
MiL-Test zum Histogramm
Integration Durchmesser
SiL- und HiL-Test auf der OBU und dem Entwicklungsrechner"""


def bachelor90(toc: iamraw.Toc):
    figures = merge_required(toc)
    assert figures == FIGURETABLE_BACHELOR90, figures


# TODO: Adjust layout parser

FIGURETABLE_BACHELOR37 = """\
SAM Skala in der 9-Punkte-Likert-Form
Mittelwerte der  N ormierungen v on  Lang et  a l. ( 2005)  und Libkuman et al. (2007)
Ergebnisse der Pilotstudie
Verlauf der 2-back-Aufgabe mit Beispiel eines Zielreizes
Zusammenfassung des ENBP-Versuchsablaufs
Überblick über die verschiedenen Inner- und Zwischensubjekt- faktoren für die statistische Datenanalyse im allgemeinen linea- ren Modell
Durchschnittliche R eaktionszeit pr o E NBP-Block  (korrekte un d falsche Reaktionen) in Prozent für unterschiedliche emotionale Qualitäten
Mittelwerte der  H erzfrequenzen z u den ei nzelnen M esszeit- punkten für die unterschiedlichen  emotionalen Qualitäten
Mittlere D ifferenz  der H erzfrequenz ( MDHF) über  di e dr ei v er- schiedenen emotionalen Qualitäten der ENBP-Blöcke
Modell der autonomen und kognitiven Verarbeitung emotionaler Stimuli und die Wirkung auf die Vermittlung durch die Mediator- variable Interozeptives Bewusstsein"""


def bachelor37(toc: iamraw.Toc):
    figures = merge_required(toc)
    assert figures == FIGURETABLE_BACHELOR37, figures


FIGURETABLE_BACHELOR63 = """\
Abbildung 1: Korotkow-Geräusche bei der auskultatorischen Blutdruckmessung [Elt01]
Abbildung 2: Manschettendruckverlauf und Oszillationen bei der oszillometrischen Blutdruckmessung [Elt01]
Abbildung 3: Volumenkompensationsmethode nach Penaz [Elt01]
Abbildung 4: Messverfahren nach R. Aaslid und AO. Brubakk [Aas81]
Abbildung 5: Schematische Darstellung einer aufgesetzten Ultraschall-Doppler-Sonde [Pau11]
Abbildung 6: Grundstruktur des Regelkreises [nach Lun10]
Abbildung 7: Digitalisierung mit Abtast-Halteglied [Reu08]
Abbildung 8: Sprungantwort eines idealen PI-Reglers
Abbildung 9: Einfache LabVIEW-Operation
Abbildung 10: Blutdruckverlauf während eines Valsalva-Manövers
Abbildung 11: Bestehender Versuchsaufbau vor der Optimierung
Abbildung 12: Blockdiagramm des ersten Modellentwurfs
Abbildung 13: Optimierung der Regelschleife - Zeitsteuerung Messschleife
Abbildung 14: Optimierung der Regelschleife - Puffer nach dem „FIFO“-Prinzip
Abbildung 15: Optimierung der Regelschleife - Regelalgorithmus (PI)
Abbildung 16: Valsalva-Press-Versuch mit altem Aufbau
Abbildung 17: Valsalva-Press-Versuch mit neuem Aufbau
Abbildung 18: Spannungsverteiler und 24V-Netzteil
Abbildung 19: Verteilerplatine
Abbildung 20: Registerkartenelement "Voreinstellungen" der Bedienoberfläche
Abbildung 21: Registerkartenelement "Wiedergabe" der Bedienoberfläche mit gespeicherter Messung
Abbildung 22: Frontpanel des Messprogramms
Abbildung 23: Optimierte Sondenfixierung
Abbildung 24: Struktur- und Signalflussplan - Legende
Abbildung 25: Struktur- und Signalflussplan - Übersicht Laboraufbau
Abbildung 26: Struktur- und Signalflussplan - Detailansicht Druckerzeugungseinheit
Abbildung 27: Struktur- und Signalflussplan - Detailansicht Mess-PC
Abbildung 28: Auswertung der Testmessungen - Beispiel für oszillometrische Messung
Abbildung 29: Auswertung der Testmessungen - Vergleich der ermittelten MAP-Werte
Abbildung 30: Auswertung der Testmessungen - Qualität der oszillometrischen Anpassung"""


def bachelor63(toc: iamraw.Toc):
    figures = merge_required(toc)
    assert figures == FIGURETABLE_BACHELOR63, figures


# TODO: REMOVE TAB 1
FIGURETABLE_MASTER75 = """\
Abb. 1: Lage Neunkirchens (Quelle: Google Maps (2017), eigene Darstellung)
Abb. 2: Untersuchungsgebiete in Neunkirchen (Datengrundlage: Google Maps (2017), eigene Darstellung)
Abb. 3: Fragebogen – Seite 1
Abb. 4: Fragebogen – Seite 2
Abb. 5: Besuchsfrequenz – Neunkirchen Männer
Abb. 6: Besuchsfrequenz – Neunkirchen Frauen
Abb. 7: Besuchsfrequenz – Standort Innenstadt Männer
Abb. 8: Besuchsfrequenz – Standort Innenstadt Frauen
Abb. 9: Besuchsfrequenz – Standort Panoramapark Männer
Abb. 10: Besuchsfrequenz – Standort Panoramapark Frauen
Abb. 11: Besuchsfrequenz – Standort Am Spitz Männer
Abb. 12: Besuchsfrequenz – Standort Am Spitz Frauen
Abb. 13: Besuchsfrequenz – Standort Sonstige Männer
Abb. 14: Besuchsfrequenz – Standort Sonstige Frauen
Abb. 15: Art der Anreise – Neunkirchen
Abb. 16: Art der Anreise – Männer
Abb. 17: Art der Anreise – Frauen
Abb. 18: Art d. Anreise – Standort Innenstadt Männer
Abb. 19: Art d. Anreise – Standort Innenstadt Frauen
Abb. 20: Art d. Anreise – Standort Panoramapark Männer
Abb. 21: Art d. Anreise – Standort Panoramapark Frauen
Abb. 22: Art d. Anreise – Standort Am Spitz Männer
Abb. 23: Art d. Anreise – Standort Am Spitz Frauen
Abb. 24: Art d. Anreise – Standort Sonstige Männer
Abb. 25: Art d. Anreise – Standort Sonstige Frauen
Abb. 26: Besuchsgrund Neunkirchen
Abb. 27: Besuchsgrund – Standort Innenstadt
Abb. 28: Besuchsgrund – Standort Panoramapark
Abb. 29: Besuchsgrund – Standort Am Spitz
Abb. 30: Besuchsgrund – Standort Sonstige
Abb. 31: Kundenbedürfnisse Neunkirchen
Abb. 32: Besucherzufriedenheit – Neunkirchen
Abb. 33: Besucherzufriedenheit – Standort Innenstadt
Abb. 34: Besucherzufriedenheit – Standort Panoramapark
Abb. 35: Besucherzufriedenheit – Standort Am Spitz
Abb. 36: Besucherzufriedenheit – Standort Sonstige
Abb. 37: Bildungsstand – Bezirk Neunkirchen Männer
Abb. 38: Bildungsstand – Bezirk Neunkirchen Frauen
Abb. 39: Bildungsstand – Befragungsteilnehmer Männer
Abb. 40: Bildungsstand – Befragungsteilnehmer Frauen
Abb. 41: Bildungsstand nach Standort (Männer)
Abb. 42: Bildungsstand nach Standort (Frauen)
Abb. 43: Herkunft aller Untersuchungsteilnehmer
Abb. 44: Herkunft – Neunkirchen Männer
Abb. 45: Herkunft – Neunkirchen Frauen
Abb. 46: Herkunft – Standort Innenstadt
Abb. 47: Herkunft – Standort Innenstadt Männer
Abb. 48: Herkunft – Standort Innenstadt Frauen
Abb. 49: Herkunft – Standort Panoramapark
Abb. 50: Herkunft – Standort Panoramapark Männer
Abb. 51: Herkunft – Standort Panoramapark Frauen
Abb. 52: Herkunft – Standort Am Spitz
Abb. 53: Herkunft – Standort Am Spitz Männer
Abb. 54: Herkunft – Standort Am Spitz Frauen
Abb. 55: Herkunft – Standort Sonstige
Abb. 56: Herkunft – Standort Sonstige Männer
Abb. 57: Herkunft – Standort Sonstige Frauen
Abb. 58: Haushaltseinkommen netto – Neunkirchen
Abb. 59: Übersicht Haushaltseinkommen netto (Prozent)
Abb. 60: Wohnsituation in Neunkirchen (Prozent)
Abb. 61: Wohnsituation nach Standorten in Prozent
Abb. 62: Alternative Einkaufsorte
Abb. 63: Herkunft der Untersuchungsteilnehmer (1) (Quelle: Bobek u. Fesl (1978), eig. Darstellung)
Abb. 64: Herkunft der Untersuchungsteilnehmer (2) (Quelle: Google Maps (2017), eig. Darstellung)
Abb. 65: Besuchsfrequenz – Neunkirchen
Abb. 66: Besuchsfrequenz nach Standorten
Abb. 67: Besuchsgrund in Neunkirchen, geschlechterdifferenziert
Abb. 68: Besuchsgrund nach Standorten (ab 4 Nennungen)
Abb. 69: Besuchsgrund in Neunkirchen – Auswärtige Besucher, geschlechterdifferenziert
Abb. 70: Besuchsgrund in Neunkirchen – Auswärtige
Abb. 71: Besuchsgrund in Neunkirchen – Einheimische
Abb. 72: Nicht befriedigte Einkaufsbedürfnisse
Abb. 73: Alternative Einkaufsorte
Abb. 74: Art der Anreise – Männer
Abb. 75: Art der Anreise – Frauen
Abb. 76: Besucherzufriedenheit nach Standorten
Abb. 77: Wohnsituation relativ nach Altersklassen
Abb. 78: Einkommenssituation relativ nach Altersklassen
Abb. 79: Bildungsstand relativ nach Altersklassen
Abb. 80: Zufriedenheit nach Altersgruppen und Geschlecht, alle Standorte
Abb. 81: Zufriedenheit Standort Innenstadt nach Alter und Geschlecht
Abb. 82: Zufriedenheit Standort Panoramapark nach Alter und Geschlecht
Abb. 83: Zufriedenheit Standort Am Spitz nach Alter und Geschlecht
Abb. 84: Zufriedenheit Standort Sonstige nach Alter und Geschlecht
Tab. 1: Stichprobenkonstruktion"""


def master75(toc: iamraw.Toc):
    figures = merge_required(toc)
    assert figures == FIGURETABLE_MASTER75, figures


TEN = tuple(range(10))


@pytest.mark.parametrize('source, validate, pages', [
    pytest.param(
        power.link(power.BACHELOR090_PDF),
        bachelor90,
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        id='bachelor90',
    ),
    pytest.param(
        power.link(power.BACHELOR037_PDF),
        bachelor37,
        (0, 1, 2, 3, 4),
        id='bachelor37',
    ),
    pytest.param(
        power.link(power.BACHELOR063_PDF),
        bachelor63,
        (59, 60, 61, 62),
        id='bachelor63',
    ),
    pytest.param(
        power.link(power.MASTER075_PDF),
        master75,
        (71, 72),
        id='master75',
    ),
])
@utilatest.longrun
def test_figuretable(source, validate, pages, monkeypatch, testdir):
    figuretable = tests.groupme_.figuretable.extract_figuretable(
        source,
        pages,
        monkeypatch,
        testdir,
    )
    validate(figuretable)
