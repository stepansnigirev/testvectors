import sys
from embit import bip39, bip32
from embit.script import Script
from embit.liquid import slip77
from embit.liquid.addresses import address
from embit.liquid.networks import NETWORKS

net = NETWORKS['liquidv1']

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} \"<mnemonic>\" <scriptpubkey-in-hex>")
        sys.exit()
    mnemonic = sys.argv[1]
    script = Script(bytes.fromhex(sys.argv[2]))
    seed = bip39.mnemonic_to_seed(mnemonic)
    root = bip32.HDKey.from_seed(seed)
    print(f"Root key: {root}")
    mbk = slip77.master_blinding_from_seed(seed)
    print(f"Master blinding key: {mbk.secret.hex()}")
    bk = slip77.blinding_key(mbk, script)
    print(f"Blinding key for script {script.data.hex()}: {bk.secret.hex()}")
    try:
        script.address()
        unconf_addr = address(script)
        conf_addr = address(script, bk)
        print(f"Unconfidential address: {unconf_addr}")
        print(f"Confidential address: {conf_addr}")
    except:
        print("Script doesn't have an address representation")

if __name__ == "__main__":
    main()
