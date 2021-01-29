import secrets
import hashlib
from bitstring import BitArray
import pandas as pd

df = pd.read_fwf('bip39_wordlist.txt', header=None)
# print(df.head())
# generation du nombre aleatoire
randKey = secrets.randbits(128)
print(randKey)
# hash du nombre genere aleatoirement
hashRandKey = hashlib.sha256(str(randKey).encode('ASCII')).hexdigest()

checksum = BitArray(hex=hashRandKey).bin[0:4]
print(checksum)
entropy = BitArray(hex=hex(randKey)).bin

listWord = entropy + checksum
words = []
temp_word = ''
for i in range(len(listWord)):
    temp_word = temp_word + listWord[i]
    if i%11 == 10:
        words.append(temp_word)
        temp_word=''
print(words)

corr_word = []
for word in words:
    corr_word.append(int(word, 2))
print(corr_word)

seedPhrase = []
for word in corr_word:
    seedPhrase.append(df.iloc[word, 0])
print(seedPhrase)
