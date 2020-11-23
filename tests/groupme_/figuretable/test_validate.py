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
Korotkow-Geräusche bei der auskultatorischen Blutdruckmessung [Elt01]
Manschettendruckverlauf und Oszillationen bei der oszillometrischen Blutdruckmessung [Elt01]
Volumenkompensationsmethode nach Penaz [Elt01]
Messverfahren nach R. Aaslid und AO. Brubakk [Aas81]
Schematische Darstellung einer aufgesetzten Ultraschall-Doppler-Sonde [Pau11]
Grundstruktur des Regelkreises [nach Lun10]
Digitalisierung mit Abtast-Halteglied [Reu08]
Sprungantwort eines idealen PI-Reglers
Einfache LabVIEW-Operation
Blutdruckverlauf während eines Valsalva-Manövers
Bestehender Versuchsaufbau vor der Optimierung
Blockdiagramm des ersten Modellentwurfs
Optimierung der Regelschleife - Zeitsteuerung Messschleife
Optimierung der Regelschleife - Puffer nach dem „FIFO“-Prinzip
Optimierung der Regelschleife - Regelalgorithmus (PI)
Valsalva-Press-Versuch mit altem Aufbau
Valsalva-Press-Versuch mit neuem Aufbau
Spannungsverteiler und 24V-Netzteil
Verteilerplatine
Registerkartenelement "Voreinstellungen" der Bedienoberfläche
Registerkartenelement "Wiedergabe" der Bedienoberfläche mit gespeicherter Messung
Frontpanel des Messprogramms
Optimierte Sondenfixierung
Struktur- und Signalflussplan - Legende
Struktur- und Signalflussplan - Übersicht Laboraufbau
Struktur- und Signalflussplan - Detailansicht Druckerzeugungseinheit
Struktur- und Signalflussplan - Detailansicht Mess-PC
Auswertung der Testmessungen - Beispiel für oszillometrische Messung
Auswertung der Testmessungen - Vergleich der ermittelten MAP-Werte
Auswertung der Testmessungen - Qualität der oszillometrischen Anpassung"""


def bachelor63(toc: iamraw.Toc):
    figures = merge_required(toc)
    assert figures == FIGURETABLE_BACHELOR63, figures


# TODO: REMOVE TAB 1
FIGURETABLE_MASTER75 = """\
Lage Neunkirchens (Quelle: Google Maps (2017), eigene Darstellung)
Untersuchungsgebiete in Neunkirchen (Datengrundlage: Google Maps (2017), eigene Darstellung)
Fragebogen – Seite 1
Fragebogen – Seite 2
Besuchsfrequenz – Neunkirchen Männer
Besuchsfrequenz – Neunkirchen Frauen
Besuchsfrequenz – Standort Innenstadt Männer
Besuchsfrequenz – Standort Innenstadt Frauen
Besuchsfrequenz – Standort Panoramapark Männer
Besuchsfrequenz – Standort Panoramapark Frauen
Besuchsfrequenz – Standort Am Spitz Männer
Besuchsfrequenz – Standort Am Spitz Frauen
Besuchsfrequenz – Standort Sonstige Männer
Besuchsfrequenz – Standort Sonstige Frauen
Art der Anreise – Neunkirchen
Art der Anreise – Männer
Art der Anreise – Frauen
Art d. Anreise – Standort Innenstadt Männer
Art d. Anreise – Standort Innenstadt Frauen
Art d. Anreise – Standort Panoramapark Männer
Art d. Anreise – Standort Panoramapark Frauen
Art d. Anreise – Standort Am Spitz Männer
Art d. Anreise – Standort Am Spitz Frauen
Art d. Anreise – Standort Sonstige Männer
Art d. Anreise – Standort Sonstige Frauen
Besuchsgrund Neunkirchen
Besuchsgrund – Standort Innenstadt
Besuchsgrund – Standort Panoramapark
Besuchsgrund – Standort Am Spitz
Besuchsgrund – Standort Sonstige
Kundenbedürfnisse Neunkirchen
Besucherzufriedenheit – Neunkirchen
Besucherzufriedenheit – Standort Innenstadt
Besucherzufriedenheit – Standort Panoramapark
Besucherzufriedenheit – Standort Am Spitz
Besucherzufriedenheit – Standort Sonstige
Bildungsstand – Bezirk Neunkirchen Männer
Bildungsstand – Bezirk Neunkirchen Frauen
Bildungsstand – Befragungsteilnehmer Männer
Bildungsstand – Befragungsteilnehmer Frauen
Bildungsstand nach Standort (Männer)
Bildungsstand nach Standort (Frauen)
Herkunft aller Untersuchungsteilnehmer
Herkunft – Neunkirchen Männer
Herkunft – Neunkirchen Frauen
Herkunft – Standort Innenstadt
Herkunft – Standort Innenstadt Männer
Herkunft – Standort Innenstadt Frauen
Herkunft – Standort Panoramapark
Herkunft – Standort Panoramapark Männer
Herkunft – Standort Panoramapark Frauen
Herkunft – Standort Am Spitz
Herkunft – Standort Am Spitz Männer
Herkunft – Standort Am Spitz Frauen
Herkunft – Standort Sonstige
Herkunft – Standort Sonstige Männer
Herkunft – Standort Sonstige Frauen
Haushaltseinkommen netto – Neunkirchen
Übersicht Haushaltseinkommen netto (Prozent)
Wohnsituation in Neunkirchen (Prozent)
Wohnsituation nach Standorten in Prozent
Alternative Einkaufsorte
Herkunft der Untersuchungsteilnehmer (1) (Quelle: Bobek u. Fesl (1978), eig. Darstellung)
Herkunft der Untersuchungsteilnehmer (2) (Quelle: Google Maps (2017), eig. Darstellung)
Besuchsfrequenz – Neunkirchen
Besuchsfrequenz nach Standorten
Besuchsgrund in Neunkirchen, geschlechterdifferenziert
Besuchsgrund nach Standorten (ab 4 Nennungen)
Besuchsgrund in Neunkirchen – Auswärtige Besucher, geschlechterdifferenziert
Besuchsgrund in Neunkirchen – Auswärtige
Besuchsgrund in Neunkirchen – Einheimische
Nicht befriedigte Einkaufsbedürfnisse
Alternative Einkaufsorte
Art der Anreise – Männer
Art der Anreise – Frauen
Besucherzufriedenheit nach Standorten
Wohnsituation relativ nach Altersklassen
Einkommenssituation relativ nach Altersklassen
Bildungsstand relativ nach Altersklassen
Zufriedenheit nach Altersgruppen und Geschlecht, alle Standorte
Zufriedenheit Standort Innenstadt nach Alter und Geschlecht
Zufriedenheit Standort Panoramapark nach Alter und Geschlecht
Zufriedenheit Standort Am Spitz nach Alter und Geschlecht
Zufriedenheit Standort Sonstige nach Alter und Geschlecht
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
