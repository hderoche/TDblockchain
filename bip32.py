import pandas as pd
import hashlib
from bitstring import BitArray


# Importing the list of words in a pandas Dataframe
df = pd.read_fwf('bip39_wordlist.txt', header=None, columns="bip39")
df = df.rename(columns={0: "bip39"})
# Checks if the dataframe contains the words in input
def checkWord(word):
    found = df[df['bip39'].str.contains(word)]
    if found.count().values > 0:
        return True
    else: 
        return False
    
# Allows to import a seed phrase and check if words are correctly spelled
def import_seed():
    seed = []
    print("Starting to build the seed phrase")
    for i in range(12):
        word = input('Entrer le mot numero ' + str(i)+ ' :')
        exist = checkWord(word)
        print(exist)
        if exist:
            seed.append(word)
        else: 
            print('the word does not exist in bip39')
            print('Retry')
            import_seed()
    print(seed)
    return seed
# seed = import_seed()
# 911, 1831, 404, 591, 1944, 1148, 267, 1834, 711, 1862, 425, 944
seed = ['one', 'able', 'miss', 'remind', 'cruel', 'until', 'icon', 'solve', 'muscle', 'shock', 'screen', 'route']
indexWords = []
binWords = []
fullentropy = ''
for word in seed:
    for i in range(df.shape[0]):
        if word == df['bip39'][i]:
            indexWords.append(i)
            binaryWord = bin(i)[2:]
            if len(binaryWord) < 11:
                binaryWord = '0'*(11 - len(binaryWord)) + binaryWord
            binWords.append(binaryWord)
            fullentropy = fullentropy + binaryWord
    # indexWords.append(index_word.values)
print(indexWords)
print(binWords)
print(fullentropy)
entropy = fullentropy[:-4]
print(entropy)
print(len(entropy))
hashRandKey = hashlib.sha256(entropy.encode()).hexdigest()

# Checksum from the hashed random number
checksum = BitArray(hex=hashRandKey).bin[0:4]
print(checksum)
print(bin(944))


# From a root seed, we can find the master private key and the master chain code
root_seed = 100110101010000000001010001101110101101011100011010010011101110001011100000101100111011110010001100110001100101100000110010111100100
# hashing the root seed using SHA512
hash_512 = hashlib.sha512(str(root_seed).encode('ASCII')).hexdigest()
bin_hash = BitArray(hex=hash_512).bin
# Separating the master private key from the master chain code
master_private_k = bin_hash[:256]
master_chain_code = bin_hash[256:]
print('mprv key', master_private_k)
print('chain code', master_chain_code)


# base_point = '0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798'
# basePoint = BitArray(hex=hex(base_point)).bin
# print(basePoint)
# print(bin(basePoint, 2))
# Verifier que y^2 - x^3 - 7 % p == 0
# Avec p = 2^256 - 2^32 - 977 

# public key K = k * G where G is basepoint and k private key