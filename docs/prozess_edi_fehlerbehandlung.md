# Prozessanweisung EDI-Fehlerbehandlung

Version 1.4, gültig ab 15.02.2026. Ersetzt Version 1.2. Gültig für alle Standorte der Musterlogistik GmbH.

## Zweck und Geltungsbereich

Diese Prozessanweisung regelt, wie fehlerhafte oder fehlende EDI-Nachrichten erkannt, zugeordnet und bearbeitet werden. Sie gilt für die Disposition, die Kundenteams, die Schichtleitungen im Wareneingang und Versand sowie für den EDI-Support der IT. Die Anweisung beschreibt nur den Umgang mit dem Nachrichtenfehler selbst. Was mit der physischen Ware passiert, regeln die Arbeitsanweisung Wareneingang und die kundenspezifischen Regelungen; diese gehen vor, wenn sie etwas anderes festlegen.

An den Standorten Süd und Nord läuft der EDI-Verkehr über denselben Konverter. Der Standort West wird nach seiner Inbetriebnahme an denselben Konverter angebunden; bis dahin gelten für ihn eigene Übergangsregeln.

## Begriffe und Nachrichtentypen

Wir verarbeiten im Tagesgeschäft vier Nachrichtentypen im Format EDIFACT. Jede Nachricht wird im Konverter geprüft, bevor sie an das Lagerverwaltungssystem (LVS) übergeben wird. Fällt die Prüfung durch, landet die Nachricht im Fehlerpostfach des Konverters und erhält einen Fehlercode.

### DESADV (Lieferavis)

Der DESADV kündigt eine Anlieferung an. Er enthält Lieferantennummer, Packstücke, Artikel, Mengen und je nach Kunde auch Chargen oder SSCC-Nummern. Ohne verarbeiteten DESADV legt das LVS keine erwartete Anlieferung an, und die Ware kann am Tor nicht gegen ein Avis gebucht werden.

### ORDERS (Auftrag)

Mit der ORDERS schickt der Kunde Auslieferaufträge. Für die Tagesplanung zählt der Zeitpunkt, an dem die ORDERS fehlerfrei im LVS angekommen ist, nicht der Sendezeitpunkt beim Kunden. Eine ORDERS, die um 12:50 Uhr gesendet wird, aber wegen eines Fehlers erst um 13:20 Uhr verarbeitet ist, gilt als nach dem Annahmeschluss eingegangen.

### INVRPT (Bestandsmeldung)

Die INVRPT ist unsere Bestandsmeldung an den Kunden. Sie wird bei den meisten Kunden täglich um 23:00 Uhr automatisch erzeugt. Fehler entstehen hier nicht beim Empfang, sondern beim Versand: Der Kunde lehnt die Nachricht ab oder bestätigt sie nicht.

### RECADV (Wareneingangsbestätigung)

Die RECADV bestätigt dem Kunden, welche Mengen tatsächlich gebucht wurden. Sie wird mit dem Abschluss der Wareneingangsbuchung erzeugt. Abweichungen zwischen DESADV und RECADV werden beim Kunden als Mengendifferenz sichtbar.

## Zuständigkeiten

| Rolle | Aufgabe im EDI-Fehlerprozess |
|---|---|
| EDI-Support (IT) | Überwachung des Fehlerpostfachs, technische Fehler, Stammdaten im Konverter, Neuversand |
| Disposition | Inhaltliche Klärung von ORDERS-Fehlern, Priorisierung gegen Abholzeiten |
| Kundenteam | Klärung mit Kunde und Lieferant, Anforderung fehlender Avise, Freigabe manueller Anlage |
| Schichtleitung Wareneingang | Meldung physischer Anlieferungen ohne verarbeiteten DESADV, Entscheidung über Sperrlager |
| Bestandsführung | Klärung von INVRPT- und RECADV-Differenzen, Korrekturbuchungen |

Der EDI-Support ist montags bis freitags von 6:00 bis 22:00 Uhr besetzt. Außerhalb dieser Zeit übernimmt die IT-Rufbereitschaft nur Fehler der Klasse 1 (siehe Eskalation).

## Fehlercodes

Der Konverter vergibt für jeden Fehler einen dreistelligen Code mit dem Präfix „EDI“. Die erste Ziffer gibt die Fehlergruppe an: 1 für Syntax und Übertragung, 2 für Stammdaten, 3 für Inhalt, 4 für Zeitfehler und fehlende Rückmeldungen. Die folgende Tabelle enthält die häufigsten Codes. Seltene Codes sind im Handbuch des Konverters beschrieben.

| Code | Nachrichtentyp | Bedeutung | Zuständig | Bearbeitungsfrist |
|---|---|---|---|---|
| EDI-101 | alle | Syntaxfehler, Nachricht nicht lesbar | EDI-Support | 2 Stunden |
| EDI-104 | alle | Doppelte Nachrichtenreferenz, Nachricht bereits verarbeitet | EDI-Support | 4 Stunden |
| EDI-210 | DESADV | Lieferantennummer unbekannt | Kundenteam | 4 Stunden |
| EDI-215 | ORDERS | Lieferadresse (GLN) nicht im Stamm | EDI-Support | 2 Stunden |
| EDI-220 | DESADV, ORDERS | Artikelnummer nicht angelegt | Kundenteam | 4 Stunden |
| EDI-310 | DESADV | Menge in Packstücken und Positionen widersprüchlich | Kundenteam | 4 Stunden |
| EDI-325 | ORDERS | Gewünschtes Lieferdatum liegt in der Vergangenheit | Disposition | 1 Stunde |
| EDI-330 | DESADV | Charge oder Verfallsdatum fehlt bei chargenpflichtigem Artikel | Kundenteam | 2 Stunden |
| EDI-340 | RECADV | Gebuchte Menge weicht vom DESADV ab | Bestandsführung | 1 Arbeitstag |
| EDI-410 | INVRPT | Keine Empfangsbestätigung vom Kunden nach 2 Stunden | EDI-Support | 1 Arbeitstag |
| EDI-420 | DESADV | Ware am Tor, aber kein DESADV vorhanden | Schichtleitung / Kundenteam | sofort |

Wichtig: EDI-420 ist kein Fehler des Konverters, sondern wird von der Schichtleitung im LVS manuell ausgelöst, wenn eine Anlieferung ohne Avis vor dem Tor steht. Damit wird der Fall im selben Postfach geführt wie die technischen Fehler.

## Ablauf bei einem EDI-Fehler

1. Der EDI-Support prüft das Fehlerpostfach zu Schichtbeginn und danach mindestens stündlich. Neue Fehler werden mit Uhrzeit, Code und Kunde in die Fehlerliste übernommen.
2. Der EDI-Support entscheidet anhand der Fehlercode-Tabelle, wer zuständig ist, und weist den Fall im Postfach der zuständigen Rolle zu.
3. Technische Fehler (Gruppe 1 und Konverter-Stammdaten) behebt der EDI-Support selbst und fordert, wenn nötig, beim Absender einen Neuversand an.
4. Inhaltliche Fehler klärt die zuständige Rolle mit dem Kunden oder Lieferanten. Die Klärung wird im Fall dokumentiert, nicht per E-Mail außerhalb des Systems.
5. Nach der Korrektur wird die Nachricht erneut eingespielt. Eine manuelle Anlage im LVS ist nur mit schriftlicher Freigabe des Kundenteams erlaubt und wird im Fall als „manuell angelegt“ markiert.
6. Der Fall wird erst geschlossen, wenn die Nachricht im LVS verarbeitet ist und die Folgeprozesse (Buchung, Kommissionierung, Bestandsmeldung) wieder laufen.

## Besonderheiten je Nachrichtentyp

### Fehlender oder fehlerhafter DESADV

Steht Ware am Tor und ist kein DESADV verarbeitet, löst die Schichtleitung EDI-420 aus. Was mit der Ware geschieht, richtet sich nach dem Kunden:

- Altmann Automotive: Ware wird nicht gebucht und im Sperrlager SP-02 abgestellt; die Schichtleitung informiert den Disponenten des Kundenteams innerhalb von 30 Minuten.
- Brenner Elektronik: Ware wird im Sperrlager SP-04 abgestellt; Meldung an das Kundenteam innerhalb von 60 Minuten.
- Holtz Möbel: Ware wird unter Vorbehalt gebucht.
- Frischland Feinkost: Kühlware wird angenommen und im Kühlbereich K2 auf dem Klärplatz abgestellt.
- Alle anderen Kunden: Annahme nur nach Rücksprache mit der Schichtleitung, wie in der Arbeitsanweisung Wareneingang beschrieben.

Ist der DESADV zwar vorhanden, aber mit EDI-310 oder EDI-330 abgelehnt, wird die Ware behandelt, als läge kein Avis vor. Der DESADV gilt erst als vorhanden, wenn er fehlerfrei verarbeitet ist.

### ORDERS-Fehler und Annahmeschluss

ORDERS-Fehler haben Vorrang vor allen anderen Fehlern, weil sie direkt die Versandleistung des Tages betreffen. Die Disposition prüft bei jedem ORDERS-Fehler, ob der Auftrag noch die Abholung des Tages erreichen kann. Wird ein Auftrag erst nach 13:00 Uhr fehlerfrei verarbeitet, geht er grundsätzlich am nächsten Werktag raus. Eine Ausnahme ist nur möglich, wenn das Kundenteam sie schriftlich anordnet und die Schichtleitung Versand zustimmt.

### INVRPT-Fehler

Bleibt die Empfangsbestätigung des Kunden aus (EDI-410), sendet der EDI-Support die Bestandsmeldung am nächsten Morgen erneut. Lehnt der Kunde die Meldung zwei Tage hintereinander ab, wird das Kundenteam informiert, weil der Kunde dann mit veralteten Beständen plant.

### RECADV-Differenzen

Eine Differenz zwischen DESADV und RECADV (EDI-340) ist meist kein technischer Fehler, sondern eine echte Mengenabweichung im Wareneingang. Die Bestandsführung prüft, ob die Abweichung bereits im LVS erfasst und dem Kunden gemeldet wurde. Für die Meldefrist an den Kunden gilt die Arbeitsanweisung Wareneingang.

## Eskalation

Fehler werden nach ihrer Auswirkung in drei Klassen eingeteilt. Die Klasse bestimmt, wer wann informiert wird.

| Klasse | Beschreibung | Beispiel | Eskalation |
|---|---|---|---|
| Klasse 1 | Konverter steht oder alle Nachrichten eines Kunden fallen durch | EDI-101 bei jeder ORDERS eines Kunden | sofort IT-Rufbereitschaft und Standortleitung |
| Klasse 2 | Einzelne Aufträge oder Anlieferungen blockiert | EDI-215 bei einem Expressauftrag | nach Ablauf der Bearbeitungsfrist an die Teamleitung des Kundenteams |
| Klasse 3 | Keine unmittelbare Auswirkung auf Ware | EDI-410 einer einzelnen Bestandsmeldung | Wochenbericht des EDI-Supports |

Wird die Bearbeitungsfrist aus der Fehlercode-Tabelle überschritten, steigt ein Fehler der Klasse 3 automatisch in Klasse 2 auf. Eine Herabstufung ist nur durch den EDI-Support möglich.

## Ausnahmen

- Bei einem Ausfall des gesamten Lagerverwaltungssystems gilt nicht diese Anweisung, sondern der Notfallprozess in der Prozessanweisung Handscanner und IT-Störungen.
- Anlieferungen von Zollware werden auch bei vorhandenem DESADV erst nach den Regeln der Prozessanweisung Zollabwicklung gebucht.
- Kunden, die keinen EDI-Anschluss haben, avisieren über das Lieferantenportal. Fehler im Portal meldet das Kundenteam direkt an den EDI-Support, ein Fehlercode wird dafür nicht vergeben.

## Mitgeltende Dokumente

- Arbeitsanweisung Wareneingang (alle Standorte), Version 3.2
- Kundenspezifische Regelungen Altmann Automotive, Brenner Elektronik, Holtz Möbel, Frischland Feinkost
- Prozessanweisung Handscanner und IT-Störungen (prozess_it_stoerungen_handscanner.md)
- Prozessanweisung Schichtübergabe und Schichtbuch (prozess_schichtuebergabe.md)
- Prozessanweisung Zollabwicklung und Versandverfahren T1 (prozess_zollabwicklung_t1.md)
