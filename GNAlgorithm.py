import heapq
import copy
import sys

def readFile(filename=None):
    if filename:
        with open(filename, "r") as f:
            ulazi = f.read().splitlines()
    else:
        ulazi = sys.stdin.read().splitlines()

    space = False
    susjedi = {}
    svojstva_vrhova = {}
    
    for idx, line in enumerate(ulazi):
        if not line.strip():
            space = True
            continue
        
        if not space:
            prvi, drugi = line.strip().split(" ")
            susjedi.setdefault(prvi, []).append(drugi)
            susjedi.setdefault(drugi, []).append(prvi)
            continue
        
        if space:
            vrh, *svojstva = line.strip().split(" ")
            svojstva_vrhova[vrh] = svojstva
            susjedi.setdefault(vrh, []) 
                
    return susjedi, svojstva_vrhova
  
  
def makeWeights(susjedi, svojstva_vrhova):
    bridovi = {}
    for vrh, susedi in susjedi.items():
        for sused in susedi:
          pair = sorted([vrh, sused], key=int)
          brid = f"{pair[0]}-{pair[1]}"
          
          if brid not in bridovi.keys():
          
              vrhSlicnost = svojstva_vrhova[vrh]
              susedSlicnost = svojstva_vrhova[sused]
              maxSlicnost = len(vrhSlicnost)
              slicnostVrhova = 0
              for i in range(len(vrhSlicnost)):
                    if vrhSlicnost[i] == susedSlicnost[i]:
                        slicnostVrhova += 1
              slicnost = maxSlicnost - (slicnostVrhova - 1) # sta ako je slicnostVrhova == 0 ?
              bridovi[brid] = slicnost
              
    return bridovi 


def duljina_brida(vrh1, vrh2, bridovi):
    pair = sorted([vrh1, vrh2], key=int)
    brid = f"{pair[0]}-{pair[1]}"
    return bridovi[brid]


def reconstruct_paths(prev, izvor, cilj):
    svi_putevi = []
    
    def backtrack(trenutni_cvor, trenutni_put):
        if trenutni_cvor == izvor:
            svi_putevi.append([izvor] + trenutni_put)
            return
        
        for roditelj in prev.get(trenutni_cvor, []):
            backtrack(roditelj, [trenutni_cvor] + trenutni_put)
            
    backtrack(cilj, [])
    
    return svi_putevi
         


def dijkstra(source, susjedi, bridovi):
    dist = {}
    prev = {}
    visited = set()
    for vrh in susjedi.keys():
        dist[vrh] = 10**9
        prev[vrh] = []
        
    dist[source] = 0
    
    pq = [(0, source)]
    
    while pq:
        trenutna_udaljenost, vrh = heapq.heappop(pq)
        
        if vrh in visited:
            continue
        
        visited.add(vrh)
        
        for sused in susjedi[vrh]:
            if sused not in visited:
                alt = dist[vrh] + duljina_brida(vrh, sused, bridovi)
                
                if alt < dist[sused]:
                    dist[sused] = alt
                    prev[sused] = [vrh]
                    heapq.heappush(pq, (alt, sused))
                    
                elif alt == dist[sused]:
                    prev[sused].append(vrh)
        
    return dist, prev
        
# jedna iteracija algoritma je kada se ova funkcija pozove za svaki vrh u grafu 
# na kraju se rezultat mora podijelit s 2 jer algo prolazi kroz sve vrhove 
def centralnost(source, susjedi, bridovi, graf_na_0):
    
    dist, prev = dijkstra(source, susjedi, bridovi)
    
    for vrh in dist.keys():
        svi_putevi_od_vrha_do_cilja = reconstruct_paths(prev, source, vrh)
        
        if len(svi_putevi_od_vrha_do_cilja) == 0: 
            continue # ne postoji put
                
        uvecaj = 1 / len(svi_putevi_od_vrha_do_cilja) 
        
        for put in svi_putevi_od_vrha_do_cilja: # vecinom samo jedan put, ali moze ih biti vise
            
            for i in range(len(put) - 1):
                pair = sorted([put[i], put[i+1]], key=int)
                brid = f"{pair[0]}-{pair[1]}"
                graf_na_0[brid] += uvecaj
                
    #graf_na_0 = {k: v/2 for k,v in graf_na_0.items()}
    return graf_na_0


from collections import deque

def check_if_same_community(source, target, susjedi):
    
    if source == target:
        return 1
    
    visited = set()
    
    queue = deque([source])
    visited.add(source)
    
    while queue:
        current = queue.popleft()
        
        for neighbor in susjedi.get(current, []):
            if neighbor == target:
                return 1
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return 0

def explore_communities(source, susjedi):
    
    visited = set()
    
    queue = deque([source])
    visited.add(source)
    
    while queue:
        current = queue.popleft()
        
        for neighbor in susjedi.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


def modularnost(susjedi, original_bridovi):
    m = sum(original_bridovi.values())
    
    tezineVrhova = {}
    for vrh in susjedi.keys():
        ukupna_tezina_vrha = 0
        for brid, tezina in original_bridovi.items():
            u, v = brid.split("-")
            if vrh == u or vrh == v: 
                ukupna_tezina_vrha += tezina
                
        tezineVrhova[vrh] = ukupna_tezina_vrha 
        
    Q = 0.0
    
    for u in susjedi.keys():
        for v in susjedi.keys():
            delta = check_if_same_community(u, v, susjedi)
            
            if delta == 1:
                pair = sorted([u, v], key=int)
                brid_naziv = f"{pair[0]}-{pair[1]}"
                A_uv = original_bridovi.get(brid_naziv, 0)
                
                Q += (A_uv - ((tezineVrhova[u] * tezineVrhova[v]) / (2 * m)))
            
    Q = Q / (2 * m)
    
    return Q
      
     
     
     
      
susjedi, svojstva_vrhova = readFile()
bridovi = makeWeights(susjedi, svojstva_vrhova)
original_bridovi = copy.deepcopy(bridovi)

graf_na_0 = dict.fromkeys(bridovi, 0)

iteracije_agoritma_stanja_grafa = [] # lista [[modularnost_iter1, susjedi_iter1], ...]

while graf_na_0:
    
    modularity = modularnost(susjedi, original_bridovi)
    
    iteracije_agoritma_stanja_grafa.append([modularity, copy.deepcopy(susjedi)])
    
    #print(f"MODULARITY: {round(modularity, 4)}")
    
    for vrh in susjedi.keys():    
        centralnost(vrh, susjedi, bridovi, graf_na_0) # racuna centralnost na grafu "graf_na_0"

    centralnost_final = {k: round(v/2, 5) for k,v in graf_na_0.items()} # jer se svaki brid gleda dvaput ukupno u algoritmu

    # mozda ima vise bridova iste max centralnosti
    max_val = max(centralnost_final.values())
    max_keys = [k for k, v in centralnost_final.items() if v == max_val]
    
    max_keys = sorted(max_keys, key=lambda kljuc: [int(cvor) for cvor in kljuc.split("-")])
    
    for max_key in max_keys:
        graf_na_0.pop(max_key) 
        bridovi.pop(max_key)
    
        # odspoji i te vrhove
        prvi, drugi = max_key.split("-")
        susjedi[prvi] = [susedi for susedi in susjedi[prvi] if susedi != drugi]
        susjedi[drugi] = [susedi for susedi in susjedi[drugi] if susedi != prvi]
        
        print(f"{prvi} {drugi}")
    
    #for k,v in centralnost_final.items():
    #    print(f"Brid:{k} | Centralnost: {v}")
    #print("----------------------------------------\n")
    
    graf_na_0 = dict.fromkeys(graf_na_0, 0)
    
    
    
max_modularnost_idx = max_modularnost = -1
for i in range(len(iteracije_agoritma_stanja_grafa)):
    if iteracije_agoritma_stanja_grafa[i][0] > max_modularnost:
        max_modularnost = iteracije_agoritma_stanja_grafa[i][0]
        max_modularnost_idx = i
        
#print(iteracije_agoritma_stanja_grafa[max_modularnost_idx][1])

visited_nodes = set()
communities = []
for node in susjedi.keys():
    if node not in visited_nodes:
        community = explore_communities(node, iteracije_agoritma_stanja_grafa[max_modularnost_idx][1])
        
        sorted_community = sorted(list(community), key=int)
        communities.append(sorted_community)
        visited_nodes.update(community)
        
putevi = []   
for comm in communities:
    putevi.append("-".join([str(x) for x in comm]))

putevi.sort(key=lambda x: (len(x.split('-')), int(x.split('-')[0])))

print(" ".join(putevi))
print()
    