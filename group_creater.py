from pandas import DataFrame
from random import randint
primes = []
with open("primes.txt","r") as f:
    for prime_str in f.readlines():
        prime = int(prime_str)
        if(prime not in primes):
            primes.append(prime)
semiprimes = []
data = []
count = 0
try:
    while len(data) < 10000000:
        prime1_ind = randint(0,len(primes)-1)
        prime2_ind = randint(0,len(primes)-1)
        if(prime1_ind != prime2_ind):
            p = primes[prime1_ind]
            q = primes[prime2_ind]
            n = p * q
            if(n not in semiprimes):
                if(p > q):
                    p,q = q,p
                semiprimes.append(n)
                data.append([p,q,n,(p-1)*(q-1),0,0])
                count += 1
                if(count % 100000 == 0):
                    print(count//100000)
finally:
    print("Please wait, Writing to the file!")
    df = DataFrame(data=data)
    df.to_csv("./result.csv",index=False, header=False)