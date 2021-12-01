from embit import bip39, bip32
from embit.liquid import slip77
from embit.liquid import networks
from embit.liquid.descriptor import LDescriptor
from embit.liquid.addresses import to_unconfidential

MNEMONIC = "aim aim aim aim aim aim aim aim aim aim aim aim"
DERIVATION = "m/84h/1h/0h"
NETWORK = networks.get_network("elementsregtest")

if __name__=="__main__":
    print("Mnemonic:", MNEMONIC)
    seed = bip39.mnemonic_to_seed(MNEMONIC)
    print("Seed:", seed.hex())
    mbk = slip77.master_blinding_from_seed(seed)
    print("Master blinding key:", mbk)
    print("Master blinding key hex:", mbk.secret.hex())
    root = bip32.HDKey.from_seed(seed)
    account = root.derive(DERIVATION)
    # change version to regtest
    account.version = NETWORK["xprv"]
    xpub = account.to_public()
    print(f"Account key at path `{DERIVATION}`:", account)
    print(f"Xpub at path `{DERIVATION}`:", xpub)

    d = LDescriptor.from_string(f"blinded(slip77({mbk}),wpkh([{root.my_fingerprint.hex()}{DERIVATION[1:]}]{xpub}/{{0,1}}/*))")
    print("Descriptor:", d)
    for i in range(5):
        addr = d.derive(i).address(NETWORK)
        print("|", i, "|", addr, "|", to_unconfidential(addr), "|")
