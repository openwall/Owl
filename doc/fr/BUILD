Ceci est le guide d'utilisation de l'environnement de compilation de Owl. Il
assume que vous ayez lu les CONCEPTS; sinon, merci de les lire avant que
vous ne continuiez avec ce document.


	Organisation de /usr/src/world.

L'environnement de compilation est pré-configuré pour l'utilisation de
/usr/src/world (la valeur de HOME= dans les fichiers buildworld.conf et
installworld.conf). Il est recommandé que vous laissiez cette valeur par
défaut et soit que vous placiez effectivement les fichiers dans
/usr/src/world soit que vous utilisiez un lien symbolique si /usr/src n'est
pas sur un périphérique approprié (voir ci-dessous les besoins).

En compilant nativement (c.-à-d. sur Owl), le répertoire est déjà là.
Autrement, vous avez besoin de créer le répertoire, ajouter le pseudo
utilisateur "build", de façon préférée avec l'UID 151 et le GID 150
("sources"), et le rendre propriétaire du répertoire.

Placez l'arborescence CVS dans /usr/src/world. La façon la plus simple pour
faire cela est en extrayant native.tar.gz disponible via les miroirs FTP.
Vous obtiendrez le répertoire "native", et un lien symbolique Makefile.

Pour compiler effectivement depuis les sources, placez également le
répertoire "sources" dans /usr/src/world.

Si vous n'êtes pas, encore, sur un système Owl et voulez installer des
paquets binaires, créez /usr/src/world/RPMS et placez y les paquets pour
votre architecture. Notez que vous avez besoin de l'arborescence CVS même
pour installer les paquets binaires.


	Besoins.

Pour (re-)compiler Owl depuis les sources, vous aurez besoin :

d'au moins de 500 Mo d'espace disque libre sous /usr/src/world utilisables
durant les compilations;

d'au moins 64 Mo de mémoire physique (il est possible de compiler sur moins
avec suffisamment d'espace de swap, mais vous ne devriez pas);

d'au moins 160 Mo de mémoire virtuelle en compilant sur et pour un Alpha;

de 1 à 5 heures de temps CPU, sur un système moderne (au moment de cette
écriture).

Et, bien sûr, vous devriez exécuter la compilation sur Owl. Compiler sur un
autre système GNU/*/Linux est possible, mais difficile et nécessite que vous
convertissiez effectivement le système en Owl avec plusieurs itérations de
"make buildworld" et "make installworld".

Voici quelques temps de compilation (heures:minutes), ainsi vous savez à
quoi vous attendre :

Quad Pentium 4, 2 GHz, 2 GB			0:21
Dual Pentium III, 1.266 GHz, 2 GB		0:30
Dual Pentium III, 800 MHz, 512 MB		0:47
Athlon, 1 GHz, 256 MB				1:10
Pentium III, 700 MHz, 192 MB			1:35
UltraSparc IIi, 400 MHz, 256 MB			3:50
Alpha 21164PC (164SX-1MB), 533 MHz, 128 MB	5:30

(Oui, gcc est si gourmand et lent sur Alpha.)

Les temps de compilation vont augmenter quand nous ajouterons plus de
paquets et mettrons à jour vers de nouvelles versions de logiciels déjà dans
Owl.


	(Re-)compilations natives.

Vous avez besoin d'avoir un noyau Linux 2.2 configuré sans /usr/src/linux.
En tant que l'utilisateur "build", changez de répertoire vers /usr/src/world
et tapez :

	make clean && make buildworld

Avec le fichier buildworld.conf par défaut, les paquets seront compilés pour
la version la plus ancienne de l'architecture du système de compilation
(voir ARCHITECTURES) et la compilation tentera d'utiliser tous les
processeurs systèmes.

Le fichier buildworld.conf (aussi bien que les autres fichiers *.conf) peut
être édité en le copiant depuis native/Owl/build vers /usr/src/world. Vous
avez d'abord besoin de supprimer le lien symbolique, si un a été créé pour
vous auparavant.

Tous les paquets sont compilés avec les versions de bibliothèques et
d'outils de compilation qui sont installés sur le système. Plusieurs
itérations de buildworld et installworld (deux sont suffisantes la plupart
du temps) doivent être utilisées quand il y a eu des mises à jour
significatives des paquets utilisés durant les compilations.


	Installations de paquets binaires.

"make installworld" installera les paquets trouvés dans /usr/src/world/RPMS
dans le système courant, ou dans tout nouveau répertoire racine de votre
choix (comme spécifié par la valeur de ROOT= dans le fichier
installworld.conf). Par défaut, les paquets seront installés dans /owl.

"make installworld" doit être exécuté en tant que root.

Actuellement, il est possible de convertir l'installation d'une Linux Red
Hat 6.x existante en Owl avec "make installworld" et quelques aides
manuelles. Assurez vous de lire et comprendre tout du fichier
installorder.conf avant d'essayer ceci. En particulier, votre noyau ne
devrait plus être une partie des paquets RPM au moment de la conversion du
système en Owl.


	(Re-)compilations de paquets individuels.

Les paquets individuels peuvent être compilés ou re-compilés avec
"make PACKAGE=nom" où "nom" est le nom du paquet source. Pour les paquets
étrangers (SRPMs) compilés avec l'environnement de compilation de Owl vous
avez aussi besoin d'inclure dans "nom" la partie numéro de version.

$Id: Owl/doc/fr/BUILD,v 1.4.2.1 2002/10/14 20:14:12 solar Exp $
