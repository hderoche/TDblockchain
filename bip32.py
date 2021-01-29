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
seed = ['impose', 'top', 'crater', 'enemy', 'vessel', 'moon', 'cannon', 'torch', 'flight', 'trip', 'cry', 'invite']
indexWords = []
for word in seed:
    for i in range(df.shape[0]):
        if word == df['bip39'][i]:
            indexWords.append(i)
    # indexWords.append(index_word.values)
print(indexWords)


#hash_512 = hashlib.sha512(str(root_seed).encode('ASCII')).hexdigest()
#bin_hash = BitArray(hex=hash_512).bin
#master_private_k = bin_hash[0:256]
#master_chain_code = bin_hash[256::]
#