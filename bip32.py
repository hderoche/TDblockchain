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


# Uncomment in order to import a seed
# seed = import_seed()
seed = ['one', 'able', 'miss', 'remind', 'cruel', 'until', 'icon', 'solve', 'muscle', 'shock', 'screen', 'rotate']
indexWords = []
binWords = []
fullentropy = ''
for word in seed:
    for i in range(1, df.shape[0]):
        if word == df['bip39'][i]:
            indexWords.append(i)
            binaryWord = bin(i)[2:]
            if len(binaryWord) < 11:
                binaryWord = '0'*(11 - len(binaryWord)) + binaryWord
            binWords.append(binaryWord)
            fullentropy = fullentropy + binaryWord
    # indexWords.append(index_word.values)
print('index of the words ', indexWords)
print('Binary representation', binWords)
print('entropy (with checksum)', fullentropy)
entropy = fullentropy[:-4]
initial_checksum = fullentropy[-4:]
initial_checksum = int(hex(int(initial_checksum, 2))[2:])

entropy = hex(int(entropy, 2))

privatekey = entropy[2:]
hashRandKey = hashlib.sha256(bytes.fromhex(privatekey)).hexdigest()
# Checksum from the hashed random number
checksum = int(hashRandKey[0])

if checksum == initial_checksum:
    print('########## private key is valid ##########')
else:
    print('########## private key is not valid ##########')


# From a root seed, we can find the master private key and the master chain code
root_seed = fullentropy
# hashing the root seed using SHA512
hash_512 = hashlib.sha512(str(root_seed).encode('ASCII')).hexdigest()
bin_hash = BitArray(hex=hash_512).bin
# Separating the master private key from the master chain code
master_private_k = bin_hash[:256]
master_chain_code = bin_hash[256:]
master_chain_code_hex = hex(int(master_chain_code, 2))

print('mprv key', master_private_k)
print('mprv key hex', hex(int(master_private_k, 2)))
print('chain code', master_chain_code)

# Generating the public master key using G and the master private key
G = '0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798'
privatekey = hex(int(master_private_k, 2))


publickey = hex(int(privatekey, 16)*int(G, 16))
print('publicKey', publickey)

#Child key derivation
def CKD(xpub, index, chaincode):

    hashChildren = hashlib.sha512()
    hashChildren.update(bytes.fromhex(xpub[2:]))
    hashChildren.update(bytes.fromhex(chaincode[2:]))
    hashChildren.update(index)
    result = hashChildren.hexdigest()
    result = BitArray(hex=result).bin
    privatekeyChildren = hex(int(result[:256], 2))
    chaincodeChildren = hex(int(result[256:], 2))
    return privatekeyChildren, chaincodeChildren

# Generating a children at index 0
print('Generating a private key and the chain code for a children at index 0 :')
print(CKD(publickey, b''.zfill(32), master_chain_code_hex))