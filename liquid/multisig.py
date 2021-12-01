from embit import bip39, bip32, ec
from embit.liquid import slip77
from embit.liquid import networks
from embit.liquid.descriptor import LDescriptor
from embit.liquid.addresses import to_unconfidential

MNEMONICS = [
    "aim aim aim aim aim aim aim aim aim aim aim aim",
    "bus bus bus bus bus bus bus bus bus bus bus bus",
    "cave cave cave cave cave cave cave cave cave cave cave cave",
]
MBK = ec.PrivateKey.from_wif("L1XvKmnKWuC4a5sbz3Ez6LCfMCbaXMBCcQk7C62ziN5NjoEgjN5N")
THRESHOLD = 2
DERIVATION = "m/48h/1h/0h/2h"
NETWORK = networks.get_network("elementsregtest")

if __name__=="__main__":
    print("Mnemonics:")
    print("\n".join(MNEMONICS))
    seeds = [bip39.mnemonic_to_seed(mnemonic) for mnemonic in MNEMONICS]
    print("Seeds:")
    print("\n".join([seed.hex() for seed in seeds]))

    print("Master blinding key:", MBK)
    print("Master blinding key hex:", MBK.secret.hex())
    roots = [bip32.HDKey.from_seed(seed) for seed in seeds]
    accounts = [root.derive(DERIVATION) for root in roots]
    # change version to regtest
    for account in accounts:
        account.version = NETWORK["xprv"]
    xpubs = [account.to_public() for account in accounts]
    print(f"Account keys at path `{DERIVATION}`:")
    print("\n".join([str(account) for account in accounts]))
    print(f"Xpubs at path `{DERIVATION}`:")
    print("\n".join([str(xpub) for xpub in xpubs]))

    keys = ",".join([f"[{roots[i].my_fingerprint.hex()}{DERIVATION[1:]}]{xpubs[i]}/{{0,1}}/*" for i in range(len(MNEMONICS))])
    d = LDescriptor.from_string(f"blinded(slip77({MBK}),wsh(sortedmulti({THRESHOLD},{keys})))")
    print("Descriptor:", d)
    for i in range(5):
        addr = d.derive(i).address(NETWORK)
        print("|", i, "|", addr, "|", to_unconfidential(addr), "|")
