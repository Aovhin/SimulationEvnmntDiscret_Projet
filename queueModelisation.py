from ciw import *

"""
1) Modéliser le réseau de files d’attente à l’aide de Ciw avec la configuration suivante :

• Temps d'initialisation (I) :                  0 s

• Durée du service statique (Y) :               0 s

• Taux de serveur dynamique ou débit (R) :      10 Mbits / s

• Bande passante réseau du serveur (S) :        1,5 Mbits / s

• Taux d'arrivée du réseau (A) :                entre 0/s et 35/s

• Taille  moyenne des fichiers (F) :            en octets (arbitrairement 5 275 octets quand nécessaire)

• Taux d'arrivée du réseau (A) :

• Taille du tampon (B) :                        arbitrairement 2 000 octets

• Bande passante réseau client (C) :


○ Taux de succès du transfert de fichier : p = B / F

__________________________________________________________

Files d'attentes (4) :

☻ SI : traitements "d'initialisation" uniques
☻ SI -> SR : une seule partie du fichier demandé est lue, traitée et transmise au réseau.
☻ SR -> SS : envoie du fichier vers Internet
☻ SS -> SC : file d'attente du client
☻ SC -> SR : possibilité que SC revienne vers SR

 ** Voir schéma ** 
__________________________________________________________

"""


