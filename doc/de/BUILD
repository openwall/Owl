Dies sind Hinweise um die Owl Arbeitsumgebung zu benutzen. Wir nehmen 
an, dass du die Datei CONCEPTS gelesen hast; wenn nicht, lese sie 
bitte bevor du hier weiterliest.


	/usr/src/world Setup.

Die Arbeitsumgebung ist standardmässig so konfiguriert, dass sie in
/usr/src/world arbeitet (die HOME= Einstellung in buildworld.conf und
installworld.conf). Es wird empfohlen, dass du diese Einstellung
änderst und die Dateien nicht in /usr/src/world plazierst oder einen
symbolischen Link benutzt, wenn /usr/src kein geeignetes Device ist
(siehe unten für die Voraussetzungen).

In den meisten Fällen existiert das Verzeichnis schon. Wenn nicht, musst
du eines erstellen, den Pseudo-Benutzer "build" anlegen, vorzugsweise
mit UID 151 und GID 150 ("sources") und ihm das Verzeichnis zu eigen
machen.

Platziere das CVS Archiv in /usr/src/world. Meistens wird das schon
gemacht, wenn du die Datei native.tar.gz, die auf den FTP-Servern er-
hältlich ist, entpackst. Du bekommst dann ein "native" Verzeichnis und
einen symbolischen Link zur Makefile.

Um aus den Quellen zu übersetzen, erstelle das "sources" Verzeichnis
ebenfalls in /usr/src/world.

Wenn du noch nicht auf einem Owl-System arbeitest und Binärpakete 
installieren willst, erstelle /usr/src/world/RPMS und plaziere die 
Pakete für deine Architektur dort. Beachte, dass du das CVS Archiv 
auch für die Installation von Binärpaketen brauchst.


	Voraussetzungen.

Um Owl aus den Quellen (neu) zu übersetzten, brauchst du:

Mindestens 500 MB freien Speicherplatz in /usr/src/world, den du
während des Übersetzens nutzen kannst;

Mindestens 64 MB Arbeitsspeicher (es geht auch mit weniger und aus-
reichendem Auslagerungsspeicher, aber lass es);

Mindestens 160 MB virtuellen Speicher wenn du auf einer Alpha
übersetzt.

Zwischen einer und fünf Stunden CPU Zeit auf einem modernen System 
(zur Zeit).

Natürlich solltest du alles auf Owl übersetzten. Es ist zwar möglich
alles auf einem anderen GNU/*/Linux System zu machen, aber man muss 
etwas tricksen um das System zu einem Owl zu machen. Das ganze geht 
mit mehreren Iterationen von "make buildworld" und "make installworld".

Hier einige Übersetzungszeiten (Stunden:Minuten), damit du weist
was dich erwartet:

Dual Pentium III, 1 GHz, 2 GB			0:36
Dual Pentium III, 800 MHz, 512 MB		0:45
Athlon, 1 GHz, 256 MB				1:10
Dual Celeron (Mendocino), 433 MHz, 256 MB	1:20
Pentium III, 700 MHz, 192 MB			1:35
UltraSparc IIi, 400 MHz, 256 MB			3:45
Alpha 21164PC (164SX-1MB), 533 MHz, 128 MB	5:20

(Ja, der gcc ist auf einer Alpha ganz schön hungrig)

Dies Zeit wird sich erhöhen, wenn wir mehr Pakete hinzufügen und
wenn wir die Software, die bereits in Owl ist, updaten.


	Richtige (Neu-)Übersetzung.

Du brauchst einen konfigurierten 2.2er Linux Kernel in /usr/src/linux.
Wechsle als Benutzer "build" nach /usr/src/world und tippe:

	make clean && make buildworld

Per Standardeinstellung in buildworld.conf werden die Pakete für
die älteste Version deiner Architektur (siehe ARCHITECTURES) über-
setzt und zusätzlich versucht, mehrere Prozessoren zu nutzen.

buildworld.conf (sowie andere *.conf's) können editiert werden, indem
du sie von native/Owl/build nach /usr/src/world kopierst. Du must als
erstes den symbolischen Links entfernen, sofern einer erstellt wurde.

Alle Pakete werden mit den Bibilotheken und Tools übersetzt, die auf dem
System vorhanden sind. Mehrere Iterationen von buildworld und
installworld (zwei sind meistens ausreichend) sollten genutzt werden,
wenn signifikante Änderungen an den Paketen während des Prozesses
aufgetreten sind.


	Installation von Binärpaketen.

"make installworld" installiert alle Pakete, die es in /usr/src/world/RPMS
findet auf das aktuelle System oder in ein anderes Verzeichnis deiner
Wahl (die ROOT= Einstellung in installworld.conf). Standardmässig werden
die Pakete nach /owl installiert.

"make installworld" sollte als root ausgeführt werden.

Momentan ist es möglich eine existierende Red Hat Linux 6.x Installation
in ein Owl mittels "make installworld" und einiger Handbuchhilfe zu 
konvertieren. Bevor du das versuchst, sei dir sicher, dass du alles in
der Datei installorder.conf gelesen und verstanden hast. Im speziellen
sollte dein Kernel während der Konvertierung kein RPM Paket mehr sein.


	Neuübersetzung individueller Pakete.

Um ein Owl Paket neu zu übersetzen entferne das SRPM in /usr/src/world/SRPMS
und alle Binärpakete, die von diesem Quelltext-Paket erstellt worden
sind. Danach tippe "make buildworld".

Wir betrachten das Übersetzen von SRPM's und das Fehlen des automatischen
Lösens der Abhängigkeiten als Bug in der Arbeitsumgebung. Wir werden das 
eventuell fixen.
