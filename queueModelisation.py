from ciw import *
import matplotlib.pyplot as plt

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


"""

"""print("_______________________________")

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

print("_______________________________")"""

avgTime = []


def createNetwork(
        n_server=1,
        I=0,
        Y=0,
        A=16,
        F=42200,
        B=16000,
        C=707000,
        S=1500000,
        R=10000000,
        nbServerSR=1
):
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
    N = ciw.create_network(
        arrival_distributions=[SI_arr_dist, SR_arr_dist, SS_arr_dist, SC_arr_dist],
        service_distributions=[SI_srvc_dist, SR_srvc_dist, SS_srvc_dist, SC_srvc_dist],
        routing=[[0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [0, 0, 0, 1],
                 [0, 1 - p, 0, 0]
                 ],
        number_of_servers=[1, nbServerSR, 1, 1]
    )
    return N


def execSimulation(time, nbExec, N):
    avgs = []
    for k in range(nbExec):

        Q = ciw.Simulation(N)
        Q.simulate_until_max_time(time)
        recs = Q.get_all_records()
        grpd_recs = sorted(recs, key=lambda r: r[0])

        i = 0
        print(len(grpd_recs))
        while i < len(grpd_recs):
            has_ended = False
            client_service_time = []
            client_rec = []
            j = i
            rec = grpd_recs[i]
            while j < len(grpd_recs) and rec.id_number == grpd_recs[j].id_number:
                client_rec += [grpd_recs[j]]
                client_service_time += [grpd_recs[j].service_time]
                has_ended = has_ended or (grpd_recs[j].node == 4 and grpd_recs[j].destination == -1)
                j += 1
            i = j
            if has_ended:
                print()
                for rec in client_rec:
                    print("*" + str(rec) + "*___", end="")
                print()
                avgs.append(sum(client_service_time))

        completed = [r for r in recs if r.destination == -1 and r.arrival_date < time]
        num_cmplted = len(completed)
        print(f"Cmplptd transactions : {num_cmplted} of {len(recs)}")

    return avgs


def varExecTimeSimulations():
    n = 50
    times = []
    for i in range(1, 6):
        avg = execSimulation(i * n, 1, createNetwork())
        avgTime.append(sum(avg) / len(avg))
        times.append(i * n)

    fig = plt.figure()
    subplot = fig.add_subplot()
    subplot.set_ybound(0, avgTime[0] + avgTime[0] / 2)
    subplot.plot(times, avgTime, scaley=False)
    subplot.set_xlabel("Execution Time")
    subplot.set_ylabel("Average Response Time")
    subplot.set_title("Evolution of Average Response Time\ndepending on Simulation Execution Time.")
    plt.show()


def varASimulations():
    A = [a for a in range(1, 36)]
    avg = []
    for a in A:
        # print(str(a)+" ", end=" - ")
        avgTmp = execSimulation(50, 1, createNetwork(A=a))
        avg.append(sum(avgTmp) / len(avgTmp))

    fig = plt.figure()
    subplot = fig.add_subplot()
    subplot.plot(A, avg)
    subplot.set_xlabel("A")
    subplot.set_ylabel("Average Response Time")
    subplot.set_ybound(0, avg[0] + avg[0] / 2)
    subplot.set_title("Evolution of Average Response Time\ndepending on the A parameter.")
    plt.show()


def multiVarSimulation():
    A = [a for a in range(1, 36)]
    avg = []
    for a in A:
        # print(str(a) + " ", end=" - ")
        avgTmp = execSimulation(100, 1, createNetwork(A=a))
        avg.append(sum(avgTmp) / len(avgTmp))

    R = 2 * 10000000
    avg2R = []
    for a in A:
        # print(str(a) + " ", end=" - ")
        avgTmp = execSimulation(100, 1, createNetwork(A=a, R=R))
        avg2R.append(sum(avgTmp) / len(avgTmp))

    S = 2 * 1500000
    avg2S = []
    for a in A:
        # print(str(a) + " ", end=" - ")
        avgTmp = execSimulation(100, 1, createNetwork(A=a, S=S))
        avg2S.append(sum(avgTmp) / len(avgTmp))

    nbServer = 2
    avg2SR = []
    for a in A:
        # print(str(a) + " ", end=" - ")
        avgTmp = execSimulation(100, 1, createNetwork(A=a, nbServerSR=nbServer))
        avg2SR.append(sum(avgTmp) / len(avgTmp))

    fig = plt.figure()
    subplot = fig.add_subplot()
    subplot.plot(A, avg, 'y')
    subplot.plot(A, avg2S, 'g')
    subplot.plot(A, avg2R, 'b')
    subplot.plot(A, avg2SR, 'r')
    subplot.set_ybound(0, max(avg) * 2)
    subplot.set_xlabel("A")
    subplot.set_ylabel("Average Response Time")
    # subplot.set_ybound(0, avg[0] + avg[0] / 2)
    subplot.set_title("Evolution of Average Response Time\ndepending on the A parameter.")
    plt.show()


varASimulations()
