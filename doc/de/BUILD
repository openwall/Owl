Im folgenden Hinweise um die Owl Arbeitsumgebung zu benutzen.  Wir nehmen
an, dass die Datei CONCEPTS gelesen wurde; wenn nicht, wäre es besser das
zu tun bevor man hier weiterliest.


	/usr/src/world Setup.

Die Arbeitsumgebung ist standardmässig so konfiguriert, dass sie in
/usr/src/world liegt (die HOME= Einstellung in buildworld.conf und
installworld.conf).  Es wird empfohlen, diese Einstellung zu
ändern und die Dateien nicht in /usr/src/world zu plazieren oder einen
symbolischen Link zu benutzen, wenn /usr/src kein geeignetes Device ist
(siehe unten für die Voraussetzungen).

In den meisten Fällen existiert das Verzeichnis schon.  Wenn nicht muss
man es erstellen, den Pseudo-Benutzer "build" anlegen, vorzugsweise
mit UID 151 und GID 150 ("sources") und ihm das Verzeichnis mittels
"chown" zur Verfügung stellen.

Das CVS Archiv ist in /usr/src/world anzulegen.  Der einfachste Weg um das
zu tun ist die Datei native.tar.gz, die auf den FTP-Servern erhältlich ist,
zu entpacken.  Man erhält dann ein "native" Verzeichnis und einen
symbolischen Link zum Makefile.

Um aus den Quellen zu übersetzen, erstellt man das "sources" Verzeichnis
ebenfalls in /usr/src/world.

Wird noch nicht auf einem Owl-System gearbeitet und Binärpakete
sollen installiert werden, so sollte /usr/src/world/RPMS erstellt,
und die Pakete für die jeweilige Architektur dort plaziert werden.
Es ist zu beachten, dass das CVS Archiv auch für die Installation
von Binärpaketen gebraucht wird.


	Voraussetzungen.

Um Owl aus den Quellen (neu) zu übersetzten, braucht man:

Mindestens 1 GB freien Speicherplatz in /usr/src/world der
während des Übersetzens genutzt werden kann;

Mindestens 64 MB Arbeitsspeicher (es geht auch mit weniger und aus-
reichendem Auslagerungsspeicher, aber davon ist abzuraten);

Mindestens 200 MB virtuellen Speicher.

Auf einem aktuellen System ein paar Stunden CPU Zeit.

Natürlich sollte man alles auf Owl übersetzten.  Es ist zwar möglich
dies alles auf einem anderen GNU/*/Linux System zu machen, aber man muss
etwas tricksen um das System zu einem Owl zu machen.  Das Ganze geht
mit mehreren Wiederholungen von "make buildworld" und "make installworld".

Hier einige Übersetzungszeiten (Stunden:Minuten) für Owl-current um
einen Eindruck zu bekommen was einen erwartet:

Dual Pentium 4 Xeon, HT (4-way MP), 2.8 GHz, 2 GB		0:50
Dual Pentium III, 600 MHz, 512 MB				3:35
UltraSparc IIi, 400 MHz, 256 MB					9:20
Alpha 21164PC (164SX-1MB), 533 MHz, 128 MB			13:30

(Ja, der gcc ist auf einer Alpha ganz schön hungrig)

Die Zeiten werden sich erhöhen, wenn in Zukunft mehr Pakete hinzugefügt werden
und wenn die Software, die bereits Bestandteil von Owl ist, ge-updated wird.


	Richtige (Neu-)Übersetzung.

Man braucht einen konfigurierten 2.4er Linux Kernel in /usr/src/linux.
Wechsle als Benutzer "build" nach /usr/src/world und gib ein:

	make clean && make buildworld

Per Standardeinstellung in buildworld.conf werden die Pakete für
die älteste Version der jeweiligen Architektur (siehe ARCHITECTURES) über-
setzt und zusätzlich wird versucht, alle Prozessoren zu nutzen.

buildworld.conf (sowie andere *.conf's) können editiert werden, indem
man sie von native/Owl/build nach /usr/src/world kopiert.  Man muss vorher
jedoch den symbolischen Link entfernen, sofern dieser erstellt wurde.

Alle Pakete werden mit den Bibilotheken und Tools übersetzt, die auf dem
System vorhanden sind.  Mehrere Wiederholungen von buildworld und
installworld (zwei sind meistens ausreichend) sollten nötig werden,
wenn signifikante Änderungen an den Paketen während des Build-Prozesses
aufgetreten sind.


	Installation von Binärpaketen.

"make installworld" installiert alle Pakete, die es in /usr/src/world/RPMS
findet auf das aktuelle System oder in ein anderes Verzeichnis freier
Wahl (ROOT= Einstellung in installworld.conf).  Standardmässig werden
die Pakete nach /owl installiert.

"make installworld" sollte als root ausgeführt werden.


	(Neu-) übersetzung individueller Pakete.

Individuelle Pakete können wieder- oder neuübersetzt werden, indem man
"make PACKAGE=name" eingibt, wobei "name" der Name des Quell-Paketes ist.
Für fremde Pakete (SRPMs) die mit der Owl-Arbeitsumgebung erstellt worden
sind, muss man zusätzlich die Versionsnummer in "name" einfügen.

$Owl: Owl/doc/de/BUILD,v 1.16 2006/01/02 10:26:38 schmidt Exp $
