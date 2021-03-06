Im folgenden Hinweise um die Owl Arbeitsumgebung zu benutzen.  Wir nehmen
an, dass die Datei CONCEPTS gelesen wurde; wenn nicht, w�re es besser das
zu tun bevor man hier weiterliest.


	/usr/src/world Setup.

Die Arbeitsumgebung ist standardm�ssig so konfiguriert, dass sie in
/usr/src/world liegt (die HOME= Einstellung in buildworld.conf und
installworld.conf).  Es wird empfohlen, diese Einstellung zu
�ndern und die Dateien nicht in /usr/src/world zu plazieren oder einen
symbolischen Link zu benutzen, wenn /usr/src kein geeignetes Device ist
(siehe unten f�r die Voraussetzungen).

In den meisten F�llen existiert das Verzeichnis schon.  Wenn nicht muss
man es erstellen, den Pseudo-Benutzer "build" anlegen, vorzugsweise
mit UID 151 und GID 150 ("sources") und ihm das Verzeichnis mittels
"chown" zur Verf�gung stellen.

Das CVS Archiv ist in /usr/src/world anzulegen.  Der einfachste Weg um das
zu tun ist die Datei native.tar.gz, die auf den FTP-Servern erh�ltlich ist,
zu entpacken.  Man erh�lt dann ein "native" Verzeichnis und einen
symbolischen Link zum Makefile.

Um aus den Quellen zu �bersetzen, erstellt man das "sources" Verzeichnis
ebenfalls in /usr/src/world.

Wird noch nicht auf einem Owl-System gearbeitet und Bin�rpakete
sollen installiert werden, so sollte /usr/src/world/RPMS erstellt,
und die Pakete f�r die jeweilige Architektur dort plaziert werden.
Es ist zu beachten, dass das CVS Archiv auch f�r die Installation
von Bin�rpaketen gebraucht wird.


	Voraussetzungen.

Um Owl aus den Quellen (neu) zu �bersetzten, braucht man:

Mindestens 1 GB freien Speicherplatz in /usr/src/world der
w�hrend des �bersetzens genutzt werden kann;

Mindestens 1 GB virtuellen Speicher.

Auf einem aktuellen System ein paar Stunden CPU Zeit.

Nat�rlich sollte man alles auf Owl �bersetzten.  Es ist zwar m�glich
dies alles auf einem anderen GNU/*/Linux System zu machen, aber man muss
etwas tricksen um das System zu einem Owl zu machen.  Das Ganze geht
mit mehreren Wiederholungen von "make buildworld" und "make installworld".

Hier einige �bersetzungszeiten (Stunden:Minuten) f�r Owl 2.0 um
einen Eindruck zu bekommen was einen erwartet:

Dual Pentium 4 Xeon, HT (4-way MP), 2.8 GHz, 2 GB		0:50
Dual Pentium III, 600 MHz, 512 MB				3:35
UltraSparc IIi, 400 MHz, 256 MB					10:00
Alpha 21164PC (164SX-1MB), 533 MHz, 128 MB			14:00

(Ja, der gcc ist auf einer Alpha ganz sch�n hungrig)

Die Zeiten werden sich erh�hen, wenn in Zukunft mehr Pakete hinzugef�gt werden
und wenn die Software, die bereits Bestandteil von Owl ist, ge-updated wird.


	Richtige (Neu-)�bersetzung.

Wechsle als Benutzer "build" nach /usr/src/world und gib ein:

	make clean && make buildworld

Per Standardeinstellung in buildworld.conf werden die Pakete f�r
die �lteste Version der jeweiligen Architektur (siehe ARCHITECTURES) �ber-
setzt und zus�tzlich wird versucht, alle Prozessoren zu nutzen.

buildworld.conf (sowie andere *.conf's) k�nnen editiert werden, indem
man sie von native/Owl/build nach /usr/src/world kopiert.  Man muss vorher
jedoch den symbolischen Link entfernen, sofern dieser erstellt wurde.

Alle Pakete werden mit den Bibilotheken und Tools �bersetzt, die auf dem
System vorhanden sind.  Mehrere Wiederholungen von buildworld und
installworld (zwei sind meistens ausreichend) sollten n�tig werden,
wenn signifikante �nderungen an den Paketen w�hrend des Build-Prozesses
aufgetreten sind.


	Installation von Bin�rpaketen.

"make installworld" installiert alle Pakete, die es in /usr/src/world/RPMS
findet auf das aktuelle System oder in ein anderes Verzeichnis freier
Wahl (ROOT= Einstellung in installworld.conf).  Standardm�ssig werden
die Pakete nach /owl installiert.

"make installworld" sollte als root ausgef�hrt werden.


	(Neu-) �bersetzung individueller Pakete.

Individuelle Pakete k�nnen wieder- oder neu�bersetzt werden, indem man
"make PACKAGE=name" eingibt, wobei "name" der Name des Quell-Paketes ist.
F�r fremde Pakete (SRPMs) die mit der Owl-Arbeitsumgebung erstellt worden
sind, muss man zus�tzlich die Versionsnummer in "name" einf�gen.

$Owl: Owl/doc/de/BUILD,v 1.20 2011/10/24 09:06:48 solar Exp $
