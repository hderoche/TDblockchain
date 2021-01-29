import secrets
import hashlib
from bitstring import BitArray
import pandas as pd

# Importing the list of words in a pandas Dataframe
df = pd.read_fwf('bip39_wordlist.txt', header=None, columns="bip39")
df = df.rename(columns={0: "bip39"})

# Generating random number
randKey = secrets.randbits(128)
print(randKey)
# Hash of the randomly generated number
hashRandKey = hashlib.sha256(str(randKey).encode('ASCII')).hexdigest()

# Checksum from the hashed random number
checksum = BitArray(hex=hashRandKey).bin[0:4]
print(checksum)
# Entropy from the random number
entropy = BitArray(hex=hex(randKey)).bin

# binary of 132bits long
listWord = entropy + checksum
print(listWord)

# Splitting the 132bit into 11 sequences of 12bits
words = []
temp_word = ''
for i in range(len(listWord)):
    temp_word = temp_word + listWord[i]
    if i%11 == 10:
        words.append(temp_word)
        temp_word=''
print(words)

# Getting the correct integer for each sequence
corr_word = []
for word in words:
    corr_word.append(int(word, 2))
print(corr_word)

# Matching the integer to the words using the dataframe
seedPhrase = []
for word in corr_word:
    seedPhrase.append(df.iloc[word, 0])
print(seedPhrase)


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
import_seed()