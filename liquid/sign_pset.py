from embit import bip39, bip32, compact
from embit.liquid import slip77
from embit.liquid import networks
from embit.liquid.descriptor import LDescriptor
from embit.psbt import *
from embit.liquid.pset import *
import sys, json

MNEMONIC = "aim aim aim aim aim aim aim aim aim aim aim aim"
DERIVATION = "m/84h/1h/0h"
NETWORK = networks.get_network("elementsregtest")

if __name__ == '__main__':
    # ugly, I know...
    rangeproof = "--rangeproof" in sys.argv
    if rangeproof:
        sys.argv.pop(sys.argv.index("--rangeproof"))
    sighash = LSIGHASH.ALL
    if rangeproof:
        sighash = sighash | LSIGHASH.RANGEPROOF

    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} path/to/base64_psbt.txt [path/to/signed.txt] [--rangeproof]")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        pset = PSET.from_string(f.read())

    root = bip32.HDKey.from_seed(bip39.mnemonic_to_seed(MNEMONIC))
    pset.sign_with(root, sighash=sighash)
    print("Hashes for signing inputs:")
    for i in range(len(pset.inputs)):
        print(i, ":", pset.sighash(i, sighash=sighash).hex())
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w") as f:
            f.write(str(pset))