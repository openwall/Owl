Im folgenden Hinweise um die Owl Arbeitsumgebung zu benutzen. Wir nehmen
an, dass die Datei CONCEPTS gelesen wurde; wenn nicht, wäre es besser das
zu tun bevor hier weitergelesen wird.


	/usr/src/world Setup.

Die Arbeitsumgebung ist standardmässig so konfiguriert, dass sie in
/usr/src/world liegt (die HOME= Einstellung in buildworld.conf und
installworld.conf). Es wird empfohlen, diese Einstellung zu
ändern und die Dateien nicht in /usr/src/world zu plazieren oder einen
symbolischen Link zu benutzen, wenn /usr/src kein geeignetes Device ist
(siehe unten für die Voraussetzungen).

In den meisten Fällen existiert das Verzeichnis schon. Wenn nicht muss
man es erstellen, den Pseudo-Benutzer "build" anlegen, vorzugsweise
mit UID 151 und GID 150 ("sources") und ihm das Verzeichnis mittels
"chown" zur Verfügung stellen.

Das CVS Archiv ist in /usr/src/world anzulegen. Meistens wird dies schon
erledigt wenn die Datei native.tar.gz, die auf den FTP-Servern er-
hältlich ist, entpackt wird. Man erhält dann ein "native" Verzeichnis und
einen symbolischen Link zum Makefile.

Um aus den Quellen zu übersetzen, erstellt man das "sources" Verzeichnis
ebenfalls in /usr/src/world.

Wird noch nicht auf einem Owl-System gearbeitet und Binärpakete
sollen installiert werden, so sollte /usr/src/world/RPMS erstellt,
und die Pakete für die jeweilige Architektur dort plaziert werden.
Es ist zu beachten, dass das CVS Archiv auch für die Installation 
von Binärpaketen gebraucht wird.


	Voraussetzungen.

Um Owl aus den Quellen (neu) zu übersetzten, braucht man:

Mindestens 500 MB freien Speicherplatz in /usr/src/world der
während des Übersetzens genutzt werden kann;

Mindestens 64 MB Arbeitsspeicher (es geht auch mit weniger und aus-
reichendem Auslagerungsspeicher, aber davon ist abzuraten);

Mindestens 160 MB virtuellen Speicher wenn auf einer Alpha
übersetzt wird.

(Momentan) zwischen einer und fünf Stunden CPU Zeit auf einem modernen System.

Natürlich sollte man alles auf Owl übersetzten. Es ist zwar möglich
dies alles auf einem anderen GNU/*/Linux System zu machen, aber man muss
etwas tricksen um das System zu einem Owl zu machen. Das Ganze geht
mit mehreren Wiederholungen von "make buildworld" und "make installworld".

Hier einige Übersetzungszeiten (Stunden:Minuten) um einen Eindruck
zu bekommen:

Dual Pentium III, 1.266 GHz, 2 GB		0:29
Dual Pentium III, 1 GHz, 2 GB			0:36
Dual Pentium III, 800 MHz, 512 MB		0:45
Athlon, 1 GHz, 256 MB				1:10
Dual Celeron (Mendocino), 433 MHz, 256 MB	1:20
Pentium III, 700 MHz, 192 MB			1:35
UltraSparc IIi, 400 MHz, 256 MB			3:45
Alpha 21164PC (164SX-1MB), 533 MHz, 128 MB	5:20

(Ja, der gcc ist auf einer Alpha ganz schön hungrig)

Die Zeiten werden sich erhöhen, wenn in Zukunft mehr Pakete hinzugefügt werden und
wenn die Software, die bereits Bestandteil von Owl ist, ge-updated wird.


	Richtige (Neu-)Übersetzung.

Man braucht einen konfigurierten 2.2er Linux Kernel in /usr/src/linux.
Wechsle als Benutzer "build" nach /usr/src/world und gib ein:

	make clean && make buildworld

Per Standardeinstellung in buildworld.conf werden die Pakete für
die älteste Version der jeweiligen Architektur (siehe ARCHITECTURES) über-
setzt und zusätzlich wird versucht, mehrere Prozessoren zu nutzen.

buildworld.conf (sowie andere *.conf's) können editiert werden, indem
man sie von native/Owl/build nach /usr/src/world kopiert. Man muss vorher jedoch
den symbolischen Link entfernen, sofern dieser erstellt wurde.

Alle Pakete werden mit den Bibilotheken und Tools übersetzt, die auf dem
System vorhanden sind. Mehrere Wiederholungen von buildworld und
installworld (zwei sind meistens ausreichend) sollten nötig werden,
wenn signifikante Änderungen an den Paketen während des Build-Prozesses
aufgetreten sind.


	Installation von Binärpaketen.

"make installworld" installiert alle Pakete, die es in /usr/src/world/RPMS
findet auf das aktuelle System oder in ein anderes Verzeichnis freier
Wahl (ROOT= Einstellung in installworld.conf). Standardmässig werden
die Pakete nach /owl installiert.

"make installworld" sollte als root ausgeführt werden.

Momentan ist es möglich eine existierende Red Hat Linux 6.x Installation
in ein Owl mittels "make installworld" und einiger Handbuchhilfe
umzuwandeln. Bevor das versucht wird, sollte alles in
der Datei installorder.conf gelesen und verstanden worden sein! Insbesondere
sollte der Kernel während der Umstellung kein RPM-Paket mehr sein.


	Neuübersetzung individueller Pakete.

Um ein Owl Paket neu zu übersetzen werden das SRPM in /usr/src/world/SRPMS
und alle Binärpakete entfernt, die aus diesem Quelltext-Paket erstellt worden
sind. Danach ist abermals "make buildworld" einzugeben.

Wir betrachten das Übersetzen von SRPM's und das Fehlen des automatischen
Lösens der Abhängigkeiten als Bug in der Arbeitsumgebung. Wir werden das
eventuell fixen.

$Id: Owl/doc/de/BUILD,v 1.5 2002/06/20 14:31:59 schmidt Exp $
