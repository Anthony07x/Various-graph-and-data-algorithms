import hashlib as h
from collections import defaultdict
import sys

def hamming_udaljenost(hash1, hash2):
    return sum(b1 != b2 for b1, b2 in zip(hash1, hash2))

def simhash(tekst):
    dokPotpis = [0] * 128
    vektor = [0] * 128
    jedinke = []
    #with open(tekst, "r") as toread:
    #for line in toread:
        #print(line)
    for jedinka in tekst.strip().split(" "):
        myhash = h.md5(jedinka.encode()).digest()
        bits = [(byte >> i) & 1 for byte in myhash for i in range(7, -1, -1)]
        
        for idx, bit in enumerate(bits):
            if bit == 0:
                vektor[idx] -= 1
            else:
                vektor[idx] += 1
    
    for idx, vek in enumerate(vektor):
        if vek >= 0:
            dokPotpis[idx] = 1
        else:
            dokPotpis[idx] = 0
    
    bitStr = "".join(map(str, dokPotpis))
    
    # ode vrati bitove u listi odma bez pretvaranja u hex
    # jer ovako listu mogu jednako podijelit u b pojasa
    #hex_result = "" 
    #for i in range(0, 128, 4):
    #    hexaCharac = bitStr[i:i+4]
    #    decimalni = int(hexaCharac, 2)
    #    hex_digit = f"{decimalni:x}"
    #    hex_result += hex_digit
   
    return bitStr
  
def build_inverted_map(original_map):
    element_to_sets = defaultdict(list)
    
    for key, s in original_map.items():
        for element in s:
            element_to_sets[element].append(s)
    
    result = defaultdict(set)
    
    for element, sets in element_to_sets.items():
        for s in sets:
            for co_element in s:
                if co_element != element:
                    result[element].add(co_element)
    
    return result  
          
 
def LSH_similar(hashevi, b = 8):
    k = len(hashevi[0])
    r = k // b
    
    # mapa u kojoj je ID pojas sazetka, a vrijednosti ce biti svi dokumenti koji imaju isti pojas sazetka
    # znaci npr 0010, 0011, r = 2, b = 2, za key = 00, vrijednost ce biti set sa ID od 0010 i 0011
    batches = {}
    
    batches = {}
    
    for doc_id, hash in enumerate(hashevi):
        for band_idx, i in enumerate(range(0, k, r)):
            band_key = (band_idx, hash[i:i+r]) 
            batches.setdefault(band_key, set()).add(doc_id)
    
    return batches
    
def compare():
    N, Q = 0, 0
    tekstovi = []
    upiti = []
    
    input_data = sys.stdin.read().splitlines()
    
    for idx, line in enumerate(input_data):
        if idx == 0:
            N = int(line)
            continue
        elif idx == N + 1:
            Q = int(line)
            continue
        elif idx < (N + 1):
            tekstovi.append(line.strip())
        else:
            upiti.append(line.strip().split(" "))
     
    hashevi = []
    texts_with_ID = {} 
    hashes_with_id = {}  
    for idx, tekst in enumerate(tekstovi):
        texts_with_ID[idx] = tekst
        docHash = simhash(tekst) # simhash ode sada vraca listu bitova, a ne hex
        hashevi.append(docHash)
        hashes_with_id[idx] = docHash
    
    # lista listi u kojoj se za svaki dokument nalazi lista dokumenata koji su slicni sa njim
    # ode zapravo samo moramo napisati fju koja ce vraitit dobar similar_with_which (slicni dok)
    similar_with_which = build_inverted_map(LSH_similar(hashevi))
    
    hamming_similar = {}
    count_hamming_similar = [[] for _ in range(len(upiti))] 
     
    for idx, (I, K) in enumerate(upiti):
        for slicniDokumenti in similar_with_which[int(I)]: # slicniDokumenti je ID dokumenta
                if hamming_udaljenost(hashes_with_id[int(I)], hashes_with_id[slicniDokumenti]) <= int(K):
                    # samo brojimo koliko ih ima ukupno po kojem upitu
                    count_hamming_similar[idx].append(slicniDokumenti)
     
    return [len(hamming_slicni) for hamming_slicni in count_hamming_similar]
  
                
#print(simhash("fakultet elektrotehnike i racunarstva"))

with open("rezzz", "w", encoding="utf-8") as f:
    for k in compare():
        f.write(f"{k}\n")