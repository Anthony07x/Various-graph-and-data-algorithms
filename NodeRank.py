import sys
def myRead():
    n = q = vrh = 0
    b = 0.
    brojIter = -1
    upiti = []
    susjedi_vrha = {}
    vrh_stupnjevi = {}
    data = sys.stdin.read().splitlines()
    for idx, line in enumerate(data):
        if idx == 0:
            n, b = line.strip().split(" ")
            n = int(n)
            b = float(b)
        
        elif idx > 0 and idx <= n:
            susjedi = [int(broj) for broj in line.strip().split(" ")]
            susjedi_vrha[vrh] = susjedi
            vrh_stupnjevi[vrh] = len(susjedi)
            vrh += 1
        
        elif idx == n + 1:
            q = int(line.strip())
            
        elif idx > n + 1:
            vrh, iteracija = map(int, line.strip().split(" "))
            if iteracija > brojIter:
                brojIter = iteracija
            upiti.append((vrh, iteracija))
                
    return n, b, q , brojIter, vrh_stupnjevi, susjedi_vrha, upiti            
                

def iterations(n, b, q, brojIter, vrh_stupnjevi, susjedi_vrha, upiti):
    rankVector = [1/n for i in range(n)]
    vektori_po_iteracijama = {}
    vektori_po_iteracijama[0] = rankVector
    
                                # !!!!!! #
    # moramo obrnit, jer dosad smo imali cvor ---> susjedi (cvor ide u susjede)
    # a mi moramo kasnije zbrajat cvor <--- susjedi (odnosno doprinos svih cvorova koji idu u cvor, a ne iz cvora)
    in_susjedi = {i: [] for i in range(n)}
    for u, susjedi in susjedi_vrha.items(): 
        for v in susjedi:
            in_susjedi[v].append(u)
    
    for i in range(brojIter): # svaka iteracija
        rankVectorUpdated = []
        ukupni_utjecaj_u_iteraciji = 0.
        
        for cvor in range(len(rankVector)): # za svaku cvor u vektoru
            utjecajCvora = 0.
            susjedi = in_susjedi[cvor] # cvor ide po svakom elementu u 
                                         # rank vektoru, znaci od 0 do n - 1
            
            for susjed in susjedi:  # susjed je index vrha (dakle taj vrh jer su vrhovi indexi zapravo)
                utjecajCvora += b * (rankVector[susjed] / vrh_stupnjevi[susjed])
                
            ukupni_utjecaj_u_iteraciji += utjecajCvora # ukupni utjecaj je S
            rankVectorUpdated.append(utjecajCvora)
        
        spillage = (1 - ukupni_utjecaj_u_iteraciji) / n
        rankVector = [spillage + utjecajVrha for utjecajVrha in rankVectorUpdated]
        #rankVector = rankVectorUpdated[:]
        vektori_po_iteracijama[i + 1] = rankVector
           
    return vektori_po_iteracijama
           
 

def printajUpite(upiti, vektori_po_iteracijama):
    for cvor, iteracija in upiti:
        vrijednost = vektori_po_iteracijama[iteracija][cvor]
        print(f"{vrijednost:.10f}")
    

                
n, b, q , brojIter, vrh_stupnjevi, susjedi_vrha, upiti = myRead()
printajUpite(upiti, iterations(n, b, q , brojIter, vrh_stupnjevi, susjedi_vrha, upiti))
#for k,v in stupnjevi_vrhova.items():
#    print(f"Vrh: {k}, Stupanj: {v}")

#for k,v in iterations(n, b, q , brojIter, vrh_stupnjevi, susjedi_vrha, upiti).items():
#    print(f"Iteracija: {k}, vektor: {sum(v)}\n")
    







