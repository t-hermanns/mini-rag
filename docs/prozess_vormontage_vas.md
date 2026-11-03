# Prozessanweisung Vormontage und Value Added Services

Version 1.2, gültig ab 01.05.2026. Gültig für die Standorte Süd und Nord.

## Zweck und Geltungsbereich

Neben Lagerung und Versand erbringt die Musterlogistik GmbH für mehrere Kunden zusätzliche Leistungen, sogenannte Value Added Services (VAS). Dazu gehören Sequenzierung, Kitting (Zusammenstellen von Sets), Etikettieren, Umpacken, Displaybau und einfache Vormontagen. Diese Prozessanweisung legt fest, an welchem Arbeitsplatz welche Leistung erbracht wird, welche Prüfschritte vorgeschrieben sind und wer die Arbeit freigibt.

Kundenspezifische Vorgaben, etwa die Sequenzbelieferung für Altmann Automotive, gehen dieser Anweisung vor. Diese Anweisung ergänzt sie um die Regeln, die für alle VAS-Arbeitsplätze gleich sind.

## Die Arbeitsplätze V1 bis V4

| Arbeitsplatz | Standort | Lage | Leistungen | Hauptkunde |
|---|---|---|---|---|
| V1 | Süd | Halle 1, direkt an Tor 7 | Sequenzierung, Beladen von Sequenzgestellen | Altmann Automotive |
| V2 | Süd | Halle 2, innerhalb des ESD-Bereichs E1 | Kitting von elektronischen Bauteilen, Set-Bildung | Brenner Elektronik |
| V3 | Süd | Halle 2, neben dem Fachbodenregal FB-1 | Etikettieren, Umpacken, Displaybau, Beipackzettel | wechselnde Kunden |
| V4 | Nord | Halle A, an Tor 6 | Sichtprüfung und Neuverpackung von Möbelpackstücken, Montage von Beschlagbeuteln | Holtz Möbel |

V1 wird in anderen Dokumenten auch als „Vormontagezone V1“ bezeichnet. Gemeint ist derselbe Arbeitsplatz. Der Standort West erhält nach aktueller Planung einen eigenen VAS-Bereich; die Arbeitsplatzbezeichnungen dort werden in einer späteren Version ergänzt.

## Zuständigkeiten

- **VAS-Teamleitung**: plant die Belegung der Arbeitsplätze, weist Mitarbeitende zu und gibt Arbeitsanweisungen für neue Aufträge frei.
- **Mitarbeitende am Arbeitsplatz**: führen die Arbeit nach Arbeitskarte aus und dokumentieren jeden Prüfschritt im Lagerverwaltungssystem.
- **Prüfer (zweite Person)**: führt die Vier-Augen-Prüfung durch, wo sie vorgeschrieben ist. Prüfer darf nur sein, wer am betreffenden Arbeitsplatz eingewiesen ist und die Arbeit nicht selbst ausgeführt hat.
- **Kundenteam**: übermittelt neue oder geänderte Kundenvorgaben und stimmt Muster mit dem Kunden ab.
- **Qualitätsmanagement**: wertet Fehler aus und führt bei Kundenreklamationen den 8D-Prozess.

## Allgemeiner Ablauf eines VAS-Auftrags

1. Der VAS-Auftrag wird im Lagerverwaltungssystem aus dem Kundenauftrag erzeugt. Er enthält die Arbeitskarte mit Stückliste, Arbeitsschritten und Prüfschritten.
2. Der Mitarbeitende meldet sich am Arbeitsplatz an und scannt den Auftrag. Erst dann werden die benötigten Materialien zur Bereitstellung angefordert.
3. Das Material wird auf der Bereitstellfläche des Arbeitsplatzes abgestellt. Jede Bereitstellung wird gescannt, damit der Bestand auf den Arbeitsplatz umgebucht wird.
4. Der Mitarbeitende führt die Arbeitsschritte in der Reihenfolge der Arbeitskarte aus. Abweichungen von der Reihenfolge sind nicht erlaubt, auch wenn sie schneller wären.
5. Nach jedem Prüfschritt wird das Ergebnis im System bestätigt. Ein nicht bestandener Prüfschritt sperrt den Auftrag automatisch.
6. Nach Abschluss bucht der Mitarbeitende die fertigen Einheiten auf den Ausgangsplatz des Arbeitsplatzes. Reste werden zurückgebucht und zurück ins Lager gebracht.

## Prüfschritte

Jeder Arbeitsplatz hat festgelegte Prüfschritte. Die Prüfschritte sind auf der Arbeitskarte mit den Kürzeln PS-1 bis PS-8 gekennzeichnet. Nicht jeder Prüfschritt gilt an jedem Arbeitsplatz.

| Prüfschritt | Inhalt | Gilt für | Durchführung | Häufigkeit |
|---|---|---|---|---|
| PS-1 | Abgleich Artikelnummer gegen Arbeitskarte | V1, V2, V3, V4 | Scan durch Mitarbeitenden | jede Einheit |
| PS-2 | Mengenkontrolle je Set oder Gestell | V1, V2 | Zählung durch Mitarbeitenden | jede Einheit |
| PS-3 | Reihenfolgeprüfung im Sequenzgestell | V1 | Vier-Augen-Prüfung | jedes Gestell |
| PS-4 | ESD-Prüfung von Armband und Schuhen | V2 | Selbsttest am Prüfgerät | bei jedem Betreten |
| PS-5 | Etikettenkontrolle (Lesbarkeit, Inhalt, Position) | V3, V4 | Scan des Etiketts | jede 20. Einheit |
| PS-6 | Mustervergleich bei Displays | V3 | Sichtvergleich mit freigegebenem Muster | erstes Display und jedes 50. |
| PS-7 | Vollständigkeit der Beschlagbeutel | V4 | Wiegen auf der Kontrollwaage | jeder Beutel |
| PS-8 | Sichtprüfung auf Transportschäden | V4 | Sichtprüfung, Foto bei Schaden | jedes Packstück |

Bei PS-7 gilt eine Toleranz von plus/minus 3 Gramm zum Sollgewicht des Beutels. Liegt das Gewicht außerhalb der Toleranz, wird der Beutel geöffnet und neu gezählt.

Bei PS-3 prüft die zweite Person das fertige Gestell gegen den Sequenzabruf, bevor es an Tor 7 verladen wird. Ein Gestell ohne bestätigtes PS-3 darf das System nicht zur Verladung freigeben.

## Besonderheiten je Arbeitsplatz

### V1: Sequenzierung

Der Sequenzabruf kommt etwa vier Stunden vor dem Verbau beim Kunden. Für die Sequenzierung bleiben in der Praxis rund 90 Minuten, weil Transport und Pufferzeit abgezogen werden müssen. Fällt ein Teil wegen Fehlmenge aus, wird nicht improvisiert: Die Schichtleitung informiert sofort das Kundenteam Automotive, das mit der Werkslogistik des Kunden entscheidet, ob eine Lücke im Gestell gelassen oder die Sequenz gesplittet wird.

### V2: Kitting im ESD-Bereich

V2 liegt innerhalb des ESD-Bereichs E1. Offene Kartons mit Bauteilen von Brenner dürfen nur hier gehandhabt werden. Vor dem Betreten führt jeder Mitarbeitende den ESD-Selbsttest (PS-4) durch. Fällt der Test durch, darf der Bereich nicht betreten werden, bis Armband oder Schuhe getauscht sind. Fertige Kits werden in ESD-Beutel verpackt und verschlossen.

### V3: Etikettieren, Umpacken und Displaybau

An V3 werden Aufträge für wechselnde Kunden bearbeitet. Für jeden neuen Auftragstyp muss vor Beginn ein freigegebenes Muster vorliegen, das am Arbeitsplatz aushängt. Ohne Muster wird nicht gearbeitet. Etiketten werden aus dem Lagerverwaltungssystem gedruckt; handschriftliche Etiketten sind nicht zulässig.

### V4: Möbelpackstücke

An V4 werden Packstücke von Holtz Möbel geprüft, deren Umverpackung beim Wareneingang beschädigt war, sowie Beschlagbeutel montiert. Neu verpackte Packstücke erhalten ein neues Kundenetikett mit derselben Packstücknummer, zum Beispiel „Packstück 2 von 3“. Mehrteilige Artikel werden an V4 nicht getrennt; alle Packstücke eines Artikels bleiben auf einem Ladungsträger.

## Arbeitsschutz an den VAS-Arbeitsplätzen

- An V1 und V4 sind Sicherheitsschuhe S3 und Handschuhe der Schnittschutzklasse B vorgeschrieben.
- An V2 werden ESD-Schuhe statt Sicherheitsschuhen getragen; diese erfüllen ebenfalls S3.
- An V3 ist das Arbeiten mit Cuttermessern nur mit Sicherheitsklinge erlaubt.
- Die Arbeitsplätze sind höhenverstellbar. Jeder Mitarbeitende stellt die Arbeitshöhe zu Schichtbeginn ein.
- Flurförderzeuge dürfen die Bereitstellflächen anfahren, aber nicht die eigentliche Arbeitsfläche. Die Grenze ist mit einer gelben Linie markiert.

## Fehler und Nacharbeit

Wird ein Fehler bei einer Prüfung entdeckt, wird die betroffene Einheit nicht ausgeliefert, sondern auf die Nacharbeitsfläche des Arbeitsplatzes gestellt. Die Nacharbeit führt eine andere Person durch als die, die den Fehler verursacht hat. Nach der Nacharbeit werden alle Prüfschritte des Arbeitsplatzes für diese Einheit wiederholt.

Häufen sich Fehler (mehr als drei gleichartige Fehler in einer Schicht), stoppt die VAS-Teamleitung den Auftrag und klärt die Ursache, bevor weitergearbeitet wird. Der Stopp und die Ursache werden im Schichtbuch vermerkt. Erreicht ein Fehler den Kunden, gilt die Prozessanweisung Reklamationsmanagement und 8D-Report.

## Ausnahmen

- Bei Zollware ist jede VAS-Leistung vorher mit der Zollabteilung abzustimmen (siehe Prozessanweisung Zollabwicklung und Versandverfahren T1).
- Kühlware wird nicht an V1 bis V4 bearbeitet. Etikettieren von Kühlware erfolgt ausschließlich im Kühlbereich.
- Eilaufträge dürfen nur von der VAS-Teamleitung vorgezogen werden. Prüfschritte entfallen dabei nicht.

## Mitgeltende Dokumente

- Kundenspezifische Regelungen Altmann Automotive, Brenner Elektronik, Holtz Möbel
- Prozessanweisung Reklamationsmanagement und 8D-Report (prozess_reklamation_8d.md)
- Prozessanweisung Schichtübergabe und Schichtbuch (prozess_schichtuebergabe.md)
- Prozessanweisung Einarbeitung neuer Mitarbeitender und Leiharbeitskräfte (prozess_einarbeitung.md)
