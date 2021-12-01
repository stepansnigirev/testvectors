# generates valid mnemonics with all same words and prints the shortest for every letter
from embit.bip39 import WORDLIST, mnemonic_is_valid
import string

mnemonics = []
for w in WORDLIST:
	mn = " ".join([w]*12)
	if mnemonic_is_valid(mn):
		mnemonics.append(mn)

mnemonics.sort(key=lambda mn: len(mn))

for l in "abcdefg":# string.ascii_lowercase:
	try:
		print([mn for mn in mnemonics if mn.startswith(l)][0])
	except:
		pass