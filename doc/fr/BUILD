Ceci est le guide d'utilisation de l'environnement de compilation de Owl. Il
assume que vous ayez lu les CONCEPTS; sinon, merci de les lire avant que
vous ne continuiez avec ce document.


	Organisation de /usr/src/world.

L'environnement de compilation est pr�-configur� pour l'utilisation de
/usr/src/world (la valeur de HOME= dans les fichiers buildworld.conf et
installworld.conf). Il est recommand� que vous laissiez cette valeur par
d�faut et soit que vous placiez effectivement les fichiers dans
/usr/src/world soit que vous utilisiez un lien symbolique si /usr/src n'est
pas sur un p�riph�rique appropri� (voir ci-dessous les besoins).

En compilant nativement (c.-�-d. sur Owl), le r�pertoire est d�j� l�.
Autrement, vous avez besoin de cr�er le r�pertoire, ajouter le pseudo
utilisateur "build", de pr�f�rence avec l'UID 151 et le GID 150
("sources"), et le rendre propri�taire du r�pertoire.

Placez l'arborescence CVS dans /usr/src/world. La fa�on la plus simple pour
faire cela est en extrayant native.tar.gz disponible via les miroirs FTP.
Vous obtiendrez le r�pertoire "native", et un lien symbolique Makefile.

Pour compiler effectivement depuis les sources, placez �galement le
r�pertoire "sources" dans /usr/src/world.

Si vous n'�tes pas, encore, sur un syst�me Owl et voulez installer des
paquets binaires, cr�ez /usr/src/world/RPMS et placez y les paquets pour
votre architecture. Notez que vous avez besoin de l'arborescence CVS m�me
pour installer les paquets binaires.


	Besoins.

Pour (re-)compiler Owl depuis les sources, vous aurez besoin :

d'au moins de 1000 Mo d'espace disque libre sous /usr/src/world utilisables
durant les compilations;

d'au moins 1000 Mo de m�moire virtuelle;

de 1 � 5 heures de temps CPU, sur un syst�me moderne (au moment de cette
�criture).

Et, bien s�r, vous devriez ex�cuter la compilation sur Owl. Compiler sur un
autre syst�me GNU/*/Linux est possible, mais difficile et n�cessite que vous
convertissiez effectivement le syst�me en Owl avec plusieurs it�rations de
"make buildworld" et "make installworld".

Voici quelques temps de compilation (heures:minutes), ainsi vous savez �
quoi vous attendre :

Dual Pentium 4 Xeon, HT (4-way MP), 2.8 GHz, 2 GB		0:50
Dual Pentium III, 600 MHz, 512 MB				3:35
UltraSparc IIi, 400 MHz, 256 MB					10:00
Alpha 21164PC (164SX-1MB), 533 MHz, 128 MB			14:00

(Oui, gcc est si gourmand et lent sur Alpha.)

Les temps de compilation vont augmenter quand nous ajouterons plus de
paquets et mettrons � jour vers de nouvelles versions de logiciels d�j� dans
Owl.


	(Re-)compilations natives.

En tant que l'utilisateur "build", changez de r�pertoire vers /usr/src/world
et tapez :

	make clean && make buildworld

Avec le fichier buildworld.conf par d�faut, les paquets seront compil�s pour
la version la plus ancienne de l'architecture du syst�me de compilation
(voir ARCHITECTURES) et la compilation tentera d'utiliser tous les
processeurs syst�mes.

Le fichier buildworld.conf (aussi bien que les autres fichiers *.conf) peut
�tre �dit� en le copiant depuis native/Owl/build vers /usr/src/world. Vous
avez d'abord besoin de supprimer le lien symbolique, si un a �t� cr�� pour
vous auparavant.

Tous les paquets sont compil�s avec les versions de biblioth�ques et
d'outils de compilation qui sont install�es sur le syst�me. Plusieurs
it�rations de buildworld et installworld (deux sont suffisantes la plupart
du temps) doivent �tre utilis�es quand il y a eu des mises � jour
significatives des paquets utilis�s durant les compilations.


	Installations de paquets binaires.

"make installworld" installera les paquets trouv�s dans /usr/src/world/RPMS
dans le syst�me courant, ou dans tout nouveau r�pertoire racine de votre
choix (comme sp�cifi� par la valeur de ROOT= dans le fichier
installworld.conf). Par d�faut, les paquets seront install�s dans /owl.

"make installworld" doit �tre ex�cut� en tant que root.


	(Re-)compilations de paquets individuels.

Les paquets individuels peuvent �tre compil�s ou re-compil�s avec
"make PACKAGE=nom" o� "nom" est le nom du paquet source. Pour les paquets
�trangers (SRPMs) compil�s avec l'environnement de compilation de Owl vous
avez aussi besoin d'inclure dans "nom" la partie num�ro de version.

$Owl: Owl/doc/fr/BUILD,v 1.13 2011/10/24 09:06:48 solar Exp $
