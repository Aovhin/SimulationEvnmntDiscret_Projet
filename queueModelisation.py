from ciw import *

"""
1) Modéliser le réseau de files d’attente à l’aide de Ciw avec la configuration suivante :

• Temps d'initialisation (I) :                  0 s

• Durée du service statique (Y) :               0 s

• Taux de serveur dynamique ou débit (R) :      10 Mbits/s 

• Bande passante réseau du serveur (S) :        1,5 Mbits/s 

• Taux d'arrivée du réseau (A) :                entre 0/s et 35/s

• Taille  moyenne des fichiers (F) :            en octets (arbitrairement 5 275 octets quand nécessaire) --> 42 200 bits

• Taille du tampon (B) :                        arbitrairement 2 000 octets --> 16 000 bits

• Bande passante réseau client (C) :            707 Kbits/s


○ Taux de succès du transfert de fichier : p = B / F
○ Débit D = B / R

__________________________________________________________

Files d'attentes (4) :

☻ SI : traitements "d'initialisation" uniques
☻ SI -> SR : une seule partie du fichier demandé est lue, traitée et transmise au réseau.
☻ SR -> SS : envoie du fichier vers Internet
☻ SS -> SC : file d'attente du client
☻ SC -> SR : possibilité que SC revienne vers SR

 ** Voir schéma ** 
__________________________________________________________


...     N = ciw.create_network(
...     arrival_distributions=[ciw.dists.Exponential(0.3),
...                            ciw.dists.Exponential(0.2),
...                            ciw.dists.NoArrivals()],
...     service_distributions=[ciw.dists.Exponential(1.0),
...                            ciw.dists.Exponential(0.4),
...                            ciw.dists.Exponential(0.5)],
...     routing=[[0.0, 0.3, 0.7],
...              [0.0, 0.0, 1.0],
...              [0.0, 0.0, 0.0]],
...     number_of_servers=[1, 2, 2] 
...    )


"""

n_server = 1
I = 0
Y = 0
A = random_choice(range(0, 35))
F = 42200
B = 16000
C = 707000
S = 1500000
R = 10000000
p = B / F

### DEF SI ###
SI_arr_dist = ciw.dists.Exponential(A)
SI_srvc_dist = ciw.dists.Deterministic(I)
### END DEF ###

### DEF SR ###
SR_arr_dist = ciw.dists.Exponential((A * F) / B)
SR_srvc_dist = ciw.dists.Exponential(1 / (Y + (B / R)))
### END DEF ###

### DEF SS ###
SS_arr_dist = ciw.dists.Exponential((A * F) / B)
SS_srvc_dist = ciw.dists.Deterministic(B / S)
### END DEF ###

### DEF SC ###
SC_arr_dist = ciw.dists.Exponential((A * F) / B)
SC_srvc_dist = ciw.dists.Deterministic(B / C)
### END DEF ###

print("_______________________________")

print("\t Taux moyen d'Arrivée")
print(f"\t * A : {A}")
print(f"\t * λ_SR : {(A * F) / B}")
print(f"\t * λ_SS : {(A * F) / B}")
print(f"\t * λ_SC : {(A * F) / B}")
print(f"\n\t Taux moyen de Service")
print(f"\t * μ_SI : {I}")
print(f"\t * μ_SR : {(1 / (Y + (B / R)))}")
print(f"\t * μ_SS : {B / S}")
print(f"\t * λ_SC : {B / C}")

print(f"\n\t Stabilité")
print(f"\t * SI : oui")
print(f"\t * SR : {((A * F) / B)/(1 / (Y + (B / R)))}")
print(f"\t * SS : {((A * F) / B)/(B / S)}")
print(f"\t * SC : {((A * F) / B)/(B / C)}")

print("_______________________________")

N = ciw.create_network(
    arrival_distributions=[SI_arr_dist, SR_arr_dist, SS_arr_dist, SC_arr_dist],
    service_distributions=[SI_srvc_dist, SR_srvc_dist, SS_srvc_dist, SC_srvc_dist],
    routing=[[0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1],
             [0, 1 - p, 0, 0]
             ],
    number_of_servers=[1, 1, 1, 1]
)

Q = ciw.Simulation(N)
Q.simulate_until_max_time(100)
recs = Q.get_all_records()
num_cmplted = len([r for r in recs if r.node == 3 and r.arrival_date < 180])

print(f"Cmplptd transactions : {num_cmplted}")
print(f"RECORD CLIENT 0 : {recs[0]} ")
