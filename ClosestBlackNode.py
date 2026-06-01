from collections import deque
import sys

def myRead():
    vrh = n = e = 0
    cvorovi = []
    graf = {}
    
    data = sys.stdin.read().splitlines()
    for idx, line in enumerate(data):
        if idx == 0:
            n, e = line.strip().split(" ")
            n = int(n)
            e = int(e)
        
        elif idx > 0 and idx <= n:
            cvor = (vrh, int(line.strip()), 0) 
            cvorovi.append(cvor)
            vrh += 1
        
        elif idx > n:   
            cvor1, cvor2 = map(int, line.strip().split(" "))
            graf.setdefault(cvorovi[cvor2],  []).append(cvorovi[cvor1])
            graf.setdefault(cvorovi[cvor1],  []).append(cvorovi[cvor2])
                
    return n, e, cvorovi, graf

def exploreBFS(n, graf, cvorovi):
    najblizi_crni = {} 
    
    for cvor in cvorovi: 
        start_idx = cvor[0]
        if cvor[1] == 1: 
            najblizi_crni[start_idx] = [start_idx, 0]
            continue
        
        posjeceni = set()
        posjeceni.add(start_idx)
        
        red = deque() 
        red.append((start_idx, cvor[1], 0))
        
        najmanja_udaljenost = 11
        kandidati = []
        
        while red:
            trenutni_idx, vrsta, dist = red.popleft()
            
            if dist > 10 or dist > najmanja_udaljenost:
                break
            
            if vrsta == 1: 
                najmanja_udaljenost = dist
                kandidati.append(trenutni_idx)
                continue 
            
            lookup_key = (trenutni_idx, vrsta, 0)
            if lookup_key in graf:
                for susjed_idx, susjed_vrsta, _ in graf[lookup_key]:
                    if susjed_idx not in posjeceni: 
                        posjeceni.add(susjed_idx) 
                        red.append((susjed_idx, susjed_vrsta, dist + 1))
                        
        if kandidati:
            najblizi_crni[start_idx] = [min(kandidati), najmanja_udaljenost]
        else:
            najblizi_crni[start_idx] = [-1, -1]
            
    return najblizi_crni
                
n, e, cvorovi, graf = myRead()
k = exploreBFS(n, graf, cvorovi)

for i in range(n):
    crni_cvor, udaljenost = k[i]
    print(f"{crni_cvor} {udaljenost}")