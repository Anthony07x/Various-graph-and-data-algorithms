import hashlib as h
import sys

def hamming_udaljenost(hash1, hash2):
    str1 = bin(int(hash1, 16))[2:].zfill(len(hash1) * 4)
    str2 = bin(int(hash2, 16))[2:].zfill(len(hash2) * 4)
    
    return sum(b1 != b2 for b1, b2 in zip(str1, str2))

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
    
    hex_result = "" 
    for i in range(0, 128, 4):
        hexaCharac = bitStr[i:i+4]
        decimalni = int(hexaCharac, 2)
        hex_digit = f"{decimalni:x}"
        hex_result += hex_digit
   
    return hex_result
    
    
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
    for tekst in tekstovi:
        hashevi.append(simhash(tekst)) 
     
    similar_with_which = [[] for _ in range(len(upiti))]  
    for idx, (I, K) in enumerate(upiti):
       for i, hash in enumerate(hashevi):
            if i == int(I): continue
            
            if hamming_udaljenost(hashevi[int(I)], hash) <= int(K):
                similar_with_which[idx].append(i)
            
    return [len(slicni_tesktovi_za_upit) for slicni_tesktovi_za_upit in similar_with_which]
            
                
#print(simhash("fakultet elektrotehnike i racunarstva"))

for k in compare():
    print(f"{k}")
                
        
    
    
                
